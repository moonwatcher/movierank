#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math

def handle_record(record, rank):
    print u'\t'.join([
        record[4],      # <content id>
        record[1],      # <content type>
        record[2],      # <content name>
        record[3],      # <release year>
        record[0],      # <person id>
        record[5],      # <person name>
        record[6],      # <age at release date>
        record[7],      # <job>
        record[8],      # <department>
        record[9],      # <content rank>
        rank,           # <person rank>
    ]).encode('utf8')
    
def handle_buffer(buffer):
    # Rank for a person is the average over all ranks for the content it is in
    # corrected by the log of the number of content the person is in 
    rank = 0.0
    for record in buffer:
        rank += float(record[9])
    rank /= float(len(buffer))
    rank *= math.log(len(buffer),2)
    rank = u'{0:.32f}'.format(rank)
        
    for record in buffer:
        handle_record(record, rank)
        
def reduce():
    buffer = []
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        # 0  <person id>
        # 1  <content type>
        # 2  <content name>
        # 3  <release year>
        # 4  <content id>
        # 5  <person name>
        # 6  <age at release date>
        # 7  <job>
        # 8  <department>
        # 9  <content rank>
        # 10 <person rank>
        record = line.strip().split(u'\t')
        if len(buffer) == 0 or record[0] == buffer[0][0]:
            buffer.append(record)
        else:
            handle_buffer(buffer)
            buffer = [record]
                
    if len(buffer) > 0: handle_buffer(buffer)
    
reduce()