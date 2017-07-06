#!/usr/bin/env python
#Usage: python2.7 view_pcaps.py
import dpkt, socket
from sys import argv
from ipaddr import IPv4Address, IPv6Address
import win_inet_pton
#import syslog
import time
import os
import pandas as pd

IP_SUFFIX = "192.168"



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
            #Checks to see if  packet is IP (TCP/UDP)
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue

                #Doesn't really do anything currently
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
                total_ips[group][str(src)] = total_ips[group].get(str(src),0) + 1
            if IP_SUFFIX in str(dst): 
                total_ips[group][str(dst)] = total_ips[group].get(str(dst),0) + 1
            
            #Parsing TCP data
            if ip.p==dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data

                    #source port, destination port
                tcp_sport = tcp.sport
                tcp_dport = tcp.dport

                if IP_SUFFIX in str(src): 
                    total_ips[group][str(src)] = total_ips[group].get(str(src),0) + 1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] = total_connections.get(con,0) + 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] = total_connections.get(con,0) + 1
                
                if IP_SUFFIX in str(dst): 
                    total_ips[group][str(dst)] = total_ips[group].get(str(dst),0) + 1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] = total_connections.get(con,0) + 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] = total_connections.get(con,0) + 1

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
                    total_ips[group][str(src)] =total_ips[group].get(str(src),0) + 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] = total_connections.get(con,0) + 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] =total_connections.get(con,0) + 1
                
                if IP_SUFFIX in str(dst): 
                    total_ips[group][str(dst)] = total_ips[group].get(str(dst),0) + 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] =total_connections.get(con,0) + 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] =total_connections.get(con,0) + 1

                

        except dpkt.UnpackError as e:
            pass
            #fout.write('\n *Unpack ERROR HERE: %s * \n' % (e))
            
        except Exception as e:
            pass
            #fout.write('\n *ERROR HERE: %s * \n' % (e))

    
    f.close()


'''
#SCANNING - for an external host, how many connections to an internal host does it make?
'''

def read_pcap_scanning(pcap_file, IP_SUFFIX="192.168"):

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
            #Checks to see if  packet is IP (TCP/UDP)
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue

                #Doesn't really do anything currently
            #Parsing IP data
            ip=eth.data
            if type(ip) == dpkt.ip.IP:
                ipaddr = IPv4Address(socket.inet_ntop(socket.AF_INET, ip.dst))
            else:
                IPv6Address(socket.inet_ntop(socket.AF_INET6, ip.dst))

            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)

                #Counts total IPs detected for either the source or destination, updates total_ips[]
            if IP_SUFFIX not in str(src):
                total_ips[group][str(src)] = total_ips[group].get(str(src),0) + 1
            if IP_SUFFIX not in str(dst):
                total_ips[group][str(dst)] = total_ips[group].get(str(dst),0) + 1

            #Parsing TCP data FOR TCP PORTS
            if ip.p==dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data

                #source port, destination port
                tcp_sport = tcp.sport
                tcp_dport = tcp.dport

                if (IP_SUFFIX not in str(src)) and (IP_SUFFIX in str(dst)):
                    total_ips[group][str(src)] = total_ips[group].get(str(src),0) + 1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] = total_connections.get(con,0) + 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] = total_connections.get(con,0) + 1

                '''
                if IP_SUFFIX in str(dst):
                    total_ips[group][str(dst)] =+1
                    con = str(src) + ":" + str(tcp_sport) + ":" + str(dst) + ":" + str(tcp_dport)
                    total_connections[con] =+ 1
                    con = str(dst) + ":" + str(tcp_dport) + ":" + str(src) + ":" + str(tcp_sport)
                    total_connections[con] =+ 1
                '''

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

            #Parsing UDP data FOR UDP PORTS
            if ip.p==dpkt.ip.IP_PROTO_UDP:

                udp = ip.data
                udp_sport = udp.sport
                udp_dport = udp.dport

                if IP_SUFFIX not in str(src) and IP_SUFFIX in str(dst):
                    total_ips[group][str(src)] = total_ips[group].get(str(src),0) + 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] = total_connections.get(con,1) + 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] = total_connections.get(con,1) + 1

                '''
                if IP_SUFFIX in str(dst):
                    total_ips[group][str(dst)] =+ 1
                    con = str(src) + ":" + str(udp_sport) + ":" + str(dst) + ":" + str(udp_dport)
                    total_connections[con] =+ 1
                    con = str(dst) + ":" + str(udp_dport) + ":" + str(src) + ":" + str(udp_sport)
                    total_connections[con] =+ 1
                '''


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
    file_name = "C:\Users\\fzhi\Downloads\Project4\SAMPLE_bacground_legit.pcap"

    #read_pcap(str(file_name))
    read_pcap_scanning(str(file_name),IP_SUFFIX)

    print(total_connections,"total connections")
    print(total_ips, "total ips")

    output = pd.DataFrame(total_connections.items(),index=total_connections.keys())
    writer = pd.ExcelWriter('OUTPUT.xlsx', engine='xlsxwriter')
    output.to_excel(writer, sheet_name='output')
    writer.save()



    '''
    f = open('view_pcaps_connections.txt', 'w')
    for con in total_connections:
        #print(con)
        f.write(con)
    f.close()
    '''


    print "Total unique (counting both directions):" + str(len(total_connections.keys())) + '\n'

