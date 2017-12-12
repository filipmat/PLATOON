#!/usr/bin/env python

import controllerGUI

import controller1
import controller_vel
import controller_vel_1truck

from platoon.msg import truckmocap
from platoon.msg import truckcontrol

import rospy
import sys


def main(args):

    address1 = ('192.168.1.194', 2390)
    address2 = ('192.168.1.193', 2390)

    address = address2   # Truck address.
    truck_id = 2
    try:
        if int(args[1]) == 1:
                address = address1   # Truck address.
                truck_id = 1
    except:
        pass

    # Information for controller subscriber.
    node_name = 'controller_sub'
    mocap_topic_name = 'truck_topic'
    mocap_topic_type = truckmocap

    truck_topic_name = 'truck_control'
    truck_topic_type = truckcontrol

    # Data for controller reference path.
    x_radius = 1.7
    y_radius = 1.2
    center = [0.3, -1.3]

    # Controller tuning variables.
    v = 0.8             # Speed of the truck.

    k_p = 0.5
    k_i = -0.02
    k_d = 3

    v_ref = 0.89

    Ts = 0.05

    k_pv = 4
    k_iv = 0
    k_dv = 0
    e_ref = 0.5
    distance_offset = 0.4

    c1 = controller1.Controller(
        address, node_name, mocap_topic_type, mocap_topic_name,
        v = v, k_p = k_p, k_i = k_i, k_d = k_d,
        truck_id = truck_id)
    c1.set_reference_path([x_radius, y_radius], center)

    vel1 = controller_vel_1truck.Controller(
        address, node_name, mocap_topic_type, mocap_topic_name,
        v = v, k_p = k_p, k_i = k_i, k_d = k_d,
        k_pv = k_pv, k_iv = k_iv, k_dv = k_dv,
        e_ref = e_ref, distance_offset = distance_offset)
    vel1.set_reference_path([x_radius, y_radius], center)

    vel = controller_vel.Controller(address1, address2, node_name,
        mocap_topic_type, mocap_topic_name,
        v_ref, k_p, k_i, k_d, k_p, k_i, k_d,
        k_pv = k_pv, k_iv = k_iv, k_dv = k_dv,
        e_ref = e_ref, distance_offset = distance_offset)
    vel.set_reference_path([x_radius, y_radius], center)

    #ctrl_gui_1 = controllerGUI.ControllerGUI(c1)
    #ctrl_gui_vel1 = controllerGUI.ControllerGUI(vel1)

    ctrl_gui_vel = controllerGUI.ControllerGUI(vel)


if __name__ == '__main__':
    main(sys.argv)
