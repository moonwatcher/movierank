#!/bin/bash

# Realtime and Big Data Analytics Fall 2014 final project
# Using a Page Rank style ranking to inspect the movie, tv show and people ontology
# Lior Galanti lior.galanti@nyu.edu N14314920

echo 'removing input file'
hadoop fs -rm -r input.tsv > /dev/null 2>&1

echo 'removing output folders'
hadoop fs -rm -r bootstrap_one bootstrap_two ranking_one ranking_two> /dev/null 2>&1

echo 'copying input file to hdfs'
hadoop fs -copyFromLocal input.tsv input.tsv

echo 'executing bootstrap phase one'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input input.tsv \
-output bootstrap_one \
-mapper bootstrap/one/map.py \
-reducer bootstrap/one/reduce.py \
-file bootstrap/one/map.py \
-file bootstrap/one/reduce.py

# show output
hadoop fs -ls bootstrap_one

echo 'executing bootstrap phase two'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input bootstrap_one/part-00000 \
-output bootstrap_two \
-mapper bootstrap/two/map.py \
-reducer bootstrap/two/reduce.py \
-file bootstrap/two/map.py \
-file bootstrap/two/reduce.py

# show output
hadoop fs -ls bootstrap_two

echo 'executing ranking phase one'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input bootstrap_two/part-00000 \
-output ranking_one \
-mapper ranking/one/map.py \
-reducer ranking/one/reduce.py \
-file ranking/one/map.py \
-file ranking/one/reduce.py

# show output
hadoop fs -ls ranking_one

echo 'executing ranking phase two'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_one/part-00000 \
-output ranking_two \
-mapper ranking/two/map.py \
-reducer ranking/two/reduce.py \
-file ranking/two/map.py \
-file ranking/two/reduce.py

# show output
hadoop fs -ls ranking_two

