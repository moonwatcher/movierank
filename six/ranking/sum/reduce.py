#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def reduce():
    content_rank_sum = 0.0
    person_rank_sum = 0.0
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        record = line.strip().split(u'\t')
        content_rank_sum += float(record[1])
        person_rank_sum += float(record[2])
        
    content_rank_sum = u'{0:.32f}'.format(content_rank_sum)
    person_rank_sum = u'{0:.32f}'.format(person_rank_sum)
    print u'\t'.join([content_rank_sum, person_rank_sum]).encode('utf8')
reduce()