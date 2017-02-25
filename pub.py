#!/usr/bin/env python

import time
import paho.mqtt.client as mqtt

Q_BROKER="localhost"
Q_PORT=1883
Q_TOPIC="hello"
#Q_BROKER="m11.cloudmqtt.com"
#Q_PORT=19873
#Q_USER="prcegtgc"
#Q_PSWD="7frPa1U_VXqA"

IsConnected=False
IsCnxnErr=False

def on_connect(client, userdata, flags, rc):
    global IsConnected,IsCnxnErr
    print("CB: Connected;rtn code [%d]"% (rc) )
    if( rc == 0 ):
        IsConnected=True
    else:
        IsCnxnErr=True

def on_disconnect(client, userdata, rc):
    global IsConnected
    print("CB: Disconnected with rtn code [%d]"% (rc) )
    IsConnected=False

def on_publish(client, userdata, msgID):
    print("CB: Published with MsgID [%d]"% (msgID) )

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def run():
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_publish = on_publish
    mqttc.on_log = on_log
#    mqttc.username_pw_set(Q_USER, Q_PSWD)

    rc=mqttc.connect(Q_BROKER, Q_PORT)
    mqttc.loop_start()

    retry=0
    while( (not IsConnected) and (not IsCnxnErr) and retry <= 10):
        print("Waiting for Connect")
        time.sleep(.05)
        retry += 1
    if( not IsConnected or IsCnxnErr ):
        print("No connection could be established")
        return 

    rc=mqttc.publish(Q_TOPIC, "Hello, World!",2)
    rc=mqttc.publish(Q_TOPIC, "Hello, World2",2)
    rc=mqttc.publish(Q_TOPIC, "Hello, World3",2)

    time.sleep(.25)

    mqttc.disconnect()
    while( IsConnected ):
        print("Waiting for Disconnect")
        time.sleep(.05)

    mqttc.loop_stop()

#import paho.mqtt.publish as publish
#publish.single(Q_TOPIC, "payload", hostname=Q_BROKER, port=Q_PORT, auth={'username':Q_USER, 'password':Q_PSWD} )


run()
