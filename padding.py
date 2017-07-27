#!/usr/bin/env python2
import struct
import math
import random
from frequency import *
from collections import Counter
import pandas as pd

def padding(artificial_payload, raw_payload):
	padding = ""
	# Get frequency of raw_payload and artificial profile payload
	artificial_frequency = frequency(artificial_payload)
	raw_payload_frequency = frequency(raw_payload)

	# To simplify padding, you only need to find the maximum frequency difference for each byte in raw_payload and artificial_payload, and pad that byte to the end of the raw_payload. Note: only consider the difference when artificial profile has higher frequency.
	#print('artificial payload',artificial_payload)
	#print('raw payload',raw_payload)

	def calcAbsFreq(string, rel_freq):
		return len(string) * rel_freq

	char_freq_diff = []
	for char in artificial_frequency:
		if char in raw_payload_frequency:
			normal_freq = calcAbsFreq(artificial_payload,artificial_frequency[char])
			attack_freq = calcAbsFreq(raw_payload,raw_payload_frequency[char])
			#normal_freq = artificial_frequency[char]
			#attack_freq = raw_payload_frequency[char]
			char_freq_diff.append([char,normal_freq-attack_freq])
		else:
			char_freq_diff.append([char, normal_freq])

	char_freq_diff = pd.DataFrame(char_freq_diff, columns=['char','freq'])
	char_freq_diff =  char_freq_diff.sort_values('freq',ascending=False)
	print('char freq difff',char_freq_diff)

	temp_char = char_freq_diff.values[0][0]
	print('temp char',temp_char)

	times = int(round(char_freq_diff.values[0][1]))
	print('times',times)
	if times > 0:
		raw_payload.extend([temp_char] * times)
	print('inside raw payload',raw_payload)




    # Depending on the difference, call raw_payload.append


    # Your code here ...

