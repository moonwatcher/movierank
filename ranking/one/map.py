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
            # we want to sort by person id so we flip 0 and 5
            rank = u'{0:.32f}'.format(float(record[11]) * float(record[7]))
            print u'\t'.join([
                record[5], 
                record[1],
                record[2],
                record[3],
                record[4],
                record[0],
                record[6],
                record[7],
                record[8],
                record[9],
                record[10],
                record[11],
                rank,       # <contant rank> * <person weight>
            ]).encode('utf8')
map()