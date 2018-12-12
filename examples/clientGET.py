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
WHITEBOX1 = {"name": "WHITEBOX1", "ip":"100.67.95.76"}
WHITEBOX2 = {"name": "WHITEBOX2", "ip":"192.168.0.120"}

# BLACKBOX
BLACKBOX1 = {"name": "BLACKBOX1", "ip":"100.78.15.169"}
BLACKBOX2 = {"name": "BLACKBOX2", "ip":"192.168.0.119"}

# --------------------------------------------------- #


"""
Server configurations:
Use any of the above device as the where server.py script is running. 
"""
# --------------------------------------------------- #

SERVER 			= WHITEBOX1
SERVER_IP_ADDRESS    	= "%(ip)s" % SERVER 

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
        # request.opt.uri_path = (b'test',)
        request.opt.uri_path = (b'counter',)
        request.opt.observe = 0
        request.remote = (ip_address(SERVER_IP_ADDRESS), coap.COAP_PORT)
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
