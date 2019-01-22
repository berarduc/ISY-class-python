'''
Universal Devices ISY class

TNB

Jan 2019

V1.0 - basic websocket and rest functions for home ISY system
V1.01 - class now accepts a list of filter items

'''

import websocket
import requests

try:
    import thread
except ImportError:
    import _thread as thread

class ISY:

    def __init__(self,ISY_ADD, Auth_String, filterItemList,callback_function):
        print("\nInside ISY class init...")
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
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.ISY_WS_URL,
                                         on_message = self.messageHandler,
                                         on_error = self.on_error,
                                         on_close = self.on_close,
                                         header = ["Authorization: Basic "+Auth_String,
                                                   "Sec-WebSocket-Protocol: ISYSUB",
                                                   "Origin: com.universal-devices.websockets.isy"])
        self.ws.on_open = self.on_open
        print("...before def run: run_forever()")
        def run(*args):
            self.ws.run_forever()
        thread.start_new_thread(run,())
        print("...done w init...")
                                         

    def on_open(self):
        print("...inside on_open...")

    def on_close(self):
        print("\n...inside on_close...\n")

    def on_error(self, error):
        print("\n\n---> WebSocket ERROR: ", error)

    def messageHandler(self, message):
        #print("\n...in messageHandler...self = ",self, "... message = ",message,"\n")
        print("Message Received: ", message)
        if self.enable_filter == True:
            for item in (self.filterItems):
                if message.find(item) != -1:
                    print("\n\n--> Found '"+item+"' filter item! Calling out to callback function...")
                    self.callback(self,message)

    def exit(self):
        self.ws.close()

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
        print("...inside SendDeviceCommand, r = ", r, ", r.content = ", r.content)
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
            




        

         
        
