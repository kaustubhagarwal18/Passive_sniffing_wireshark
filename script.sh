#!/bin/bash
#Check for available interfaces
tshark -D  
 # Check which channel is selected
iwlist wlp2s0 channel   
# kill other processes that might interfere with the card
sudo airmon-ng check kill 
# start monitor mode!
sudo airmon-ng start wlp2s0   
mkdir drive
cd drive
ls
# Monitor 2.4 and 5 GHz channels with
#time interval 0.2 sec and write the data to file
sudo airodump-ng -M -f 200 --band abg  --write asdf wlp2s0mon   
# start networking again
sudo airmon-ng stop wlp2s0mon
sudo service networking start
sudo service network-manager start
