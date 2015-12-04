Configuration
=============

Basic Process
-------------

 1. Boot master node (`pinode-0`) with WiFi dongle
 2. 'sudo raspi-config' expand file system; restart
 3. Clone this repo to home directory
 4. Deploy configuration (`./deploy.sh <node number>`)
 5. Reboot
 6. Boot remaining nodes
 7. On each node, deploy (git clone git@github.com:sdsc/sandbox-cluster-guide.git) and reboot
 8. Shutdown DHCP server on `pinode-0` (`service isc-dhcp-server stop; update-rc.d isc-dhcp-server disable`)

Manual Steps
------------

 * Configure wlan0
 * On pinode-0 generate RSA key pair for cluster (`ssh-keygen` with no passphrase)
 * Shutdown DHCP server after other nodes are up
