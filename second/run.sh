#!/bin/bash

# Realtime and Big Data Analytics Fall 2014 final project
# Using a Page Rank style ranking to inspect the movie, tv show and people ontology
# Lior Galanti lior.galanti@nyu.edu N14314920
ITERATIONS=50

#echo 'removing old input file from hdfs'
#hadoop fs -rm -r input.tsv > /dev/null 2>&1

#echo 'copying input file to hdfs'
#hadoop fs -copyFromLocal input.tsv input.tsv

echo 'cleaning up old output folders from hdfs'
hadoop fs -rm -r bootstrap_* ranking_*> /dev/null 2>&1

echo 'Bootstrapping...'

echo 'Cleaning...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input input.tsv \
-output bootstrap_clean \
-mapper bootstrap/clean/map.py \
-reducer bootstrap/clean/reduce.py \
-file bootstrap/clean/map.py \
-file bootstrap/clean/reduce.py

#echo 'Counting people...'
#hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
#-input bootstrap_clean/part-00000 \
#-output bootstrap_zero_people \
#-mapper "bootstrap/zero/map.py person" \
#-reducer bootstrap/zero/reduce.py \
#-file bootstrap/zero/map.py \
#-file bootstrap/zero/reduce.py

#NUMBER_OF_PEOPLE=$(hadoop fs -cat bootstrap_zero_people/part-00000)
#echo "Found $NUMBER_OF_PEOPLE people nodes"

echo 'Counting content...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input bootstrap_clean/part-00000 \
-output bootstrap_zero_content \
-mapper "bootstrap/zero/map.py content" \
-reducer bootstrap/zero/reduce.py \
-file bootstrap/zero/map.py \
-file bootstrap/zero/reduce.py

NUMBER_OF_CONTENT=$(hadoop fs -cat bootstrap_zero_content/part-00000)
echo "Found $NUMBER_OF_CONTENT content nodes"

echo 'Allocating uniform ranks to content'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input bootstrap_clean/part-00000 \
-output ranking_content \
-mapper bootstrap/one/map.py \
-reducer bootstrap/one/reduce.py \
-file bootstrap/one/map.py \
-file bootstrap/one/reduce.py

echo 'Initializing people ranks'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_content/part-00000 \
-output ranking_people \
-mapper "ranking/person/map.py $NUMBER_OF_CONTENT" \
-reducer ranking/person/reduce.py \
-file ranking/person/map.py \
-file ranking/person/reduce.py

echo 'Done bootstrapping. Starting movie rank iterations...'

COUNTER=0
while [ $COUNTER -lt $ITERATIONS ]; do 
    echo "Running ranking iteration $COUNTER"
    
    echo 'Removing content stage'
    hadoop fs -rm -r ranking_content > /dev/null 2>&1
    hadoop fs -rm -r ranking_sum > /dev/null 2>&1
    
    echo 'Calculating people ranking normalization factor'
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_people/part-00000 \
    -output ranking_sum \
    -mapper ranking/sum/map.py \
    -reducer ranking/sum/reduce.py \
    -file ranking/sum/map.py \
    -file ranking/sum/reduce.py
    TOTAL_PEOPLE_RANK=$(hadoop fs -cat ranking_sum/part-00000|cut -f 2)
    echo "People normalization factor is $TOTAL_PEOPLE_RANK"
    
    echo 'Ranking people...'
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_people/part-00000 \
    -output ranking_content \
    -mapper "ranking/content/map.py $TOTAL_PEOPLE_RANK" \
    -reducer ranking/content/reduce.py \
    -file ranking/content/map.py \
    -file ranking/content/reduce.py
    
    echo 'Removing people stage'
    hadoop fs -rm -r ranking_people > /dev/null 2>&1
    hadoop fs -rm -r ranking_sum > /dev/null 2>&1
    
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_content/part-00000 \
    -output ranking_sum \
    -mapper ranking/sum/map.py \
    -reducer ranking/sum/reduce.py \
    -file ranking/sum/map.py \
    -file ranking/sum/reduce.py
    TOTAL_CONTENT_RANK=$(hadoop fs -cat ranking_sum/part-00000|cut -f 1)
    echo "Content normalization factor is $TOTAL_CONTENT_RANK"
    
    echo 'Ranking content...'
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input ranking_content/part-00000 \
    -output ranking_people \
    -mapper "ranking/person/map.py $TOTAL_CONTENT_RANK"\
    -reducer ranking/person/reduce.py \
    -file ranking/person/map.py \
    -file ranking/person/reduce.py
    
    let COUNTER=COUNTER+1;
done

hadoop fs -rm -r ranking_sum > /dev/null 2>&1

echo 'Calculating final normalization factors'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_people/part-00000 \
-output ranking_sum \
-mapper ranking/sum/map.py \
-reducer ranking/sum/reduce.py \
-file ranking/sum/map.py \
-file ranking/sum/reduce.py

TOTALS="$(hadoop fs -cat ranking_sum/part-00000)"
TOTAL_CONTENT_RANK=$(echo "$TOTALS"|cut -f 1)
TOTAL_PEOPLE_RANK=$(echo "$TOTALS"|cut -f 2)
echo "Normalization factor are $TOTAL_CONTENT_RANK and $TOTAL_PEOPLE_RANK"

echo 'Calculating final ranks'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_people/part-00000 \
-output ranking_normalized \
-mapper "normalize/map.py $TOTAL_CONTENT_RANK $TOTAL_PEOPLE_RANK" \
-reducer normalize/reduce.py \
-file normalize/map.py \
-file normalize/reduce.py

echo 'Extracting results...'
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_normalized/part-00000 \
-output ranking_content_result \
-mapper extract/content/map.py \
-reducer extract/content/reduce.py \
-file extract/content/map.py \
-file extract/content/reduce.py

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input ranking_normalized/part-00000 \
-output ranking_people_result \
-mapper extract/people/map.py \
-reducer extract/people/reduce.py \
-file extract/people/map.py \
-file extract/people/reduce.py

echo 'Copy to local file system...'
rm -f movie.rank people.rank
hadoop fs -copyToLocal ranking_content_result/part-00000 movie.rank
hadoop fs -copyToLocal ranking_people_result/part-00000 people.rank
cat movie.rank|sort -rn > movie.rank.sorted
cat people.rank|sort -rn > people.rank.sorted

# hadoop fs -copyToLocal ranking_people/part-00000 movie.raw
# cat movie.raw |./extract/content/map.py|sort -n|./extract/content/reduce.py|sort -rn > movie.rank
# cat movie.raw |./extract/people/map.py|sort -n|./extract/people/reduce.py|sort -rn > people.rank