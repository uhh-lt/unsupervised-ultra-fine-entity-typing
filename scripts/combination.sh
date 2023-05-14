#!/bin/bash 

# path of python
PYTHONBIN=/home/sevgili/anaconda3-2020-11/envs/unsupervisedufet-env/bin/python3.7
OUTDIR="predictions_combination"


# 1
echo "predictions of combination from our system and model by Choi et al. (2018) w/o limit and w/o exclude"
# --limit-number is given 0, since we do not want to limit for this run.
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--ufet-predictions-file-path ../open_type/best_model/test.json \
--limit-number 0 \
--file-path ../open_type/release/crowd/test.json \
--not-exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_wo_limit_wo_exclude.json


# 2
echo "predictions of combination from our system and model by Choi et al. (2018) w/o limit and with exclude"
# --limit-number is given 0, since we do not want to limit for this run.
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--ufet-predictions-file-path ../open_type/best_model/test.json \
--limit-number 0 \
--file-path ../open_type/release/crowd/test.json \
--exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_wo_limit_exclude.json


# 3
echo "predictions of combination from our system and model by Choi et al. (2018) with limit and w/o exclude"
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--ufet-predictions-file-path ../open_type/best_model/test.json \
--limit-number 5 \
--file-path ../open_type/release/crowd/test.json \
--not-exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_limit5_wo_exclude.json


# 4
echo "predictions of combination from our system and model by Choi et al. (2018) with limit and with exclude"
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--ufet-predictions-file-path ../open_type/best_model/test.json \
--limit-number 5 \
--file-path ../open_type/release/crowd/test.json \
--exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_limit5_exclude.json

#### to check #####
# 5
echo "predictions of combination from our system and model by Choi et al. (2018) w/o limit and w/o exclude"
# --limit-number is given 0, since we do not want to limit for this run.
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path ../open_type/best_model/test.json \
--ufet-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--limit-number 0 \
--file-path ../open_type/release/crowd/test.json \
--not-exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_wo_limit_wo_exclude_check.json


# 6
echo "predictions of combination from our system and model by Choi et al. (2018) w/o limit and with exclude"
# --limit-number is given 0, since we do not want to limit for this run.
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path ../open_type/best_model/test.json \
--ufet-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--limit-number 0 \
--file-path ../open_type/release/crowd/test.json \
--exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_wo_limit_exclude_check.json


# 7
echo "predictions of combination from our system and model by Choi et al. (2018) with limit and w/o exclude"
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path ../open_type/best_model/test.json \
--ufet-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--limit-number 5 \
--file-path ../open_type/release/crowd/test.json \
--not-exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_limit5_wo_exclude_check.json


# 8
echo "predictions of combination from our system and model by Choi et al. (2018) with limit and with exclude"
$PYTHONBIN combination.py \
--jobimtext-predictions-file-path ../open_type/best_model/test.json \
--ufet-predictions-file-path predictions_jobimtext/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--limit-number 5 \
--file-path ../open_type/release/crowd/test.json \
--exclude-pronouns \
--output-file-path $OUTDIR/predictions_test_combination_limit5_exclude_check.json
