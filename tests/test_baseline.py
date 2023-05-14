import random
import stanza
import inflect
import pytest
import json
import baseline
import jobimtext_handler
import preprocess
import open_type_et_with_jobimtext
from sentence_transformers import SentenceTransformer


# https://github.com/pytest-dev/pytest/issues/3118
pytest.model = SentenceTransformer('all-mpnet-base-v2')
f = open("../open_type/release/crowd/dev.json", "r")
pytest.data = [json.loads(sent.strip()) for sent in f.readlines()]
with open("../open_type/release/ontology/types.txt", 'r') as f:
    types_lines = f.readlines()
pytest.types = [type_.strip() for type_ in types_lines]
pytest.mention_senses_info, pytest.count_no_results = open_type_et_with_jobimtext.prepare_senses_info(
    model=pytest.model, data=pytest.data, include_isas=True, cluster_type="200,200", number_of_cluster_terms=20,
    head_word=True, n=None, first=None, number_of_isas=20, weighted_average=False, apply_preprocess=True, 
    lower=False, apply_postprocess=True, noisy_isas=['thing'], types=pytest.types)


def test_baseline_first_cluster():
    # test if the results are really matching with the first result
    samples_for_check = random.sample(population=pytest.data, k=200)
    number_of_predictions = 10
    predictions_first = baseline.baseline_first_cluster(data=pytest.data, 
                                                        mention_senses_info=pytest.mention_senses_info, 
                                                        number_of_predictions=number_of_predictions)

    count_not_checked = 0
    inflect_engine = inflect.engine()
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    mentions = set([mention_info["mention_span"] for mention_info in pytest.data])
    search_mentions, _ = preprocess.get_headword_of_mentions(mentions=mentions, inflect_engine=inflect_engine, 
                                                             nlp=nlp, apply_preprocess=True)

    for mention_info in samples_for_check:
        search_mention = search_mentions[mention_info['mention_span']]
        results = jobimtext_handler.get_senses_from_jobimtext(mention=search_mention, 
                                                              cluster_type="200,200")

        if results:
            # sometimes although there are senses, there are no isas, like "you", to catch them, I put flag
            senses, isas = jobimtext_handler.process_jobimtext_result(result=results[0],
                                                                      number_of_cluster_terms=20,
                                                                      number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=nlp, 
                                                                      inflect_engine=inflect_engine, 
                                                                      noisy_isas=['thing'],
                                                                      types=pytest.types)

            if senses and isas and len(senses) > 0 and len(isas) > 0:
                assert predictions_first[mention_info['annot_id']]['pred'] == isas[:number_of_predictions]
            else:
                count_not_checked += 1
        else:
            count_not_checked += 1
    
    # count_not_checked is either for no results or no isas/terms in the first cluster       
    assert count_not_checked < 50
    
    
def test_baseline_random_cluster():
    # test the final predictions should be in one of the clusters for the mention.
    samples_for_check = random.sample(population=pytest.data, k=200)
    
    number_of_predictions = 10
    predictions_random = baseline.baseline_random_cluster(data=pytest.data, 
                                                          mention_senses_info=pytest.mention_senses_info, 
                                                          number_of_predictions=number_of_predictions)
    
    count_not_checked = 0
    inflect_engine = inflect.engine()
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    mentions = set([mention_info["mention_span"] for mention_info in pytest.data])
    search_mentions, _ = preprocess.get_headword_of_mentions(mentions=mentions, inflect_engine=inflect_engine, 
                                                             nlp=nlp, apply_preprocess=True)

    for mention_info in samples_for_check:
        search_mention = search_mentions[mention_info['mention_span']]
        results = jobimtext_handler.get_senses_from_jobimtext(mention=search_mention, 
                                                              cluster_type="200,200")
        clusters_isas = []
        if results:
            # sometimes although there are senses, there are no isas, like "you", to catch them, I put flag
            flag = False
            for result in results:
                senses, isas = jobimtext_handler.process_jobimtext_result(result=result,
                                                                          number_of_cluster_terms=20,
                                                                          number_of_isas=20, 
                                                                          apply_postprocess=True, nlp=nlp, 
                                                                          inflect_engine=inflect_engine, 
                                                                          noisy_isas=['thing'],
                                                                          types=pytest.types)

                if senses and isas and len(senses) > 0 and len(isas) > 0:
                    flag = True
                    clusters_isas.append(isas[:number_of_predictions])
            if flag:
                assert predictions_random[mention_info['annot_id']]['pred'] in clusters_isas
            else:
                count_not_checked += 1
        else:
            count_not_checked += 1
    
    # count_not_checked is either for no results or no isas/terms
    assert count_not_checked < 50  
