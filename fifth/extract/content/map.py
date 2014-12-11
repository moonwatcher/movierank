#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def map():
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        # 0  <content id>
        # 1  <content type>
        # 2  <content name>
        # 3  <release year>
        # 4  <person id>
        # 5  <person name>
        # 6  <age at release date>
        # 7  <job>
        # 8  <department>
        # 9  <content rank>
        # 10 <person rank>        
        record = line.strip().split(u'\t')
        print u'\t'.join([
            record[0],  # 0  <content id> 
            record[1],  # 1  <content type>
            record[2],  # 2  <content name>
            record[3],  # 3  <release year>
            record[9],  # 4 <content rank>
        ]).encode('utf8')
map()