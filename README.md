txThings
========
A very simple example of M2M communication protocol called CoAP with Twisted framework. I made a slight modification for myself from [this repository](https://github.com/mwasilak/txThings).

##### Requirements
Run the following command - 

    sudo pip install --upgrade pip    
    sudo pip install -r requirements.txt

##### How to run?
For this experiment we could use one single device (either a PC or a RPi). But I took 2 Raspberry Pi where one is client and another is server having following configuration. I made dictonay
 where every device has two keys named `name` & `ip`. You just need to change the value for `ip` since IP is changed from network to network.
- server
  * `WHITEBOX1` --- 100.67.95.76
  * `WHITEBOX2` --- 192.168.0.120
- client
  * `BLACKBOX1` --- 100.78.15.169
  * `BLACKBOX2` --- 192.168.0.119

We do not actually need any client IP but to see from which device the server is getting the request for a specific request. Lets keep it easy for now. 

- **server**
Let us assume, the first RPi (WHITEBOX1) is our server. We need the IP for client to send the request to it. So let's get the IP and then run the server script to the first RPi (WHITEBOX1).

        ifconfig | grep inet[^6]
        sudo python3 examples/server.py

- **client**
We got `100.67.95.76` (you may get different) as `ifconfig | grep inet[^6]` at the first RPi (WHITEBOX1). I use BLACKBOX1 as client to see whether WHITEBOX1 server got the request from it or
 not? Then I modifidy cilent script to access the server at `examples/clientGET.py`. We need to modify 4 things here -- 
  * `ip` --- we need to modify ip value to 100.67.95.76 at `WHITEBOX1` device in dictionary definition as server at line -- 

        WHITEBOX1 = {"name":"WHITEBOX1", "ip":"100.67.95.76"}

  * `SERVER` --- 

        SERVER = WHITEBOX1

  * `URI` --- request.opt.uri_path (binary string value) at requestResource in Agent class

        request.opt.uri_path = (b'counter',)
  
  * SERVER_IP_ADDRESS --- 

        request.remote = (ip_address(SERVER_IP_ADDRESS), coap.COAP_PORT)

Finally, just run the client script following at BLACKBOX1 --
 
        sudo python3 examples/clientGET.py

##### Observation
Now look at 
- WHITEBOX1 
  * IP, port and requested url of the client with log messages
- BLACKBOX1 
  * response of the server with log messages