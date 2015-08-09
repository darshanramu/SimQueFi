#!/bin/sh
echo "Creating Question Set\n"
./create_question_set.py
echo "POS tagging the questions\n"
./POS_tag_Synonym.py
echo "Running K-means\n"
./kmeans_algorithm.py > $1
