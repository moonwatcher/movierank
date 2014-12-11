#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def print_record(record):
    print u'\t'.join([
        record[0],      # <content id>
        record[2],      # <content type>
        record[18],     # <content name>
        record[4],      # <release year>
        record[1],      # <person id>
        record[17],     # <person name>
        record[5],      # <age at release date>
        record[6],      # <job>
        record[7],      # <department>
        '1',            # <content rank>
        '1',            # <person rank>
    ]).encode('utf8')
    
def print_buffer(buffer):
    for record in buffer: print_record(record)
    
def reduce():
    buffer = []
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        #index  movie                                       tv show                     tv season                   tv episode
        #--------------------------------------------------------------------------------------------------------------------------
        #0      <movie id>                                  <tv show id>                <tv season id>              <tv episode id>
        #1      <person id>                                 <person id>                 <person id>                 <person id>
        #2      <media kind:movie>                          <media kind:tv show>        <media kind:tv season>      <media kind:tv season>
        #3      <order>                                     <order>                     <order>                     <order>
        #4      <release year>                              <release year>              <release year>              <release year>
        #5      <age at release date>                       <age at release date>       <age at release date>       <age at release date>
        #6      <job>                                       <job>                       <job>                       <job>
        #7      <department>                                <department>                <department>                <department>
        #8      <budget>                                    <budget>                    <budget>                    <budget>
        #9      <revenue>                                   <revenue>                   <revenue>                   <revenue>
        #10     <tmdb popularity>
        #11     <tmdb vote average>
        #12     <tmdb vote count>
        #13     <rotten tomatoes audience rating>
        #14     <rotten tomatoes audience score>
        #15     <rotten tomatoes critics rating>
        #16     <rotten tomatoes critics score>
        #17     <person name>                               <person name>               <person name>               <person name>
        #18     <movie name>                                <tv show name>              <tv season number>          <tv episode name>
        record = line.strip().split(u'\t')
        if len(buffer) == 0 or record[0] == buffer[0][0]:
            buffer.append(record)
        else:
            print_buffer(buffer)
            buffer = [record]
            
    if len(buffer) > 0: print_buffer(buffer)
    
reduce()