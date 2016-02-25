---
layout: post
title:  "Sandbox Cluster Guide"
date:   2016-02-25 09:30:00 
categories:   cluster lessons
---
## Materials
* 4 Raspberry Pi
* 4 Micro-USB cable (the cable you would use to charge an Android phone)
* 4 microSD cards with adapters
* 1 HDMI cable
* 4 Ethernet cable
* 1 USB keyboard 
* 1 USB Mouse
* 1 4-port ethernet switch
* 1 4-port usb hub


----

## Basic Process

### Installing Operating System Image:

If you bought the microSD cards with the NOOB image installed on it, then you can skip these instructions. These instructions are for if you do not have an operating system installed on your microSD card or if you encounter a problem during any of the following steps and need to restart. A good resource that may help you with majority of the steps can be found at: [https://www.raspberrypi.org/documentation/installation/installing-images/README.md]

For the following instructions, it is created for the image Raspbian Jessie.

Optional helpful software for Mac users: [http://ivanx.com/raspberrypi/]

Once the tool has been downloaded, unzip the folder and the tool will be ready to run. When installing the image onto the SD card, you can utilize this tool which will give you an estimate of the remaining time till the card is completed. It provides step by step aid on what to do throughout the process.

----

## The Process:

### pinode-0 (Master node):
1. Boot master node (pinode-0) with WiFi dongle, an HDMI cable,  an ethernet cable, keyboard and mouse plugged in.
   1. Change the password of the master node
       1. Type passwd into the terminal
       2. By default, the current password = raspberry 
       3. Enter the new password twice (write that down just in case)
2. Expanding the raspberry pi file system
   1. Type `sudo raspi-config` into the terminal
   2. Navigate to Expand File System and click **Enter**
   3. After selecting the expanded file system option, it should return an **OK**
   4. The System may ask to be rebooted
3. Set up the keyboard, time configuration, and wifi
   1. Go to Menu -> Preferences -> Raspberry Pi Configuration-> Localisation
   2. Set the appropriate Locale, Timezone and the Keyboard and then click **OK**
   3. Reboot
   4. Connect to Wifi - SDSC
4. Configure wlan0
   1. Use `ssh-keygen` to generate the RSA key pair
      1. Press **ENTER** for “Enter the file in which to save the key”
      2. Press **ENTER** for the “Enter passphrase"
          *  _it will be empty because we do not want to establish a password_ 
5. Clone this repo to home directory
   1. Copy the github address to clone that repository from [https://github.com/sdsc/sandbox-cluster-guide](https://github.com/sdsc/sandbox-cluster-guide)
   2. Type `git clone https://github.com/sdsc/sandbox-cluster-guide.git`  into the terminal.
   3. Change into the sandbox-cluster-guide folder:  `cd sandbox-cluster-guide`
   4. Changes the branch to the appropriate version: `git checkout beta-workshop`
   5. Change into the config folder: `cd config`
6.Deploy configuration (./deploy.sh <node number>)
   1. Call the deploy script from the config directory. It takes a parameter which is a number that represents which node this is. Use the following command in the terminal:  `./deploy.sh 0` This command may take a few minutes to finish.
      1. After the script is complete, it is fine if you see “sudo: unable to resolve host raspberrypi” in the output. As long as the script completed, you can continue with the instructions.
   2. Verify that the hostname is set:
      1. Type `more/etc/hosts` into the terminal.  You should see an ip address similar to **127.0.0.1** on the left side and the name of the node on the right across from the ip address should be pinode-0. Check to make sure that it is set accordingly
7. Reboot
8. Restore the iptables rule-set
   1. Type `sudo iptables-restore < /etc/network/iptables` into the terminal. After this command is completed, it should return to a new line.
 
### All other nodes:

**_The following instructions will be repeated for the remaining raspberry pi nodes. Note: All of the following commands will still be run from pinode-0, or the master node. There is no need to unplug and plug the keyboard and mouse into each new node._**

1. Boot another raspberry pi with an ethernet cable plugged in. Give it a minute or two before continuing with the instructions.
2. Check what the IP address of the new node is
   1. Since the master node is running a DCHP server, you can check the IP address that the server assigned to the new node. Type `arp -a` into the terminal. Look for the address that has a mac address and has not previously been used by another node.
   2.Check that the IP address is accessible from pinode-0 by pinging it.
      1. Type `sudo ping -c 4 <ip address>` into the terminal.
      2. Wait until all 4 packets have been sent. If the address is accessible, it will return with a statement that all packets were sent successfully. If the packets were not sent successfully and were lost, then that is probably not the correct address. Restart step 2.
3. Connecting to the new node
   1. After you have found the correct IP address, type `ssh <ip address>` into the terminal to connect to it.
      1. Enter **yes** into the prompt about adding the key from this node into memory.
      2. You will be prompted for the default password of the node that you are accessing. Enter the default raspberry pi password. **raspberry**
4. Expanding the raspberry pi file system
   1. Type `sudo raspi-config` into the terminal.
   2. Navigate to Expand File System and click **ENTER**.
   3. After selecting the expand file system option, it should return an **OK**.
   4. System may ask to be rebooted.
5. Clone the github repo to home directory
   1. After the raspberry pi has been rebooted, connect back to the node using `ssh <ip address>` and using the default raspberry pi password.
   2. Copy the github address to clone that repository from [https://github.com/sdsc/sandbox-cluster-guide](https://github.com/sdsc/sandbox-cluster-guide)
   3. Type `git clone https://github.com/sdsc/sandbox-cluster-guide.git` into the terminal.
   4. Change into the sandbox-cluster-guide folder: `cd sandbox-cluster-guide`
   5. Changes the branch to the appropriate version: `git checkout beta-workshop`
   6. Change into the config folder: `cd config`  
6. Deploy configuration (./deploy.sh <node number>)
   1. Call the deploy script from the config directory. It takes a parameter, #, which is a number that represents which node this is. Use the following command in the terminal:  `./deploy.sh #` This command may take a few minutes to finish.
      1. After the script is complete, it is fine if you see “_sudo: unable to resolve host raspberrypi_” in the output. As long as the script completed, you can continue with the instructions.
   2. Verify that the hostname is set:
      1. Type `more /etc/hosts` into the terminal.  You should see an ip address similar to 172.x.x.x on the left side and the name of the node on the right across from the ip address should be the pinode-# where # is the same as the number that you entered for the deploy script section. Check to make sure that it is set accordingly.
7. Reboot
8. Verify that the node was set up correctly
   1. After the node has been fully rebooted, type `ssh pinode-#` into the terminal. The “#” should be the same as the number that you entered for the deploy script section. If the node was set up successfully, you should be able to access the node without having the enter any password. 
      * Note: On the first connect, you might have to enter `yes` when prompted to adding the key from this node into memory.


### Notes:

To access the terminal, you can either:
* Click the Desktop icon on the top menu bar
* Go through Menu->Accessories->Terminal

To check which files are in the current directory: 
* ls


[https://www.raspberrypi.org/documentation/installation/installing-images/README.md]:https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[http://ivanx.com/raspberrypi/]:http://ivanx.com/raspberrypi/

