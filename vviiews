#!/usr/bin/env python

#Usage: python2.7 view_pcaps.py

import dpkt, socket
from sys import argv
from ipaddr import IPv4Address, IPv6Address
import win_inet_pton
#import syslog
import time
import os

IP_SUFFIX = "10.0"

def read_pcap(pcap_file):

    print ('Reading:' + str(pcap_file) + '\n')
    f = open(str(pcap_file), "rb")
    pcap = dpkt.pcap.Reader(f)

    group = ''
    if "CnC" in str(pcap_file):
        group = "cnc"
    elif "scan" in str(pcap_file):
        group = "scan"
    elif "ddos" in str(pcap_file):
        group = "ddos"
        
    total_ips[group] = {}
            
    for ts, pkt in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(pkt) 
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue

            #Parsing IP data
            ip=eth.data
            if type(ip) == dpkt.ip.IP:
                ipaddr = IPv4Address(socket.inet_ntop(socket.AF_INET, ip.dst)) 
            else:
                IPv6Address(socket.inet_ntop(socket.AF_INET6, ip.dst))

            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)

                #Sees whether a line is the source or destination
            if IP_SUFFIX in str(src):
                total_ips[group][str(src)] = 1
            if IP_SUFFIX in str(dst): 
                total_ips[group][str(dst)] = 1
            
            #Parsing TCP data
            if ip.p==dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data

                    #source port, destination port
                tcp_sport = tcp.sport
                tcp_dport = tcp.dport

                if IP_SUFFIX in str(src): 
                    total_ips[group][str(src)] = 1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] = 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] = 1
                
                if IP_SUFFIX in str(dst): 
                    total_ips[group][str(dst)] = 1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] = 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] = 1

                #print str(src)
                #print str(dst)
                                          
                #Parsing HTTP data Responses:
                if (tcp.sport == 80) and len(tcp.data) > 0: 

                    http = dpkt.http.Response(tcp.data)
                    #print(http.body)
                    #print(http.status)
                    
                #Parsing HTTP data Requests:
                elif tcp.dport == 80 and len(tcp.data) > 0:

                    http = dpkt.http.Request(tcp.data)
                    #print(http.headers)
                    #print(http.uri)
                                        
            if ip.p==dpkt.ip.IP_PROTO_UDP:

                udp = ip.data
                udp_sport = udp.sport
                udp_dport = udp.dport

                if IP_SUFFIX in str(src): 
                    total_ips[group][str(src)] = 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] = 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] = 1
                
                if IP_SUFFIX in str(dst): 
                    total_ips[group][str(dst)] = 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] = 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] = 1

                

        except dpkt.UnpackError as e:
            pass
            #fout.write('\n *Unpack ERROR HERE: %s * \n' % (e))
            
        except Exception as e:
            pass
            #fout.write('\n *ERROR HERE: %s * \n' % (e))


    f.close()


    
if __name__ == "__main__":

    total_ips = {}
    total_connections = {}

    file_name = "C:\Snort\\bin\evaluation.pcap"

    read_pcap(str(file_name))

    f = open('view_pcaps_connections.txt', 'w')    
    for con in total_connections:
        print(con)
        f.write(con)
    f.close()

    print "Total unique (counting both directions):" + str(len(total_connections.keys())) + '\n'
    
