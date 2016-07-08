Configuration
=============

Basic Process
-------------

 1. Boot master node (`pinode-0`) with WiFi dongle
 2. 'sudo raspi-config' expand file system; restart
 3. If needed, set timezone, keyboard, and language using graphical interface.
 4. Clone this repo to home directory
 5. Deploy configuration (`./deploy.sh <node number>`)
 6. Reboot
 7. Boot remaining nodes
 8. On each node, deploy (git clone git@github.com:sdsc/sandbox-cluster-guide.git) and reboot

Manual Steps
------------

 * Configure wlan0
 * On `pinode-0` generate RSA key pair for cluster (`ssh-keygen` with no passphrase)

