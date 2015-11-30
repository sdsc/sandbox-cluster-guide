#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Must supply node number."
    echo "Example: ./deploy.sh 1"
    exit -1
fi

nodenum=$1

sudo apt-get install emacs openmpi-bin libopenmpi-dev python-mpi4py -y
if [ $nodenum -eq 0 ]
then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    sudo apt-get install nfs-kernel-server rpcbind isc-dhcp-server -y
    for i in 2 3 4 5
    do
        sudo mv rc$i.d/S01nfs-kernel-server rc$i.d/S02nfs-kernel-server
        sudo ln -s init.d/rpcbind rc$i.d/S01rpcbind
    done
fi

sudo cp -rf pinode-$nodenum/* /etc/
sudo cp -rf common/* /etc/


