#!/usr/bin/env python2
import struct
import math
import dpkt
import socket
from collections import Counter
from frequency import *
import pandas as pd

def substitute(attack_payload, subsitution_table):
    # Using the substitution table you generated to encrypt attack payload
    # Note that you also need to generate a xor_table which will be used to decrypt the attack_payload
    # i.e. (encrypted attack payload) XOR (xor_table) = (original attack payload)
    b_attack_payload = bytearray(attack_payload)
    result = []
    xor_table = []
    # Based on your implementattion of substitution table, please prepare result and xor_table as output

    return (xor_table, result)

def findFrequency(character,lst):
    output = 'NOTHING'
    for item in lst:
        if character ==  item[0]:
            output = item[1]
    return output

def getNormalMapping(substitution_table,sorted_attack_frequency):
        substitution_table = pd.DataFrame(substitution_table,columns=['Attack Char','Normal Char','Normal Frequency'])
        #print(substitution_table)
        grouped =  substitution_table.groupby(['Attack Char'])['Normal Frequency'].sum()
        ratios = pd.Series(index=grouped.index.values)
        for char in grouped.index.values:
            ratios.loc[char] = findFrequency(char,sorted_attack_frequency)/grouped.loc[char]
        print(grouped.sort_values(ascending=False))
        sorted_ratios = ratios.sort_values(ascending=False)
        print(sorted_ratios)
        return sorted_ratios


def getSubstitutionTable(artificial_payload, attack_payload):
    # You will need to generate a substitution table which can be used to encrypt the attack body by replacing the most frequent byte in attack body by the most frequent byte in artificial profile one by one

    # Note that the frequency for each byte is provided below in dictionay format. Please check frequency.py for more details
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)

    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)

    # Your code here ...
    substitution_table = []
    for i in range(0,len(sorted_attack_frequency)):
        line = [sorted_attack_frequency[i][0],sorted_artificial_frequency[i][0],sorted_artificial_frequency[i][1]]
        #print(line)
        substitution_table.append(line)

    #substitution_table.append(['a','o',1])

    x_char = sorted_artificial_frequency[len(sorted_attack_frequency)][0]
    print(n_char)

    sorted_ratios = getNormalMapping(substitution_table,sorted_attack_frequency)
    y_char ='d'
    x_char_freq =0.2
    line = [y_char, x_char, x_char_freq]

    # You may implement substitution table in your way. Just make sure it can be used in substitute(attack_payload, subsitution_table)

    #return substitution_table


def getAttackBodyPayload(path):
    f = open(path)
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        if socket.inet_ntoa(ip.dst) == "192.150.11.111": # verify the dst IP from your attack payload
            tcp = ip.data
            if tcp.data == "":
                continue
            return tcp.data.rstrip()

def getArtificialPayload(path):
    f = open(path)
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        if tcp.sport == 80 and len(tcp.data) > 0:
            return tcp.data
