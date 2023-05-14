import random
import json
import logging
from sentence_transformers import SentenceTransformer
from open_type_et_with_jobimtext import prepare_senses_info
import numpy as np


def baseline_first_cluster(data, mention_senses_info, number_of_predictions):
    predictions_first = {}
    for mention_info in data:  
        senses_info = mention_senses_info[mention_info["mention_span"]]
        if len(senses_info) > 1:
            info = []        
            
            # sorting is done for just sanity check
            # casting cui to int to be able to sort
            for sense_info in senses_info:
                info.append(dict((k, v) if k != 'cui' else (k, int(v)) for k, v in sense_info.items()))

            # for testing
            for index, sense in enumerate(info):
                for k, v in sense.items():
                    if k == 'sense_embedding':
                        assert np.array_equal(sense[k], senses_info[index][k])
                    elif k == 'cui':
                        assert str(sense[k]) == senses_info[index][k]
                    else:
                        assert sense[k] == senses_info[index][k]
            # sort by cui
            sorted_info = sorted(info, key=lambda x: x['cui'], reverse=False)

            # check the info is already sorted
            assert sorted_info == info
            
            logging.info("for search mention: " + sorted_info[0]['search_mention'] +
                         " cui: " + str(sorted_info[0]['cui']) + " is selected, with isas: " +
                         str(sorted_info[0]['isas']))
            predictions_first[mention_info['annot_id']] = {"gold": mention_info["y_str"], 
                                                           "pred": sorted_info[0]['isas'][:number_of_predictions]}
        else:
            logging.info("No sorting applied. For search mention: " + senses_info[0]['search_mention'] +
                         " cui: " + str(senses_info[0]['cui']) + " is selected, with isas: " +
                         str(senses_info[0]['isas']))
            predictions_first[mention_info['annot_id']] = {"gold": mention_info["y_str"], 
                                                           "pred": senses_info[0]['isas'][:number_of_predictions]}

    assert len(predictions_first) == len(data)
    return predictions_first


def baseline_random_cluster(data, mention_senses_info, number_of_predictions):
    predictions_random = {}
    for mention_info in data:  
        senses_info = mention_senses_info[mention_info["mention_span"]]

        if len(senses_info) > 1:
            # https://docs.python.org/3/library/random.html#random.randint
            # a <= N <= b
            random_index = random.randint(0, len(senses_info)-1)
            
            logging.info("for search mention: " + senses_info[random_index]['search_mention'] +
                         " cui: " + str(senses_info[random_index]['cui']) + " is selected, with isas: " +
                         str(senses_info[random_index]['isas']))

            predictions_random[mention_info['annot_id']] = {"gold": mention_info["y_str"], 
                                                            "pred": senses_info[random_index]['isas']
                                                            [:number_of_predictions]}
        else:
            logging.info("No randomization applied. For search mention: " + senses_info[0]['search_mention'] +
                         " cui: " + str(senses_info[0]['cui']) + " is selected, with isas: " +
                         str(senses_info[0]['isas']))
            predictions_random[mention_info['annot_id']] = {"gold": mention_info["y_str"], 
                                                            "pred": senses_info[0]['isas'][:number_of_predictions]}

    assert len(predictions_random) == len(data)
    return predictions_random


def get_parameters():
    import argparse
    parser = argparse.ArgumentParser(description='Performs Baseline for Unsupervised Knowledge-Free Open Type\
                                     - Ultra Fine Entity Typing using JoBimText.')
    
    parser.add_argument('--file-path', dest='file_path', 
                        default="../open_type/release/crowd/test.json", type=str,
                        help='determines the path for test or dev file provided by open type (Choi et al., 2018) \
                        -- https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html \
                        (default is local path for file release/crowd/test.json)')
    
    parser.add_argument('--types-file-path', dest='types_file_path', 
                        default="../open_type/release/ontology/types.txt", type=str,
                        help='determines the path for types file (vocabulary for the types) \
                        provided by open type (Choi et al., 2018) \
                        -- https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html \
                        (default is local path -- for release/ontology/types.json)')
    
    include_isas = parser.add_mutually_exclusive_group(required=False)
    include_isas.add_argument('--include-isas', dest='include_isas', action='store_true',
                              help='includes isas label words while creating cluster representations. \
                              Note that it is not any important here, will be used to be able to call \
                              prepare_senses_info func.')
    include_isas.add_argument('--not-include-isas', dest='include_isas', action='store_false',
                              help='does not include isas label words while creating cluster representations. \
                              Note that it is not any important here, will be used to be able to call \
                              prepare_senses_info func.')
    parser.set_defaults(include_isas=True)
    
    parser.add_argument('--weighted-average', default=None, type=str,
                        help='determines which weighted average methods for embeddings of cluster terms/isas \
                        will be used. Note that it is not any important here, will be used to be able to call \
                        prepare_senses_info func.(default None, means that the average will not be \
                        weighted -- other options "cosine", "rank")')
    
    parser.add_argument('--number-of-isas', dest='number_of_isas', default=10, type=int,
                        help='determines how many isas label words while CREATING \
                        cluster representations. \
                        Note that it is not any important here, will be used to be able to call prepare_senses_info \
                        func. (default 10)')
    
    parser.add_argument('--number-of-predictions', dest='number_of_predictions', default=10, type=int,
                        help='determines how many isas labels will be used for final PREDICTION \
                        (default 10)')
    
    parser.add_argument('--number-of-terms-in-cluster', dest='number_of_cluster_terms', default=10, type=int,
                        help='determines how many terms in sense clusters will be used  \
                        while creating/evaluating cluster representations. \
                        Note that it is not any important here, will be used to be able to call prepare_senses_info \
                        func. (default 10)')
    
    parser.add_argument('--ngram', dest='ngram', default=1, type=int,
                        help='determines n for the ngram, which will be used for the search in JoBimText \
                        (default 1)')
    
    first = parser.add_mutually_exclusive_group(required=False)
    first.add_argument('--first', dest='first', action='store_true',
                       help='determines if ngram is extracted from the first part of mention or last part')
    first.add_argument('--last', dest='first', action='store_false',
                       help='determines if ngram is extracted from the first part of mention or last part')
    parser.set_defaults(first=False)
    
    use_sklearn = parser.add_mutually_exclusive_group(required=False)
    use_sklearn.add_argument('--use-sklearn', dest='use_sklearn', action='store_true',
                             help='determines if sklearn implementation for ngram extraction will be used or not \
                             (default not means nltk implementation will be used)')
    use_sklearn.add_argument('--not-use-sklearn', dest='use_sklearn', action='store_false',
                             help='determines if sklearn implementation for ngram extraction will be used or not \
                             (default not means nltk implementation will be used)')
    parser.set_defaults(use_sklearn=False)
    
    headword = parser.add_mutually_exclusive_group(required=False)
    headword.add_argument('--headword', dest='headword', action='store_true',
                          help='determines whether headword will be extracted for each mention for search on JoBimText \
                          or ngram of mention will be extracted (default is False mean ngram will be extracted)')
    headword.add_argument('--not-headword', dest='headword', action='store_false',
                          help='determines whether headword will be extracted for each mention for search on JoBimText \
                          or ngram of mention will be extracted (default is False mean ngram will be extracted)')
    parser.set_defaults(headword=False)
    
    apply_preprocess = parser.add_mutually_exclusive_group(required=False)
    apply_preprocess.add_argument('--apply-preprocess', dest='apply_preprocess', action='store_true',
                                  help='determines if the preprocess (i.e. singularization) for a mention \
                                  before the search in JoBimText will be applied or not')
    apply_preprocess.add_argument('--not-apply-preprocess', dest='apply_preprocess', action='store_false',
                                  help='determines if the preprocess (i.e. singularization) for a mention \
                                  before the search in JoBimText will be applied or not')
    parser.set_defaults(apply_preprocess=True)
    
    apply_postprocess = parser.add_mutually_exclusive_group(required=False)
    apply_postprocess.add_argument('--apply-postprocess', dest='apply_postprocess', action='store_true',
                                   help='determines the labels predicted from our system will be processed \
                                   (i.e. singularized, lowerized, underscored, and filtered) or not')
    apply_postprocess.add_argument('--not-apply-postprocess', dest='apply_postprocess', action='store_false',
                                   help='determines the labels predicted from our system will be processed \
                                   (i.e. singularized, lowerized, underscored, and filtered) or not')
    parser.set_defaults(apply_postprocess=True)
    
    lowerize = parser.add_mutually_exclusive_group(required=False)
    lowerize.add_argument('--lowerize', dest='lowerize', action='store_true',
                          help='determines if a mention will be lowerized \
                          before the search in JoBimText or not')
    lowerize.add_argument('--not-lowerize', dest='lowerize', action='store_false',
                          help='determines if a mention will be lowerized \
                          before the search in JoBimText or not')
    parser.set_defaults(lowerize=False)
    
    parser.add_argument('--cluster-type', dest='cluster_type', default="200,200", type=str,
                        help='determines which type of clustering (Chinese Whisper) will be used while searching \
                        mention in JoBimText (default "200,200" -- other options "200,50", "50,50")')
    
    first_cluster = parser.add_mutually_exclusive_group(required=False)
    first_cluster.add_argument('--first-cluster', dest='first_cluster', action='store_true',
                               help='determines the baseline predictions are from first cluster')
    first_cluster.add_argument('--random-cluster', dest='first_cluster', action='store_false',
                               help='determines the baseline predictions are from random cluster')
    parser.set_defaults(first_cluster=False)
    
    parser.add_argument('--output-file-path', dest='output_file_path', 
                        default='predictions_baseline_open_type_with_jobimtext.json', type=str,
                        help='determines the file path to store the predictions done by the model, \
                        that will be used later for evaluation, directly using the scorer by (Choi et al., 2018)\
                        -- https://github.com/uwnlp/open_type/blob/master/scorer.py\
                        (default is "predictions_baseline_open_type_with_jobimtext.json")')
    
    parser.add_argument('--log-file', dest='log_file', default='baseline_open_type_with_jobimtext.log', type=str,
                        help='the progress while running the script will be stored in the log file\
                        (default "baseline_open_type_with_jobimtext.log")')
    
    parser.add_argument('--args-file', dest='args_file', default='args_baseline_open_type_with_jobimtext.json', 
                        type=str, help='the arguments are stored only to check \
                        (default "args_baseline_open_type_with_jobimtext.json")')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parameters()
    print(args)
    # args are stored to check -- see test_open_type_et_with_jobimtext.ipynb
    with open(args.args_file, "w") as f:
        json.dump(vars(args), f)
    
    # https://docs.python.org/3/howto/logging.html
    logging.basicConfig(filename=args.log_file, format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info("Baseline for Open Type - Ultra Fine Entity Typing with JoBimText is started  " + str(vars(args)))
    
    # we won't use the model but just for prepare_senses_info call, we will use.
    # so given the default model.
    model_sentence_transformer = SentenceTransformer('all-mpnet-base-v2')
    logging.info("model is loaded")
    
    f = open(args.file_path, "r")
    data_ = [json.loads(sent.strip()) for sent in f.readlines()]
    logging.info("data is loaded")
    
    with open(args.types_file_path, 'r') as f:
        types_lines = f.readlines()
    types_ = [type_.strip() for type_ in types_lines]
    logging.info("types file is loaded")  
    
    assert len(types_) == len(set(types_))
    
    # the same preprocess and postprocess are applied.
    mention_senses_info_, count_no_results_ = prepare_senses_info(model=model_sentence_transformer, data=data_,
                                                                  include_isas=args.include_isas,
                                                                  cluster_type=args.cluster_type,
                                                                  number_of_cluster_terms=args.number_of_cluster_terms,
                                                                  head_word=args.headword,
                                                                  n=args.ngram, first=args.first,
                                                                  number_of_isas=args.number_of_isas,
                                                                  weighted_average=args.weighted_average,
                                                                  apply_preprocess=args.apply_preprocess,
                                                                  lower=args.lowerize,
                                                                  apply_postprocess=args.apply_postprocess, 
                                                                  types=types_, noisy_isas=['thing'],
                                                                  use_sklearn=args.use_sklearn)
    
    not_founds = [mention_senses_info_[mention_info['mention_span']][0] for mention_info in data_ if 
                  len(mention_senses_info_[mention_info['mention_span']]) == 1 
                  and not mention_senses_info_[mention_info['mention_span']][0]['JoBimText']]
    for not_found in not_founds:
        assert not_found['sense_embedding'] is None
        assert not_found['isas'] == ['person']
        assert not_found['cui'] == 0
        assert not_found['isas_wo_process'] is None
    
    coverage = (len(data_) - len(not_founds))/len(data_)
    
    logging.info("cluster embeddings are prepared, and there are no output from our system for " + 
                 str(len(not_founds)) + " entries in the data, and for " + str(count_no_results_) +
                 " different mentions, the coverage is " + str(coverage))
    
    if args.first_cluster:
        logging.info("baseline_first_cluster function called")
        predictions = baseline_first_cluster(data=data_, mention_senses_info=mention_senses_info_,
                                             number_of_predictions=args.number_of_predictions)
    else:
        logging.info("baseline_random_cluster function called")
        predictions = baseline_random_cluster(data=data_, mention_senses_info=mention_senses_info_,
                                              number_of_predictions=args.number_of_predictions)
        
    logging.info("predictions are collected")

    # predictions_baseline_first.json
    # predictions_baseline_random.json
    with open(args.output_file_path, "w") as f:
        json.dump(predictions, f)
