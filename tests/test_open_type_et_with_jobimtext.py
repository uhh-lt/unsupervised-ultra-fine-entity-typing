from sentence_transformers import SentenceTransformer, util
import json
import stanza
import inflect
import random
import pytest
import numpy as np
import open_type_et_with_jobimtext
import preprocess
import jobimtext_handler
from sklearn.metrics.pairwise import cosine_similarity


# https://github.com/pytest-dev/pytest/issues/3118
pytest.model = SentenceTransformer('all-mpnet-base-v2')
f = open("../open_type/release/crowd/dev.json", "r")
pytest.data = [json.loads(sent.strip()) for sent in f.readlines()]
with open('../open_type/release/ontology/types.txt', 'r') as f:
    types_lines = f.readlines()
pytest.types = [type_.strip() for type_ in types_lines]

pytest.mention_senses_info, _ = open_type_et_with_jobimtext.prepare_senses_info(model=pytest.model, data=pytest.data,
                                                                                include_isas=True,
                                                                                cluster_type="200,200",
                                                                                number_of_cluster_terms=20,
                                                                                head_word=True, n=None, first=None,
                                                                                number_of_isas=20,
                                                                                weighted_average=False,
                                                                                apply_preprocess=True,
                                                                                lower=False, apply_postprocess=True,
                                                                                noisy_isas=['thing'],
                                                                                types=pytest.types)

pytest.nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
pytest.inflect_engine = inflect.engine()
pytest.mentions_set = set([mention_info['mention_span'] for mention_info in pytest.data])
pytest.search_mentions, _ = preprocess.get_headword_of_mentions(mentions=pytest.mentions_set,
                                                                inflect_engine=pytest.inflect_engine,
                                                                nlp=pytest.nlp, apply_preprocess=True)


def test_prepare_senses_info():
    # test-1: the amount of cuis for the search mention should be equal to amounts of length of senses info
    # for this searched mention
    assert set([mention_info['mention_span'] for mention_info in pytest.data]) == set(pytest.mention_senses_info.keys())
    
    noisy_isas = ['thing']
    count = 0
    for mention in pytest.mention_senses_info:
        info = pytest.mention_senses_info[mention]
        senses_info = jobimtext_handler.get_senses_from_jobimtext(mention=info[0]['search_mention'], 
                                                                  cluster_type="200,200")
        try:
            senses = [s for s in senses_info if s['isas']]
            if not senses:
                assert len(info) == 1
                assert not info[0]['JoBimText']
                assert info[0]['isas'] == ['person']
            else:
                assert len(info) == len([s for s in senses_info if s['isas'] and [label for label in s['isas'] if not
                                                                                  label.split(':')[0] in noisy_isas]])
        except AssertionError:
            count += 1

        # all search mentions for the mention should be the same
        search_mention = info[0]['search_mention']
        for sense in info:
            assert search_mention == sense['search_mention']
    
    # the errors are due to the isas that are not in the type list
    # (or possibly the processed version is not in the type list)
    # e.g. isas: ['West End shopping district:68'] -- see open_type_et_with_jobimtext.ipynb for all.
    assert count == 43

    # test 2 - search mentions are correct based on selection
    for mention in pytest.mention_senses_info:
        info = pytest.mention_senses_info[mention]
        assert pytest.search_mentions[mention] == info[0]['search_mention']
    
    # test 3 - for no JoBimText mentions, there is really no isas from joBimText
    no_jobimtext_mentions = [mention for mention in pytest.mention_senses_info if
                             len(pytest.mention_senses_info[mention]) == 1 and
                             not pytest.mention_senses_info[mention][0]['JoBimText']]

    for mention in no_jobimtext_mentions:
        senses_info = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                  cluster_type="200,200")
        # either no results or no isas in any sense
        try:
            assert not senses_info
        except AssertionError:
            assert not [label for sense in senses_info for label in sense['isas']]
        
    # test 4 - isas info matches: choose randomly mentions and check
    # https://docs.python.org/3/library/random.html
    # In the future, the population must be a sequence. Instances of set are no longer supported...
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=100)
    skipped = 0
    for mention in sample_mentions:
        senses_info_from_jobimtext = jobimtext_handler.get_senses_from_jobimtext(
            mention=pytest.search_mentions[mention], cluster_type="200,200")

        senses_info_from_function = pytest.mention_senses_info[mention]
        if len(senses_info_from_function) == 1 and not senses_info_from_function[0]['JoBimText']:
            skipped += 1
            continue
        for sense in senses_info_from_function:
            sense_jobimtext = [s for s in senses_info_from_jobimtext if s['cui'] == sense['cui']][0]
            assert [label.split(':')[0] for label in sense_jobimtext['isas']] == sense['isas_wo_process']

            _, processed_isas = jobimtext_handler.process_jobimtext_result(result=sense_jobimtext, 
                                                                           number_of_cluster_terms=20, 
                                                                           number_of_isas=20, apply_postprocess=True, 
                                                                           nlp=pytest.nlp,
                                                                           inflect_engine=pytest.inflect_engine,
                                                                           types=pytest.types, noisy_isas=['thing'])
            assert processed_isas == sense['isas']
    assert skipped < 10 
    
    # test 5 - randomly select some mentions and compute sense embedding information and check they are all the same.
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=100)
    skipped = 0
    for mention in sample_mentions:
        senses_info_from_jobimtext = jobimtext_handler.get_senses_from_jobimtext(
            mention=pytest.search_mentions[mention], cluster_type="200,200")

        senses_info_from_function = pytest.mention_senses_info[mention]
        if len(senses_info_from_function) == 1 and not senses_info_from_function[0]['JoBimText']:
            skipped += 1
            continue
        for sense in senses_info_from_function:
            sense_jobimtext = [s for s in senses_info_from_jobimtext if s['cui'] == sense['cui']][0]

            processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(
                result=sense_jobimtext, number_of_cluster_terms=20, number_of_isas=20, apply_postprocess=True,
                nlp=pytest.nlp, inflect_engine=pytest.inflect_engine, types=pytest.types, noisy_isas=['thing'])
            processed_senses.extend(processed_isas)
            embed = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, 
                                                                         senses=processed_senses, 
                                                                         weighted=False, weights=None, mention=mention)
            assert np.array_equal(sense['sense_embedding'], embed)

    assert skipped < 10   
    

def test_generate_sense_embedding():    
    # test 1 - model.encode(senses) --> check it is the same by doing iteratively one by one
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine,
                                                                      types=pytest.types,
                                                                      noisy_isas=['thing'])

            senses.extend(isas)
            encoded = pytest.model.encode(senses)
            for index, sense in enumerate(senses):
                # np.array_equal did not work, since when encoded all and
                # individually the results are not always the same,
                # but at worst two digits are the same always
                encode_sense = pytest.model.encode(sense)
                for j in range(len(encode_sense)):
                    assert round(encoded[index][j], 2) == round(encode_sense[j], 2)
                    
    # test 2 - check with np.mean(word_embedding_avg_collective, axis=0 .. --> 
    # https://github.com/sdimi/average-word2vec/blob/master/avg_word2vec_from_documents.py
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            senses.extend(isas)

            representations = pytest.model.encode(senses)
            np.array_equal(np.mean(representations, axis=0), np.average(a=representations, axis=0))
            # check by just sum and divide by n
            avg = np.average(a=representations, axis=0)
            for dim in range(768):
                sums = sum([embed[dim] for embed in representations])
                assert round(sums/len(representations), 3).astype('float32') == round(avg[dim], 3)

    # test 3 - with average and without average and outside average check
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            senses.extend(isas)

            embed_func = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses,
                                                                              weighted=False, weights=None,
                                                                              mention=None)
            assert np.array_equal(np.average(a=pytest.model.encode(senses), axis=0), embed_func)

    # test 4: if weights are all equal, the results with weights and w/o it should be the same.
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            senses.extend(isas)

            weights = [1/len(senses) for _ in senses]
            embed_with_weights = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses, 
                                                                                      weighted=True, weights=weights, 
                                                                                      mention=None)

            embed_wo_weights = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses, 
                                                                                    weighted=False, weights=None, 
                                                                                    mention=None)
            
            # did not work with assert np.array_equal(embed_with_weights, embed_wo_weights)
            # but the difference is small
            assert np.allclose(embed_with_weights, embed_wo_weights, rtol=1e-05)
    
    # test 5: with some random weight and check externally
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            senses.extend(isas)
            weights = [random.randint(1, 10) for _ in senses]
            embed_with_weights = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses, 
                                                                                      weighted=True, weights=weights, 
                                                                                      mention=None)

            representations = pytest.model.encode(senses)
            total_weights = sum(weights)
            for dim in range(768):
                sums = sum([weights[index]*embed[dim] for index, embed in enumerate(representations)])
                assert round(sums/total_weights, 3) == round(embed_with_weights[dim], 3)

    # test 6: with mention similarity and w/o it, check with external
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=50)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            senses.extend(isas)
            mention_rep = pytest.model.encode(mention)
            representations = pytest.model.encode(senses)
            weights = [cosine_similarity(mention_rep.reshape(1, -1), rep.reshape(1, -1))[0][0]
                       for rep in representations]

            embed_with_weights = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses, 
                                                                                      weighted=True, weights=weights, 
                                                                                      mention=None)

            embed_wo_weights = open_type_et_with_jobimtext.generate_sense_embedding(model=pytest.model, senses=senses, 
                                                                                    weighted=True, weights=None, 
                                                                                    mention=mention)

            assert np.array_equal(embed_with_weights, embed_wo_weights)
            total_weights = sum(weights)
            for dim in range(768):
                sums = sum([weights[index]*embed[dim] for index, embed in enumerate(representations)])
                assert round(sums/total_weights, 3).astype('float32') == round(embed_with_weights[dim], 3)
                
                
def test_compute_weight_by_rank():
    # test 1 - lengths should be the same --> the input and output
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=100)

    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])

            weights = open_type_et_with_jobimtext.compute_weight_by_rank(sense_terms=senses, isas=isas)
            assert len(weights) == len(senses) + len(isas)
            
    # test 2 - randomly select some and check it with its order (should be the same as 1/order)
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=100)
    count = 0
    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])
            if len(senses) > 0 and len(isas) > 0:
                weights = open_type_et_with_jobimtext.compute_weight_by_rank(sense_terms=senses, isas=isas)
                sample_sense = random.randint(0, len(senses)-1)
                assert weights[sample_sense] == 1/(sample_sense+1) 
                sample_isas = random.randint(0, len(isas)-1)
                assert weights[len(senses)+sample_isas] == 1/(sample_isas+1) 
            else:
                count += 1
    assert count < 20
    
    # test 3 - the output weights should be in decreasing order
    sample_mentions = random.sample(population=list(pytest.mentions_set), k=100)
    count = 0
    for mention in sample_mentions:
        responses = jobimtext_handler.get_senses_from_jobimtext(mention=pytest.search_mentions[mention], 
                                                                cluster_type="200,200")
        if len(responses) > 1:
            sample_cui = random.randint(0, len(responses)-1)
            senses, isas = jobimtext_handler.process_jobimtext_result(result=responses[sample_cui], 
                                                                      number_of_cluster_terms=20, number_of_isas=20, 
                                                                      apply_postprocess=True, nlp=pytest.nlp, 
                                                                      inflect_engine=pytest.inflect_engine, 
                                                                      types=pytest.types, 
                                                                      noisy_isas=['thing'])
            if len(senses) > 0 and len(isas) > 0:
                weights = open_type_et_with_jobimtext.compute_weight_by_rank(sense_terms=senses, isas=isas)
                weights_senses = weights[:len(senses)]
                assert np.array_equal(sorted(weights_senses, reverse=True), weights_senses)
                weights_isas = weights[len(senses):]
                assert np.array_equal(sorted(weights_isas, reverse=True), weights_isas)
            else:
                count += 1
    assert count < 20
    
    
def test_find_highest_similar():
    # test 1 - cosine with the sentence embeddings' util.cos_sim
    # https://www.sbert.net/docs/usage/semantic_textual_similarity.html
    sample_data = random.sample(population=pytest.data, k=100)
    count = 0
    
    for mention_info in sample_data:
        sense_info = pytest.mention_senses_info[mention_info['mention_span']]

        if len(sense_info) > 1:
            left_context = ' '.join(mention_info["left_context_token"])
            mention = mention_info["mention_span"]
            right_context = ' '.join(mention_info["right_context_token"])
            context = left_context + ' ' + mention + ' ' + right_context
            context_embed = pytest.model.encode(context)

            ranked_senses = open_type_et_with_jobimtext.find_highest_similar(context_embed=context_embed, 
                                                                             senses_info=sense_info, mention_embed=None)
            
            # with mention 
            mention_embed = pytest.model.encode(mention)
            ranked_senses_document, ranked_senses_with_mention = open_type_et_with_jobimtext.find_highest_similar(
                                                                                            context_embed=context_embed, 
                                                                                            senses_info=sense_info,
                                                                                            mention_embed=mention_embed)

            assert ranked_senses_document == ranked_senses
            for sense in ranked_senses:
                s_info = [info for info in sense_info if info['cui'] == sense['cui']]
                assert len(s_info) == 1
                s_info = s_info[0]
                assert round(float(sense['score']), 3) == round(float(util.cos_sim(context_embed, 
                                                                                   s_info['sense_embedding'])), 3)
                assert sense['score'] == cosine_similarity(context_embed.reshape(1, -1),
                                                           s_info['sense_embedding'].reshape(1, -1))[0][0]

            for sense in ranked_senses_with_mention:
                s_info = [info for info in sense_info if info['cui'] == sense['cui']]
                assert len(s_info) == 1
                s_info = s_info[0]
                assert round(float(sense['score']), 3) == round((float(util.cos_sim(context_embed,
                                                                                    s_info['sense_embedding']))
                                                                 + float(util.cos_sim(mention_embed, 
                                                                                      s_info['sense_embedding'])))/2, 3)
                sim = (cosine_similarity(context_embed.reshape(1, -1), s_info['sense_embedding'].reshape(1, -1))[0][0] +
                       cosine_similarity(mention_embed.reshape(1, -1),
                                         s_info['sense_embedding'].reshape(1, -1))[0][0])/2
                assert sense['score'] == sim
        else:
            count += 1
    assert count < 20

    # test 2 - all returned info should be the same as send
    sample_data = random.sample(population=pytest.data, k=100)
    for mention_info in sample_data:
        sense_info = pytest.mention_senses_info[mention_info['mention_span']]

        if len(sense_info) > 1:
            left_context = ' '.join(mention_info["left_context_token"])
            mention = mention_info["mention_span"]
            right_context = ' '.join(mention_info["right_context_token"])
            context = left_context + ' ' + mention + ' ' + right_context
            context_embed = pytest.model.encode(context)

            ranked_senses = open_type_et_with_jobimtext.find_highest_similar(context_embed=context_embed, 
                                                                             senses_info=sense_info, mention_embed=None)

            # with mention 
            mention_embed = pytest.model.encode(mention)
            ranked_senses_document, ranked_senses_with_mention = open_type_et_with_jobimtext.find_highest_similar(
                                                                                            context_embed=context_embed, 
                                                                                            senses_info=sense_info,
                                                                                            mention_embed=mention_embed)
            assert ranked_senses_document == ranked_senses

            for sense in ranked_senses:
                s_info = [info for info in sense_info if info['cui'] == sense['cui']]
                assert len(s_info) == 1
                s_info = s_info[0]
                assert s_info['isas'] == sense['isas']
                assert s_info['search_mention'] == sense['search_mention']
                assert s_info['isas_wo_process'] == sense['isas_wo_process']
                assert s_info['JoBimText'] == sense['JoBimText']

            for sense in ranked_senses_with_mention:
                s_info = [info for info in sense_info if info['cui'] == sense['cui']]
                assert len(s_info) == 1
                s_info = s_info[0]
                assert s_info['isas'] == sense['isas']
                assert s_info['search_mention'] == sense['search_mention']
                assert s_info['isas_wo_process'] == sense['isas_wo_process']
                assert s_info['JoBimText'] == sense['JoBimText']

    # test 3 - all returned scores should be in decreasing order
    sample_data = random.sample(population=pytest.data, k=100)
    for mention_info in sample_data:
        sense_info = pytest.mention_senses_info[mention_info['mention_span']]

        if len(sense_info) > 1:
            left_context = ' '.join(mention_info["left_context_token"])
            mention = mention_info["mention_span"]
            right_context = ' '.join(mention_info["right_context_token"])
            context = left_context + ' ' + mention + ' ' + right_context
            context_embed = pytest.model.encode(context)

            ranked_senses = open_type_et_with_jobimtext.find_highest_similar(context_embed=context_embed, 
                                                                             senses_info=sense_info, mention_embed=None)

            # with mention 
            mention_embed = pytest.model.encode(mention)
            ranked_senses_document, ranked_senses_with_mention = open_type_et_with_jobimtext.find_highest_similar(
                                                                                            context_embed=context_embed, 
                                                                                            senses_info=sense_info,
                                                                                            mention_embed=mention_embed)
            assert ranked_senses_document == ranked_senses
            for index, sense in enumerate(ranked_senses):
                previous_score = sense['score']
                for index_j in range(index, len(ranked_senses)):
                    sense_j = ranked_senses[index_j]
                    assert sense_j['score'] <= previous_score

            # test with sort
            scores_check = ranked_senses.copy()
            scores_check.sort(key=lambda p: p['score'], reverse=True)
            assert scores_check == ranked_senses

            scores_check2 = [s['score'] for s in ranked_senses]
            for i in range(len(scores_check2)):
                for j in range(len(scores_check2)):
                    if i < j:
                        assert scores_check2[i] >= scores_check2[j]

            # -- with mention
            for index, sense in enumerate(ranked_senses_with_mention):
                previous_score = sense['score']
                for index_j in range(index, len(ranked_senses_with_mention)):
                    sense_j = ranked_senses_with_mention[index_j]
                    assert sense_j['score'] <= previous_score

            # test with sort
            scores_check = ranked_senses_with_mention.copy()
            scores_check.sort(key=lambda p: p['score'], reverse=True)
            assert scores_check == ranked_senses_with_mention

            scores_check2 = [s['score'] for s in ranked_senses_with_mention]
            for i in range(len(scores_check2)):
                for j in range(len(scores_check2)):
                    if i < j:
                        assert scores_check2[i] >= scores_check2[j]
