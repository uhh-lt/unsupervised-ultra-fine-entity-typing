import preprocess
from string import punctuation
import json
import stanza
import inflect
import pytest


basic_mentions = ['the building , a violation of the Clean Air Act',  # comma at the beginning
                  'a club playing in the Fourth National division',  # a/an/the
                  'an English football player and manager',  # a/an/the
                  'terms of its righteousness', 
                  # from mention error analysis -- file:///Users/ozge/Downloads/mention_analysis_29092022_200_dev.html
                  # terms of .. cannot be singularized
                  'a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England', 
                  # comma at the beginning
                  "the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-",  # -LRB-, -RRB-, at the end
                  'present Erwin Arnada -- now at large --',  # check --
                  "the percentage of Americans who do `` real exercise to build the heart ''",  # check ''
                  'the sound `` I Can See Clearly Now',  # the original mention is
                  # 'the sound of `` I Can See Clearly Now' removed 'of' to check ``
                  "Paul Gauguin -LRB- also known as Lilas -RRB-"  # the original mention is "Paul Gauguin 's
                  # Vase de Fleurs -LRB- also known as Lilas -RRB-" removed "'s Vase de Fleurs" to check '-LRB-'
                  ]
# multiple_head_mentions found in 'test_preprocess.ipynb'
multiple_head_mentions = ['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver',
                          'Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,',
                          'the O.J . Simpson trial']

# selected random 20 samples to test in 'test_preprocess.ipynb'
mentions_sample_20 = ['a power-sharing administration', 'many years', 'support', 'some strongholds',
                      'the nearby village of Livenka', 'Small car makers', 'Thursday', 'new areas',
                      'His large scale sculpture', 'an East German border town',
                      'Latin America , Africa , and the South Pacific', 'Eusebius',
                      'tribal leaders and other activists',
                      'The main event', 'Michael',
                      'Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox',
                      'Multinationals', 'the concept', 'Friday prayers', 'Algeria']

# https://github.com/pytest-dev/pytest/issues/3118
test_total_mentions = basic_mentions + mentions_sample_20 + multiple_head_mentions
pytest.test_mentions = test_total_mentions


def test_get_first_ngram_of_mentions():
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    mentions_ = [mention_info['mention_span'] for mention_info in dev_data]
    mentions = set(mentions_)
    
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    inflect_engine = inflect.engine()
    
    # test-1: if len(mention.split()) == 1: search_token == mention
    processed_mentions_n1 = preprocess.get_first_ngram_of_mentions(mentions=mentions, 
                                                                   n=1, inflect_engine=inflect_engine, 
                                                                   nlp=nlp, apply_preprocess=False)

    processed_mentions_n2 = preprocess.get_first_ngram_of_mentions(mentions=mentions, 
                                                                   n=2, inflect_engine=inflect_engine, 
                                                                   nlp=nlp, apply_preprocess=False)

    processed_mentions_n3 = preprocess.get_first_ngram_of_mentions(mentions=mentions, 
                                                                   n=3, inflect_engine=inflect_engine, 
                                                                   nlp=nlp, apply_preprocess=False)
    checked = 0
    for mention in mentions:
        if len(mention.split()) == 1:
            assert processed_mentions_n1[mention] == mention
            assert processed_mentions_n2[mention] == mention
            assert processed_mentions_n3[mention] == mention
            checked += 1
    # be sure some mentions are checked
    assert checked == 232
    
    # test-2: try w/o apply_preprocess and call preprocess after for each mention. 
    # check the diff if apply_preprocess=True, they should be the same
    processed_mentions_n1_prepro = preprocess.get_first_ngram_of_mentions(mentions=mentions, n=1, 
                                                                          inflect_engine=inflect_engine, 
                                                                          nlp=nlp, apply_preprocess=True)

    processed_mentions_n2_prepro = preprocess.get_first_ngram_of_mentions(mentions=mentions, n=2, 
                                                                          inflect_engine=inflect_engine, 
                                                                          nlp=nlp, apply_preprocess=True)

    processed_mentions_n3_prepro = preprocess.get_first_ngram_of_mentions(mentions=mentions, n=3, 
                                                                          inflect_engine=inflect_engine, 
                                                                          nlp=nlp, apply_preprocess=True)

    for mention in mentions:
        search_token_n1 = processed_mentions_n1[mention]
        singularized_token_n1 = preprocess.preprocess(mention=search_token_n1, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n1_prepro[mention] == singularized_token_n1

        search_token_n2 = processed_mentions_n2[mention]
        singularized_token_n2 = preprocess.preprocess(mention=search_token_n2, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n2_prepro[mention] == singularized_token_n2

        search_token_n3 = processed_mentions_n3[mention]
        singularized_token_n3 = preprocess.preprocess(mention=search_token_n3, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n3_prepro[mention] == singularized_token_n3

    # test-3: the final tokens should be in the mention
    for mention in mentions:
        filter_list = [item for item in punctuation]
        filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
        mention_ = ' '.join([token for token in mention.split() if token not in filter_list])

        assert processed_mentions_n1[mention] in mention_
        assert processed_mentions_n2[mention] in mention_
        assert processed_mentions_n3[mention] in mention_
    #     for prepro -- ('leaf', 'leaves') or ('their life', 'their lives')
    #     assert processed_mentions_n1_prepro[mention] in mention_
    #     assert processed_mentions_n2_prepro[mention] in mention_
    #     assert processed_mentions_n3_prepro[mention] in mention_

    # test-4 test with manual check: some selected ones and some random ones.
    first_n1 = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=1,
                                                      inflect_engine=inflect_engine, nlp=nlp,
                                                      apply_preprocess=False)
    first_n1_prep = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=1,
                                                           inflect_engine=inflect_engine, nlp=nlp,
                                                           apply_preprocess=True)

    first_n2 = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=2,
                                                      inflect_engine=inflect_engine, nlp=nlp,
                                                      apply_preprocess=False)
    first_n2_prep = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=2,
                                                           inflect_engine=inflect_engine, nlp=nlp,
                                                           apply_preprocess=True)

    first_n3 = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=3,
                                                      inflect_engine=inflect_engine, nlp=nlp,
                                                      apply_preprocess=False)
    first_n3_prep = preprocess.get_first_ngram_of_mentions(mentions=pytest.test_mentions, n=3,
                                                           inflect_engine=inflect_engine, nlp=nlp,
                                                           apply_preprocess=True)

    assert first_n1['a power-sharing administration'] == 'power-sharing'
    assert first_n1_prep['a power-sharing administration'] == 'power-sharing'
    assert first_n2['a power-sharing administration'] == 'a power-sharing'
    assert first_n2_prep['a power-sharing administration'] == 'a power-sharing'
    assert first_n3['a power-sharing administration'] == 'a power-sharing administration'
    assert first_n3_prep['a power-sharing administration'] == 'a power-sharing administration'

    assert first_n1['many years'] == 'many'
    assert first_n1_prep['many years'] == 'many'
    assert first_n2['many years'] == 'many years'
    assert first_n2_prep['many years'] == 'many year'
    assert first_n3['many years'] == 'many years'
    assert first_n3_prep['many years'] == 'many year'

    assert first_n1['support'] == 'support'
    assert first_n1_prep['support'] == 'support'
    assert first_n2['support'] == 'support'
    assert first_n2_prep['support'] == 'support'
    assert first_n3['support'] == 'support'
    assert first_n3_prep['support'] == 'support'

    assert first_n1['some strongholds'] == 'some'
    assert first_n1_prep['some strongholds'] == 'some'
    assert first_n2['some strongholds'] == 'some strongholds'
    assert first_n2_prep['some strongholds'] == 'some stronghold'
    assert first_n3['some strongholds'] == 'some strongholds'
    assert first_n3_prep['some strongholds'] == 'some stronghold'

    assert first_n1['the nearby village of Livenka'] == 'nearby'
    assert first_n1_prep['the nearby village of Livenka'] == 'nearby'
    assert first_n2['the nearby village of Livenka'] == 'the nearby'
    assert first_n2_prep['the nearby village of Livenka'] == 'the nearby'
    assert first_n3['the nearby village of Livenka'] == 'the nearby village'
    assert first_n3_prep['the nearby village of Livenka'] == 'the nearby village'

    assert first_n1['Small car makers'] == 'Small'
    assert first_n1_prep['Small car makers'] == 'Small'
    assert first_n2['Small car makers'] == 'Small car'
    assert first_n2_prep['Small car makers'] == 'Small car'
    assert first_n3['Small car makers'] == 'Small car makers'
    assert first_n3_prep['Small car makers'] == 'Small car maker'

    assert first_n1['Thursday'] == 'Thursday'
    assert first_n1_prep['Thursday'] == 'Thursday'
    assert first_n2['Thursday'] == 'Thursday'
    assert first_n2_prep['Thursday'] == 'Thursday'
    assert first_n3['Thursday'] == 'Thursday'
    assert first_n3_prep['Thursday'] == 'Thursday'

    assert first_n1['new areas'] == 'new'
    assert first_n1_prep['new areas'] == 'new'
    assert first_n2['new areas'] == 'new areas'
    assert first_n2_prep['new areas'] == 'new area'
    assert first_n3['new areas'] == 'new areas'
    assert first_n3_prep['new areas'] == 'new area'

    assert first_n1['His large scale sculpture'] == 'His'
    assert first_n1_prep['His large scale sculpture'] == 'His'
    assert first_n2['His large scale sculpture'] == 'His large'
    assert first_n2_prep['His large scale sculpture'] == 'His large'
    assert first_n3['His large scale sculpture'] == 'His large scale'
    assert first_n3_prep['His large scale sculpture'] == 'His large scale'

    assert first_n1['an East German border town'] == 'East'
    assert first_n1_prep['an East German border town'] == 'East'
    assert first_n2['an East German border town'] == 'an East'
    assert first_n2_prep['an East German border town'] == 'an East'
    assert first_n3['an East German border town'] == 'an East German'
    assert first_n3_prep['an East German border town'] == 'an East German'

    assert first_n1['Latin America , Africa , and the South Pacific'] == 'Latin'
    assert first_n1_prep['Latin America , Africa , and the South Pacific'] == 'Latin'
    assert first_n2['Latin America , Africa , and the South Pacific'] == 'Latin America'
    assert first_n2_prep['Latin America , Africa , and the South Pacific'] == 'Latin America'
    assert first_n3['Latin America , Africa , and the South Pacific'] == 'Latin America Africa'
    assert first_n3_prep['Latin America , Africa , and the South Pacific'] == 'Latin America Africa'

    assert first_n1['Eusebius'] == 'Eusebius'
    assert first_n1_prep['Eusebius'] == 'Eusebius'
    assert first_n2['Eusebius'] == 'Eusebius'
    assert first_n2_prep['Eusebius'] == 'Eusebius'
    assert first_n3['Eusebius'] == 'Eusebius'
    assert first_n3_prep['Eusebius'] == 'Eusebius'

    # note this one
    assert first_n1['tribal leaders and other activists'] == 'tribal'
    assert first_n1_prep['tribal leaders and other activists'] == 'tribal'
    assert first_n2['tribal leaders and other activists'] == 'tribal leaders'
    assert first_n2_prep['tribal leaders and other activists'] == 'tribal leader'
    assert first_n3['tribal leaders and other activists'] == 'tribal leaders and'
    assert first_n3_prep['tribal leaders and other activists'] == 'tribal leaders and'  # ?

    assert first_n1['The main event'] == 'main'
    assert first_n1_prep['The main event'] == 'main'
    assert first_n2['The main event'] == 'The main'
    assert first_n2_prep['The main event'] == 'The main'
    assert first_n3['The main event'] == 'The main event'
    assert first_n3_prep['The main event'] == 'The main event'

    assert first_n1['Michael'] == 'Michael'
    assert first_n1_prep['Michael'] == 'Michael'
    assert first_n2['Michael'] == 'Michael'
    assert first_n2_prep['Michael'] == 'Michael'
    assert first_n3['Michael'] == 'Michael'
    assert first_n3_prep['Michael'] == 'Michael'

    assert first_n1['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'
    assert first_n1_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'
    assert first_n2['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette'
    assert first_n2_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette'
    assert first_n3['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette Rod'
    assert first_n3_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette Rod'

    assert first_n1['Multinationals'] == 'Multinationals'
    assert first_n1_prep['Multinationals'] == 'Multinational'
    assert first_n2['Multinationals'] == 'Multinationals'
    assert first_n2_prep['Multinationals'] == 'Multinational'
    assert first_n3['Multinationals'] == 'Multinationals'
    assert first_n3_prep['Multinationals'] == 'Multinational'

    assert first_n1['the concept'] == 'concept'
    assert first_n1_prep['the concept'] == 'concept'
    assert first_n2['the concept'] == 'the concept'
    assert first_n2_prep['the concept'] == 'the concept'
    assert first_n3['the concept'] == 'the concept'
    assert first_n3_prep['the concept'] == 'the concept'

    assert first_n1['Friday prayers'] == 'Friday'
    assert first_n1_prep['Friday prayers'] == 'Friday'
    assert first_n2['Friday prayers'] == 'Friday prayers'
    assert first_n2_prep['Friday prayers'] == 'Friday prayer'
    assert first_n3['Friday prayers'] == 'Friday prayers'
    assert first_n3_prep['Friday prayers'] == 'Friday prayer'

    assert first_n1['Algeria'] == 'Algeria'
    assert first_n1_prep['Algeria'] == 'Algeria'
    assert first_n2['Algeria'] == 'Algeria'
    assert first_n2_prep['Algeria'] == 'Algeria'
    assert first_n3['Algeria'] == 'Algeria'
    assert first_n3_prep['Algeria'] == 'Algeria'

    ########################
    assert first_n1['the building , a violation of the Clean Air Act'] == 'building'
    assert first_n1_prep['the building , a violation of the Clean Air Act'] == 'building'
    assert first_n2['the building , a violation of the Clean Air Act'] == 'the building'
    assert first_n2_prep['the building , a violation of the Clean Air Act'] == 'the building'
    assert first_n3['the building , a violation of the Clean Air Act'] == 'the building a'
    assert first_n3_prep['the building , a violation of the Clean Air Act'] == 'the building a'

    assert first_n1['a club playing in the Fourth National division'] == 'club'
    assert first_n1_prep['a club playing in the Fourth National division'] == 'club'
    assert first_n2['a club playing in the Fourth National division'] == 'a club'
    assert first_n2_prep['a club playing in the Fourth National division'] == 'a club'
    assert first_n3['a club playing in the Fourth National division'] == 'a club playing'
    assert first_n3_prep['a club playing in the Fourth National division'] == 'a club playing'

    assert first_n1['an English football player and manager'] == 'English'
    assert first_n1_prep['an English football player and manager'] == 'English'
    assert first_n2['an English football player and manager'] == 'an English'
    assert first_n2_prep['an English football player and manager'] == 'an English'
    assert first_n3['an English football player and manager'] == 'an English football'
    assert first_n3_prep['an English football player and manager'] == 'an English football'

    assert first_n1['terms of its righteousness'] == 'terms'
    assert first_n1_prep['terms of its righteousness'] == 'term'
    assert first_n2['terms of its righteousness'] == 'terms of'
    assert first_n2_prep['terms of its righteousness'] == 'terms of'  # note this one
    assert first_n3['terms of its righteousness'] == 'terms of its'
    assert first_n3_prep['terms of its righteousness'] == 'terms of its'  # note this one

    assert first_n1['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish'
    assert first_n1_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish'
    assert first_n2['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'a parish'
    assert first_n2_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'a parish'
    assert first_n3['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'a parish church'
    assert first_n3_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'a parish church'

    assert first_n1["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'settlement'
    assert first_n1_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'settlement'
    assert first_n2["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement'
    assert first_n2_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement'
    assert first_n3["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement Tubabodaga'
    assert first_n3_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement Tubabodaga'

    assert first_n1['present Erwin Arnada -- now at large --'] == 'present'
    assert first_n1_prep['present Erwin Arnada -- now at large --'] == 'present'
    assert first_n2['present Erwin Arnada -- now at large --'] == 'present Erwin'
    assert first_n2_prep['present Erwin Arnada -- now at large --'] == 'present Erwin'
    assert first_n3['present Erwin Arnada -- now at large --'] == 'present Erwin Arnada'
    assert first_n3_prep['present Erwin Arnada -- now at large --'] == 'present Erwin Arnada'

    assert first_n1["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'
    assert first_n1_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'
    assert first_n2["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage'
    assert first_n2_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage'
    assert first_n3["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage of'
    assert first_n3_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage of'

    assert first_n1['the sound `` I Can See Clearly Now'] == 'sound'
    assert first_n1_prep['the sound `` I Can See Clearly Now'] == 'sound'
    assert first_n2['the sound `` I Can See Clearly Now'] == 'the sound'
    assert first_n2_prep['the sound `` I Can See Clearly Now'] == 'the sound'
    assert first_n3['the sound `` I Can See Clearly Now'] == 'the sound I'
    assert first_n3_prep['the sound `` I Can See Clearly Now'] == 'the sound I'

    assert first_n1['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'
    assert first_n1_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'
    assert first_n2['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin'
    assert first_n2_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin'
    assert first_n3['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin also'
    assert first_n3_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin also'

    assert first_n1['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front'
    assert first_n1_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front'
    assert first_n2['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line'
    assert first_n2_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line'
    assert first_n3['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line member'
    assert first_n3_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line member'

    assert first_n1['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'
    assert first_n1_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'
    assert first_n2['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of'
    assert first_n2_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of'
    assert first_n3['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of Dominica'
    assert first_n3_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of Dominica'

    assert first_n1['the O.J . Simpson trial'] == 'O.J'
    assert first_n1_prep['the O.J . Simpson trial'] == 'O.J'
    assert first_n2['the O.J . Simpson trial'] == 'the O.J'
    assert first_n2_prep['the O.J . Simpson trial'] == 'the O.J'
    assert first_n3['the O.J . Simpson trial'] == 'the O.J Simpson'
    assert first_n3_prep['the O.J . Simpson trial'] == 'the O.J Simpson'
    
    
def test_get_last_ngram_of_mentions():
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    mentions_ = [mention_info['mention_span'] for mention_info in dev_data]
    mentions = set(mentions_)
    
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    inflect_engine = inflect.engine()
    
    # test-1: if len(mention.split()) == 1: search_token == mention
    processed_mentions_n1_last = preprocess.get_last_ngram_of_mentions(mentions=mentions, 
                                                                       n=1, inflect_engine=inflect_engine, 
                                                                       nlp=nlp, apply_preprocess=False)

    processed_mentions_n2_last = preprocess.get_last_ngram_of_mentions(mentions=mentions, 
                                                                       n=2, inflect_engine=inflect_engine, 
                                                                       nlp=nlp, apply_preprocess=False)

    processed_mentions_n3_last = preprocess.get_last_ngram_of_mentions(mentions=mentions, 
                                                                       n=3, inflect_engine=inflect_engine, 
                                                                       nlp=nlp, apply_preprocess=False)
    checked = 0
    for mention in mentions:
        if len(mention.split()) == 1:
            assert processed_mentions_n1_last[mention] == mention
            assert processed_mentions_n2_last[mention] == mention
            assert processed_mentions_n3_last[mention] == mention
            checked += 1
    # be sure some mentions are checked
    assert checked == 232
    
    # test-2: try w/o apply_preprocess and call preprocess after for each mention. 
    # check the diff if apply_preprocess=True, they should be the same
    processed_mentions_n1_last_prepro = preprocess.get_last_ngram_of_mentions(mentions=mentions, n=1, 
                                                                              inflect_engine=inflect_engine, 
                                                                              nlp=nlp, apply_preprocess=True)

    processed_mentions_n2_last_prepro = preprocess.get_last_ngram_of_mentions(mentions=mentions, n=2, 
                                                                              inflect_engine=inflect_engine, 
                                                                              nlp=nlp, apply_preprocess=True)

    processed_mentions_n3_last_prepro = preprocess.get_last_ngram_of_mentions(mentions=mentions, n=3, 
                                                                              inflect_engine=inflect_engine, 
                                                                              nlp=nlp, apply_preprocess=True)

    for mention in mentions:
        search_token_n1 = processed_mentions_n1_last[mention]
        singularized_token_n1 = preprocess.preprocess(mention=search_token_n1, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n1_last_prepro[mention] == singularized_token_n1

        search_token_n2 = processed_mentions_n2_last[mention]
        singularized_token_n2 = preprocess.preprocess(mention=search_token_n2, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n2_last_prepro[mention] == singularized_token_n2

        search_token_n3 = processed_mentions_n3_last[mention]
        singularized_token_n3 = preprocess.preprocess(mention=search_token_n3, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n3_last_prepro[mention] == singularized_token_n3
    
    # test-3: the final tokens should be in the mention
    for mention in mentions:
        filter_list = [item for item in punctuation]
        filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
        mention_ = ' '.join([token for token in mention.split() if token not in filter_list])

        assert processed_mentions_n1_last[mention] in mention_
        assert processed_mentions_n2_last[mention] in mention_
        assert processed_mentions_n3_last[mention] in mention_
    #     for prepro -- ('leaf', 'leaves') or ('their life', 'their lives')
    #     assert processed_mentions_n1_last_prepro[mention] in mention_
    #     assert processed_mentions_n2_last_prepro[mention] in mention_
    #     assert processed_mentions_n3_last_prepro[mention] in mention_
    
    # test-4 test with manual check: some selected ones and some random ones.
    last_n1 = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=1, 
                                                    inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=False)
    last_n1_prep = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=1, 
                                                         inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=True)

    last_n2 = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=2, 
                                                    inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=False)
    last_n2_prep = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=2, 
                                                         inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=True)

    last_n3 = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=3, 
                                                    inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=False)
    last_n3_prep = preprocess.get_last_ngram_of_mentions(mentions=pytest.test_mentions, n=3, 
                                                         inflect_engine=inflect_engine, nlp=nlp, apply_preprocess=True)

    assert last_n1['a power-sharing administration'] == 'administration'
    assert last_n1_prep['a power-sharing administration'] == 'administration'
    assert last_n2['a power-sharing administration'] == 'power-sharing administration'
    assert last_n2_prep['a power-sharing administration'] == 'power-sharing administration'
    assert last_n3['a power-sharing administration'] == 'a power-sharing administration'
    assert last_n3_prep['a power-sharing administration'] == 'a power-sharing administration'

    assert last_n1['many years'] == 'years'
    assert last_n1_prep['many years'] == 'year'
    assert last_n2['many years'] == 'many years'
    assert last_n2_prep['many years'] == 'many year'
    assert last_n3['many years'] == 'many years'
    assert last_n3_prep['many years'] == 'many year'

    assert last_n1['support'] == 'support'
    assert last_n1_prep['support'] == 'support'
    assert last_n2['support'] == 'support'
    assert last_n2_prep['support'] == 'support'
    assert last_n3['support'] == 'support'
    assert last_n3_prep['support'] == 'support'

    assert last_n1['some strongholds'] == 'strongholds'
    assert last_n1_prep['some strongholds'] == 'stronghold'
    assert last_n2['some strongholds'] == 'some strongholds'
    assert last_n2_prep['some strongholds'] == 'some stronghold'
    assert last_n3['some strongholds'] == 'some strongholds'
    assert last_n3_prep['some strongholds'] == 'some stronghold'

    assert last_n1['the nearby village of Livenka'] == 'Livenka'
    assert last_n1_prep['the nearby village of Livenka'] == 'Livenka'
    assert last_n2['the nearby village of Livenka'] == 'of Livenka'
    assert last_n2_prep['the nearby village of Livenka'] == 'of Livenka'
    assert last_n3['the nearby village of Livenka'] == 'village of Livenka'
    assert last_n3_prep['the nearby village of Livenka'] == 'village of Livenka'

    assert last_n1['Small car makers'] == 'makers'
    assert last_n1_prep['Small car makers'] == 'maker'
    assert last_n2['Small car makers'] == 'car makers'
    assert last_n2_prep['Small car makers'] == 'car maker'
    assert last_n3['Small car makers'] == 'Small car makers'
    assert last_n3_prep['Small car makers'] == 'Small car maker'

    assert last_n1['Thursday'] == 'Thursday'
    assert last_n1_prep['Thursday'] == 'Thursday'
    assert last_n2['Thursday'] == 'Thursday'
    assert last_n2_prep['Thursday'] == 'Thursday'
    assert last_n3['Thursday'] == 'Thursday'
    assert last_n3_prep['Thursday'] == 'Thursday'

    assert last_n1['new areas'] == 'areas'
    assert last_n1_prep['new areas'] == 'area'
    assert last_n2['new areas'] == 'new areas'
    assert last_n2_prep['new areas'] == 'new area'
    assert last_n3['new areas'] == 'new areas'
    assert last_n3_prep['new areas'] == 'new area'

    assert last_n1['His large scale sculpture'] == 'sculpture'
    assert last_n1_prep['His large scale sculpture'] == 'sculpture'
    assert last_n2['His large scale sculpture'] == 'scale sculpture'
    assert last_n2_prep['His large scale sculpture'] == 'scale sculpture'
    assert last_n3['His large scale sculpture'] == 'large scale sculpture'
    assert last_n3_prep['His large scale sculpture'] == 'large scale sculpture'

    assert last_n1['an East German border town'] == 'town'
    assert last_n1_prep['an East German border town'] == 'town'
    assert last_n2['an East German border town'] == 'border town'
    assert last_n2_prep['an East German border town'] == 'border town'
    assert last_n3['an East German border town'] == 'German border town'
    assert last_n3_prep['an East German border town'] == 'German border town'

    assert last_n1['Latin America , Africa , and the South Pacific'] == 'Pacific'
    assert last_n1_prep['Latin America , Africa , and the South Pacific'] == 'Pacific'
    assert last_n2['Latin America , Africa , and the South Pacific'] == 'South Pacific'
    assert last_n2_prep['Latin America , Africa , and the South Pacific'] == 'South Pacific'
    assert last_n3['Latin America , Africa , and the South Pacific'] == 'the South Pacific'
    assert last_n3_prep['Latin America , Africa , and the South Pacific'] == 'the South Pacific'

    assert last_n1['Eusebius'] == 'Eusebius'
    assert last_n1_prep['Eusebius'] == 'Eusebius'
    assert last_n2['Eusebius'] == 'Eusebius'
    assert last_n2_prep['Eusebius'] == 'Eusebius'
    assert last_n3['Eusebius'] == 'Eusebius'
    assert last_n3_prep['Eusebius'] == 'Eusebius'

    # note this one
    assert last_n1['tribal leaders and other activists'] == 'activists'
    assert last_n1_prep['tribal leaders and other activists'] == 'activist'
    assert last_n2['tribal leaders and other activists'] == 'other activists'
    assert last_n2_prep['tribal leaders and other activists'] == 'other activist'
    assert last_n3['tribal leaders and other activists'] == 'and other activists'
    assert last_n3_prep['tribal leaders and other activists'] == 'and other activist'

    assert last_n1['The main event'] == 'event'
    assert last_n1_prep['The main event'] == 'event'
    assert last_n2['The main event'] == 'main event'
    assert last_n2_prep['The main event'] == 'main event'
    assert last_n3['The main event'] == 'The main event'
    assert last_n3_prep['The main event'] == 'The main event'

    assert last_n1['Michael'] == 'Michael'
    assert last_n1_prep['Michael'] == 'Michael'
    assert last_n2['Michael'] == 'Michael'
    assert last_n2_prep['Michael'] == 'Michael'
    assert last_n3['Michael'] == 'Michael'
    assert last_n3_prep['Michael'] == 'Michael'

    assert last_n1['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Cox'
    assert last_n1_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Cox'
    assert last_n2['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Wally Cox'
    assert last_n2_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Wally Cox'
    assert last_n3['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'sequence Wally Cox'
    assert last_n3_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'sequence Wally Cox'

    assert last_n1['Multinationals'] == 'Multinationals'
    assert last_n1_prep['Multinationals'] == 'Multinational'
    assert last_n2['Multinationals'] == 'Multinationals'
    assert last_n2_prep['Multinationals'] == 'Multinational'
    assert last_n3['Multinationals'] == 'Multinationals'
    assert last_n3_prep['Multinationals'] == 'Multinational'

    assert last_n1['the concept'] == 'concept'
    assert last_n1_prep['the concept'] == 'concept'
    assert last_n2['the concept'] == 'the concept'
    assert last_n2_prep['the concept'] == 'the concept'
    assert last_n3['the concept'] == 'the concept'
    assert last_n3_prep['the concept'] == 'the concept'

    assert last_n1['Friday prayers'] == 'prayers'
    assert last_n1_prep['Friday prayers'] == 'prayer'
    assert last_n2['Friday prayers'] == 'Friday prayers'
    assert last_n2_prep['Friday prayers'] == 'Friday prayer'
    assert last_n3['Friday prayers'] == 'Friday prayers'
    assert last_n3_prep['Friday prayers'] == 'Friday prayer'

    assert last_n1['Algeria'] == 'Algeria'
    assert last_n1_prep['Algeria'] == 'Algeria'
    assert last_n2['Algeria'] == 'Algeria'
    assert last_n2_prep['Algeria'] == 'Algeria'
    assert last_n3['Algeria'] == 'Algeria'
    assert last_n3_prep['Algeria'] == 'Algeria'

    ########################
    assert last_n1['the building , a violation of the Clean Air Act'] == 'Act'
    assert last_n1_prep['the building , a violation of the Clean Air Act'] == 'Act'
    assert last_n2['the building , a violation of the Clean Air Act'] == 'Air Act'
    assert last_n2_prep['the building , a violation of the Clean Air Act'] == 'Air Act'
    assert last_n3['the building , a violation of the Clean Air Act'] == 'Clean Air Act'
    assert last_n3_prep['the building , a violation of the Clean Air Act'] == 'Clean Air Act'

    assert last_n1['a club playing in the Fourth National division'] == 'division'
    assert last_n1_prep['a club playing in the Fourth National division'] == 'division'
    assert last_n2['a club playing in the Fourth National division'] == 'National division'
    assert last_n2_prep['a club playing in the Fourth National division'] == 'National division'
    assert last_n3['a club playing in the Fourth National division'] == 'Fourth National division'
    assert last_n3_prep['a club playing in the Fourth National division'] == 'Fourth National division'

    assert last_n1['an English football player and manager'] == 'manager'
    assert last_n1_prep['an English football player and manager'] == 'manager'
    assert last_n2['an English football player and manager'] == 'and manager'
    assert last_n2_prep['an English football player and manager'] == 'and manager'
    assert last_n3['an English football player and manager'] == 'player and manager'
    assert last_n3_prep['an English football player and manager'] == 'player and manager'

    assert last_n1['terms of its righteousness'] == 'righteousness'
    assert last_n1_prep['terms of its righteousness'] == 'righteousness'
    assert last_n2['terms of its righteousness'] == 'its righteousness'
    assert last_n2_prep['terms of its righteousness'] == 'its righteousness' 
    assert last_n3['terms of its righteousness'] == 'of its righteousness'
    assert last_n3_prep['terms of its righteousness'] == 'of its righteousness' 

    assert last_n1['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'England'
    assert last_n1_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'England'
    assert last_n2['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Nottinghamshire England'
    assert last_n2_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Nottinghamshire England'
    assert last_n3['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Wolds Nottinghamshire England'
    assert last_n3_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Wolds Nottinghamshire England'
    
    assert last_n1["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'whites'
    assert last_n1_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'white'
    assert last_n2["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the whites'
    assert last_n2_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the white'
    assert last_n3["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'of the whites'
    assert last_n3_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'of the white'

    assert last_n1['present Erwin Arnada -- now at large --'] == 'large'
    assert last_n1_prep['present Erwin Arnada -- now at large --'] == 'large'
    assert last_n2['present Erwin Arnada -- now at large --'] == 'at large'
    assert last_n2_prep['present Erwin Arnada -- now at large --'] == 'at large'
    assert last_n3['present Erwin Arnada -- now at large --'] == 'now at large'
    assert last_n3_prep['present Erwin Arnada -- now at large --'] == 'now at large'

    assert last_n1["the percentage of Americans who do `` real exercise to build the heart ''"] == 'heart'
    assert last_n1_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'heart'
    assert last_n2["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the heart'
    assert last_n2_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the heart'
    assert last_n3["the percentage of Americans who do `` real exercise to build the heart ''"] == 'build the heart'
    assert last_n3_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'build the heart'

    assert last_n1['the sound `` I Can See Clearly Now'] == 'Now'
    assert last_n1_prep['the sound `` I Can See Clearly Now'] == 'Now'
    assert last_n2['the sound `` I Can See Clearly Now'] == 'Clearly Now'
    assert last_n2_prep['the sound `` I Can See Clearly Now'] == 'Clearly Now'
    assert last_n3['the sound `` I Can See Clearly Now'] == 'See Clearly Now'
    assert last_n3_prep['the sound `` I Can See Clearly Now'] == 'See Clearly Now'

    assert last_n1['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Lilas'
    assert last_n1_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Lilas'
    assert last_n2['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'as Lilas'
    assert last_n2_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'as Lilas'
    assert last_n3['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'known as Lilas'
    assert last_n3_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'known as Lilas'

    assert last_n1['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'driver'
    assert last_n1_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'driver'
    assert last_n2['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Valley driver'
    assert last_n2_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Valley driver'
    assert last_n3['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Death Valley driver'
    assert last_n3_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Death Valley driver'

    assert last_n1['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Roseau'
    assert last_n1_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Roseau'
    assert last_n2['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Dominica Roseau'
    assert last_n2_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Dominica Roseau'
    assert last_n3['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'of Dominica Roseau'
    assert last_n3_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'of Dominica Roseau'

    assert last_n1['the O.J . Simpson trial'] == 'trial'
    assert last_n1_prep['the O.J . Simpson trial'] == 'trial'
    assert last_n2['the O.J . Simpson trial'] == 'Simpson trial'
    assert last_n2_prep['the O.J . Simpson trial'] == 'Simpson trial'
    assert last_n3['the O.J . Simpson trial'] == 'O.J Simpson trial'
    assert last_n3_prep['the O.J . Simpson trial'] == 'O.J Simpson trial'
    
    
def test_get_headword_of_mentions():
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    mentions_ = [mention_info['mention_span'] for mention_info in dev_data]
    mentions = set(mentions_)
    
    nlp_headwords = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    inflect_engine = inflect.engine()
    
    # test-1: len(doc.sentences) == 1 --> all mentions should have 1 sentences
    count = 0
    for mention in mentions:
        doc = nlp_headwords(mention)
        try:
            assert len(doc.sentences) == 1
        except AssertionError:
            # print(len(doc.sentences), mention)
            count += 1
            
    assert count == 3  # for 3 mentions, there are 2 sentences
    # 2 Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,
    # 2 Front Line member Eric Young in the main event ,
    #   which he lost after Young pinned him following a Death Valley driver
    # 2 the O.J . Simpson trial
    
    # test-2: the output should be in the mention
    processed_mentions_headwords, count_multiple_heads = preprocess.get_headword_of_mentions(mentions=mentions, 
                                                                                             inflect_engine=inflect_engine, 
                                                                                             nlp=nlp_headwords, 
                                                                                             apply_preprocess=False)
    assert count_multiple_heads == 3
    for mention in mentions:
        assert processed_mentions_headwords[mention] in mention
    
    # test-3: length of the returned string is always 1
    processed_mentions_headwords_prepro, count_multiple = preprocess.get_headword_of_mentions(mentions=mentions, 
                                                                                              inflect_engine=inflect_engine, 
                                                                                              nlp=nlp_headwords, 
                                                                                              apply_preprocess=True)
    for mention in processed_mentions_headwords:
        assert len(processed_mentions_headwords[mention].split()) == 1
        assert len(processed_mentions_headwords_prepro[mention].split()) == 1
    
    # test-4 headwords: try w/o apply_preprocess and call preprocess after for each mention. 
    # check the diff if apply_preprocess=True, they should be the same
    for mention in mentions:
        search_token = processed_mentions_headwords[mention]
        singularized_token = preprocess.preprocess(mention=search_token, inflect_engine=inflect_engine, nlp=nlp_headwords)
        assert processed_mentions_headwords_prepro[mention] == singularized_token
        
    # test-5 test with manual check: some selected ones and some random ones.
    headword, count_multiple_heads = preprocess.get_headword_of_mentions(mentions=pytest.test_mentions, 
                                                                         inflect_engine=inflect_engine, 
                                                                         nlp=nlp_headwords, apply_preprocess=False)
    headword_prep, count_multiple_heads_prep = preprocess.get_headword_of_mentions(mentions=pytest.test_mentions, 
                                                                                   inflect_engine=inflect_engine, 
                                                                                   nlp=nlp_headwords, 
                                                                                   apply_preprocess=True)
    assert count_multiple_heads == 3
    assert count_multiple_heads_prep == 3

    assert headword['a power-sharing administration'] == 'administration'
    assert headword_prep['a power-sharing administration'] == 'administration'

    assert headword['many years'] == 'years'
    assert headword_prep['many years'] == 'year'

    assert headword['support'] == 'support'
    assert headword_prep['support'] == 'support'

    assert headword['some strongholds'] == 'strongholds'
    assert headword_prep['some strongholds'] == 'stronghold'

    assert headword['the nearby village of Livenka'] == 'village'
    assert headword_prep['the nearby village of Livenka'] == 'village'

    assert headword['Small car makers'] == 'makers'
    assert headword_prep['Small car makers'] == 'maker'

    assert headword['Thursday'] == 'Thursday'
    assert headword_prep['Thursday'] == 'Thursday'

    assert headword['new areas'] == 'areas'
    assert headword_prep['new areas'] == 'area'

    assert headword['His large scale sculpture'] == 'sculpture'
    assert headword_prep['His large scale sculpture'] == 'sculpture'

    assert headword['an East German border town'] == 'town'
    assert headword_prep['an East German border town'] == 'town'

    assert headword['Latin America , Africa , and the South Pacific'] == 'America'  # note this
    assert headword_prep['Latin America , Africa , and the South Pacific'] == 'America'

    assert headword['Eusebius'] == 'Eusebius'
    assert headword_prep['Eusebius'] == 'Eusebius'

    # note this one
    assert headword['tribal leaders and other activists'] == 'leaders'
    assert headword_prep['tribal leaders and other activists'] == 'leader'

    assert headword['The main event'] == 'event'
    assert headword_prep['The main event'] == 'event'

    assert headword['Michael'] == 'Michael'
    assert headword_prep['Michael'] == 'Michael'

    # Note this: Suzanne
    assert headword['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'
    assert headword_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'

    assert headword['Multinationals'] == 'Multinationals'
    assert headword_prep['Multinationals'] == 'Multinational'

    assert headword['the concept'] == 'concept'
    assert headword_prep['the concept'] == 'concept'

    assert headword['Friday prayers'] == 'prayers'
    assert headword_prep['Friday prayers'] == 'prayer'

    assert headword['Algeria'] == 'Algeria'
    assert headword_prep['Algeria'] == 'Algeria'

    ########################
    assert headword['the building , a violation of the Clean Air Act'] == 'building'
    assert headword_prep['the building , a violation of the Clean Air Act'] == 'building'

    assert headword['a club playing in the Fourth National division'] == 'club'
    assert headword_prep['a club playing in the Fourth National division'] == 'club'

    assert headword['an English football player and manager'] == 'player'  # note this
    assert headword_prep['an English football player and manager'] == 'player'

    assert headword['terms of its righteousness'] == 'terms'
    assert headword_prep['terms of its righteousness'] == 'term'

    assert headword['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'church'
    assert headword_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'church'

    assert headword["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'Tubabodaga'
    assert headword_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'Tubabodaga'

    assert headword['present Erwin Arnada -- now at large --'] == 'present'
    assert headword_prep['present Erwin Arnada -- now at large --'] == 'present'

    assert headword["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'
    assert headword_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'

    assert headword['the sound `` I Can See Clearly Now'] == 'sound'
    assert headword_prep['the sound `` I Can See Clearly Now'] == 'sound'

    assert headword['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'
    assert headword_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'

    # to check multihead mentions
    assert headword['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'member'
    assert headword_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'member'

    assert headword['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'
    assert headword_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'

    assert headword['the O.J . Simpson trial'] == 'O.J'
    assert headword_prep['the O.J . Simpson trial'] == 'O.J'
    
    
def test_preprocess():
    # test preprocess: some basic strings like women, people, feet, actress, etc.
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    nlp_headwords = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    inflect_engine = inflect.engine()
    assert 'woman' == preprocess.preprocess(mention='women', inflect_engine=inflect_engine, nlp=nlp)
    assert 'woman' == preprocess.preprocess(mention='women', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'person' == preprocess.preprocess(mention='people', inflect_engine=inflect_engine, nlp=nlp)
    assert 'person' == preprocess.preprocess(mention='people', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'foot' == preprocess.preprocess(mention='feet', inflect_engine=inflect_engine, nlp=nlp)
    assert 'foot' == preprocess.preprocess(mention='feet', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'actress' == preprocess.preprocess(mention='actress', inflect_engine=inflect_engine, nlp=nlp)
    assert 'actress' == preprocess.preprocess(mention='actress', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'shareholder' == preprocess.preprocess(mention='shareholders', inflect_engine=inflect_engine, nlp=nlp)
    assert 'shareholder' == preprocess.preprocess(mention='shareholders', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'company' == preprocess.preprocess(mention='companies', inflect_engine=inflect_engine, nlp=nlp_headwords)
    assert 'company' == preprocess.preprocess(mention='companies', inflect_engine=inflect_engine, nlp=nlp_headwords)
    # the below mentions did not work, since works is labeled as SING since it is taken as verb.
    # assert 'work' == preprocess.preprocess(mention='works', inflect_engine=inflect_engine, nlp=nlp)
    # assert 'work' == preprocess.preprocess(mention='works', inflect_engine=inflect_engine, nlp=nlp_headwords)

    
def test_get_first_ngram_of_mentions_sklearn():
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    mentions_ = [mention_info['mention_span'] for mention_info in dev_data]
    mentions = set(mentions_)
    
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    inflect_engine = inflect.engine()
    
    # test-1: first sklearn if len(mention.split()) == 1: search_token == mention
    processed_mentions_n1_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                   n=1, inflect_engine=inflect_engine, 
                                                                                   nlp=nlp, apply_preprocess=False)

    processed_mentions_n2_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                   n=2, inflect_engine=inflect_engine, 
                                                                                   nlp=nlp, apply_preprocess=False)

    processed_mentions_n3_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                   n=3, inflect_engine=inflect_engine, 
                                                                                   nlp=nlp, apply_preprocess=False)
    checked = 0
    for mention in mentions:
        if len(mention.split()) == 1:
            assert processed_mentions_n1_sklearn[mention] == mention
            assert processed_mentions_n2_sklearn[mention] == mention
            assert processed_mentions_n3_sklearn[mention] == mention
            checked += 1
    # be sure some mentions are checked
    assert checked == 232

    # test-2: first sklearn try w/o apply_preprocess and call preprocess after for each mention. 
    # check the diff if apply_preprocess=True, they should be the same
    processed_mentions_n1_prepro_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, n=1, 
                                                                                          inflect_engine=inflect_engine, 
                                                                                          nlp=nlp, apply_preprocess=True)

    processed_mentions_n2_prepro_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, n=2, 
                                                                                          inflect_engine=inflect_engine, 
                                                                                          nlp=nlp, apply_preprocess=True)

    processed_mentions_n3_prepro_sklearn = preprocess.get_first_ngram_of_mentions_sklearn(mentions=mentions, n=3, 
                                                                                          inflect_engine=inflect_engine, 
                                                                                          nlp=nlp, apply_preprocess=True)

    for mention in mentions:
        search_token_n1 = processed_mentions_n1_sklearn[mention]
        singularized_token_n1 = preprocess.preprocess(mention=search_token_n1, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n1_prepro_sklearn[mention] == singularized_token_n1

        search_token_n2 = processed_mentions_n2_sklearn[mention]
        singularized_token_n2 = preprocess.preprocess(mention=search_token_n2, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n2_prepro_sklearn[mention] == singularized_token_n2

        search_token_n3 = processed_mentions_n3_sklearn[mention]
        singularized_token_n3 = preprocess.preprocess(mention=search_token_n3, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n3_prepro_sklearn[mention] == singularized_token_n3

    # test-3: first sklearn the final tokens should be in the mention
    # not necessarily be in like for mentions ('re sign', 're-sign various players') or
    # ('only few', 'only a few areas')
    # so skipping this test
    # for mention in mentions:
        # filter_list = [item for item in punctuation]
        # filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
        # mention_ = ' '.join([token for token in mention.split() if not token in filter_list])

        # assert processed_mentions_n1_last_sklearn[mention] in mention_
        # assert processed_mentions_n2_last_sklearn[mention] in mention_
        # assert processed_mentions_n3_last_sklearn[mention] in mention_
        # for prepro -- ('leaf', 'leaves')  or ('their life', 'their lives')
        # assert processed_mentions_n1_last_prepro[mention] in mention_
        # assert processed_mentions_n2_last_prepro[mention] in mention_
        # assert processed_mentions_n3_last_prepro[mention] in mention_
    
    # test-4 test with manual check: some selected ones and some random ones.
    first_sklearn_n1 = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=1, 
                                                                      inflect_engine=inflect_engine, nlp=nlp, 
                                                                      apply_preprocess=False)
    first_sklearn_n1_prep = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=1, 
                                                                           inflect_engine=inflect_engine, nlp=nlp, 
                                                                           apply_preprocess=True)

    first_sklearn_n2 = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=2, 
                                                                      inflect_engine=inflect_engine, nlp=nlp, 
                                                                      apply_preprocess=False)
    first_sklearn_n2_prep = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=2, 
                                                                           inflect_engine=inflect_engine, nlp=nlp, 
                                                                           apply_preprocess=True)

    first_sklearn_n3 = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=3, 
                                                                      inflect_engine=inflect_engine, nlp=nlp, 
                                                                      apply_preprocess=False)
    first_sklearn_n3_prep = preprocess.get_first_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=3, 
                                                                           inflect_engine=inflect_engine, nlp=nlp, 
                                                                           apply_preprocess=True)

    assert first_sklearn_n1['a power-sharing administration'] == 'power'
    assert first_sklearn_n1_prep['a power-sharing administration'] == 'power'
    assert first_sklearn_n2['a power-sharing administration'] == 'power sharing'
    assert first_sklearn_n2_prep['a power-sharing administration'] == 'power sharing'
    assert first_sklearn_n3['a power-sharing administration'] == 'power sharing administration'
    assert first_sklearn_n3_prep['a power-sharing administration'] == 'power sharing administration'

    assert first_sklearn_n1['many years'] == 'many'
    assert first_sklearn_n1_prep['many years'] == 'many'
    assert first_sklearn_n2['many years'] == 'many years'
    assert first_sklearn_n2_prep['many years'] == 'many year'
    assert first_sklearn_n3['many years'] == 'many years'
    assert first_sklearn_n3_prep['many years'] == 'many year'

    assert first_sklearn_n1['support'] == 'support'
    assert first_sklearn_n1_prep['support'] == 'support'
    assert first_sklearn_n2['support'] == 'support'
    assert first_sklearn_n2_prep['support'] == 'support'
    assert first_sklearn_n3['support'] == 'support'
    assert first_sklearn_n3_prep['support'] == 'support'

    assert first_sklearn_n1['some strongholds'] == 'some'
    assert first_sklearn_n1_prep['some strongholds'] == 'some'
    assert first_sklearn_n2['some strongholds'] == 'some strongholds'
    assert first_sklearn_n2_prep['some strongholds'] == 'some stronghold'
    assert first_sklearn_n3['some strongholds'] == 'some strongholds'
    assert first_sklearn_n3_prep['some strongholds'] == 'some stronghold'

    assert first_sklearn_n1['the nearby village of Livenka'] == 'nearby'
    assert first_sklearn_n1_prep['the nearby village of Livenka'] == 'nearby'
    assert first_sklearn_n2['the nearby village of Livenka'] == 'the nearby'
    assert first_sklearn_n2_prep['the nearby village of Livenka'] == 'the nearby'
    assert first_sklearn_n3['the nearby village of Livenka'] == 'the nearby village'
    assert first_sklearn_n3_prep['the nearby village of Livenka'] == 'the nearby village'

    assert first_sklearn_n1['Small car makers'] == 'Small'
    assert first_sklearn_n1_prep['Small car makers'] == 'Small'
    assert first_sklearn_n2['Small car makers'] == 'Small car'
    assert first_sklearn_n2_prep['Small car makers'] == 'Small car'
    assert first_sklearn_n3['Small car makers'] == 'Small car makers'
    assert first_sklearn_n3_prep['Small car makers'] == 'Small car maker'

    assert first_sklearn_n1['Thursday'] == 'Thursday'
    assert first_sklearn_n1_prep['Thursday'] == 'Thursday'
    assert first_sklearn_n2['Thursday'] == 'Thursday'
    assert first_sklearn_n2_prep['Thursday'] == 'Thursday'
    assert first_sklearn_n3['Thursday'] == 'Thursday'
    assert first_sklearn_n3_prep['Thursday'] == 'Thursday'

    assert first_sklearn_n1['new areas'] == 'new'
    assert first_sklearn_n1_prep['new areas'] == 'new'
    assert first_sklearn_n2['new areas'] == 'new areas'
    assert first_sklearn_n2_prep['new areas'] == 'new area'
    assert first_sklearn_n3['new areas'] == 'new areas'
    assert first_sklearn_n3_prep['new areas'] == 'new area'

    assert first_sklearn_n1['His large scale sculpture'] == 'His'
    assert first_sklearn_n1_prep['His large scale sculpture'] == 'His'
    assert first_sklearn_n2['His large scale sculpture'] == 'His large'
    assert first_sklearn_n2_prep['His large scale sculpture'] == 'His large'
    assert first_sklearn_n3['His large scale sculpture'] == 'His large scale'
    assert first_sklearn_n3_prep['His large scale sculpture'] == 'His large scale'

    assert first_sklearn_n1['an East German border town'] == 'East'
    assert first_sklearn_n1_prep['an East German border town'] == 'East'
    assert first_sklearn_n2['an East German border town'] == 'an East'
    assert first_sklearn_n2_prep['an East German border town'] == 'an East'
    assert first_sklearn_n3['an East German border town'] == 'an East German'
    assert first_sklearn_n3_prep['an East German border town'] == 'an East German'

    assert first_sklearn_n1['Latin America , Africa , and the South Pacific'] == 'Latin'
    assert first_sklearn_n1_prep['Latin America , Africa , and the South Pacific'] == 'Latin'
    assert first_sklearn_n2['Latin America , Africa , and the South Pacific'] == 'Latin America'
    assert first_sklearn_n2_prep['Latin America , Africa , and the South Pacific'] == 'Latin America'
    assert first_sklearn_n3['Latin America , Africa , and the South Pacific'] == 'Latin America Africa'
    assert first_sklearn_n3_prep['Latin America , Africa , and the South Pacific'] == 'Latin America Africa'

    assert first_sklearn_n1['Eusebius'] == 'Eusebius'
    assert first_sklearn_n1_prep['Eusebius'] == 'Eusebius'
    assert first_sklearn_n2['Eusebius'] == 'Eusebius'
    assert first_sklearn_n2_prep['Eusebius'] == 'Eusebius'
    assert first_sklearn_n3['Eusebius'] == 'Eusebius'
    assert first_sklearn_n3_prep['Eusebius'] == 'Eusebius'

    # note this one
    assert first_sklearn_n1['tribal leaders and other activists'] == 'tribal'
    assert first_sklearn_n1_prep['tribal leaders and other activists'] == 'tribal'
    assert first_sklearn_n2['tribal leaders and other activists'] == 'tribal leaders'
    assert first_sklearn_n2_prep['tribal leaders and other activists'] == 'tribal leader'
    assert first_sklearn_n3['tribal leaders and other activists'] == 'tribal leaders and'
    assert first_sklearn_n3_prep['tribal leaders and other activists'] == 'tribal leaders and'  # ?

    assert first_sklearn_n1['The main event'] == 'main'
    assert first_sklearn_n1_prep['The main event'] == 'main'
    assert first_sklearn_n2['The main event'] == 'The main'
    assert first_sklearn_n2_prep['The main event'] == 'The main'
    assert first_sklearn_n3['The main event'] == 'The main event'
    assert first_sklearn_n3_prep['The main event'] == 'The main event'

    assert first_sklearn_n1['Michael'] == 'Michael'
    assert first_sklearn_n1_prep['Michael'] == 'Michael'
    assert first_sklearn_n2['Michael'] == 'Michael'
    assert first_sklearn_n2_prep['Michael'] == 'Michael'
    assert first_sklearn_n3['Michael'] == 'Michael'
    assert first_sklearn_n3_prep['Michael'] == 'Michael'

    assert first_sklearn_n1['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'
    assert first_sklearn_n1_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne'
    assert first_sklearn_n2['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette'
    assert first_sklearn_n2_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette'
    assert first_sklearn_n3['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette Rod'
    assert first_sklearn_n3_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Suzanne Pleshette Rod'

    assert first_sklearn_n1['Multinationals'] == 'Multinationals'
    assert first_sklearn_n1_prep['Multinationals'] == 'Multinational'
    assert first_sklearn_n2['Multinationals'] == 'Multinationals'
    assert first_sklearn_n2_prep['Multinationals'] == 'Multinational'
    assert first_sklearn_n3['Multinationals'] == 'Multinationals'
    assert first_sklearn_n3_prep['Multinationals'] == 'Multinational'

    assert first_sklearn_n1['the concept'] == 'concept'
    assert first_sklearn_n1_prep['the concept'] == 'concept'
    assert first_sklearn_n2['the concept'] == 'the concept'
    assert first_sklearn_n2_prep['the concept'] == 'the concept'
    assert first_sklearn_n3['the concept'] == 'the concept'
    assert first_sklearn_n3_prep['the concept'] == 'the concept'

    assert first_sklearn_n1['Friday prayers'] == 'Friday'
    assert first_sklearn_n1_prep['Friday prayers'] == 'Friday'
    assert first_sklearn_n2['Friday prayers'] == 'Friday prayers'
    assert first_sklearn_n2_prep['Friday prayers'] == 'Friday prayer'
    assert first_sklearn_n3['Friday prayers'] == 'Friday prayers'
    assert first_sklearn_n3_prep['Friday prayers'] == 'Friday prayer'

    assert first_sklearn_n1['Algeria'] == 'Algeria'
    assert first_sklearn_n1_prep['Algeria'] == 'Algeria'
    assert first_sklearn_n2['Algeria'] == 'Algeria'
    assert first_sklearn_n2_prep['Algeria'] == 'Algeria'
    assert first_sklearn_n3['Algeria'] == 'Algeria'
    assert first_sklearn_n3_prep['Algeria'] == 'Algeria'

    ########################
    assert first_sklearn_n1['the building , a violation of the Clean Air Act'] == 'building'
    assert first_sklearn_n1_prep['the building , a violation of the Clean Air Act'] == 'building'
    assert first_sklearn_n2['the building , a violation of the Clean Air Act'] == 'the building'
    assert first_sklearn_n2_prep['the building , a violation of the Clean Air Act'] == 'the building'
    assert first_sklearn_n3['the building , a violation of the Clean Air Act'] == 'the building violation'
    assert first_sklearn_n3_prep['the building , a violation of the Clean Air Act'] == 'the building violation'

    assert first_sklearn_n1['a club playing in the Fourth National division'] == 'club'
    assert first_sklearn_n1_prep['a club playing in the Fourth National division'] == 'club'
    assert first_sklearn_n2['a club playing in the Fourth National division'] == 'club playing'
    assert first_sklearn_n2_prep['a club playing in the Fourth National division'] == 'club playing'
    assert first_sklearn_n3['a club playing in the Fourth National division'] == 'club playing in'
    assert first_sklearn_n3_prep['a club playing in the Fourth National division'] == 'club playing in'

    assert first_sklearn_n1['an English football player and manager'] == 'English'
    assert first_sklearn_n1_prep['an English football player and manager'] == 'English'
    assert first_sklearn_n2['an English football player and manager'] == 'an English'
    assert first_sklearn_n2_prep['an English football player and manager'] == 'an English'
    assert first_sklearn_n3['an English football player and manager'] == 'an English football'
    assert first_sklearn_n3_prep['an English football player and manager'] == 'an English football'

    assert first_sklearn_n1['terms of its righteousness'] == 'terms'
    assert first_sklearn_n1_prep['terms of its righteousness'] == 'term'
    assert first_sklearn_n2['terms of its righteousness'] == 'terms of'
    assert first_sklearn_n2_prep['terms of its righteousness'] == 'terms of'  # note this one
    assert first_sklearn_n3['terms of its righteousness'] == 'terms of its'
    assert first_sklearn_n3_prep['terms of its righteousness'] == 'terms of its'  # note this one

    assert first_sklearn_n1['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish'
    assert first_sklearn_n1_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish'
    assert first_sklearn_n2['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish church'
    assert first_sklearn_n2_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish church'
    assert first_sklearn_n3['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish church in'
    assert first_sklearn_n3_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'parish church in'

    assert first_sklearn_n1["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'settlement'
    assert first_sklearn_n1_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'settlement'
    assert first_sklearn_n2["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement'
    assert first_sklearn_n2_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement'
    assert first_sklearn_n3["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement Tubabodaga'
    assert first_sklearn_n3_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the settlement Tubabodaga'

    assert first_sklearn_n1['present Erwin Arnada -- now at large --'] == 'present'
    assert first_sklearn_n1_prep['present Erwin Arnada -- now at large --'] == 'present'
    assert first_sklearn_n2['present Erwin Arnada -- now at large --'] == 'present Erwin'
    assert first_sklearn_n2_prep['present Erwin Arnada -- now at large --'] == 'present Erwin'
    assert first_sklearn_n3['present Erwin Arnada -- now at large --'] == 'present Erwin Arnada'
    assert first_sklearn_n3_prep['present Erwin Arnada -- now at large --'] == 'present Erwin Arnada'

    assert first_sklearn_n1["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'
    assert first_sklearn_n1_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'percentage'
    assert first_sklearn_n2["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage'
    assert first_sklearn_n2_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage'
    assert first_sklearn_n3["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage of'
    assert first_sklearn_n3_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the percentage of'

    assert first_sklearn_n1['the sound `` I Can See Clearly Now'] == 'sound'
    assert first_sklearn_n1_prep['the sound `` I Can See Clearly Now'] == 'sound'
    assert first_sklearn_n2['the sound `` I Can See Clearly Now'] == 'the sound'
    assert first_sklearn_n2_prep['the sound `` I Can See Clearly Now'] == 'the sound'
    assert first_sklearn_n3['the sound `` I Can See Clearly Now'] == 'the sound Can'  # note this
    assert first_sklearn_n3_prep['the sound `` I Can See Clearly Now'] == 'the sound Can'

    assert first_sklearn_n1['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'
    assert first_sklearn_n1_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul'
    assert first_sklearn_n2['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin'
    assert first_sklearn_n2_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin'
    assert first_sklearn_n3['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin also'
    assert first_sklearn_n3_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Paul Gauguin also'

    assert first_sklearn_n1['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front'
    assert first_sklearn_n1_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front'
    assert first_sklearn_n2['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line'
    assert first_sklearn_n2_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line'
    assert first_sklearn_n3['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line member'
    assert first_sklearn_n3_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Front Line member'

    assert first_sklearn_n1['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'
    assert first_sklearn_n1_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior'
    assert first_sklearn_n2['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of'
    assert first_sklearn_n2_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of'
    assert first_sklearn_n3['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of Dominica'
    assert first_sklearn_n3_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Interior of Dominica'

    assert first_sklearn_n1['the O.J . Simpson trial'] == 'Simpson'  # note this
    assert first_sklearn_n1_prep['the O.J . Simpson trial'] == 'Simpson'
    assert first_sklearn_n2['the O.J . Simpson trial'] == 'the Simpson'
    assert first_sklearn_n2_prep['the O.J . Simpson trial'] == 'the Simpson'
    assert first_sklearn_n3['the O.J . Simpson trial'] == 'the Simpson trial'
    assert first_sklearn_n3_prep['the O.J . Simpson trial'] == 'the Simpson trial'
    
    
def test_get_last_ngram_of_mentions_sklearn():
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    mentions_ = [mention_info['mention_span'] for mention_info in dev_data]
    mentions = set(mentions_)
    
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    inflect_engine = inflect.engine()
    
    # test-1: last sklearn if len(mention.split()) == 1: search_token == mention
    processed_mentions_n1_last_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                       n=1, inflect_engine=inflect_engine, 
                                                                                       nlp=nlp, apply_preprocess=False)

    processed_mentions_n2_last_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                       n=2, inflect_engine=inflect_engine, 
                                                                                       nlp=nlp, apply_preprocess=False)

    processed_mentions_n3_last_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, 
                                                                                       n=3, inflect_engine=inflect_engine, 
                                                                                       nlp=nlp, apply_preprocess=False)
    checked = 0
    for mention in mentions:
        if len(mention.split()) == 1:
            assert processed_mentions_n1_last_sklearn[mention] == mention
            assert processed_mentions_n2_last_sklearn[mention] == mention
            assert processed_mentions_n3_last_sklearn[mention] == mention
            checked += 1
    # be sure some mentions are checked
    assert checked == 232

    # test-2: last sklearn try w/o apply_preprocess and call preprocess after for each mention. 
    # check the diff if apply_preprocess=True, they should be the same
    processed_mentions_n1_last_prepro_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, n=1, 
                                                                                              inflect_engine=inflect_engine, 
                                                                                              nlp=nlp, apply_preprocess=True)

    processed_mentions_n2_last_prepro_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, n=2, 
                                                                                              inflect_engine=inflect_engine, 
                                                                                              nlp=nlp, apply_preprocess=True)

    processed_mentions_n3_last_prepro_sklearn = preprocess.get_last_ngram_of_mentions_sklearn(mentions=mentions, n=3, 
                                                                                              inflect_engine=inflect_engine, 
                                                                                              nlp=nlp, apply_preprocess=True)

    for mention in mentions:
        search_token_n1 = processed_mentions_n1_last_sklearn[mention]
        singularized_token_n1 = preprocess.preprocess(mention=search_token_n1, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n1_last_prepro_sklearn[mention] == singularized_token_n1

        search_token_n2 = processed_mentions_n2_last_sklearn[mention]
        singularized_token_n2 = preprocess.preprocess(mention=search_token_n2, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n2_last_prepro_sklearn[mention] == singularized_token_n2

        search_token_n3 = processed_mentions_n3_last_sklearn[mention]
        singularized_token_n3 = preprocess.preprocess(mention=search_token_n3, inflect_engine=inflect_engine, nlp=nlp)
        assert processed_mentions_n3_last_prepro_sklearn[mention] == singularized_token_n3

    # test-3: last sklearn the final tokens should be in the mention
    # not neccessarily be in like for mentions ('re sign', 're-sign various players') or 
    # ('only few', 'only a few areas')
    # so skipping this test
    # for mention in mentions:
        # filter_list = [item for item in punctuation]
        # filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
        # mention_ = ' '.join([token for token in mention.split() if not token in filter_list])

        # assert processed_mentions_n1_last_sklearn[mention] in mention_
        # assert processed_mentions_n2_last_sklearn[mention] in mention_
        # assert processed_mentions_n3_last_sklearn[mention] in mention_
        # for prepro -- ('leaf', 'leaves') or ('their life', 'their lives')
        # assert processed_mentions_n1_last_prepro[mention] in mention_
        # assert processed_mentions_n2_last_prepro[mention] in mention_
        # assert processed_mentions_n3_last_prepro[mention] in mention_
    
    # test-4 test with manual check: some selected ones and some random ones.
    last_sklearn_n1 = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=1, 
                                                                    inflect_engine=inflect_engine, nlp=nlp, 
                                                                    apply_preprocess=False)
    last_sklearn_n1_prep = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=1, 
                                                                         inflect_engine=inflect_engine, nlp=nlp, 
                                                                         apply_preprocess=True)

    last_sklearn_n2 = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=2, 
                                                                    inflect_engine=inflect_engine, nlp=nlp, 
                                                                    apply_preprocess=False)
    last_sklearn_n2_prep = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=2, 
                                                                         inflect_engine=inflect_engine, nlp=nlp, 
                                                                         apply_preprocess=True)

    last_sklearn_n3 = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=3, 
                                                                    inflect_engine=inflect_engine, nlp=nlp, 
                                                                    apply_preprocess=False)
    last_sklearn_n3_prep = preprocess.get_last_ngram_of_mentions_sklearn(mentions=pytest.test_mentions, n=3, 
                                                                         inflect_engine=inflect_engine, nlp=nlp, 
                                                                         apply_preprocess=True)

    assert last_sklearn_n1['a power-sharing administration'] == 'administration'
    assert last_sklearn_n1_prep['a power-sharing administration'] == 'administration'
    assert last_sklearn_n2['a power-sharing administration'] == 'sharing administration'
    assert last_sklearn_n2_prep['a power-sharing administration'] == 'sharing administration'
    assert last_sklearn_n3['a power-sharing administration'] == 'power sharing administration'
    assert last_sklearn_n3_prep['a power-sharing administration'] == 'power sharing administration'

    assert last_sklearn_n1['many years'] == 'years'
    assert last_sklearn_n1_prep['many years'] == 'year'
    assert last_sklearn_n2['many years'] == 'many years'
    assert last_sklearn_n2_prep['many years'] == 'many year'
    assert last_sklearn_n3['many years'] == 'many years'
    assert last_sklearn_n3_prep['many years'] == 'many year'

    assert last_sklearn_n1['support'] == 'support'
    assert last_sklearn_n1_prep['support'] == 'support'
    assert last_sklearn_n2['support'] == 'support'
    assert last_sklearn_n2_prep['support'] == 'support'
    assert last_sklearn_n3['support'] == 'support'
    assert last_sklearn_n3_prep['support'] == 'support'

    assert last_sklearn_n1['some strongholds'] == 'strongholds'
    assert last_sklearn_n1_prep['some strongholds'] == 'stronghold'
    assert last_sklearn_n2['some strongholds'] == 'some strongholds'
    assert last_sklearn_n2_prep['some strongholds'] == 'some stronghold'
    assert last_sklearn_n3['some strongholds'] == 'some strongholds'
    assert last_sklearn_n3_prep['some strongholds'] == 'some stronghold'

    assert last_sklearn_n1['the nearby village of Livenka'] == 'Livenka'
    assert last_sklearn_n1_prep['the nearby village of Livenka'] == 'Livenka'
    assert last_sklearn_n2['the nearby village of Livenka'] == 'of Livenka'
    assert last_sklearn_n2_prep['the nearby village of Livenka'] == 'of Livenka'
    assert last_sklearn_n3['the nearby village of Livenka'] == 'village of Livenka'
    assert last_sklearn_n3_prep['the nearby village of Livenka'] == 'village of Livenka'

    assert last_sklearn_n1['Small car makers'] == 'makers'
    assert last_sklearn_n1_prep['Small car makers'] == 'maker'
    assert last_sklearn_n2['Small car makers'] == 'car makers'
    assert last_sklearn_n2_prep['Small car makers'] == 'car maker'
    assert last_sklearn_n3['Small car makers'] == 'Small car makers'
    assert last_sklearn_n3_prep['Small car makers'] == 'Small car maker'

    assert last_sklearn_n1['Thursday'] == 'Thursday'
    assert last_sklearn_n1_prep['Thursday'] == 'Thursday'
    assert last_sklearn_n2['Thursday'] == 'Thursday'
    assert last_sklearn_n2_prep['Thursday'] == 'Thursday'
    assert last_sklearn_n3['Thursday'] == 'Thursday'
    assert last_sklearn_n3_prep['Thursday'] == 'Thursday'

    assert last_sklearn_n1['new areas'] == 'areas'
    assert last_sklearn_n1_prep['new areas'] == 'area'
    assert last_sklearn_n2['new areas'] == 'new areas'
    assert last_sklearn_n2_prep['new areas'] == 'new area'
    assert last_sklearn_n3['new areas'] == 'new areas'
    assert last_sklearn_n3_prep['new areas'] == 'new area'

    assert last_sklearn_n1['His large scale sculpture'] == 'sculpture'
    assert last_sklearn_n1_prep['His large scale sculpture'] == 'sculpture'
    assert last_sklearn_n2['His large scale sculpture'] == 'scale sculpture'
    assert last_sklearn_n2_prep['His large scale sculpture'] == 'scale sculpture'
    assert last_sklearn_n3['His large scale sculpture'] == 'large scale sculpture'
    assert last_sklearn_n3_prep['His large scale sculpture'] == 'large scale sculpture'

    assert last_sklearn_n1['an East German border town'] == 'town'
    assert last_sklearn_n1_prep['an East German border town'] == 'town'
    assert last_sklearn_n2['an East German border town'] == 'border town'
    assert last_sklearn_n2_prep['an East German border town'] == 'border town'
    assert last_sklearn_n3['an East German border town'] == 'German border town'
    assert last_sklearn_n3_prep['an East German border town'] == 'German border town'

    assert last_sklearn_n1['Latin America , Africa , and the South Pacific'] == 'Pacific'
    assert last_sklearn_n1_prep['Latin America , Africa , and the South Pacific'] == 'Pacific'
    assert last_sklearn_n2['Latin America , Africa , and the South Pacific'] == 'South Pacific'
    assert last_sklearn_n2_prep['Latin America , Africa , and the South Pacific'] == 'South Pacific'
    assert last_sklearn_n3['Latin America , Africa , and the South Pacific'] == 'the South Pacific'
    assert last_sklearn_n3_prep['Latin America , Africa , and the South Pacific'] == 'the South Pacific'

    assert last_sklearn_n1['Eusebius'] == 'Eusebius'
    assert last_sklearn_n1_prep['Eusebius'] == 'Eusebius'
    assert last_sklearn_n2['Eusebius'] == 'Eusebius'
    assert last_sklearn_n2_prep['Eusebius'] == 'Eusebius'
    assert last_sklearn_n3['Eusebius'] == 'Eusebius'
    assert last_sklearn_n3_prep['Eusebius'] == 'Eusebius'

    # note this one
    assert last_sklearn_n1['tribal leaders and other activists'] == 'activists'
    assert last_sklearn_n1_prep['tribal leaders and other activists'] == 'activist'
    assert last_sklearn_n2['tribal leaders and other activists'] == 'other activists'
    assert last_sklearn_n2_prep['tribal leaders and other activists'] == 'other activist'
    assert last_sklearn_n3['tribal leaders and other activists'] == 'and other activists'
    assert last_sklearn_n3_prep['tribal leaders and other activists'] == 'and other activist'

    assert last_sklearn_n1['The main event'] == 'event'
    assert last_sklearn_n1_prep['The main event'] == 'event'
    assert last_sklearn_n2['The main event'] == 'main event'
    assert last_sklearn_n2_prep['The main event'] == 'main event'
    assert last_sklearn_n3['The main event'] == 'The main event'
    assert last_sklearn_n3_prep['The main event'] == 'The main event'

    assert last_sklearn_n1['Michael'] == 'Michael'
    assert last_sklearn_n1_prep['Michael'] == 'Michael'
    assert last_sklearn_n2['Michael'] == 'Michael'
    assert last_sklearn_n2_prep['Michael'] == 'Michael'
    assert last_sklearn_n3['Michael'] == 'Michael'
    assert last_sklearn_n3_prep['Michael'] == 'Michael'

    assert last_sklearn_n1['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Cox'
    assert last_sklearn_n1_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Cox'
    assert last_sklearn_n2['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Wally Cox'
    assert last_sklearn_n2_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'Wally Cox'
    assert last_sklearn_n3['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'sequence Wally Cox'
    assert last_sklearn_n3_prep['Suzanne Pleshette , Rod Taylor , Jane Russell -LRB- playing herself entertaining for the USO in a flashback sequence -RRB- , Wally Cox'] == 'sequence Wally Cox'

    assert last_sklearn_n1['Multinationals'] == 'Multinationals'
    assert last_sklearn_n1_prep['Multinationals'] == 'Multinational'
    assert last_sklearn_n2['Multinationals'] == 'Multinationals'
    assert last_sklearn_n2_prep['Multinationals'] == 'Multinational'
    assert last_sklearn_n3['Multinationals'] == 'Multinationals'
    assert last_sklearn_n3_prep['Multinationals'] == 'Multinational'

    assert last_sklearn_n1['the concept'] == 'concept'
    assert last_sklearn_n1_prep['the concept'] == 'concept'
    assert last_sklearn_n2['the concept'] == 'the concept'
    assert last_sklearn_n2_prep['the concept'] == 'the concept'
    assert last_sklearn_n3['the concept'] == 'the concept'
    assert last_sklearn_n3_prep['the concept'] == 'the concept'

    assert last_sklearn_n1['Friday prayers'] == 'prayers'
    assert last_sklearn_n1_prep['Friday prayers'] == 'prayer'
    assert last_sklearn_n2['Friday prayers'] == 'Friday prayers'
    assert last_sklearn_n2_prep['Friday prayers'] == 'Friday prayer'
    assert last_sklearn_n3['Friday prayers'] == 'Friday prayers'
    assert last_sklearn_n3_prep['Friday prayers'] == 'Friday prayer'

    assert last_sklearn_n1['Algeria'] == 'Algeria'
    assert last_sklearn_n1_prep['Algeria'] == 'Algeria'
    assert last_sklearn_n2['Algeria'] == 'Algeria'
    assert last_sklearn_n2_prep['Algeria'] == 'Algeria'
    assert last_sklearn_n3['Algeria'] == 'Algeria'
    assert last_sklearn_n3_prep['Algeria'] == 'Algeria'

    ########################
    assert last_sklearn_n1['the building , a violation of the Clean Air Act'] == 'Act'
    assert last_sklearn_n1_prep['the building , a violation of the Clean Air Act'] == 'Act'
    assert last_sklearn_n2['the building , a violation of the Clean Air Act'] == 'Air Act'
    assert last_sklearn_n2_prep['the building , a violation of the Clean Air Act'] == 'Air Act'
    assert last_sklearn_n3['the building , a violation of the Clean Air Act'] == 'Clean Air Act'
    assert last_sklearn_n3_prep['the building , a violation of the Clean Air Act'] == 'Clean Air Act'

    assert last_sklearn_n1['a club playing in the Fourth National division'] == 'division'
    assert last_sklearn_n1_prep['a club playing in the Fourth National division'] == 'division'
    assert last_sklearn_n2['a club playing in the Fourth National division'] == 'National division'
    assert last_sklearn_n2_prep['a club playing in the Fourth National division'] == 'National division'
    assert last_sklearn_n3['a club playing in the Fourth National division'] == 'Fourth National division'
    assert last_sklearn_n3_prep['a club playing in the Fourth National division'] == 'Fourth National division'

    assert last_sklearn_n1['an English football player and manager'] == 'manager'
    assert last_sklearn_n1_prep['an English football player and manager'] == 'manager'
    assert last_sklearn_n2['an English football player and manager'] == 'and manager'
    assert last_sklearn_n2_prep['an English football player and manager'] == 'and manager'
    assert last_sklearn_n3['an English football player and manager'] == 'player and manager'
    assert last_sklearn_n3_prep['an English football player and manager'] == 'player and manager'

    assert last_sklearn_n1['terms of its righteousness'] == 'righteousness'
    assert last_sklearn_n1_prep['terms of its righteousness'] == 'righteousness'
    assert last_sklearn_n2['terms of its righteousness'] == 'its righteousness'
    assert last_sklearn_n2_prep['terms of its righteousness'] == 'its righteousness' 
    assert last_sklearn_n3['terms of its righteousness'] == 'of its righteousness'
    assert last_sklearn_n3_prep['terms of its righteousness'] == 'of its righteousness' 

    assert last_sklearn_n1['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'England'
    assert last_sklearn_n1_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'England'
    assert last_sklearn_n2['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Nottinghamshire England'
    assert last_sklearn_n2_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Nottinghamshire England'
    assert last_sklearn_n3['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Wolds Nottinghamshire England'
    assert last_sklearn_n3_prep['a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England'] == 'Wolds Nottinghamshire England'

    assert last_sklearn_n1["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'whites'
    assert last_sklearn_n1_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'white'
    assert last_sklearn_n2["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the whites'
    assert last_sklearn_n2_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'the white'
    assert last_sklearn_n3["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'of the whites'
    assert last_sklearn_n3_prep["the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"] == 'of the white'

    assert last_sklearn_n1['present Erwin Arnada -- now at large --'] == 'large'
    assert last_sklearn_n1_prep['present Erwin Arnada -- now at large --'] == 'large'
    assert last_sklearn_n2['present Erwin Arnada -- now at large --'] == 'at large'
    assert last_sklearn_n2_prep['present Erwin Arnada -- now at large --'] == 'at large'
    assert last_sklearn_n3['present Erwin Arnada -- now at large --'] == 'now at large'
    assert last_sklearn_n3_prep['present Erwin Arnada -- now at large --'] == 'now at large'

    assert last_sklearn_n1["the percentage of Americans who do `` real exercise to build the heart ''"] == 'heart'
    assert last_sklearn_n1_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'heart'
    assert last_sklearn_n2["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the heart'
    assert last_sklearn_n2_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'the heart'
    assert last_sklearn_n3["the percentage of Americans who do `` real exercise to build the heart ''"] == 'build the heart'
    assert last_sklearn_n3_prep["the percentage of Americans who do `` real exercise to build the heart ''"] == 'build the heart'

    assert last_sklearn_n1['the sound `` I Can See Clearly Now'] == 'Now'
    assert last_sklearn_n1_prep['the sound `` I Can See Clearly Now'] == 'Now'
    assert last_sklearn_n2['the sound `` I Can See Clearly Now'] == 'Clearly Now'
    assert last_sklearn_n2_prep['the sound `` I Can See Clearly Now'] == 'Clearly Now'
    assert last_sklearn_n3['the sound `` I Can See Clearly Now'] == 'See Clearly Now'
    assert last_sklearn_n3_prep['the sound `` I Can See Clearly Now'] == 'See Clearly Now'

    assert last_sklearn_n1['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Lilas'
    assert last_sklearn_n1_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'Lilas'
    assert last_sklearn_n2['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'as Lilas'
    assert last_sklearn_n2_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'as Lilas'
    assert last_sklearn_n3['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'known as Lilas'
    assert last_sklearn_n3_prep['Paul Gauguin -LRB- also known as Lilas -RRB-'] == 'known as Lilas'

    assert last_sklearn_n1['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'driver'
    assert last_sklearn_n1_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'driver'
    assert last_sklearn_n2['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Valley driver'
    assert last_sklearn_n2_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Valley driver'
    assert last_sklearn_n3['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Death Valley driver'
    assert last_sklearn_n3_prep['Front Line member Eric Young in the main event , which he lost after Young pinned him following a Death Valley driver'] == 'Death Valley driver'

    assert last_sklearn_n1['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Roseau'
    assert last_sklearn_n1_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Roseau'
    assert last_sklearn_n2['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Dominica Roseau'
    assert last_sklearn_n2_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'Dominica Roseau'
    assert last_sklearn_n3['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'of Dominica Roseau'
    assert last_sklearn_n3_prep['Interior of Dominica Photo by Ken Bosma The capital of Dominica , Roseau ,'] == 'of Dominica Roseau'

    assert last_sklearn_n1['the O.J . Simpson trial'] == 'trial'
    assert last_sklearn_n1_prep['the O.J . Simpson trial'] == 'trial'
    assert last_sklearn_n2['the O.J . Simpson trial'] == 'Simpson trial'
    assert last_sklearn_n2_prep['the O.J . Simpson trial'] == 'Simpson trial'
    assert last_sklearn_n3['the O.J . Simpson trial'] == 'the Simpson trial'
    assert last_sklearn_n3_prep['the O.J . Simpson trial'] == 'the Simpson trial'

    