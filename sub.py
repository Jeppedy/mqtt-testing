#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time

Q_BROKER="localhost"
Q_PORT=1883
Q_TOPIC="temperatures"
#Q_BROKER="m11.cloudmqtt.com"
#Q_PORT=19873
#Q_USER="prcegtgc"
#Q_PSWD="7frPa1U_VXqA"

# The callback for when the client receives a CONNACK response from the server.
IsConnected=False
cnxnRC=-1

def on_connect(client, userdata, flags, rc):
    global IsConnected,cnxnRC
    print("CB: Connected;rtn code [%d]"% (rc) )
    print("Flags:"+str(flags))
    cnxnRC=rc
    if( rc == 0 ):
        IsConnected=True
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(Q_TOPIC, 1)

def on_disconnect(client, userdata, rc):
    global IsConnected
    print("CB: Disconnected with rtn code [%d]"% (rc) )
    IsConnected=False

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_log(client, userdata, level, buf):
    print("log: ",buf)



def run(client):
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
#    client.on_log = on_log
#    client.username_pw_set(Q_USER, Q_PSWD)

    client.connect(Q_BROKER, Q_PORT, 60)

    retry=0
    while( (not IsConnected) and cnxnRC == -1 and retry <= 10):
        print("Waiting for Connect")
        time.sleep(.05)
        client.loop()
        retry += 1
    if( not IsConnected ):
        print("No connection could be established: rc[%d]") % cnxnRC
        return

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()


mqttc = mqtt.Client(__file__, clean_session=True)
try:
    run(mqttc)
except KeyboardInterrupt:
    print "Keyboard Interrupt..."
finally:
    print "Exiting."

    time.sleep(.25)
    mqttc.disconnect()
    while( IsConnected ):
        print("Waiting for Disconnect")
        time.sleep(.05)
        mqttc.loop()


