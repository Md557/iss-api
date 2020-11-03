## Summary
A Python script that will accept the following command line arguments, along with any required information, and print the expected results
## Usage
```python main.py [command] (where command is pass [lat,long], people, loc)```

###         loc
    print the current location of the ISS
    Example: “The ISS current location at {time} is {LAT, LONG}”
###         pass
    print the passing details of the ISS for a given location
    Example: “The ISS will be overhead {LAT, LONG} at {time} for {duration}”
###         people
    for each craft print the details of those people that are currently in space
    Example: “There are {number} people aboard the {craft}. They are {name[0]}…{name[n]}”


### API_DEFS = [ # From https://github.com/open-notify/Open-Notify-API/blob/master/app.py
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
