#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def map():
    content_rank_sum = 0.0
    person_rank_sum = 0.0
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
        content_rank_sum += float(record[9])
        person_rank_sum += float(record[10])
        
    content_rank_sum = u'{0:.32f}'.format(content_rank_sum)
    person_rank_sum = u'{0:.32f}'.format(person_rank_sum)
    print u'\t'.join([u'0', content_rank_sum, person_rank_sum]).encode('utf8')
map()