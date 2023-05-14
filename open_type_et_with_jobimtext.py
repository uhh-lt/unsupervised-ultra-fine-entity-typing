# https://inflect.readthedocs.io/en/latest/#inflect.engine.singular_noun
import inflect
import stanza
from preprocess import get_headword_of_mentions, get_first_ngram_of_mentions, get_last_ngram_of_mentions
from preprocess import get_first_ngram_of_mentions_sklearn, get_last_ngram_of_mentions_sklearn
from jobimtext_handler import get_senses_from_jobimtext, process_jobimtext_result
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import argparse
import logging
# https://www.sbert.net/docs/usage/semantic_textual_similarity.html


# the weights are between queried mention and sense terms (and/or isas)
def generate_sense_embedding(model, senses, weighted=False, weights=None, mention=None):
    representations = model.encode(senses)

    if weighted:
        if weights:
            return np.average(a=representations, axis=0, weights=weights)

        mention_rep = model.encode(mention)
        sims = [cosine_similarity(mention_rep.reshape(1, -1), rep.reshape(1, -1))[0][0] for rep in representations]
        return np.average(a=representations, axis=0, weights=sims)
    else:
        return np.average(a=representations, axis=0)


# for each mention: 1- search strings are derived, 2- its cluster information is taken, 
# 3- a sense embedding for each cluster is generated 
def prepare_senses_info(model, data, include_isas, cluster_type, number_of_cluster_terms, head_word, n, first,
                        number_of_isas, noisy_isas, weighted_average=None, apply_preprocess=True, lower=False,
                        apply_postprocess=True, types=None, use_sklearn=False):
    inflect_engine = inflect.engine()
        
    mentions = set([mention_info["mention_span"] for mention_info in data])
    if head_word:
        # https://stanfordnlp.github.io/stanza/depparse.html
        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')        
        search_mentions, _ = get_headword_of_mentions(mentions=mentions, inflect_engine=inflect_engine, 
                                                      nlp=nlp, apply_preprocess=apply_preprocess)
        logging.info("headwords are extracted, nlp loaded accordingly")
    else:
        # https://stanfordnlp.github.io/CoreNLP/udfeats.html
        # https://universaldependencies.org/guidelines.html
        # https://universaldependencies.org/u/overview/morphology.html
        # https://universaldependencies.org/u/feat/index.html
        # https://stanfordnlp.github.io/stanza/pos.html
        # 'mwt' does not loaded since -- https://stanfordnlp.github.io/stanza/mwt.html
        # Note: Only languages with multi-word tokens (MWT), such as German or French, 
        # require MWTProcessor; other languages, such as English or Chinese, do not support 
        # this processor in the pipeline.
        # and when added, I got a warning:
        # 2022-08-09 13:41:45 WARNING: Can not find mwt: default from official model list. Ignoring it.
        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        if first:
            if use_sklearn:
                search_mentions = get_first_ngram_of_mentions_sklearn(mentions=mentions, n=n, 
                                                                      inflect_engine=inflect_engine, nlp=nlp,
                                                                      apply_preprocess=apply_preprocess)
                logging.info("first, sklearn are extracted with n:" + str(n) + " nlp loaded accordingly")
            else:
                search_mentions = get_first_ngram_of_mentions(mentions=mentions, n=n, 
                                                              inflect_engine=inflect_engine, nlp=nlp,
                                                              apply_preprocess=apply_preprocess)
                logging.info("first, nltk are extracted with n:" + str(n) + " nlp loaded accordingly")
        else:
            if use_sklearn:
                search_mentions = get_last_ngram_of_mentions_sklearn(mentions=mentions, n=n, 
                                                                     inflect_engine=inflect_engine, nlp=nlp,
                                                                     apply_preprocess=apply_preprocess)
                logging.info("last, sklearn are extracted with n:" + str(n) + " nlp loaded accordingly")
            else:
                search_mentions = get_last_ngram_of_mentions(mentions=mentions, n=n, 
                                                             inflect_engine=inflect_engine, nlp=nlp,
                                                             apply_preprocess=apply_preprocess)
                logging.info("last, nltk are extracted with n:" + str(n) + " nlp loaded accordingly")
    assert len(mentions) == len(search_mentions)
    
    mention_senses_info = {}
    count, multi_occ_mentions, count_no_results = 0, 0, 0
    for mention_info in data:  
        mention = mention_info["mention_span"]
        count += 1
        if count % 100 == 0:
            logging.info(str(count) + ' mentions are processed over ' + str(len(data)) + ' mentions')
            # print(count, 'mentions are processed over', len(data), 'mentions')
        try:
            _ = mention_senses_info[mention]
            multi_occ_mentions += 1
            continue
        except KeyError:
            mention_senses_info[mention] = []
            search_mention = search_mentions[mention]
            if lower:
                search_mention = search_mention.lower()
            results = get_senses_from_jobimtext(mention=search_mention, cluster_type=cluster_type)

            if results:
                # sometimes although there are senses, there are no isas, like "you", to catch them, I put flag
                flag = False
                for result in results:
                    senses, isas = process_jobimtext_result(result=result,
                                                            number_of_cluster_terms=number_of_cluster_terms,
                                                            number_of_isas=number_of_isas, 
                                                            apply_postprocess=apply_postprocess, nlp=nlp, 
                                                            inflect_engine=inflect_engine, types=types, 
                                                            noisy_isas=noisy_isas)

                    if senses and isas and len(senses) > 0 and len(isas) > 0:
                        flag = True
                        weights = compute_weight_by_rank(senses, isas) if include_isas and weighted_average == "rank" \
                            else None
                        if include_isas:
                            senses.extend(isas)
                        
                        weighted = True if weighted_average == "cosine" or weighted_average == "rank" else False
                        sense_embedding = generate_sense_embedding(model=model, senses=senses, weighted=weighted,
                                                                   weights=weights, mention=mention)

                        mention_senses_info[mention].append({'sense_embedding': sense_embedding,
                                                             'isas': isas, 'cui': result['cui'],
                                                             'search_mention': search_mention,
                                                             'isas_wo_process': [i.split(':')[0]
                                                                                 for i in result['isas']],
                                                             'JoBimText': True})

                # if no isas info available, like "you" for "200,200"
                if not flag:
                    logging.info('No flag! mention: ' + mention + ' search mention: ' + search_mention +
                                 ' results: ' + str(results))
                    # for now most frequent label in dev set is given "person",
                    # shown in open_type_et_with_jobimtext.ipynb
                    mention_senses_info[mention].append({'sense_embedding': None, 'isas': ['person'], 'cui': 0,
                                                         'JoBimText': False, 'search_mention': search_mention,
                                                         'isas_wo_process': None})
                    count_no_results += 1

            else:
                logging.info('No results! mention: ' + mention + ' search mention: ' + search_mention)
                # for now most frequent label in dev set is given "person",
                # shown in open_type_et_with_jobimtext.ipynb
                mention_senses_info[mention].append({'sense_embedding': None, 'isas': ['person'], 'cui': 0,
                                                     'JoBimText': False, 'search_mention': search_mention,
                                                     'isas_wo_process': None})
                count_no_results += 1
    
    assert len(data) - multi_occ_mentions == len(mentions)
    assert len(mentions) == len(mention_senses_info)
    return mention_senses_info, count_no_results


# produce weights by term and isas orders
def compute_weight_by_rank(sense_terms, isas):
    weights_rank = [1.0/(index+1) for index in range(len(sense_terms))]
    weights_rank_isas = [1.0/(index+1) for index in range(len(isas))]
    weights_rank.extend(weights_rank_isas)
    
    return weights_rank


# finds the highest similar sense, based on context embedding (and/or mention embedding)
def find_highest_similar(context_embed, senses_info, mention_embed=None):
    similarities_doc = []
    similarities_average = []
    
    for sense_info in senses_info:
        sense_embedding = sense_info['sense_embedding']
        similarity = cosine_similarity(context_embed.reshape(1, -1), sense_embedding.reshape(1, -1))[0][0]
        updated_info = {info: sense_info[info] for info in sense_info if info != 'sense_embedding'}
        updated_info['score'] = similarity
        similarities_doc.append(updated_info)
        
        if type(mention_embed) != type(None):
            men_sim = cosine_similarity(mention_embed.reshape(1, -1), sense_embedding.reshape(1, -1))[0][0]
            updated_info_ = {info: sense_info[info] for info in sense_info if info != 'sense_embedding'}
            updated_info_['score'] = (similarity+men_sim)/2
            similarities_average.append(updated_info_)
    
    # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    similarities_doc = sorted(similarities_doc, key=lambda x: x['score'], reverse=True)
    similarities_average = sorted(similarities_average, key=lambda x: x['score'], reverse=True)
    if type(mention_embed) != type(None):
        return similarities_doc, similarities_average
    return similarities_doc


# collect predictions in the same format as predictions from Choi et al., 2018 -- 
# http://nlp.cs.washington.edu/entity_type (redirects -- https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html)
def get_predictions(model, data, mention_senses_info, number_of_predictions, include_mention=True,
                    include_mention_sim=False, analyse=False):
    predictions = {}
    
    for mention_info in data:
        left_context = ' '.join(mention_info["left_context_token"])
        mention = mention_info["mention_span"]
        right_context = ' '.join(mention_info["right_context_token"])
        
        if include_mention:
            context = left_context + ' ' + mention + ' ' + right_context
        else:
            context = left_context + ' ' + right_context
        context_embed = model.encode(context)
   
        senses_info = mention_senses_info[mention]
        if len(senses_info) > 1:
            if include_mention_sim:
                mention_embed = model.encode(mention)
                _, prediction_info_all = find_highest_similar(context_embed=context_embed, 
                                                              senses_info=senses_info, mention_embed=mention_embed)
                prediction_info = prediction_info_all[0]
            else:
                prediction_info = find_highest_similar(context_embed=context_embed, senses_info=senses_info)[0]
        elif len(senses_info) == 1:
            prediction_info = senses_info[0]
        else:
            raise Exception('mention_senses_info returns nothing for the mention:', mention)
        
        prediction = prediction_info['isas'][:number_of_predictions]
        if analyse:
            try:
                score = '{:.4f}'.format(prediction_info["score"]) 
            except KeyError:
                score = None
            predictions[mention_info['annot_id']] = {"gold": mention_info["y_str"], "pred": prediction,
                                                     "cui": prediction_info["cui"], "mention": mention,
                                                     "search_mention": prediction_info["search_mention"],
                                                     "isas_wo_process": prediction_info["isas_wo_process"],
                                                     "score": score}
        else:
            predictions[mention_info['annot_id']] = {"gold": mention_info["y_str"], "pred": prediction}
    return predictions


def get_parameters():
    parser = argparse.ArgumentParser(description='Performs Unsupervised Knowledge-Free Open Type - Ultra Fine Entity \
                                     Typing using JoBimText.')
    # among current models, best performing is the "all-mpnet-base-v2" (the date I checked: 14.07.2022)
    # https://www.sbert.net/docs/pretrained_models.html
    parser.add_argument('--model', dest='model',
                        default='all-mpnet-base-v2', 
                        type=str, help='Sentence BERT model name (default is "all-mpnet-base-v2")')
    
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
                              help='includes isas label words while creating cluster representations')
    include_isas.add_argument('--not-include-isas', dest='include_isas', action='store_false',
                              help='does not include isas label words while creating cluster representations')
    parser.set_defaults(include_isas=True)
    
    parser.add_argument('--weighted-average', default=None, type=str,
                        help='determines which weighted average methods for embeddings of cluster terms/isas will be \
                        used (default None, means that the average will not be weighted -- other options \
                        "cosine", "rank")')
    
    parser.add_argument('--number-of-isas', dest='number_of_isas', default=10, type=int,
                        help='determines how many isas label words while CREATING \
                        cluster representations (default 10)')
    
    parser.add_argument('--number-of-predictions', dest='number_of_predictions', default=10, type=int,
                        help='determines how many isas labels will be used for final PREDICTION \
                        (default 10)')
    
    parser.add_argument('--number-of-terms-in-cluster', dest='number_of_cluster_terms', default=10, type=int,
                        help='determines how many terms in sense clusters will be used  \
                        while creating/evaluating cluster representations (default 10)')
    
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
    parser.set_defaults(headword=True)
    
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
                          help='determines if a mention will be lowerized before the search in JoBimText or not')
    lowerize.add_argument('--not-lowerize', dest='lowerize', action='store_false',
                          help='determines if a mention will be lowerized before the search in JoBimText or not')
    parser.set_defaults(lowerize=False)
    
    parser.add_argument('--cluster-type', dest='cluster_type', default="200,200", type=str,
                        help='determines which type of clustering (Chinese Whisper) will be used while searching \
                        mention in JoBimText (default "200,200" -- other options "200,50", "50,50")')
    
    analyse = parser.add_mutually_exclusive_group(required=False)
    analyse.add_argument('--analyse', dest='analyse', action='store_true',
                         help='determines whether the predictions also contains detailed information \
                         for later analysis or not')
    analyse.add_argument('--not-analyse', dest='analyse', action='store_false',
                         help='determines whether the predictions also contains detailed information \
                         for later analysis or not')
    parser.set_defaults(analyse=False)
    
    include_mention_sim = parser.add_mutually_exclusive_group(required=False)
    include_mention_sim.add_argument('--include-mention-sim', dest='include_mention_sim', action='store_true',
                                     help='determines whether the similarity of mention to sense clusters will\
                                     be included or not')
    include_mention_sim.add_argument('--not-include-mention-sim', dest='include_mention_sim', action='store_false',
                                     help='determines whether the similarity of mention to sense clusters will\
                                     be included or not')
    parser.set_defaults(include_mention_sim=False)
    
    include_mention = parser.add_mutually_exclusive_group(required=False)
    include_mention.add_argument('--include-mention', dest='include_mention', action='store_true',
                                 help='determines whether mention string will be included to the context embedding\
                                 computation or not (left words + mention + right words)')
    include_mention.add_argument('--not-include-mention', dest='include_mention', action='store_false',
                                 help='determines whether mention string will be included to the context embedding\
                                 computation or not (left words + right words)')
    parser.set_defaults(include_mention=True)
    
    parser.add_argument('--output-file-path', dest='output_file_path', 
                        default='predictions_open_type_with_jobimtext.json', type=str,
                        help='determines the file path to store the predictions done by the model, \
                        that will be used later for evaluation, directly using the scorer by (Choi et al., 2018)\
                        -- https://github.com/uwnlp/open_type/blob/master/scorer.py\
                        (default is "predictions_open_type_with_jobimtext.json")')
    
    parser.add_argument('--log-file', dest='log_file', default='open_type_with_jobimtext.log', type=str,
                        help='the progress while running the script will be stored in the log file\
                        (default "open_type_with_jobimtext.log")')
    
    parser.add_argument('--args-file', dest='args_file', default='args_open_type_with_jobimtext.json', type=str,
                        help='the arguments are stored only to check (default "args_open_type_with_jobimtext.json")')
    
    # note that I did not get noisy_isas from outside, since I just removed the most common one 'thing'.
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parameters()

    # args are stored to check -- see test_open_type_et_with_jobimtext.ipynb
    with open(args.args_file, "w") as f:
        json.dump(vars(args), f)
    
    # https://docs.python.org/3/howto/logging.html
    logging.basicConfig(filename=args.log_file, format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info("Open Type - Ultra Fine Entity Typing with JoBimText is started  " + str(vars(args)))
    
    # among current models, best performing is the "all-mpnet-base-v2" (the date I checked: 14.07.2022)
    # https://www.sbert.net/docs/pretrained_models.html
    model_sentence_transformer = SentenceTransformer(args.model)
    logging.info("model is loaded")
    
    with open(args.file_path, "r") as f:
        data_lines = f.readlines()
    data_ = [json.loads(sent.strip()) for sent in data_lines]
    logging.info("data is loaded")
    
    with open(args.types_file_path, 'r') as f:
        types_lines = f.readlines()
    types_ = [type_.strip() for type_ in types_lines]
    logging.info("types file is loaded") 
    
    assert len(types_) == len(set(types_))
    
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
        
    predictions_ = get_predictions(model=model_sentence_transformer, data=data_,
                                   mention_senses_info=mention_senses_info_,
                                   number_of_predictions=args.number_of_predictions,
                                   include_mention=args.include_mention,
                                   include_mention_sim=args.include_mention_sim, analyse=args.analyse)
    
    logging.info("predictions are collected")
    
    with open(args.output_file_path, "w") as f:
        json.dump(predictions_, f)
        
    logging.info("predictions are stored in " + args.output_file_path)
    
    
