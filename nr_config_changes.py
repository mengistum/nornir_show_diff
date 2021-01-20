#!/usr/bin/env python

"""
Author:    Meheretab Mengistu
Purpose:   To modify config on Cisco switches
Version:   1.0
Works with: Nornir 3.0
Date:      January 14, 2021
"""

# Import NORNIR, nornir_netmiko, nornir_utils modules and myfuncs package
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from myfuncs.imp_funct import get_credentials, read_file, generate_hosts_yaml


# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username, password):
    """Use user credentials to generate defaults.yaml file

    Parameters:
    username  - username to SSH to the remote device
    password  - password to SSH to the remote device

    Returns:
    """

    # Open (or create and open) defaults.yaml file to sotre
    # username/password to SSH to devices
    with open('inventory/defaults.yaml', 'w') as default_file:
        default_file.write(f'---\nusername: {username}\npassword: {password}\n')
        default_file.write('...')

def main():
    """Execution starts here
    """

    # The following lines added to make it easily human readable
    print("\n" + "*"*79)
    print("\n 		Network Automation built using NORNIR Automation Framework!!!    \n")
    print("*"*79 + "\n")

    # Get IP addresses of devices you want to connect with
    devices_txt = input("Please enter .txt file containing IP addresses [devices.txt]: ")\
    or 'devices.txt'
    devices = read_file(devices_txt)

    # Generate hosts.yaml file for NORNIR
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')

    # Get the list of commands to run on each device
    commands_txt = input("Please enter .txt file containing commands [commands_config.txt]: ")\
    or 'commands_config.txt'

    # Accept user credentials from the user
    username, password = get_credentials()

    # Generate defaults.yaml file for NORNIR
    generate_defaults_yaml(username, password)

    # Instantiate a NORNIR object from .yaml file
    nr_obj = InitNornir(config_file='config.yaml')

    # Push the commands to the device and print the result
    nr_result = nr_obj.run(task=netmiko_send_config, config_file=commands_txt)
    print_result(nr_result)

    # Wipe out defaults.yaml file to remove credentials
    generate_defaults_yaml('cisco', 'password')

    # Wipe out hosts.yaml file to remove devices IP addresses
    devices = ['1.1.1.1', '2.2.2.2']
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')


if __name__ == "__main__":
    # Execute main from here
    main()

    # Freeze screen until any key pressed
    input('Press any key to exit!!!')
