#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def print_record(record, weight):
    print u'\t'.join([
        record[0],      # <content id>
        record[2],      # <content type>
        unicode(0.0),   # <content weight> will be calculated in the next phase
        record[18],     # <content name>
        record[4],      # <release year>
        record[1],      # <person id>
        record[17],     # <person name>
        weight,         # <person weight>
        record[5],      # <age at release date>
        record[6],      # <job>
        record[7],      # <department>
        unicode(1.0),   # <content rank> this will be the initial content rank
        unicode(0.0),   # <person rank> people get ranks later on
    ]).encode('utf8')
    
def print_buffer(buffer):
    # The buffer contains all the people in the content and we calculate the weight for each person in the content
    # We also allocate the initial content rank
    weight = unicode(1.0 / float(len(buffer)))
    for record in buffer:
        print_record(record, weight)
        
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
        if len(record) == 19: # otherwise something went wrong...
            if len(buffer) == 0 or record[0] == buffer[0][0]:
                buffer.append(record)
            else:
                print_buffer(buffer)
                buffer = [record]
                
    if len(buffer) > 0: print_buffer(buffer)
    
reduce()