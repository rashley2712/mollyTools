#!/usr/bin/env python3
import sys, os
import argparse, glob
import subprocess

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Looks for headers in Starlink SDF files.')
	parser.add_argument('files', nargs='+', type=str, help='Files to search through.')
	parser.add_argument('-k', '--key', type=str, default='all', help='The header to look for.')
	parser.add_argument('--keep', action="store_true", default=False, help='Keep the temporary files of keys.')
	arg = parser.parse_args()
	# print(arg)
	
	tempFiles = []
	for f in arg.files:
		# Dump the fitskeys tp a simple text file
		tempFilename = "zzz_keys_" + f +".tmp"
		tempFiles.append(tempFilename)
		keysfile = open(tempFilename, "wt")
		subprocess.call(["/storage/astro1/phsaap/software/star-2018A/bin/figaro/fitskeys", f], stdout=keysfile)
		keysfile.close()

		key = arg.key
		keyfile = open(tempFilename, 'rt')
		allKeys = []
		for line in keyfile:
			line = line.strip()
			header = line[0:8].strip()
			value = line[9:28].strip()
			comment = line[29:].strip()
			keyDict = {'header': header, 'value': value, 'comment':comment}
			allKeys.append(keyDict)
		#print(allKeys)

		if key=='all':
			for k in allKeys: print(f, k['header'], k['value'])
		else:
			for k in allKeys:
				if key in k['header']: print(f, key, k['value'])
		keyfile.close()
	
	# Clean up things before leaving
	if not arg.keep:
		for t in tempFiles:
			os.remove(t)

	sys.exit()		

