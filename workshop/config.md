# Configuring the Cluster

## Installing Operating System Image

If you bought the microSD cards with the NOOB image installed on it,
or if the cards have already been imaged by a friendly instructor, you
can skip this section. These instructions are for if you do
not have an operating system installed on your microSD card or if you
encounter a problem during any of the following steps and need to
restart. A good resource that may help you with majority of the steps
can be found
[in the Raspberry Pi documentation](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

For the following instructions, it is created for the image Raspbian Jessie.

Optional helpful software for Mac users: [http://ivanx.com/raspberrypi/]

Once the tool has been downloaded, unzip the folder and the tool will
be ready to run. When installing the image onto the SD card, you can
utilize this tool which will give you an estimate of the remaining
time till the card is completed. It provides step by step aid on what
to do throughout the process.

## Setup `pinode-0` (the "Master" Node)

_Hint: `pinode-0` goes to the left hand LCD panel._

1. Boot `pinode-0` with WiFi dongle (if needed), an HDMI cable, an ethernet cable, keyboard and mouse plugged in. 
1. If your SD cards have NOOBS pre-installed you will be prompted at the
beginning to install the operating system Raspbian. Just select
Raspbian and click install.
1. After the node boots set up the keyboard, time configuration, and WiFi
   1. Go to Menu -> Preferences -> Raspberry Pi Configuration-> Localisation
   1. Set the appropriate Locale (probably changing the Country to "USA"), Timezone (e.g., Area as "US" and Location as "Pacific") and the Keyboard (Country to "United States" and Variant to "English (US)", you may need to scroll up) and then click **OK**
   1. Reboot when prompted
1. Connect to WiFi
   1. Click on the network icon in the top right of the screen.
   1. Select or enter the SSID for your wireless connection.
   1. Enter the SSID password when prompted.
1. Open a terminal (this is the icon that looks like a TV on the upper
   left of the desktop).
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

   1. Expand the Raspberry Pi file system by typing `sudo raspi-config
    --expand-rootfs ` into the terminal. Reboot the Pi if prompted.
   1. Use `ssh-keygen` to generate the RSA key pair
      1. Press **ENTER** for “Enter the file in which to save the key”
      1. Press **ENTER** for the “Enter passphrase" _(It will be empty
      because we do not want to establish a password so we can
      automatically connect between our compute nodes.)_
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
  1. In a terminal window clone the workshop repository to home directory.
     1. Copy the GitHub address to clone that repository from [https://github.com/sdsc/sandbox-cluster-guide](https://github.com/sdsc/sandbox-cluster-guide)
     1. Type `git clone --depth=1 https://github.com/sdsc/sandbox-cluster-guide.git`  into the
        terminal. (The `--depth=1` option tells `git` to only pull down the latest version
        to save time and space.)
     1. Change into the sandbox-cluster-guide folder:  `cd sandbox-cluster-guide`
     1. Change into the config folder: `cd config`
     1. Deploy configuration (`./deploy.sh <node number>`)
     ```
     pi@raspberry:~ $ git clone --depth=1 https://github.com/sdsc/sandbox-cluster-guide.git
     Cloning into 'sandbox-cluster-guide'...
     remote: Counting objects: 452, done.
     remote: Compressing objects: 100% (43/43), done.
     remote: Total 452 (delta 20), reused 0 (delta 0), pack-reused 406
     Receiving objects: 100% (452/452), 471.98 KiB | 717.00 KiB/s, done.
     Resolving deltas: 100% (186/186), done.
     Checking connectivity... done.
     pi@raspberry:~ $ cd sandbox-cluster-guide/
     Colossus:sandbox-cluster-guide rpwagner$ ls
     README.md config    doc       examples  workshop
     pi@raspberry:~ $ cd config/
     pi@raspberry:~ $ ls
     README.md deploy.sh pinode-0  pinode-1  pinode-2  pinode-3
     pi@raspberry:~ $ ./deploy.sh 0
     ```
     * Call the deploy script from the config directory. It takes a parameter which is a number that represents which node this is. Use the following command in the terminal:  `./deploy.sh 0` This command may take a few minutes to finish.
     * After the script is complete, it is fine if you see `sudo: unable to resolve host raspberrypi` in the output. As long as the script completed, you can continue with the instructions.
     1. Verify that the hostname is set: Type `more /etc/hosts` into the terminal.  You should see an ip address similar to **127.0.1.1** on the left side and the name of the node on the right across from the IP address should be `pinode-0`. Check to make sure that it is set accordingly.
1. Reboot
```
pi@raspberry:~ $ sudo reboot
```

## The Other Node, `pinode-1`

**_This can be repeated for clusters with more than two Raspberry Pis._**

1. Boot the other Raspberry Pi with the keyboard and mouse plugged in
   to it, and the Ethernet cable plugged in to `pinode-0`. Give it a
   minute or two before continuing with the instructions.
1. Repeat the processes from above to, rebooting when prompted:
   * Expand the root file system.
   * Set the locale.
   * Set the time zone
   * Set the keyboard locale.
   * Connect to WiFi.
1. In a terminal clone the GitHub repo to home directory and navigate
   to the `sandbox-cluster-guide/config` directory.
   1. Deploy the configuration (`./deploy.sh 1`)
   1. Verify that the hostname is set:
      Type `cat /etc/hosts` into the terminal.  You should see an ip address similar to **127.0.1.1** on the left side and the name of the node on the right across from the IP address should be `pinode-0`. Check to make sure that it is set accordingly.
1. Reboot `pinode-1`.

## Verify the Setup

To verify that the nodes were set up correctly we're going to try to
connect from one to the other using [SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/).

1. Open a terminal on which Raspberry Pi has the mouse and keyboard
connected to it.
1. Use the `ssh` command to log on to other other Raspberry Pi. (Note:
On the first SSH connect, you might have to enter `yes` when prompted
to adding the key from this node into a list of machine you want to
access.) If you're on `pinode-0` you would use

    ```
    pi@pinode-0:~ $ ssh pinode-1
    The authenticity of host 'pinode-1 (10.0.0.11)' can't be established.
    ECDSA key fingerprint is 88:7a:61:1e:00:41:ea:0b:37:08:f6:e0:2b:ee:13:2f.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added 'pinode-1,10.0.0.11' (ECDSA) to the list of known hosts.
    
    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Thu Jul  7 19:03:25 2016
    pi@pinode-1:~ $
    ```

1. To completely lose track of where you are and feel like a
   combination of The Matrix and Inception you can then log back on to
   the previous Raspberry Pi from the current one.

    ```
    pi@pinode-1:~ $ ssh pinode-0
    The authenticity of host 'pinode-0 (10.0.0.10)' can't be established.
    ECDSA key fingerprint is 3a:26:c1:10:33:e0:c3:9e:bd:2c:a3:ec:a1:cf:c0:2d.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added 'pinode-0,10.0.0.10' (ECDSA) to the list of known hosts.
    
    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.
    
    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Thu Jul  7 21:05:50 2016
    pi@pinode-0:~ $
    ```

1. To get out of this mess type `exit` until the terminal window closes.

    ```
    pi@pinode-0:~ $ exit
    logout
    Connection to pinode-0 closed.
    pi@pinode-1:~ $ exit
    logout
    Connection to pinode-1 closed.
    pi@pinode-0:~ $ exit
    ```

## Next

![](coffee.png) Go have some coffee!

## Previous

[Networking, Security, Data](networking.md)

## Agenda

[Agenda](agenda.md)
