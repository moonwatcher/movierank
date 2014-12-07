#!/bin/bash

# Realtime and Big Data Analytics Fall 2014 final project
# Using a Page Rank style ranking to inspect the movie, tv show and people ontology
# Lior Galanti lior.galanti@nyu.edu N14314920

# echo 'removing input file'
# hadoop fs -rm -r input.tsv > /dev/null 2>&1

# echo 'copying input file to hdfs'
# hadoop fs -copyFromLocal input.tsv input.tsv

ITERATIONS=10

echo 'removing old output folders'
hadoop fs -rm -r bootstrap_* ranking_*> /dev/null 2>&1

echo 'Bootstrapping...'

echo 'Counting people...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input input.tsv \
-output bootstrap_zero_people \
-mapper 'bootstrap/zero/map.py person' \
-reducer bootstrap/zero/reduce.py \
-file bootstrap/zero/map.py \
-file bootstrap/zero/reduce.py

NUMBER_OF_PEOPLE=$(hadoop fs -cat bootstrap_zero_people/part-00000)
echo "Found $NUMBER_OF_PEOPLE people nodes"

echo 'Counting content...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input input.tsv \
-output bootstrap_zero_content \
-mapper 'bootstrap/zero/map.py content' \
-reducer bootstrap/zero/reduce.py \
-file bootstrap/zero/map.py \
-file bootstrap/zero/reduce.py

NUMBER_OF_CONTENT=$(hadoop fs -cat bootstrap_zero_content/part-00000)
echo "Found $NUMBER_OF_CONTENT content nodes"
RANK=$(echo "scale=32;1.0/$NUMBER_OF_CONTENT"|bc)
echo "Initial uniform content rank is $RANK"

echo 'Calculating people weights and initial content ranks...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input input.tsv \
-output bootstrap_one \
-mapper bootstrap/one/map.py \
-reducer "bootstrap/one/reduce.py $NUMBER_OF_CONTENT" \
-file bootstrap/one/map.py \
-file bootstrap/one/reduce.py

echo 'Calculating content weights...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input bootstrap_one/part-00000 \
-output ranking_people \
-mapper bootstrap/two/map.py \
-reducer bootstrap/two/reduce.py \
-file bootstrap/two/map.py \
-file bootstrap/two/reduce.py

echo 'Done bootstrapping. Starting movie rank iterations...'

COUNTER=0
while [ $COUNTER -lt $ITERATIONS ]; do 
    echo "Running ranking iteration $COUNTER"
    
    echo 'Removing stage two input'
    hadoop fs -rm -r ranking_content > /dev/null 2>&1
    
    echo 'Ranking people...'
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_people/part-00000 \
    -output ranking_content \
    -mapper ranking/one/map.py \
    -reducer ranking/one/reduce.py \
    -file ranking/one/map.py \
    -file ranking/one/reduce.py
    
    echo 'Removing stage one input'
    hadoop fs -rm -r ranking_people > /dev/null 2>&1
    
    echo 'Ranking content...'
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_content/part-00000 \
    -output ranking_people \
    -mapper ranking/two/map.py \
    -reducer ranking/two/reduce.py \
    -file ranking/two/map.py \
    -file ranking/two/reduce.py
    
    let COUNTER=COUNTER+1;
done


