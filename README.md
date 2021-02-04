# Network automation codes - originally written for Cisco switches and routers

SUMMARY: This script runs show commands on a Cisco device, compare the result with a template file, and stores the output in a text file. 

WHAT YOU WILL NEED: You can download and use these codes for Cisco IOS XE devices. Here is the list of files you will need:

- devices.txt ==> contians the IP addresses of network equipments you need to SSH to. Please modify it to the correct IP addresses you want to SSH to.

- commands\_show.txt ==> list of show commands you need to run --> One command per line. Please modify it with the correct commands you need to run. I have added all the commands I used when I was checking for Phase-2&3 LAN Upgrade.

- config.yaml ==> an inventory list containing info about hosts, groups and defaults setup. You do NOT need to modify!

- myfuncs ==> a package containing functions I wrote. You do NOT need to modify!

- inventory ==> a folder containing list of yaml files. You do NOT need to modify!

- templates ==> a folder containing list of template files, which we will use to compare the output of the running config with. Please modify it with the correct template files based on the commands you add in commands\_show.txt file.

- nr\_show\_diff.py ==> a python script to run show commands and compare config to a template config. Do NOT modify (unless you know what you are doing)!


REQUIREMENTS: This script was written and run using the following:
			python 3.8.7
			nornir 3.0.0
			nornir_netmiko 0.1.1
			nornir_utils 0.1.1
			

USAGE: 
1) If you want it to run on Windows OS, Mac OS, or Linux OS, please install all packages listed under REQUIREMENTS section. And run nr\_show\_diff.py script. You will be prompted to enter files containing devices and commands (simply press ENTER to use the default files), and enter your SSH username and password.

2) You can also run it on a DOCKER environment. Please pull the container to your docker environment as follows: "docker pull useth2020/nornir-show-diff" without the quotation marks. Then, change directory to /src/Nornir (cd /src/Nornir); modify either commands\_show.txt and devices.txt files; and run "python3 nr\_show\_cmds.py" without the quotation marks. You will be prompted to enter files containing devices and commands (simply press ENTER to use the default files), and enter your SSH username and password.


OUTPUT: If you enter correct information, the result will be written to TWO subfolders (EXTRA and MISSING) in a folder created by the script (name starts with "Nornir-" followed by datetime). When you open the subfolders, you will find text files with the commands names.
The files in EXTRA subfolder contains output of configs which are not found in the template files these are EXTRA or wrong configs.
The files in MISSING subfolder contains output of configs which are missing in the device(s); these are MISSING configs.
