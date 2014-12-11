#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def map(total):
    total = float(total)
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
            record[0], 
            record[1],
            record[2],
            record[3],
            record[4],
            record[5],
            record[6],
            record[7],
            record[8],
            record[9],
            u'{0:.32f}'.format(float(record[10]) / total),
        ]).encode('utf8')
map(sys.argv[1])