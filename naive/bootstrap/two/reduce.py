#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def print_record(record, weight):
    print u'\t'.join([
        record[5],      # <content id>
        record[1],      # <content type>
        weight,         # <content weight>
        record[3],      # <content name>
        record[4],      # <release year>
        record[0],      # <person id>
        record[6],      # <person name>
        record[7],      # <person weight>
        record[8],      # <age at release date>
        record[9],      # <job>
        record[10],     # <department>
        record[11],     # <content rank>
        record[12],     # <person rank>
    ]).encode('utf8')
    
def print_buffer(buffer):
    # The buffer contains all the content for a person and we calculate the weight for each content in a person
    weight = u'{0:.32f}'.format(1.0 / float(len(buffer)))
    for record in buffer:
        print_record(record, weight)
        
def reduce():
    buffer = []
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        # 0  <person id>
        # 1  <content type>
        # 2  <content weight>
        # 3  <content name>
        # 4  <release year>
        # 5  <content id>
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