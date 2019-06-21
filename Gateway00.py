# importing libraries
import paho.mqtt.client as paho_client
import os
import socket
import ssl
from time import sleep
from random import uniform
import json


#### local mosquitto parameters ####
host_local = '127.0.0.1'
username_local = 'yolanda'
mqttPwd_local = '123456'

def on_connect_local(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tag1")
    client.subscribe("tag2")

def on_message_local(client, userdata, msg):
    print("on_message")
    print(msg.topic + " " + str(msg.payload))

mqttc_local = paho_client.Client()
mqttc_local.username_pw_set("yolanda", password = "123456")
mqttc_local.on_connect = on_connect_local
mqttc_local.on_message = on_message_local
#mqttc_local.tls_set()
mqttc_local.connect(host_local, 1883, 60)


mqttc_local.loop_forever()

connflag = False

def on_connect_aws(client, userdata, flags, rc):            # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message_aws(client, userdata, msg):                  # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

mqttc_aws = paho_client.Client()                                   # mqttc object
mqttc_aws.on_connect = on_connect_aws                       # assign on_connect func
mqttc_aws.on_message = on_message_aws

#### AWS parameters #### 
awshost = "a2rbctfgaq78we-ats.iot.us-east-2.amazonaws.com"  # Endpoint
awsport = 8883                                              # Port no.   
clientId = "gateway"                                        # Thing_Name
thingName = "gateway"                                       # Thing_Name
caPath = "root-ca.pem"                                      # Root_CA_Certificate_Name
certPath = "cer.pem.crt"                                    # <Thing_Name>.cert.pem
keyPath = "private.pem.key"                                 # <Thing_Name>.private.key

# mqttc_aws.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

# mqttc_aws.connect(awshost, awsport, keepalive=60)         # connect to aws server

# mqttc_aws.loop_start()

#while True:
    # if connflag == True:
    #     pass
