# Configuring the Cluster

## Installing Operating System Image

If you bought the microSD cards with the NOOB image installed on it, then you can skip these instructions. These instructions are for if you do not have an operating system installed on your microSD card or if you encounter a problem during any of the following steps and need to restart. A good resource that may help you with majority of the steps can be found [in the Raspberry Pi documentation](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

For the following instructions, it is created for the image Raspbian Jessie.

Optional helpful software for Mac users: [http://ivanx.com/raspberrypi/]

Once the tool has been downloaded, unzip the folder and the tool will be ready to run. When installing the image onto the SD card, you can utilize this tool which will give you an estimate of the remaining time till the card is completed. It provides step by step aid on what to do throughout the process.

## Setup `pinode-0` (the "Master" Node)

1. Boot the master node (pinode-0) with WiFi dongle (if needed), an HDMI cable, an ethernet cable, keyboard and mouse plugged in. 
1. Open a terminal
   1. Change the password of the master node
       1. Type passwd into the terminal
       1. By default, the current password = raspberry 
       1. Enter the new password twice (write that down just in case)
       ```
       pi@raspberrypi:~ $ passwd
       Changing password for pi.
       (current) UNIX password:
       Enter new UNIX password:
       Retype new UNIX password:
       pi@raspberrypi:~ $
       ```
   1. Expanding the Raspberry Pi file system
      1. Type `sudo raspi-config` into the terminal
       ```
       pi@raspberrypi:~ $ sudo raspi-config
       ```
      1. Navigate to Expand File System and click **Enter**
      1. After selecting the expanded file system option, it should return an **OK**
      1. The system may ask to be rebooted
1. Set up the keyboard, time configuration, and WiFi
   1. Go to Menu -> Preferences -> Raspberry Pi Configuration-> Localisation
   1. Set the appropriate Locale (probably changing the Country to "USA"), Timezone (e.g., Area as "US" and Location as "Pacific") and the Keyboard (Country to "United States" and Variant to "English (US)", you may need to scroll up) and then click **OK**
   1. Reboot when prompted
   1. Connect to WiFi
   1. Click on the network icon in the top right of the screen.
   1. Select or enter the SSID for your wireless connection.
   1. Enter the SSID password when prompted.
1. Use `ssh-keygen` to generate the RSA key pair
      1. Press **ENTER** for “Enter the file in which to save the key”
      2. Press **ENTER** for the “Enter passphrase"
          *  _it will be empty because we do not want to establish a password_ 
      ```
      pi@raspberrypi:~ $ ssh-keygen 
      Generating public/private rsa key pair.
      Enter file in which to save the key (/home/pi/.ssh/id_rsa): 
      Created directory '/home/pi/.ssh'.
      Enter passphrase (empty for no passphrase): 
      Enter same passphrase again: 
      Your identification has been saved in /home/pi/.ssh/id_rsa.
      Your public key has been saved in /home/pi/.ssh/id_rsa.pub.
      The key fingerprint is:
      ...snip...
      The key's randomart image is:
      +---[RSA 2048]----+
      ...snip...
      +-----------------+
      pi@raspberrypi:~ $ 
      ```
1. Clone the workshop repository to home directory
   1. Copy the github address to clone that repository from [https://github.com/sdsc/sandbox-cluster-guide](https://github.com/sdsc/sandbox-cluster-guide)
   2. Type `git clone https://github.com/sdsc/sandbox-cluster-guide.git`  into the terminal.
   3. Change into the sandbox-cluster-guide folder:  `cd sandbox-cluster-guide`
   4. Changes the branch to the appropriate version: `git checkout beta-workshop`
   5. Change into the config folder: `cd config`
1.Deploy configuration (./deploy.sh <node number>)
   1. Call the deploy script from the config directory. It takes a parameter which is a number that represents which node this is. Use the following command in the terminal:  `./deploy.sh 0` This command may take a few minutes to finish.
      1. After the script is complete, it is fine if you see “sudo: unable to resolve host raspberrypi” in the output. As long as the script completed, you can continue with the instructions.
   2. Verify that the hostname is set:
      1. Type `more/etc/hosts` into the terminal.  You should see an ip address similar to **127.0.0.1** on the left side and the name of the node on the right across from the ip address should be pinode-0. Check to make sure that it is set accordingly
1. Reboot
1. Restore the iptables rule-set
   1. Type `sudo iptables-restore < /etc/network/iptables` into the terminal. After this command is completed, it should return to a new line.

## The Other Node, `pinode-1`

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

## Next

[Linux Clusters](clusters.md)

