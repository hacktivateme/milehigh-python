"""
Example python code by Robert King, https://google.com/+RobertKing
"""
 
import json
import urllib
import urllib2
from time import time, sleep
from pprint import pprint
 
 
class MileHigh:
    TOKEN = "YOUR_TOKEN"
 
    BASE_URL = 'http://challenge.hacktivate.me:3000'
    POST_URL = "%s/post" % BASE_URL
    GET_URL = "%s/get?token=%s" % (BASE_URL, TOKEN)
    VIEW_URL = "%s/view?token=%s" % (BASE_URL, TOKEN)
 
    def __init__(self):
        print "Initializing MileHigh"
        print "You may view the simulation at %s" % self.VIEW_URL
 
        self.post_time = time()
        self.refresh_time = time()
        self.throttle = 0.2
 
        self.data = None
        self.refresh_data()
 
    def do_post(self, data_dict):
        if "token" not in data_dict or data_dict["token"] != self.TOKEN:
            raise ValueError("you must include your token")
 
        time_since = time() - self.post_time
        self.post_time = time()
        block_time = self.throttle - time_since
        if block_time > 0:
            print "blocking do_post for ", block_time
            sleep(block_time)
 
        print "do_post posting.."
 
        data = json.dumps(data_dict)
        req = urllib2.Request(self.POST_URL, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        print "RESPONSE",  response
        f.close()
 
    def refresh_data(self):
        time_since = time() - self.refresh_time
        self.refresh_time = time()
        block_time = self.throttle - time_since
        if block_time > 0:
            print "blocking refresh_data for ", block_time
            sleep(block_time)
 
        print "refresh_data connecting with server.."
 
        try:
            self.data = json.load(urllib.urlopen(self.GET_URL))
        except ValueError:
            attempts = 1
            if attempts >= 1:
                raise ValueError("Error connecting with token %s, Invalid Token?, perhaps you need a /new-session" % self.TOKEN)
 
 
class Fleet:
    def __init__(self, data):
        self.planes = []
        self.refresh(data)
 
    def refresh(self, data):
        print "refreshing fleet.."
        print data['boundary']
        print data['runway']
        #pprint(data['objects'])
        #pprint(data)
 
    def directions(self):
        directions = []
        #example algorithm:
        for plane in self.planes:
            directions.append(
                {
                    "plane_id": plane.plane_id,
                    "waypoint": {"x": 650, "y": 650} #{"x": runway.point.x, "y": runway.point.y}
                }
            )
        return directions
 
 
MH = MileHigh()
fleet = Fleet(MH.data)
 
while True:
    MH.refresh_data()
    fleet.refresh(MH.data)
    output = {
            "token": MH.TOKEN,
            "directions": fleet.directions()
        }
    MH.do_post(output)