#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def print_record(record, rank):
    print u'\t'.join([
        record[0],      # <content id>
        record[1],      # <content type>
        record[2],      # <content weight>
        record[3],      # <content name>
        record[4],      # <release year>
        record[5],      # <person id>
        record[6],      # <person name>
        record[7],      # <person weight>
        record[8],      # <age at release date>
        record[9],      # <job>
        record[10],     # <department>
        rank,           # <content rank>
        record[12],     # <person rank>
    ]).encode('utf8')
    
def print_buffer(buffer):
    rank = 0.0
    for record in buffer: rank += float(record[11])
    rank = u'{0:.32f}'.format(rank)
    for record in buffer:
        print_record(record, rank)
        
def reduce():
    buffer = []
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        # 0  <content id>
        # 1  <content type>
        # 2  <content weight>
        # 3  <content name>
        # 4  <release year>
        # 5  <person id>
        # 6  <person name>
        # 7  <person weight>
        # 8  <age at release date>
        # 9  <job>
        # 10 <department>
        # 11 <content rank>
        # 12 <person rank>
        record = line.strip().split(u'\t')
        if len(record) == 13: # otherwise something went wrong...
            if len(buffer) == 0 or record[0] == buffer[0][0]:
                buffer.append(record)
            else:
                print_buffer(buffer)
                buffer = [record]
                
    if len(buffer) > 0: print_buffer(buffer)
    
reduce()