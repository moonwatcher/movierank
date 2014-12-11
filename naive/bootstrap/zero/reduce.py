#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def reduce():
    count = 0
    entity = None
    for line in sys.stdin:
        record = line.strip()
        if entity is None: entity = record
        elif entity != record:
            count += 1
            entity = record
                
    if entity is not None:
        count += 1
    print count
    
reduce()