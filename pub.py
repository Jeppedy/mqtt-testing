#!/usr/bin/env python

import time
import paho.mqtt.client as mqtt

Q_BROKER="localhost"
Q_PORT=1883
Q_TOPIC="temperatures"
#Q_BROKER="m11.cloudmqtt.com"
#Q_PORT=19873
Q_USER="prcegtgc"
Q_PSWD="7frPa1U_VXqA"

IsConnected=False
cnxnRC=-1

def on_connect(client, userdata, flags, rc):
    global IsConnected,cnxnRC
    print("CB: Connected;rtn code [%d]"% (rc) )
    cnxnRC=rc
    if( rc == 0 ):
        IsConnected=True

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
#    mqttc.on_log = on_log
#    mqttc.username_pw_set(Q_USER, Q_PSWD)

    rc=mqttc.connect(Q_BROKER, Q_PORT)
    mqttc.loop_start()

    retry=0
    while( (not IsConnected) and cnxnRC == -1 and retry <= 10):
        print("Waiting for Connect")
        time.sleep(.05)
        mqttc.loop()
        retry += 1
    if( not IsConnected ):
        print("No connection could be established: rc[%d]") % cnxnRC
        return 

#    for x in range(1000):
    info=mqttc.publish(Q_TOPIC, "Message goes here", False)
#      print ("MsgID?:"+str(info) )
#      print ("IsPub?: %s")%(str(info.is_published()))
    info.wait_for_publish()
#      print ("IsPub?: %s")%(str(info.is_published()))
    print ("Pubish complete")

#    time.sleep(1)

    mqttc.disconnect()
    while( IsConnected ):
        print("Waiting for Disconnect")
        time.sleep(.05)

    mqttc.loop_stop()

#import paho.mqtt.publish as publish
#publish.single(Q_TOPIC, "payload", hostname=Q_BROKER, port=Q_PORT, auth={'username':Q_USER, 'password':Q_PSWD} )


run()
