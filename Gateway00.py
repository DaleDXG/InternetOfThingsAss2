# importing libraries
import paho.mqtt.client as paho_client
import os
import socket
import ssl
from time import sleep
from random import uniform
import json


#### AWS parameters #### 
awshost = "a2rbctfgaq78we-ats.iot.us-east-2.amazonaws.com"  # Endpoint
awsport = 8883                                              # Port no.   
clientId = "gateway"                                        # Thing_Name
thingName = "gateway"                                       # Thing_Name
caPath = "root-ca.pem"                                      # Root_CA_Certificate_Name
certPath = "cer.pem.crt"                                    # <Thing_Name>.cert.pem
keyPath = "private.pem.key"                                 # <Thing_Name>.private.key

connflag = False

def on_connect_aws(client, userdata, flags, rc):            # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message_aws(client, userdata, msg):                  # Func for Sending msg
    print("on_message_aws")
    #print(msg.topic+" "+str(msg.payload))

mqttc_aws = paho_client.Client()                                   # mqttc object
mqttc_aws.on_connect = on_connect_aws                       # assign on_connect func
mqttc_aws.on_message = on_message_aws

mqttc_aws.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
mqttc_aws.connect(awshost, awsport, keepalive=60)         # connect to aws server

#### local mosquitto parameters ####
host_local = 'jc_pi' #'127.0.0.1'
username_local = 'yolanda'
mqttPwd_local = '123456'

def on_connect_local(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tag")

def on_message_local(client, userdata, msg):
    print("on_message")
    print(msg.topic + " " + str(msg.payload))
    mqttc_aws.publish(msg.topic, msg.payload)

mqttc_local = paho_client.Client()
mqttc_local.username_pw_set("yolanda", password = "123456")
mqttc_local.on_connect = on_connect_local
mqttc_local.on_message = on_message_local
mqttc_local.tls_set("/etc/mosquitto/ca_certificates/ca.crt")
mqttc_local.connect(host_local, 8883, 60)


mqttc_local.loop_start()
mqttc_aws.loop_forever()

