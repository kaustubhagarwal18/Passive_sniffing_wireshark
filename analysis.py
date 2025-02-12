#Script reused from https://github.com/yarongoldshtein/Wifi_Parser
#Added modifications for handling beacon frames

import logging

from scapy.layers.dot11 import Dot11, Dot11Elt
from scapy.all import Dot11Beacon
from scapy.all import *
from collections import Counter
import numpy as np

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from operator import itemgetter
import os
from os.path import basename
from manuf import manuf



MY_COLORS = np.array(['c', 'y', 'm', 'gray', 'b', 'r', 'g', 'k','gold'])
BW_STANDARD_WIFI = 15E7


class parser:
    def __init__(self, path):
        self.pcap_file = rdpcap(path)
        self.path = path


    def graph_by_receiver(self):

        mac_addresses = {}  # new dictionary
        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11):
                mac_addresses.update({pkt[Dot11].addr1: 0})
        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11):
                mac_addresses[pkt[Dot11].addr1] += 1

        MA = []
        for ma in mac_addresses:
            MA.append(mac_addresses[ma])

        plt.clf()
        plt.suptitle('Number of packets of every receiver', fontsize=14, fontweight='bold')
        plt.bar(range(len(mac_addresses)), sorted(MA), align='center', color=MY_COLORS)

        plt.xticks(range(len(mac_addresses)), sorted(mac_addresses.keys()))

        plt.rcParams.update({'font.size': 10})

        plt.xlabel('Receivers mac addresses')
        plt.ylabel('Number of packets')

        # Set tick colors:
        ax = plt.gca()
        ax.tick_params(axis='x', colors='k')
        ax.tick_params(axis='y', colors='r')
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.show()

    def graph_by_sender(self):

        mac_adresses = {}  # new dictionary
        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11):
                mac_adresses.update({pkt[Dot11].addr2: 0})
        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11):
                mac_adresses[pkt[Dot11].addr2] += 1

        MA = []
        for ma in mac_adresses:
            MA.append(mac_adresses[ma])

        plt.clf()
        plt.suptitle('Number of packets of every sender', fontsize=14, fontweight='bold')
        plt.bar(range(len(mac_adresses)), sorted(MA), align='center', color=MY_COLORS)

        plt.xticks(range(len(mac_adresses)), sorted(mac_adresses.keys()))

        plt.rcParams.update({'font.size': 10})

        plt.xlabel('Senders mac addresses')
        plt.ylabel('Number of packets')

        # Set tick colors:
        ax = plt.gca()
        ax.tick_params(axis='x', colors='k')
        ax.tick_params(axis='y', colors='r')
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.show()

    def display_by_AP(self):

        networks = {}

        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11Elt):

                temp = str((pkt[Dot11Elt].info).decode("utf-8", "ignore"))
                if temp is "":
                    temp = pkt[Dot11].addr1

                networks.update({temp: 0})

        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11Elt):

                temp = str((pkt[Dot11Elt].info).decode("utf-8", "ignore"))

                if temp is "":
                    temp = pkt[Dot11].addr1

            networks[temp] += 1

        networks_list = sorted(networks.items(), key=itemgetter(1))
        print networks_list
        print range(len(networks_list))
        print  [int(i[1]) for i in networks_list]
        print [i[0] for i in networks_list]



        plt.clf()
        plt.suptitle('Number of packets in every Access point', fontsize=14, fontweight='bold')
        plt.bar(range(len(networks_list)), [int(i[1]) for i in networks_list], align='center', color=MY_COLORS)

        plt.xticks(range(len(networks_list)), [i[0] for i in networks_list])

        plt.rcParams.update({'font.size': 10})

        plt.xlabel('Access point name')
        plt.ylabel('Number of packets')

        # Set tick colors:
        ax = plt.gca()
        ax.tick_params(axis='x', colors='r')
        ax.tick_params(axis='y', colors='k')
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=60)

        plt.show()


    def display_channel(self):


        mac_adresses = {}  # new dictionary

        count = 0
        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11Beacon):
                try:
                    temp = int(ord(pkt[Dot11Elt:3].info))
                except:
                    count = 0

                mac_adresses.update({pkt[Dot11].addr2: temp})

        print  [i[0] for i in mac_adresses]
        print  [i[1] for i in mac_adresses]

        freq = {}
        for key in mac_adresses.keys():
            if (mac_adresses[key] in freq):
                freq[mac_adresses[key]] += 1
            else:
                freq[mac_adresses[key]] = 1

        freqq= sorted(freq.items(), key=lambda kv: kv[0])

        print [int(i[1]) for i in freqq]
        print [i[0] for i in freqq]

        plt.clf()
        plt.suptitle('Channel distribution', fontsize=14, fontweight='bold')
        plt.bar(range(len(freqq)), [int(i[1]) for i in freqq], color=MY_COLORS)

        plt.xticks(range(len(freqq)), [i[0] for i in freqq])
        plt.rcParams.update({'font.size': 10})

        plt.xlabel('Access point name')
        plt.ylabel('Number of AP')



        plt.rcParams.update({'font.size': 10})
        plt.hist(mac_adresses.keys(), normed=True, bins=30)
        plt.xlabel('Access point name')
        plt.ylabel('Number of AP')

        # Set tick colors:
        ax = plt.gca()
        ax.tick_params(axis='x', colors='r')
        ax.tick_params(axis='y', colors='k')
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=60)
        plt.show()


    def display_frames(self):

        frame_map = {}
        for pkt in self.pcap_file:
            frame_map.update({pkt.payload.payload.name: 0})

        for pkt in self.pcap_file:
            frame_map[pkt.payload.payload.name] += 1

        frame_list = frame_map.items()
        pies = [pie for (pie, percent) in list(frame_list)]
        percents = [percent for (pie, percent) in list(frame_list)]
        # Make a pie graph.
        colors = ['lightgreen', 'pink', 'r', 'orange', 'c', 'brown','y','m']
        plt.clf()
        plt.figure(num=1, figsize=(12, 8))
        plt.axes(aspect=1)
        plt.suptitle('Frames PIE', fontsize=14, fontweight='bold')
        plt.title("Number of types: " + str(len(frame_list)))
        plt.rcParams.update({'font.size': 10})
        plt.pie(percents, labels=pies, autopct='%.1f%%', startangle=90, colors=colors, pctdistance=0.7,labeldistance=1.2)

        plt.show()

    def display_graph(self):

        G = nx.Graph()

        count = 0
        edges = set()
        edges_list = []

        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11Elt):
                src = pkt[Dot11].addr1
                dst = pkt[Dot11].addr2

                edges_list.append((src, dst))
                edges.add(src)
                edges.add(dst)


        plt.clf()
        filepath = os.path.splitext(self.path)[0]
        filename = basename(filepath)
        plt.suptitle('Connection Map of: '+ str(filename), fontsize=14, fontweight='bold')
        plt.title("\n Number of Users: " + str(int(len(edges))))
        plt.rcParams.update({'font.size': 10})
        G.add_edges_from(edges_list)
        nx.draw(G, with_labels=True, node_color=MY_COLORS)
        plt.show()

    def display_channel_efficiency(self):

        size = 0

        start_time = self.pcap_file[0].time
        end_time = self.pcap_file[len(self.pcap_file) - 1].time

        duration = (end_time - start_time)/1000

        for i in range(len(self.pcap_file) - 1):
            size += len(self.pcap_file[i])
        ans = (((size * 8) / duration) / BW_STANDARD_WIFI) * 100
        ans = float("%.2f" % ans)
        labels = ['utilized', 'unutilized']
        sizes = [ans, 100.0 - ans]
        colors = ['g', 'r']

        # Make a pie graph
        plt.clf()
        plt.figure(num=1, figsize=(8, 6))
        plt.axes(aspect=1)
        plt.suptitle('Channel efficiency', fontsize=14, fontweight='bold')
        plt.title("Bits/s: " + str(float("%.2f" % ((size*8)/duration))),fontsize = 12)
        plt.rcParams.update({'font.size': 17})
        plt.pie(sizes, labels=labels, autopct='%.2f%%', startangle=60, colors=colors, pctdistance=0.7, labeldistance=1.2)

        plt.show()

    def display_bits_per_second(self):

        max_time = int(self.pcap_file[len(self.pcap_file) - 1].time) - int(self.pcap_file[0].time)
        bits_list = [0] * (max_time + 1)

        first_time = self.pcap_file[0].time

        for i in range(len(self.pcap_file)):
            interval_time = int(self.pcap_file[i].time - first_time)
            length = len(self.pcap_file[i]) * 8
            bits_list[interval_time] += length

        time_unit = list(range(max_time + 1))

        plt.clf()
        plt.suptitle('bits per second', fontsize=14, fontweight='bold')
        plt.xlabel('Time (in seconds)')
        plt.ylabel('bits')

        plt.plot(time_unit, bits_list, marker='.', color='blue')
        plt.show()

    def display_PER(self):

        number_of_pkts = len(self.pcap_file)
        retransmission_pkts = 0

        for pkt in self.pcap_file:

            if (pkt[Dot11].FCfield & 0x8) != 0:
                retransmission_pkts += 1

        ans = (retransmission_pkts / number_of_pkts)*100
        ans = float("%.2f" % ans)
        labels = ['Standard packets', 'Retransmitted packets']
        sizes = [100.0 - ans,ans]


        colors = ['g', 'firebrick']

        # Make a pie graph
        plt.clf()
        plt.figure(num=1, figsize=(8, 6))
        plt.axes(aspect=1)
        plt.suptitle('Retransmitted packet', fontsize=14, fontweight='bold')
        plt.rcParams.update({'font.size': 13})
        plt.pie(sizes, labels=labels, autopct='%.2f%%', startangle=60, colors=colors, pctdistance=0.7, labeldistance=1.2)

        plt.show()


    def destroy_fig(self):
        if plt:
            plt.close()

    def save_information_as_text(self):

        start_time = self.pcap_file[0].time

        f = open('Communication Data', 'w')

        for pkt in self.pcap_file:
            f.write("Time: " + str(pkt.time - start_time) + " -> Source: " + str(pkt[Dot11].addr1) + " -> destenation: " + str(pkt[Dot11].addr2) + "\nThe Hex in this packet:\n" + str(pkt[Dot11]) + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        f.close()

    def display_graph_by_specific_mac(self, mac_address):

        G = nx.Graph()

        count = 0
        edges = set()
        edges_list = []


        for pkt in self.pcap_file:

            src = pkt[Dot11].addr1
            dst = pkt[Dot11].addr2

            if mac_address in [src, dst]:
                edges_list.append((src, dst))
                edges.add(src)
                edges.add(dst)

        plt.clf()
        plt.suptitle('Communicating with ' + str(mac_address), fontsize=14, fontweight='bold')
        plt.title("\n Number of Communicating Users: " + str(int(len(edges))))
        plt.rcParams.update({'font.size': 10})
        G.add_edges_from(edges_list)
        nx.draw(G, with_labels=True, node_color=MY_COLORS)
        plt.show()

    def display_by_time_interval(self, mac_address, start_time, end_time):

        mac_adresses = {}  # new dictionary

        begin_time = self.pcap_file[0].time

        for pkt in self.pcap_file:

            time = pkt.time - begin_time
            if (pkt[Dot11].addr1 == mac_address) and (start_time <= time and time <= end_time):
                mac_adresses.update({pkt[Dot11].addr2: 0})

        for pkt in self.pcap_file:

            time = pkt.time - begin_time
            if (pkt[Dot11].addr1 == mac_address) and (start_time <= time and time <= end_time):
                mac_adresses[pkt[Dot11].addr2] += 1

        MA = []
        for ma in mac_adresses:
            MA.append(mac_adresses[ma])

        plt.clf()
        plt.suptitle('Number of packets by interval tine and MAC address'+ str(mac_address), fontsize=14, fontweight='bold')
        plt.bar(range(len(mac_adresses)), sorted(MA), align='center', color=MY_COLORS)

        plt.xticks(range(len(mac_adresses)), sorted(mac_adresses.keys()))

        plt.rcParams.update({'font.size': 10})

        plt.xlabel('Sender mac address')
        plt.ylabel('Number of packets')

        # Set tick colors:
        ax = plt.gca()
        ax.tick_params(axis='x', colors='blue')
        ax.tick_params(axis='y', colors='red')
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.show()

    def display_graph_by_AP(self):

        G = nx.Graph()
        edges_set = set()

        for pkt in self.pcap_file:
            src = pkt[Dot11].addr1
            dst = pkt[Dot11].addr2
            ssid = str(pkt[Dot11].addr3)

            edges_set.add((ssid, dst))
            edges_set.add((dst, ssid))
            edges_set.add((src, ssid))
            edges_set.add((ssid, src))

        edges_list = list(edges_set)

        plt.clf()
        plt.suptitle('Communicating with Access Points', fontsize=14, fontweight='bold')
        plt.rcParams.update({'font.size': 10})
        G.add_edges_from(edges_list)
        nx.draw(G, with_labels=True, node_color=MY_COLORS)
        plt.show()

    def display_graph_IP(self):

        G = nx.Graph()

        count = 0
        edges = set()
        edges_list = []

        for pkt in self.pcap_file:
            if hasattr(pkt.payload, 'src') and hasattr(pkt.payload, 'dst'):
                count += 1
                edges_list.append((pkt.payload.src, pkt.payload.dst))
                edges.add(pkt.payload.src)
                edges.add(pkt.payload.dst)

        plt.clf()
        filepath = os.path.splitext(self.path)[0]
        filename = basename(filepath)
        plt.suptitle('Connection Map of: ' + str(filename), fontsize=14, fontweight='bold')
        plt.title("\n Number of Users: " + str(int(len(edges))) + "\n Number of packets: " + str(count))
        plt.rcParams.update({'font.size': 10})
        G.add_edges_from(edges_list)
        nx.draw(G, with_labels=True, node_color=MY_COLORS)
        plt.show()


    def get_Manufacturer(self):

        p = manuf.MacParser(update=True)

        for pkt in self.pcap_file:
            #if pkt.haslayer(Dot11Beacon):
            if pkt.haslayer(Dot11Elt):
                print p.get_manuf(pkt[Dot11].addr2)

        for pkt in self.pcap_file:
            if pkt.haslayer(Dot11Elt):
                try:
                    print str((pkt[Dot11Elt].info).decode("utf-8", "ignore"))
                except:
                    print "err"



# End of class ex3


def open_file(file_name='/home/teresa/outputINDUS_beacon.pcap'):
    return parser(file_name)


def main():
    ex3_object = open_file()
    #ex3_object.display_channel()
    #ex3_object.display_graph()
    #ex3_object.display_by_time_interval()

    #ex3_object.display_channel_efficiency()
    #ex3_object.graph_by_receiver()
    #ex3_object.graph_by_sender()
    ex3_object.get_Manufacturer()
    ex3_object.display_by_AP()
    #ex3_object.display_frames()
    #ex3_object.display_graph()
    #ex3_object.display_bits_per_second()
    #ex3_object.display_PER()
    #ex3_object.display_graph_IP()


if __name__ == '__main__':
    main()
