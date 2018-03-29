import csv
import os

def to_csv(l,filename):
	append_write = 'w'


	with open(filename, append_write) as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in l:
			for j in i[1]:
				for k,l in j[1]:				
					filewriter.writerow([j[0], i[0], k, l])

