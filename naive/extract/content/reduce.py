#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def print_entity(entity):
    print u'\t'.join([
        '{0:.32f}'.format(float(entity[4])),
        entity[0],
        entity[3],
        entity[1],
        entity[2],
    ]).encode('utf8')
    
def reduce():
    entity = None
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        record = line.strip().split(u'\t')
        # 0  <content id> 
        # 1  <content type>
        # 2  <content name>
        # 3  <release year>
        # 4  <content rank>
        if len(record) == 5: # otherwise something went wrong...
            if entity is None: entity = record
            elif entity[0] != record[0]:
                print_entity(entity)
                entity = record
                
    if entity is not None: print_entity(entity)
    
reduce()