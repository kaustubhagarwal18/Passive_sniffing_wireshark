sudo ifconfig wlp2s0 down
sudo iwconfig wlp2s0 mode monitor
sudo kismet




tshark -r Kismet-20190303-17-57-01-1.pcapdump -Y "wlan.fc.type_subtype==0x08"  -w outputINDUS_beacon.pcap


tshark -r outputINDUS_beacon.pcap -Y "wlan.fc.type_subtype==0x08" -T fields -e frame.time_epoch -e wlan.sa -e wlan_radio.signal_dbm -e wlan.ds.current_channel  >> outputINDUS_beacon.csv


tshark -r outputCENTER_beacon.pcap -Y "wlan.fc.type_subtype==0x08" -T fields -e frame.time_epoch -e wlan.sa -e wlan_radio.signal_dbm -e wlan_radio.phy -e wlan_radio.channel >> outputCENTER_beacon.csv


