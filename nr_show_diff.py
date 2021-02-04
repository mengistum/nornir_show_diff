#!/usr/bin/env python

"""
Author: Meheretab Mengistu
Purpose: A script based on Nornir 3.0.0 framework to run one or more
    "show commands" on one or more network devices, compare the output
    with template file(s), and save the output to file(s).
Version: 2.0
Date: February 4, 2021
"""

# Import NORNIR module, datetime module, OS module
# and myfuncs module (module written by me)
import os
from datetime import datetime
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
#from nornir_utils.plugins.functions import print_result
from myfuncs.imp_funct import get_credentials, read_file, generate_hosts_yaml


# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username, password):
    """Use user credentials to generate defaults.yaml file
    Parameters:
    username - username to SSH to the remote device
    password - password to SSH to the remote device
    Returns:
    """

    # Open (or create and open) defaults.yaml file to store
    # username/password to SSH to devices
    with open('inventory/defaults.yaml', 'w') as default_file:
        default_file.write(f'---\nusername: {username}\npassword: {password}\n')
        default_file.write('...')


# Compare two lists and return the difference
def difference(list1, list2):
    """Take two lists, compare them, and return the difference
    Parameters:
    list1 - first list to compare
    list2 - second list to compare
    Returns:
    list: diff_list
    """
    diff_list = list(set(list1)-set(list2))
    return diff_list


def main():
    """
    Execution begins here
    """

    # The following lines added to make it easy for human users to read
    print('\n' + '*' * 79)
    print('\n       Network automation built using NORNIR Automation Framework!!    \n')
    print('*' * 79 + '\n')

    # Get IP addresses of devices you want to connect and generate hosts.yaml file
    devices_txt = input('Please enter .txt file containing IP addresses [devices.txt]: ')\
     or 'devices.txt'
    devices = read_file(devices_txt)
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')

    # Get the list of commands to run on each device
    commands_txt = input('Please enter .txt file containing commands [commands_show.txt]: ')\
     or 'commands_show.txt'
    commands = read_file(commands_txt)

    # Get user credentials from the user
    username, password = get_credentials()
    # Generate 'inventory/defaults.yaml' file containing user credential
    generate_defaults_yaml(username, password)

    # Instantiate a Nornir object from .yaml file
    nr_obj = InitNornir(config_file='config.yaml')

    # Get the current time
    time_now = datetime.now().isoformat(timespec='seconds')

    # Create a Folder as a holder for the output files
    dirname = 'NORNIR-' + time_now.replace(':', '')
    os.mkdir(dirname)

    # Add subfolders, EXTRA and MISSING, inside the main folder
    dirname_extra = '/'.join((dirname, "EXTRA"))
    os.mkdir(dirname_extra)
    dirname_missing = '/'.join((dirname, "MISSING"))
    os.mkdir(dirname_missing)

    # Iterate on each command provided by the user
    for cmd in commands:
        # Run the command cmd suing netmiko send command
        nr_result = nr_obj.run(task=netmiko_send_command, command_string=cmd)
        # Print AggregatedResult to screen
        # If you are going to print_result, uncomment the import line:
        # ... import print_result and the line below
        # print_result(nr_result)

        # Replace '|' and ' ' characters with '_' for filename
        cmd_name = cmd.replace('|', '_').replace(' ', '_')

        # Create two files for each command
        # filename_extra: to compare the switch config with the template
        filename_extra = '/'.join((dirname_extra, f'result_{cmd_name}.txt'))
        # filename_missing: to reverse compare the template with the switch config
        filename_missing = '/'.join((dirname_missing, f'result_{cmd_name}.txt'))

        # Retrieve the template_file list from the command to process; each of
        # these template files need to exist in the parent folder
        template_file = read_file(f'templates/{cmd_name}.txt')

        # Open the file you created to write to
        with open(filename_extra, 'w+') as new_file:

            # Print to a file in a human-friendly format
            for device, results in nr_result.items():
                if not results[0].failed:
                    # Create interim_list by comparing the output of the command with the template
                    interim_list = difference((results[0].result.splitlines()), template_file)

                    # Get the final_list to print; the final_list should not contain snmp-server
                    # location or aaa password (when hashed it will be different for each device
                    # -- even if the password is the same)
                    final_list = [substr for substr in interim_list if not substr.startswith(\
                        (' key 7', 'snmp-server location'))]

                    # Convert the final_list to a string, out_str, and write the output to
                    # a file if it is not empty
                    if final_list != ['']:
                        if final_list != []:
                            # Convert the list to a string
                            out_str = '\n'.join(map(str, final_list))
                            # Write the output to a file
                            print(f'\n"{device}": \n\n{out_str}\n\n', file=new_file)

        # Open the file you created to write to
        with open(filename_missing, 'w+') as new_file:

            # Print to a file in a human-friendly format
            for device, results in nr_result.items():
                if not results[0].failed:
                    # Create interim_list by comparing the output of the command with the template
                    interim_list = difference(template_file, (results[0].result.splitlines()))

                    # Get the final_list to print; the final_list should not contain snmp-server
                    # location or aaa password (when hashed it will be different for each device
                    # -- even if the password is the same)
                    final_list = [substr for substr in interim_list if not substr.startswith(\
                        (' key 7', 'snmp-server location'))]

                    # Convert the final_list to a string, out_str, and write the output to
                    # a file if it is not empty
                    if final_list != ['']:
                        if final_list != []:
                            # Convert the list to a string
                            out_str = '\n'.join(map(str, final_list))
                            # Write the output to a file
                            print(f'\n"{device}": \n\n{out_str}\n\n', file=new_file)


    # Wipe out defaults.yaml file to remove credentials
    # Use 'cisco' and 'password' as place holder credentials
    generate_defaults_yaml('cisco', 'password')

    # Wipe out hosts.yaml file to remove devices IP addresses
    # Use 1.1.1.1 and 2.2.2.2 as a place holder IP addresses
    devices = ['1.1.1.1', '2.2.2.2']
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')


if __name__ == "__main__":
    # Execute main from here
    main()

    # Freeze screen until any key pressed
    input('Enter any key to exit!!!')
