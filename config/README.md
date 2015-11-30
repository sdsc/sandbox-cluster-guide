Configuration
=============

Basic Process
-------------

 1. Boot master node (`pinode-0`) with WiFi dongle
 2. Clone this repo to home directory
 3. Deploy configuration (`./deploy.sh <node number>`)
 4. Reboot
 5. Boot remaining nodes
 6. On each node, deploy and reboot
 7. Shutdown DHCP server on `pinode-0` (`service isc-dhcp-server stop; update-rc.d isc-dhcp-server disable`)

Manual Steps
------------

 * Configure wlan0
 * `raspi-config` expand file system
 * On pinode-0 generate RSA key pair for cluster (`ssh-keygen` with no passphrase)
 * Shutdown DHCP server after other nodes are up
