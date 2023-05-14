#!/bin/bash 

# path of python
PYTHONBIN=/home/sevgili/anaconda3-2020-11/envs/unsupervisedufet-env/bin/python3.7
OUTDIR="predictions_baseline"

#####################################
## run with best parameters for test
#####################################

echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for the first cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--first-cluster \
--output-file-path $OUTDIR/baseline_test_first_cluster.json \
--log-file $OUTDIR/baseline_test_first_cluster.log \
--args-file $OUTDIR/args_test_baseline_first_cluster.json


echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for a random cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--random-cluster \
--output-file-path $OUTDIR/baseline_test_random1_cluster.json \
--log-file $OUTDIR/baseline_test_random1_cluster.log \
--args-file $OUTDIR/args_test_baseline_random1_cluster.json


echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for a random cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--random-cluster \
--output-file-path $OUTDIR/baseline_test_random2_cluster.json \
--log-file $OUTDIR/baseline_test_random2_cluster.log \
--args-file $OUTDIR/args_test_baseline_random2_cluster.json


echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for a random cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--random-cluster \
--output-file-path $OUTDIR/baseline_test_random3_cluster.json \
--log-file $OUTDIR/baseline_test_random3_cluster.log \
--args-file $OUTDIR/args_test_baseline_random3_cluster.json


echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for a random cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--random-cluster \
--output-file-path $OUTDIR/baseline_test_random4_cluster.json \
--log-file $OUTDIR/baseline_test_random4_cluster.log \
--args-file $OUTDIR/args_test_baseline_random4_cluster.json



echo "predictions of TEST baseline for unsupervised ultra-fine entity typing for a random cluster"
# include-isas, number-of-isas, number-of-terms-in-cluster, ngram, first  do not matter in the below config
# --weighted-average are not given since we want to give None for them
$PYTHONBIN baseline.py \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--random-cluster \
--output-file-path $OUTDIR/baseline_test_random5_cluster.json \
--log-file $OUTDIR/baseline_test_random5_cluster.log \
--args-file $OUTDIR/args_baseline_test_random5_cluster.json


