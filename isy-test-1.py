'''
ISY class test app 1
'''
from ISY import *
import sys
import time
import datetime

def readItemInConfigFile(fileName,item,separator=" "):
    try:
        file = open(fileName,"r")
    except IOError:
        return -1
    else:
        fileLine = file.readline().split(separator) # all input file elements must be separated by SPACES
        while fileLine != []: # must have at least ONE BLANK LINE at end of file indicating EOF
            if fileLine[0] == item:
                file.close()
                return fileLine
            fileLine = file.readline().split(separator) 
        file.close()
        return -1
    
# all application-specific info is stored in external files - not tracked by git

config_file = "/home/pi/python/ISY-class-python/ISY-devices.config"
    
# ISY objects - devices and variable definitions - here is where you define your specific system
FrontOutsideLights = [readItemInConfigFile(config_file, "FrontOutsideLights",",")[1],readItemInConfigFile(config_file, "FrontOutsideLights",",")[2]]
FrontDoorOutsideLight = [readItemInConfigFile(config_file, "FrontDoorOutsideLight",",")[1],readItemInConfigFile(config_file, "FrontDoorOutsideLight",",")[2]]
FruitTreeMotionSensor = [readItemInConfigFile(config_file, "FruitTreeMotionSensor",",")[1],readItemInConfigFile(config_file, "FruitTreeMotionSensor",",")[2]]
HotTubMotionSensor = [readItemInConfigFile(config_file, "HotTubMotionSensor",",")[1],readItemInConfigFile(config_file, "HotTubMotionSensor",",")[2]]
DrivewayMotionSensor = [readItemInConfigFile(config_file, "DrivewayMotionSensor",",")[1],readItemInConfigFile(config_file, "DrivewayMotionSensor",",")[2]]
GazeboMotionSensor = [readItemInConfigFile(config_file, "GazeboMotionSensor",",")[1],readItemInConfigFile(config_file, "GazeboMotionSensor",",")[2]]
BigGarageLights = [readItemInConfigFile(config_file, "BigGarageLights",",")[1],readItemInConfigFile(config_file, "BigGarageLights",",")[2]]
SmallGarageLightsMaster = [readItemInConfigFile(config_file, "SmallGarageLightsMaster",",")[1],readItemInConfigFile(config_file, "SmallGarageLightsMaster",",")[2]]
SmallGarageLightsSlave = [readItemInConfigFile(config_file, "SmallGarageLightsSlave",",")[1],readItemInConfigFile(config_file, "FrontOutsideLights",",")[2]]
PorticoLights = [readItemInConfigFile(config_file, "PorticoLights",",")[1],readItemInConfigFile(config_file, "PorticoLights",",")[2]]
PhotoCell = [readItemInConfigFile(config_file, "PhotoCell",",")[1],readItemInConfigFile(config_file, "PhotoCell",",")[2]]
FrontFountain = [readItemInConfigFile(config_file, "FrontFountain",",")[1],readItemInConfigFile(config_file, "FrontFountain",",")[2]]
BackFountain = [readItemInConfigFile(config_file, "BackFountain",",")[1],readItemInConfigFile(config_file, "BackFountain",",")[2]]
OutsideLightsNotificationActiveVariable = [readItemInConfigFile(config_file, "OutsideLightsNotificationActiveVariable",",")[1],readItemInConfigFile(config_file, "OutsideLightsNotificationActiveVariable",",")[2]]
FrontFountainWaterSensor = [readItemInConfigFile(config_file, "FrontFountainWaterSensor",",")[1],readItemInConfigFile(config_file, "FrontFountainWaterSensor",",")[2]]
BackFountainWaterSensor = [readItemInConfigFile(config_file, "BackFountainWaterSensor",",")[1],readItemInConfigFile(config_file, "BackFountainWaterSensor",",")[2]]
FrontFountainEnabledVariable = [readItemInConfigFile(config_file, "FrontFountainEnabledVariable",",")[1],readItemInConfigFile(config_file, "FrontFountainEnabledVariable",",")[2]]
BackFountainEnabledVariable = [readItemInConfigFile(config_file, "BackFountainEnabledVariable",",")[1],readItemInConfigFile(config_file, "BackFountainEnabledVariable",",")[2]]


# ISY actions
SetToOn = ["DON", "set to on"]
SetToOFF = ["DOF", "set to off"]
SetTo = ["ST", "set at"]

# ISY sets - All items in these sets will be tracked - put items in sets to 'subscribe' to events related to them

IsyDevices = [FrontOutsideLights,
              FrontDoorOutsideLight,
              HotTubMotionSensor,
              DrivewayMotionSensor,
              GazeboMotionSensor,
              BigGarageLights,
              SmallGarageLightsMaster,
              SmallGarageLightsSlave,
              PorticoLights,
              PhotoCell,
              FrontFountain,
              BackFountain,
              FruitTreeMotionSensor,
              FrontFountainWaterSensor,
              BackFountainWaterSensor
              ]

IsyVariables = [OutsideLightsNotificationActiveVariable,
                FrontFountainEnabledVariable,
                BackFountainEnabledVariable]

IsyActions = [SetToOn,
              SetToOFF,
              SetTo
              ]

def constructFilterFromDevsAndVarsLists(devs,variables):
    # input both devices and variables lists and output properly formatted filter list
    filterList = []
    for dev in devs:
        filterList.append(dev[0])
    for var in variables:
        filterList.append(var[0])
    return filterList

def getDateTimeString():
    now = datetime.datetime.now()
    nowString = now.strftime("%A %b %d %I:%M %p")
    DTstring = nowString.replace(' 0','  ')
    return DTstring

def getFriendlyTextForItemInSet(eventItem,set):
    # run through all tuples and determine which one is being requested, then return friendly text associated with it
    for element in set:
        if element[0].find(eventItem) != -1:
            return element[1]
    # return error code if can't find valid value
    return -1

def parseDeviceMessage(message):
    # break apart message into separate 'action', 'value', and 'misc' sections
    #print("inside parseDeviceMessage...message = ", message)
    # right now this code only looks for 'DON', 'DOF', and 'ST' messages, returns error if it finds something else
    action = ""
    value = ""
    misc = ""
    error = False
    if message.find("DON") != -1:
        # found DON
        action = "DON"
        message1 = message.split("DON")[1].lstrip()
    elif message.find("DOF") != -1:
        # found DOF
        action = "DOF"
        message1 = message.split("DOF")[1].lstrip()
    elif message.find("ST") != -1:
        # found ST
        action = "ST"
        message1 = message.split("ST")[1].lstrip()
    else:
        print("error in parseMessage - can't find action")
        error = True
    if not error:
        #print("message1 = /",message1)
        remainder = message1.split(" ")
        #print("remainder = /",remainder)
        value = remainder[0]
        if len(remainder) > 1:
            misc = remainder[1]+remainder[2]
            #print("...found 3 values: action = ",action,", value = ", value,", misc = ", misc)
            return 0, action, value, misc
        else:
            #print("...found 2 values: action = ",action,"value = ", value)
            return 0, action, value, misc
    else:
        # on error return -1
        return -1,action, value, misc 
    
def callbackFunction(isy, eventItem, eventMessage):
    #print("...inside callbackFunction...eventItem: ", eventItem, ", eventMessage: ", eventMessage)
    isDevice = False
    isVariable = False
    error = False
    # first check for device event
    friendlyTextObject = getFriendlyTextForItemInSet(eventItem,IsyDevices)
    if friendlyTextObject != -1:
        isDevice = True
        parseError, action,value,misc = parseDeviceMessage(eventMessage)
        if parseError != -1:
            friendlyTextAction = getFriendlyTextForItemInSet(action, IsyActions)
        else:
            error = True
    else:
        # if not device event, check for variable event
        friendlyTextObject = getFriendlyTextForItemInSet(eventItem, IsyVariables)
        if friendlyTextObject != -1:
            isVariable = True
            # since it's a variable, just extract value directly
            value = eventMessage.split(eventItem+" ]")[1].lstrip()
        else:
            error = True
    if friendlyTextObject != -1 and not error:
        if isDevice:
            if action == "DON" or action == "DOF":
                print(getDateTimeString()," - ", friendlyTextObject, friendlyTextAction)
            else:
                print(getDateTimeString()," - ", friendlyTextObject, friendlyTextAction, value, "%")
        elif isVariable:
            print(getDateTimeString()," - ", friendlyTextObject, "is set to ", value)
    else:
        # print error message if it finds something not expected
        print("ERROR in Text Function...got event but cannot find Friendly text...Event Item = ", eventItem,", Event Message = ", eventMessage)

def main():
    print("ISY Test Program...starting up...")
    
    # get creds
    cred_file = "/home/pi/python/ISY-class-python/ISY-creds.txt"
    ISY_ADD = readItemInConfigFile(cred_file, "ISYADD")[1]
    ISY_AUTH_STRING = readItemInConfigFile(cred_file, "ISYAuthString")[1]
    #print("ISYADD = ", ISY_ADD, ", ISY-auth-string = ", ISY_AUTH_STRING)

    # set up and kick off ISY stream monitoring
    isy = ISY(ISY_ADD, ISY_AUTH_STRING, constructFilterFromDevsAndVarsLists(IsyDevices, IsyVariables), callbackFunction)
    print("...back in main...waiting for ISY Events...")
    # this is where your main code/event loop will be
    while True:
        pass


    print("...exiting...")
    sys.exit()

main()    
