#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def map():
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
            rank = unicode(float(record[11]) * float(record[7]))
            print u'\t'.join([
                record[0],  # 0  <content id> 
                record[1],  # 1  <content type>
                record[3],  # 3  <content name>
                record[4],  # 4  <release year>
                record[11], # 11 <content rank>
            ]).encode('utf8')
map()