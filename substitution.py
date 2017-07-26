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
    attack_encoded = []

    for char in attack_payload:
        replace_dict = subsitution_table[char]

        #TODO:Choose Probabilistically
        replace_char = list(replace_dict)[0]
        attack_encoded.append(replace_char)

    attack_encoded = ''.join(attack_encoded)

    print('attack payload', attack_payload)
    print('encloded attack',attack_encoded)

    b_attack_payload = bytearray(attack_payload)
    b_encoded_payload = bytearray(attack_encoded)

    xor_table = []
    #Generate XOR table

    l_attack_payload = list(attack_payload)
    l_encoded_payload = list(attack_encoded)
    for i in range(0,len(b_attack_payload)):
        xor_table.append(chr(b_attack_payload[i] ^ b_encoded_payload[i]))

    print('xor table',xor_table)

    # Based on your implementattion of substitution table, please prepare result and xor_table as output
    attack_encoded = list(attack_encoded)
    return (xor_table, attack_encoded)


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
    #print(grouped.sort_values(ascending=False))
    sorted_ratios = ratios.sort_values(ascending=False)
    #print(sorted_ratios)
    return sorted_ratios


def getSubstitutionTable(artificial_payload, attack_payload):
    # You will need to generate a substitution table which can be used to encrypt the attack body by replacing the most frequent byte in attack body by the most frequent byte in artificial profile one by one

    # Note that the frequency for each byte is provided below in dictionay format. Please check frequency.py for more details
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)

    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)
    print('normal frquency',sorted_artificial_frequency)

    substitution_table = []
    sub_output = {}
    for i in range(0,len(sorted_attack_frequency)):
        line = [sorted_attack_frequency[i][0],sorted_artificial_frequency[i][0],sorted_artificial_frequency[i][1]]
        substitution_table.append(line)
        sub_output[sorted_attack_frequency[i][0]]={sorted_artificial_frequency[i][0]:sorted_artificial_frequency[i][1]}


    for i in range(len(sorted_attack_frequency),len(sorted_artificial_frequency)):
        x_char = sorted_artificial_frequency[i][0]

        sorted_ratios = getNormalMapping(substitution_table,sorted_attack_frequency)
        #print('sorted ratios',type(sorted_ratios))
        y_char = sorted_ratios.index[0]
        x_char_freq = sorted_ratios.iloc[0]
        #print('x char frq', x_char_freq)
        line = [y_char, x_char, x_char_freq]
        substitution_table.append(line)

        sub_output[y_char][x_char] = x_char_freq

    # You may implement substitution table in your way. Just make sure it can be used in substitute(attack_payload, subsitution_table)
    return sub_output


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
