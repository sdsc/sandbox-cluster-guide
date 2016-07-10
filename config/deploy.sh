#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Must supply node number."
    echo "Example: ./deploy.sh 1"
    exit -1
fi

nodenum=$1

echo "*************************************"
echo "************* Updating **************"
echo "*************************************"
echo
sudo apt-get update -y

echo
echo "*************************************"
echo "******** Installing Packages ********"
echo "*************************************"
echo

sudo apt-get install emacs openmpi-bin libopenmpi-dev python-mpi4py vim -y
if [ $nodenum -eq 0 ]
then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    sudo apt-get install nfs-kernel-server -y
    for i in 2 3 4 5
    do
        sudo mv /etc/rc$i.d/S01nfs-kernel-server /etc/rc$i.d/S02nfs-kernel-server
        sudo ln -s /etc/init.d/rpcbind /etc/rc$i.d/S01rpcbind
    done
fi

echo
echo "*************************************"
echo "****** Deploying Configuration ******"
echo "*************************************"
echo

sudo cp -rf pinode-$nodenum/* /etc/

sudo sed -i 's/BLANK_TIME=30/BLANK_TIME=0/g' /etc/kbd/config
sudo sed -i 's/POWERDOWN_TIME=30/POWERDOWN_TIME=0/g' /etc/kbd/config
sudo sed -i 's/#xserver-command=X/xserver-command=X -s 0 dpms/' /etc/lightdm/lightdm.conf


