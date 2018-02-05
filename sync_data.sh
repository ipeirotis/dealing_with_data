#!/bin/bash

sudo rm -rf /data
sudo mkdir -p /data
sudo git clone https://github.com/ipeirotis/data.git /data

rm /home/ubuntu/sync_data.sh 
ln -s /home/ubuntu/jupyter/NYU_Notes/sync_data.sh /home/ubuntu/sync_data.sh 
