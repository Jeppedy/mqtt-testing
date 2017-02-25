#!/usr/bin/env python

import paho.mqtt.client as mqtt

Q_BROKER="localhost"
Q_PORT=1883
Q_TOPIC="hello"
#Q_BROKER="m11.cloudmqtt.com"
#Q_PORT=19873
#Q_USER="prcegtgc"
#Q_PSWD="7frPa1U_VXqA"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("CB: Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Q_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_log(client, userdata, level, buf):
    print("log: ",buf)

client = mqtt.Client()
#client.username_pw_set(Q_USER, Q_PSWD)
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log


client.connect(Q_BROKER, Q_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
