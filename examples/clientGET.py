"""
Created on 08-09-2012

@author: Maciej Wasilak
"""

import sys
from ipaddress import ip_address

from twisted.internet import reactor
from twisted.python import log

import txthings.coap as coap
import txthings.resource as resource



""" 
IoT device IP list with device name 
"""
# --------------------------------------------------- #

# WHITEBOX 
WHITEBOX1 = {"name": "WHITEBOX1", "ip":"100.67.95.76", "location":"TS430"}
WHITEBOX2 = {"name": "WHITEBOX2", "ip":"192.168.0.120", "location":"PSOAS"}

# BLACKBOX
BLACKBOX1 = {"name": "BLACKBOX1", "ip":"100.78.15.169", "location":"TS430"}
BLACKBOX2 = {"name": "BLACKBOX2", "ip":"192.168.0.119", "location":"PSOAS"}

# MaxPain
MAXPAIN1 = {"name": "MAXPAIN1", "ip":"100.74.234.165", "location":"TS430"}
MAXPAIN2 = {"name": "MAXPAIN2", "ip":"192.168.0.106", "location":"PSOAS"}
# --------------------------------------------------- #


"""
Server configurations:
Use any of the above device as the where server.py script is running. 
"""
# --------------------------------------------------- #

# SERVER  		= WHITEBOX1 			
# SERVER  		= WHITEBOX2 			
# SERVER  		= BLACKBOX1 			
# SERVER  		= BLACKBOX2 			
# SERVER 		= MAXPAIN1
SERVER 			= MAXPAIN2
SERVER_IP_ADDRESS    	= "%(ip)s" % SERVER 

# --------------------------------------------------- #


"""
URI: Unifrom Resource Identifier
URL: Unifrom Resource Locator

URI &/ URL should be in byte i.e. some_string.encode(encoding) or bytes(some_string, encoding).
Here default encoding is 'utf-8' if no explicit encoding pass encode method.

# Send request to "coap://coap.me:5683/test"
# request.opt.uri_path = (b'test',)
"""
# --------------------------------------------------- #

URI_COUNTER 			= b'test'
#URI_COUNTER 			= bytes('test', 'utf-8') 
#URI_COUNTER 			= 'test'.encode() 
#URI_COUNTER 			= 'test'.encode('utf-8') 

# --------------------------------------------------- #



class Agent:
    """
    Example class which performs single GET request to coap.me
    port 5683 (official IANA assigned CoAP port), URI "test".
    Request is sent 1 second after initialization.

    Remote IP address is hardcoded - no DNS lookup is preformed.

    Method requestResource constructs the request message to
    remote endpoint. Then it sends the message using protocol.request().
    A deferred 'd' is returned from this operation.

    Deferred 'd' is fired internally by protocol, when complete response is received.

    Method printResponse is added as a callback to the deferred 'd'. This
    method's main purpose is to act upon received response (here it's simple print).
    """

    def __init__(self, protocol):
        self.protocol = protocol
        reactor.callLater(1, self.requestResource)

    def requestResource(self):
        request = coap.Message(code=coap.GET)
        # Send request to "coap://coap.me:5683/test"
        request.opt.uri_path = (URI_COUNTER, )
        request.opt.observe = 0
        request.remote = (ip_address(SERVER_IP_ADDRESS), coap.COAP_PORT)
        print("-----------------------------------------------------------", request.opt.uri_path)
        d = protocol.request(request, observeCallback=self.printLaterResponse)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        print('First result: ' + str(response.payload, 'utf-8'))
        # reactor.stop()

    def printLaterResponse(self, response):
        print('Observe result: ' + str(response.payload, 'utf-8'))

    def noResponse(self, failure):
        print('Failed to fetch resource:')
        print(failure)
        # reactor.stop()


log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol)

reactor.listenUDP(61616, protocol)  # , interface="::")
reactor.run()
