#!usr/bin/env python

import optparse
from zmqfan import zmqsub
import thingsbus.client
import socket
import time
import json

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri
json_string = "{value:'Not set'}"
arr = {}
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".js"):
                f = open(curdir + sep + "scripts/" + self.path) #self.path has /test.html
                self.send_response(200)
                self.send_header('Content-type',	'application/x-javascript')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".css"):
                f = open(curdir + sep + "styles/" + self.path) #self.path has /test.html
                self.send_response(200)
                self.send_header('Content-type',	'text/css')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".json"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',	'application/json')
                self.end_headers()
                self.wfile.write(json_string)
                return
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

if __name__ == '__main__':
    client = thingsbus.client.Client(zone='pumpingstationone.org')

    def print_e(e):
        global json_string, arr
        print (e.thing.ns)
        arr[e.thing.ns] = e.data
        json_string=json.dumps(arr)

    #thing = client.directory.get_thing("spacemon.electronics")
    thing = client.directory.root
    thing.subscribe(print_e, thingsbus.client.F_TREE)
    try:
        server = HTTPServer(('', 8042), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

