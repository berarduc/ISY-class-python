'''
Universal Devices ISY class

TNB

Jan 2019

V1.0 - basic websocket and rest functions for home ISY system
V1.01 - class now accepts a list of filter items
V1.2 - Now this class accepts a list of filter items, and sends back via callback only 'eventInfo' data for devices or variables
V1.3 - added SetVariable method
V1.4 - added GetVariable method to ISY class


'''

import websocket
import requests

try:
    import thread
except ImportError:
    import _thread as thread


class ISY:

    def __init__(self,ISY_ADD, Auth_String, filterItemList,callback_function):
        self.debug_on = False
        if self.debug_on: print("\nInside ISY class init...")
        # defaults
        self.ISY_REST_URL = "http://"+ISY_ADD+"/rest"
        self.ISY_WS_URL = "ws://"+ISY_ADD+"/rest/subscribe"
        self.headers = {'Authorization':'Basic '+Auth_String}
        self.callback = callback_function
        # class accepts a list of filter items
        self.filterItems = []
        if len(filterItemList) == 0:
            self.enable_filter = False
        else:
            self.enable_filter = True
            self.filterItems = filterItemList
        # set up websocket connection and run forever as separate thread
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(self.ISY_WS_URL,
                                         on_message = self.messageHandler,
                                         on_error = self.on_error,
                                         on_close = self.on_close,
                                         header = ["Authorization: Basic "+Auth_String,
                                                   "Sec-WebSocket-Protocol: ISYSUB",
                                                   "Origin: com.universal-devices.websockets.isy"])
        self.ws.on_open = self.on_open
        if self.debug_on: print("...before def run: run_forever()")
        def run(*args):
            self.ws.run_forever()
        thread.start_new_thread(run,())
        if self.debug_on: print("...done w init...")

    
    def isolateKeywordPayload(self,message, keyword):
        # determine payload of eventInfo portion of websocket streaming data and return
        if self.debug_on: print("...inside isolateEventInfoPayload...")
        keyword_start = "<"+keyword+">"
        keyword_end = "</"+keyword+">"
        start = message.find(keyword_start)
        end = message.find(keyword_end)
        if self.debug_on: print("start = ",start, ", end = ",end)
        if start != -1 and end != -1:
                # ok both ends of xml are present
                string1 = message.split(keyword_start)[1]
                if self.debug_on: print("string1 = ", string1)
                string2 = string1.split(keyword_end)[0]
                if self.debug_on: print("string2 = ", string2)
                if string2 == "":
                    # payload is empty
                    return -1
                else:
                    return string2
        else: return -1                                     

    def on_open(self):
        if self.debug_on: print("...inside on_open...")

    def on_close(self):
        if self.debug_on: print("\n...inside on_close...\n")

    def on_error(self, error):
        print("\n\n---> WebSocket ERROR: ", error)
        
    def filterEvents(self,event):
        # filter out undesired event messages from stream
        result = event.find("[")
        if result == 0: return event
        else: return -1

    def messageHandler(self, message):
        #print("\n...in messageHandler...self = ",self, "... message = ",message,"\n")
        node = ""
        eventInfo = ""
        control = ""
        action = ""
        if self.debug_on: print("Message Received: ", message)
        node = self.isolateKeywordPayload(message, "node")
        #print("Node Info from message: ", node)
        eventInfo_interim = self.isolateKeywordPayload(message,"eventInfo")
        if eventInfo_interim != -1:
            eventInfo = self.filterEvents(eventInfo_interim)
        else:
            eventInfo = eventInfo_interim
        #print("EventInfo from message: ", eventInfo)
        # filter out all 'eventInfo' reports 
        if eventInfo != -1:
            if self.debug_on: print("Event: "+eventInfo)
            if eventInfo != "":
                if self.enable_filter == True:
                    for item in (self.filterItems):
                        if message.find(item) != -1:
                            print("\n\n--> Found '"+item+"' filter item! Calling out to callback function...")
                            if eventInfo != -1: 
                                self.callback(self,item,eventInfo)

    def SendDeviceCommand(self, deviceID, command):
        error = False
        targetURL = self.ISY_REST_URL+"/nodes/"+deviceID+"/cmd/"+command
        print("...inside SendDeviceCommand...targetURL = ",targetURL,"\n")
        try:
            r = requests.get(targetURL,timeout = 0.5, headers=self.headers)
        except:
            print("\n\n--> REST ERROR - Send Device Command attempt FAILED.\n")
            error = True
            return error
        if self.debug_on: print("...inside SendDeviceCommand, r = ", r, ", r.content = ", r.content)
        return error

    def GetDeviceStatus(self, deviceID):
        error = False
        statusString = ""
        try:
            r = requests.get(self.ISY_REST_URL+"/status/"+deviceID, timeout = 0.5, headers=self.headers)
        except:
            print("\n\n--> REST ERROR - Get Device Status attempt FAILED.\n")
            error = True
            return statusString, error
        '''
        else:
            if r["cod"]==200:
                print("successful attempt, status = ", r)
            else:
                print("error, status code received: ", r["cod"])
                error = True
                return statusString, error
        '''
        statusString = r.content
        return statusString, error

    def SetVariable(self,variable,value):
        error = False
        targetURL = self.ISY_REST_URL+"/vars/set/2/"+variable+"/"+value
        if self.debug_on: print("...inside ISY.SetVariable...targetURL = ", targetURL,"\n")
        try:
            r=requests.get(targetURL,timeout=0.5,headers=self.headers)
        except:
            print("\n\n REST ERROR - Set Variable attempt FAILED.\n")
            error = True
            return error
        if self.debug_on: print("...after set variable attempt, r = ",r,", r.content = ", r.content)
        return error

    def GetVariable(self,variable):
        error = False
        var = 0
        targetURL = self.ISY_REST_URL+"/vars/get/2/"+variable
        if self.debug_on: print("...inside ISY.GetVariable...targetURL = ", targetURL,"\n")
        try:
            r=requests.get(targetURL,timeout=0.5,headers=self.headers)
        except:
            print("\n\n REST ERROR - Get Variable attempt FAILED.\n")
            error = True
            return error,var
        var = self.isolateKeywordPayload(str(r.content),"val")
        if self.debug_on: print("...after get variable attempt, r = ",r,", r.content = ", r.content)
        return error,var

            




        

         
        
