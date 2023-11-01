# Experiments for Unsupervised Ultra Fine Entity Typing
This repository contains an implemention for Unsupervised Ultra Fine Entity Typing with JoBimText API desribed in the paper Unsupervised Ultra-Fine Entity Typing with Distributionally Induced Word Senses (link soon).

## Configuration

### 1. Install requirements
(python version used in the experiments is 3.7.10)
```
(optional)
conda create -n unsupervisedufet-env python=3.7.10
conda activate unsupervisedufet-env
```
```
pip install -r requirements.txt
```
### 2. Download the data 
- The dataset is available at http://nlp.cs.washington.edu/entity_type (redirects to https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html), or alternatively here http://nlp.cs.washington.edu/entity_type/data/ultrafine_acl18.tar.gz.
- Create a directory ../open_type/. Extract the downloaded data and move it to ../open_type/.

### 3. Run tests (optional)
- Note that it takes some time. There are sometimes assertion errors in test_open_type_et_with_jobimtext.py while comparing cosine similarity results or the representations. Re-run if it is the case.
```
pytest tests/test_preprocess.py
pytest tests/test_jobimtext_handler.py
pytest tests/test_open_type_et_with_jobimtext.py
```
- If you want, you can also run other tests.

### 4. Get predictions
- Run open_type_et_with_jobimtext.py with the features/parameters you want to try, which will produce a predictions file. (see sample -- scripts/open_type_et_with_jobimtext.sh)

- To produce the same scores as in the experiments, change the python and output directories in scripts/open_type_et_with_jobimtext.sh.
```
bash scripts/open_type_et_with_jobimtext.sh
```
- Note that for PRP scores, see the commented out lines in jobimtext_handler.py.

### 5. Clone open_type

- To evaluate predictions, the scorer.py function provided by Choi et al. (2018) is used. Clone the repository (https://github.com/uwnlp/open_type) to ../open_type/ directory
```
cd ../open_type
git clone https://github.com/uwnlp/open_type.git
```
### 6. Compute scores
- Comment out the lines 78, 81, 82 in ../open_type/open_type/scorer.py files, since only P, R, and F1 scores will be computed.
- To compute the scores (assumed your predictions are stored in "predictions_jobimtext/predictions_open_type_with_jobimtext.json"):
```
cd ../open_type/open_type
python scorer.py ../../unsupervised-ultra-fine-entity-typing/predictions_jobimtext/predictions_open_type_with_jobimtext
```
### 7. Compute combination
- The best model and its predictions of model by Choi et al. 2018 are available, again, at
http://nlp.cs.washington.edu/entity_type. Download best model and outputs from "Pretrained model / outputs", or alternatively here http://nlp.cs.washington.edu/entity_type/model/best_model.tar.gz.
- Extract the downloaded compressed folder and move it to ../open_type/.
- Change the python and output directories in scripts/combination.sh, accordingly.
```
bash scripts/combination.sh
```
- Note that before computing scores, first convert them to set, e.g. as done in convert_combination.ipynb.
- Compute the scores in the same way as in step 6.

#### Note for computing without pronouns scores
- To get without pronouns predictions for jobimtext predictions and/or Choi et al. (2018) predictions, use "exclude_pronouns" function in the combination.py file, e.g. as done in wo_pronouns.ipynb.
- Compute the scores in the same way as in step 6.

#### Note for License
- Disclaimer: before the use, be sure to check licenses of all dependencies, dependencies in the requirements.txt file, and the license of dataset and code provided by Choi et al. (2018).

