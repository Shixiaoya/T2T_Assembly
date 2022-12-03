#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   getgaps.py
@Time    :   2022/05/01
@Author  :   Zhou Lab
@Version :   1.0
@Github  :   https://github.com/zhouyflab
@License :   (C)Copyright 2021-2022, CAAS ShenZhen
@Desc    :   To get the gaps information of the genome
'''

import datetime, sys
# here put the import lib
print('***********************************************************')
print('Start Time:    '+ str(datetime.datetime.now()))
print('***********************************************************')

# Import necessary packages
import argparse
import re
from Bio import SeqIO

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("fasta")
args = parser.parse_args()

# Open FASTA, search for masked regions, print in GFF3 format
with open(args.fasta) as handle:
    i = 0
    for record in SeqIO.parse(handle, "fasta"):
        for match in re.finditer('N+', str(record.seq)):
            i = i+1
            print (record.id, ".", "gap", match.start() + 1, match.end(), ".", ".", ".", "Name=gap" + str(i) + ";size=" + str(match.end()-match.start()), sep='\t')

#use the following at CMD: FILENAME.py FILENAME.fasta >> FILENAME.gff3  here
