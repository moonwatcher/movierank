#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

NUMBER_OF_STARS=3
ABOVE_THE_LINE_FRAGMENT=0.8

def print_record(record, weight,rank):
    print u'\t'.join([
        record[0],      # <content id>
        record[2],      # <content type>
        '0',            # <content weight> will be calculated in the next phase
        record[18],     # <content name>
        record[4],      # <release year>
        record[1],      # <person id>
        record[17],     # <person name>
        weight,         # <person weight>
        record[5],      # <age at release date>
        record[6],      # <job>
        record[7],      # <department>
        rank,           # <content rank> this will be the initial content rank
        '0',            # <person rank> people get ranks later on
    ]).encode('utf8')
    
def print_buffer(buffer, rank):
    # The buffer contains all the people in the content and we calculate the weight for each person in the content
    # We seperate the "above the line" http://en.wikipedia.org/wiki/Above_the_line_(filmmaking) 
    # and "bellow the line" http://en.wikipedia.org/wiki/Below_the_line_(filmmaking) credits
    # We basically want the directors, screenwriters, producers and stars to get the majority of the weight
    # Knowing who the "stars" are is somewhat tricky...
    
    above_the_line = []
    bellow_the_line = []
    star = NUMBER_OF_STARS
    
    for record in buffer:
        if  (record[7] == 'directing' and record[6] == 'director') or \
            (record[7] == 'writing' and record[6] == 'screenplay') or \
            (record[7] == 'production' and record[6] == 'producer'):
            above_the_line.append(record)
            
        elif (record[7] == 'acting' and record[6] == 'actor' and star > 0):
            above_the_line.append(record)
            star -= 1
        else:
            bellow_the_line.append(record)
    above_the_line_fragment = ABOVE_THE_LINE_FRAGMENT
    
    if len(bellow_the_line) == 0: above_the_line_weight = 1.0 # weird, but who knows...
    if len(above_the_line) == 0: above_the_line_weight = 0.0 # even weirder, but who knows...
    
    if len(above_the_line) > 0:
        above_the_line_weight = u'{0:.32f}'.format((1.0 / float(len(above_the_line))) * above_the_line_fragment)
        for record in above_the_line:
            print_record(record, above_the_line_weight, rank)
            
    if len(bellow_the_line) > 0:
        bellow_the_line_weight = u'{0:.32f}'.format((1.0 / float(len(bellow_the_line))) * (1.0 - above_the_line_fragment))
        for record in bellow_the_line:
            print_record(record, bellow_the_line_weight, rank)
            
def reduce(content_count):
    rank = u'{0:.32f}'.format(1.0 / float(content_count))
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
                print_buffer(buffer, rank)
                buffer = [record]
                
    if len(buffer) > 0: print_buffer(buffer, rank)
    
reduce(sys.argv[1])