#!/usr/bin/env python

import rospy
from modeltruck_platooning.msg import drive_param

from socket import *
import struct
import time

import sys

seqNum = 0

firstPack = True

packer = struct.Struct('<IIHhhh') # Format: <timestamp ms> <timestamp us> <seqNum> <velocity> <angle> <gear>

def receiver(vehicle_id):
    global seqNum, firstPack
    velocity = 1500
    angle = 1500
    gear = 60   #first gear

    vel = velocity
    ang = angle
    gr = gear

    if vehicle_id == 1:
        address = ('192.168.1.193', 2390)

    elif vehicle_id == 2:
        address = ('192.168.1.194', 2390)

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(0.1)

    ms = 0xFFFFFFFF # Send all F in first pack to notify data-reset
    ns = 0xFFFFFFFF
    seqNum = 0xFFFF
    firstPack = False

    while True:
        inpt = eval(raw_input('\nEnter velocity\n'))


        if inpt != 0:
            vel = inpt


        t = time.time()
        ms = int(t)
        ns = int((t % 1) * (10**9))

        print('\nVelocity: {}\nAngle: {}\nGear: {}'.format(vel, ang, gr))


        command_msg = packer.pack(*(ms,  ns, seqNum, vel, ang, gr))
        client_socket.sendto(command_msg, address)

        if len(inpt) == 0:
            break



if __name__ == '__main__':
    try:
        receiver(int(sys.argv[1])) # argv[1] which truck it is.
    except:
        pass
