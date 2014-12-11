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
            record[4],  # 4  <person id> 
            record[10], # 10 <person rank>
            record[5],  # 5  <person name>
        ]).encode('utf8')
map()