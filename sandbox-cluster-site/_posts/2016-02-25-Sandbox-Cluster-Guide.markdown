---
layout: post
title:  "Sandbox Cluster Guide"
date:   2016-02-25 09:30:00 
categories:   cluster lessons
---
## Materials
	4 Raspberry Pi
	4 Micro-USB cable (the cable you would use to charge an Android phone)
	4 microSD cards with adapters
	1 HDMI cable
	4 Ethernet cable
	USB keyboard 
	USB Mouse
	1 4-port ethernet switch
	1 4-port usb hub


----

## Basic Process

### Installing Operating System Image:

If you bought the microSD cards with the NOOB image installed on it, then you can skip these instructions. These instructions are for if you do not have an operating system installed on your microSD card or if you encounter a problem during any of the following steps and need to restart. A good resource that may help you with majority of the steps can be found at: [https://www.raspberrypi.org/documentation/installation/installing-images/README.md]

For the following instructions, it is created for the image Raspbian Jessie.

Optional helpful software for Mac users: [http://ivanx.com/raspberrypi/]

Once the tool has been downloaded, unzip the folder and the tool will be ready to run. When installing the image onto the SD card, you can utilize this tool which will give you an estimate of the remaining time till the card is completed. It provides step by step aid on what to do throughout the process.

----

## The Process:

pinode-0 (Master node):
Boot master node (pinode-0) with WiFi dongle, an HDMI cable,  an ethernet cable, keyboard and mouse plugged in.
Change the password of the master node.
Type passwd into the terminal.
By default, the current password = raspberry 
Enter the new password twice (write that down just in case)


[https://www.raspberrypi.org/documentation/installation/installing-images/README.md]:https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[http://ivanx.com/raspberrypi/]:http://ivanx.com/raspberrypi/

