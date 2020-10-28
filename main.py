import os, sys
import requests
from datetime import datetime

'''
Task
Implement a Python script that will accept the following command line arguments, along with any required information, and print the expected results
·         loc
o    print the current location of the ISS
o    Example: “The ISS current location at {time} is {LAT, LONG}”
·         pass
o    print the passing details of the ISS for a given location
o    Example: “The ISS will be overhead {LAT, LONG} at {time} for {duration}”
·         people
o    for each craft print the details of those people that are currently in space
o    Example: “There are {number} people aboard the {craft}. They are {name[0]}…{name[n]}”

'''
API_DEFS = [ # From https://github.com/open-notify/Open-Notify-API/blob/master/app.py
    {
        "title": "ISS Location Now",
        "link": "/iss-now.json",
        "desc": "Current ISS location over Earth (latitude/longitude)",
        "doclink": "http://open-notify.org/Open-Notify-API/ISS-Location-Now",
        "docname": "ISS-Location-Now"},
    {
        "title": "ISS Pass Times",
        "link": "/iss-pass.json?lat=45.0&lon=-122.3",
        "desc": "Predictions when the space station will fly over a particular location",
        "doclink": "http://open-notify.org/Open-Notify-API/ISS-Pass-Times",
        "docname": "ISS-Pass-Times"},
    {
        "title": "People in Space Right Now",
        "link": "/astros.json",
        "desc": "The number of people in space at this moment. List of names when known.",
        "doclink": "http://open-notify.org/Open-Notify-API/People-In-Space",
        "docname": "People-In-Space"},
]

def apiLoc():
    #/iss-now.json
    #response = app.response_class(response=json.dumps(globalJson),status=200,mimetype='application/json')
    URL = "http://api.open-notify.org/iss-now.json"
    r = requests.get(URL)
    data = r.json() 
    #debug: print response data #print(data)
    if(data['message']=='success'):
        #print("Successful request")
        parsedTime=parseTime(data['timestamp'])
        print("The ISS current location at %s is %s, %s "% (parsedTime, data['iss_position']['latitude'], data['iss_position']['longitude']))
    else:
        print("a valid response was not received by the iss-now.json API")

def apiPeople():
    #/astros.json
    URL="http://api.open-notify.org/astros.json"
    r = requests.get(URL)
    data = r.json() 
    #debug: print response data #print(data)
    if(data['message']=='success'):
        #print("Successful request")
        num=0
        skip=0
        peopleDict=data['people']
        numExp=data['number']
        #actNum=len(data['people'])
        craftExp='ISS'
        #nameList=[]
        namesStr=''
        ######### shorter way if not checking craft:
        #  nameList=[people['name']  for i in peopleDict]
        for people in peopleDict:
            if people['craft']==craftExp:
                #nameList.append(people['name'])
                if num==numExp-1:
                    namesStr+=', and '                    
                elif num>0:
                    namesStr+=', '
                namesStr+=people['name']
                num+=1                
            else:
                skip+=1
        if skip>0:
            print("Some astros were skipped, aboard a different craft than expected (number=%s)"%skip)
        print("There are %s people aboard the %s. They are %s"% (num,craftExp,namesStr))
    else:
        print("a valid response was not received by the people/astros.json API")

def apiPass(lat,long):
    #/iss-pass.json?lat=45.0&lon=-122.3
    #curTime=datetime.now().timestamp()
    #print(curTime)
    
    URL = "http://api.open-notify.org/iss-pass.json?lat=%s&lon=%s&n=1"%(lat,long) #add n=1, only want next pass
    #print("apiPass URL: ",URL)
    r = requests.get(URL)
    data = r.json() 
    #debug: print response data #print(data)
    if(data['message']=='success'):    
        nextPass=parseTime(data['response'][0]['risetime'])
        passDur=data['response'][0]['duration']
        print("The ISS will be overhead (%s, %s) at %s for %s seconds"%(lat,long,nextPass,passDur))
    else:
        print("a valid response was not received by the iss-pass.json API") 
        
def parseTime(timeInt): #returns time string from given unix time
    
    timeObj=datetime.fromtimestamp(timeInt)
    # https://docs.python.org/3/library/datetime.html
    parsedTimeStr=timeObj.strftime("%I:%M%p") #for day add to start %A, %d. %B %Y 
    return parsedTimeStr


    
if __name__ == "__main__":
    ''' 
    This is used when running locally only. 
    Usage: python main.py [loc,pass,people] (pass lat/long)
     [] = required argument () = optional argument
     
    '''

    #print("argv: ", sys.argv)
    try:
        arg1=sys.argv[1]
    except:
        print("couldn't read first argument, usage: python main.py [command] (where command is pass [lat,long], people, loc)")
        
    if (arg1=='loc'):
        print("location selected")
        #call api
        apiLoc()
    elif (arg1=='pass'): # pass expects valid lat/long as argv
        try:
            lat=float(sys.argv[2])
            long=float(sys.argv[3])
            if lat>=-90 and lat<=90 and long>=-180 and long<=180:
                print("pass time for given (lat,long)=(%s,%s)"%(lat,long))
                #Call api
            else:
                print("Invalid lat or long range entered (-90<=lat<=90) and (-180<=long<=180)")
            apiPass(lat,long)
            
        except:
            print("Error parsing lat and long, pass usage (without brackets): main.py pass [lat] [long]")
    elif (arg1=='people'):
        print("people selected")
        #call api
        apiPeople()
    
