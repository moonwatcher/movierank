#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# We start with some initial cleaning to remove some spurious records:
# * movies without a release year
# * movies who's release year is in the future

def map():
    for line in sys.stdin:
        line = unicode(line, 'utf8')
        #index  movie                                       tv show                     tv season                   tv episode
        #--------------------------------------------------------------------------------------------------------------------------
        #0      <media kind:movie>                          <media kind:tv show>        <media kind:tv season>      <media kind:tv season>
        #1      <person id>                                 <person id>                 <person id>                 <person id>
        #2      <movie id>                                  <tv show id>                <tv season id>              <tv episode id>
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
            try:
                year = int(record[4])
                if year <= 2014:
                    print u'\t'.join(record).encode('utf8')
            except ValueError as e:
                pass
map()