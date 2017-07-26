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

	sorted_artificial_freq = sorted(artificial_frequency)
	sorted_raw_payload_freq = sorted(raw_payload_frequency)

	# To simplify padding, you only need to find the maximum frequency difference for each byte in raw_payload and artificial_payload, and pad that byte to the end of the raw_payload. Note: only consider the difference when artificial profile has higher frequency.
	print('artificial frequency',artificial_frequency)
	print('raw frequency',raw_payload_frequency)

	def calcAbsFreq(string, rel_freq):
		return len(string) * rel_freq
	'''
	shared_char = []
	for char in artificial_frequency:
		if char in raw_payload_frequency:
			normal_freq = calcAbsFreq(artificial_payload,artificial_frequency[char])
			attack_freq = calcAbsFreq(raw_payload,raw_payload_frequency[char])
			print('normal freq abs',normal_freq)
			print('attack freq abs',attack_freq)
			if normal_freq-attack_freq > 0:
				shared_char.append([char,normal_freq-attack_freq])

	shared_char = pd.DataFrame(shared_char, columns=['char','freq'])
	shared_char =  shared_char.sort_values('freq',ascending=False)
	print(shared_char)

    # Depending on the difference, call raw_payload.append


    # Your code here ... 
	'''
