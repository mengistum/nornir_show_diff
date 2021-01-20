#!/usr/bin/env python

"""
Author: Meheretab Mengistu
Purpose: A module containing multiple common functions.
Version: 1.3
Date: January 20, 2021
"""

# Import Netmiko and getpass modules
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,\
 NetMikoAuthenticationException


# Get Credentials
def get_credentials():
    """Get username and password

    Parameters:

    Returns:
    str: username
    str: password
    """

    username = input('\nPlease enter username: ')
    password = getpass()

    return username, password

# Get a text file and return lists
def read_file(filename):
    """Read a file and return lists

    Parameters:
    filename - a text file to read

    Returns:
    list: lines
    """

    with open(filename) as file:
        lines = file.read().splitlines()

    return lines

def connect_send(devices, commands, username, password):
    """SSH to devices, run the commands, and disconnect

    Parameters:
    devices - list of devices IP addresses
    commands - list of commands to run
    username - SSH username
    password - SSH password

    Returns:
    """
    # Iterate over the list of devices
    for ipaddr in devices:
        # Prepare device object to send to Netmiko
        device = {'device_type':'cisco_ios', 'ip':ipaddr, \
        'username':username, 'password':password}
        # Check whether there is Timeout or Authentication Error
        try:
            # Setup connection to the device using Netmiko
            connect_dev = ConnectHandler(**device)
            # Prepare and open file to write to
            filename = connect_dev.base_prompt + '.txt'
            with open(filename, 'w') as out_file:
                # Run each command on the device
                for cmd in commands:
                    out_file.write('*'*79)
                    out_file.write(' '*15 + '\n' + cmd + '\n')
                    out_file.write('*'*79)
                    out_file.write('\n'*2)
                    cmd_sent = connect_dev.send_command(cmd)
                    out_file.write(cmd_sent + '\n'*2)
                    out_file.write('#'*79)
                    out_file.write('#'*79)
                    # Print the result
                    print(cmd_sent)
            # Disconnect SSH to the device
            connect_dev.disconnect()
        except (NetMikoAuthenticationException, \
            NetMikoTimeoutException) as err:
            print(str(err))

# Generate hosts.yaml file for Nornir
def generate_hosts_yaml(devices, filename):
    """Use devices IP info to generate hosts.yaml file

    Parameters:
    devices - list of devices IP addresses
    filename - a file to write hosts in yaml format

    Returns:
    """

    # Open hosts file (or create one) to add hosts
    with open(filename, 'w') as hosts_file:
        # Make it YAML file
        hosts_file.write('---')
        # Iterate over the list of IP addresses
        for ipaddr in devices:
            if ipaddr[-2:]=='.1':
                hosts_file.write(f'\nSW_{ipaddr}:')
                hosts_file.write(f'\n  hostname: {ipaddr}')
                hosts_file.write('\n  groups:')
                hosts_file.write('\n    - BorderSW\n')
            else:
                hosts_file.write(f'\nSW_{ipaddr}:')
                hosts_file.write(f'\n  hostname: {ipaddr}')
                hosts_file.write('\n  groups:')
                hosts_file.write('\n    - Switch\n')
        hosts_file.write('...')
