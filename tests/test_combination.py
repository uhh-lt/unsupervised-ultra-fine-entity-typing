import json
import combination
import random 


def test_combine():
    f = open('../open_type/release/crowd/test.json', "r")
    data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    # test-1: when giving first and second, results should be the same -- w/o exclusion, w/o limit
    with open('predictions_jobimtext/predictions_test_open_type_with_\
jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json', 'r') as f:    
        predictions_jobimtext = json.load(f)

    with open('../open_type/best_model/test.json', 'r') as f:
        predictions_ufet = json.load(f)

    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])
        
    # test-2: the gold results should be the same -- with exclusion, w/o limit
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])
        
    # test-3: when giving first and second, results should be the same -- w/o exclusion, with limit
    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext,
                                       limit_number=limit_number)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext,
                                       limit_number=limit_number)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext,
                                       limit_number=limit_number)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext,
                                       limit_number=limit_number)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions1 = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet, predictions_second=predictions_jobimtext,
                                       limit_number=limit_number)

    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])
        
    # test-4: when giving first and second, results should be the same -- with exclusion, with limit
    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_,
                                       limit_number=limit_number)
    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_,
                                       limit_number=limit_number)
    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_,
                                       limit_number=limit_number)
    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_,
                                       limit_number=limit_number)
    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])

    # 5 random limit numbers tried
    limit_number = random.randint(1,20)
    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext) 
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet) 
    
    predictions1 = combination.combine(predictions_first=predictions_jobimtext_, predictions_second=predictions_ufet_,
                                       limit_number=limit_number)
    predictions2 = combination.combine(predictions_first=predictions_ufet_, predictions_second=predictions_jobimtext_,
                                       limit_number=limit_number)
    for k, v in predictions1.items():
        assert set(predictions2[k]['gold']) == set(v['gold'])
        assert set(predictions2[k]['pred']) == set(v['pred'])
    
    # test-6: check number of predictions lower than limit -- w/o exclude
    limit_number = random.randint(1,20)
    predictions = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)

    for k, v in predictions.items():
        # multiply by 2, since limit is applied, separately
        assert len(v['pred']) <= 2 * limit_number

    # test-7: check number of predictions lower than limit -- with exclude
    limit_number = random.randint(1,20)
    predictions_jobimtext = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext)   
    predictions_ufet = combination.exclude_pronouns(data=data,predictions=predictions_ufet)
    
    predictions = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)

    for k, v in predictions.items():
        # multiply by 2, since limit is applied, separately
        assert len(v['pred']) <= 2 * limit_number
    
    # test-8: if limited, the first n should be first set of predictions, and second one in second predictions
    limit_number = random.randint(1,20)
    predictions = combination.combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                                       limit_number=limit_number)

    for k, v in predictions.items():
        # len_first is taken, since the number of prediction can be lower than limit_number
        if len(predictions_jobimtext[k]['pred']) < limit_number:
            len_first = len(predictions_jobimtext[k]['pred'][:limit_number])
        else:
            len_first = limit_number
        assert v['pred'][:len_first] == predictions_jobimtext[k]['pred'][:limit_number]
        assert v['pred'][len_first:] == predictions_ufet[k]['pred'][:limit_number]
        
    # test bash run results: read the files and check the first part should be in the first file and 
    # the second part should be in the second file.
    with open('predictions_jobimtext/predictions_test_open_type_with_\
jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json', 'r') as f:    
        predictions_jobimtext = json.load(f)

    with open('../open_type/best_model/test.json', 'r') as f:
        predictions_ufet = json.load(f)
   
    pronouns = {'i', 'me', 'myself', 'we', 'us', 'ourselves', 'he', 'him', 'himself', 'she', 'her', 'herself',
                'it', 'itself', 'they', 'them', 'themselves', 'you', 'yourself'}
    
    with open('predictions_combination/predictions_test_combination_wo_limit_wo_exclude.json', 'r') as f:    
        predictions_combination_wo_limit_wo_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_wo_limit_wo_exclude_check.json', 'r') as f:    
        predictions_combination_wo_limit_wo_exclude_check = json.load(f)

    count = 0
    for k, v in predictions_combination_wo_limit_wo_exclude.items():
        assert set(v['gold']) == set(predictions_combination_wo_limit_wo_exclude_check[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_wo_limit_wo_exclude_check[k]['pred'])

        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])

        assert v['pred'][:len(predictions_jobimtext[k]['pred'])] == predictions_jobimtext[k]['pred']
        assert v['pred'][len(predictions_jobimtext[k]['pred']):] == predictions_ufet[k]['pred']
        count += 1
    assert count == 1998

    assert len(predictions_combination_wo_limit_wo_exclude) == len(predictions_combination_wo_limit_wo_exclude_check)

    count = 0
    with open('predictions_combination/predictions_test_combination_wo_limit_exclude.json', 'r') as f:    
        predictions_combination_wo_limit_with_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_wo_limit_exclude_check.json', 'r') as f:    
        predictions_combination_wo_limit_with_exclude_check = json.load(f)

    for k, v in predictions_combination_wo_limit_with_exclude.items():
        assert set(v['gold']) == set(predictions_combination_wo_limit_with_exclude_check[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_wo_limit_with_exclude_check[k]['pred'])

        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])

        assert v['pred'][:len(predictions_jobimtext[k]['pred'])] == predictions_jobimtext[k]['pred']
        assert v['pred'][len(predictions_jobimtext[k]['pred']):] == predictions_ufet[k]['pred']
        count += 1
    assert count == 1210

    assert len(predictions_combination_wo_limit_with_exclude) == len(predictions_combination_wo_limit_with_exclude_check)

    count = 0
    with open('predictions_combination/predictions_test_combination_limit5_wo_exclude.json', 'r') as f:    
        predictions_combination_limit5_wo_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_limit5_wo_exclude_check.json', 'r') as f:    
        predictions_combination_limit5_wo_exclude_check = json.load(f)

    for k, v in predictions_combination_limit5_wo_exclude.items():
        assert set(v['gold']) == set(predictions_combination_limit5_wo_exclude_check[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_limit5_wo_exclude_check[k]['pred'])

        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])

        limit = 5 if len(predictions_jobimtext[k]['pred']) >= 5 else len(predictions_jobimtext[k]['pred'])
        assert v['pred'][:limit] == predictions_jobimtext[k]['pred'][:limit]
        assert v['pred'][limit:] == predictions_ufet[k]['pred'][:5]
        assert len(v['pred']) <= 10
        count += 1
    assert count == 1998

    assert len(predictions_combination_limit5_wo_exclude) == len(predictions_combination_limit5_wo_exclude_check)

    count = 0
    with open('predictions_combination/predictions_test_combination_limit5_exclude.json', 'r') as f:    
        predictions_combination_limit5_with_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_limit5_exclude_check.json', 'r') as f:    
        predictions_combination_limit5_with_exclude_check = json.load(f)

    for k, v in predictions_combination_limit5_with_exclude.items():
        assert set(v['gold']) == set(predictions_combination_limit5_with_exclude_check[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_limit5_with_exclude_check[k]['pred'])

        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])

        limit = 5 if len(predictions_jobimtext[k]['pred']) >= 5 else len(predictions_jobimtext[k]['pred'])
        assert v['pred'][:limit] == predictions_jobimtext[k]['pred'][:limit]
        assert v['pred'][limit:] == predictions_ufet[k]['pred'][:5]
        assert len(v['pred']) <= 10
        count += 1
    assert count == 1210

    assert len(predictions_combination_limit5_with_exclude) == len(predictions_combination_limit5_with_exclude_check)


def test_exclude_pronouns():
    f = open('../open_type/release/crowd/test.json', "r")
    data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    # test-1: all returned info should be in the original ones
    with open('predictions_jobimtext/predictions_test_open_type_with_\
jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json', 'r') as f:   
        predictions_jobimtext = json.load(f)

    with open('../open_type/best_model/test.json', 'r') as f:
        predictions_ufet = json.load(f)

    predictions_jobimtext_ = combination.exclude_pronouns(data=data, predictions=predictions_jobimtext)
    predictions_ufet_ = combination.exclude_pronouns(data=data, predictions=predictions_ufet)
    
    for k, v in predictions_jobimtext_.items():
        original_predictions = predictions_jobimtext[k]['pred']
        for p in v['pred']:
            assert p in original_predictions

    for k, v in predictions_ufet_.items():
        original_predictions = predictions_ufet[k]['pred']
        for p in v['pred']:
            assert p in original_predictions
    
    # test-2: pronouns should not be in the predictions
    pronouns = {'i', 'me', 'myself', 'we', 'us', 'ourselves', 'he', 'him', 'himself', 'she', 'her', 'herself',
                'it', 'itself', 'they', 'them', 'themselves', 'you', 'yourself'}
    count = 0
    for mention_info in data:
        if mention_info['mention_span'].lower() in pronouns:
            assert mention_info['annot_id'] not in predictions_jobimtext_.keys()
            assert mention_info['annot_id'] not in predictions_ufet_.keys()
            continue
        count += 1

    assert count == len(predictions_jobimtext_)
    assert count == len(predictions_ufet_)
    
    # test exclude pronouns on written file.
    with open('predictions_jobimtext/predictions_test_open_type_with_\
jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json', 'r') as f:    
        predictions_jobimtext = json.load(f)

    with open('../open_type/best_model/test.json', 'r') as f:
        predictions_ufet = json.load(f)
        
    with open('predictions_combination/\
predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050_wo_pronouns.json', "r") as f:
        predictions_jobimtext_check_ = json.load(f)
    
    with open('predictions_combination/predictions_test_ufet_wo_pronouns.json', "r") as f:
        predictions_ufet_check_ = json.load(f)

    assert len(predictions_jobimtext_check_) == 1210
    assert len(predictions_ufet_check_) == 1210


    for k, v in predictions_ufet_check_.items():
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])
        assert set(v['pred']) == set(predictions_ufet[k]['pred'])

        assert set(v['gold']) == set(predictions_jobimtext_check_[k]['gold'])
        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])

    for k, v in predictions_jobimtext_check_.items():
        assert set(v['gold']) == set(predictions_jobimtext[k]['gold'])
        assert set(v['pred']) == set(predictions_jobimtext[k]['pred'])

        assert set(v['gold']) == set(predictions_ufet_check_[k]['gold'])
        assert set(v['gold']) == set(predictions_ufet[k]['gold'])
        
        
### tests for the converted cases:
def test_converted():
    # test-1: all predictions are in the original predictions
    # wo limit wo exclude
    with open('predictions_combination/predictions_test_combination_wo_limit_wo_exclude.json', 'r') as f:    
        predictions_combination_wo_limit_wo_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_wo_limit_wo_exclude_converted.json', 'r') as f:    
        predictions_combination_wo_limit_wo_exclude_converted = json.load(f)
        
    # with limit wo exclude
    with open('predictions_combination/predictions_test_combination_limit5_wo_exclude.json', 'r') as f:    
        predictions_combination_limit5_wo_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_limit5_wo_exclude_converted.json', 'r') as f:    
        predictions_combination_limit5_wo_exclude_converted = json.load(f)
        
    # wo limit with exclude
    with open('predictions_combination/predictions_test_combination_wo_limit_exclude.json', 'r') as f:    
        predictions_combination_wo_limit_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_wo_limit_exclude_converted.json', 'r') as f:    
        predictions_combination_wo_limit_exclude_converted = json.load(f)
        
    # with limit with exclude
    with open('predictions_combination/predictions_test_combination_limit5_exclude.json', 'r') as f:    
        predictions_combination_limit5_exclude = json.load(f)

    with open('predictions_combination/predictions_test_combination_limit5_exclude_converted.json', 'r') as f:    
        predictions_combination_limit5_exclude_converted = json.load(f)
    
    f = open('../open_type/release/crowd/test.json', "r")
    data = [json.loads(sent.strip()) for sent in f.readlines()]
    
    # test-1: all converted info should be in the original ones
    for k, v in predictions_combination_wo_limit_wo_exclude_converted.items():
        assert set(v['gold']) == set(predictions_combination_wo_limit_wo_exclude[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_wo_limit_wo_exclude[k]['pred'])
        
        original_predictions = predictions_combination_wo_limit_wo_exclude[k]['pred']
        for p in v['pred']:
            assert p in original_predictions
        
            
    for k, v in predictions_combination_limit5_wo_exclude_converted.items():
        assert set(v['gold']) == set(predictions_combination_limit5_wo_exclude[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_limit5_wo_exclude[k]['pred'])
        
        original_predictions = predictions_combination_limit5_wo_exclude[k]['pred']
        for p in v['pred']:
            assert p in original_predictions
            
    for k, v in predictions_combination_wo_limit_exclude_converted.items():
        assert set(v['gold']) == set(predictions_combination_wo_limit_exclude[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_wo_limit_exclude[k]['pred'])
        
        original_predictions = predictions_combination_wo_limit_exclude[k]['pred']
        for p in v['pred']:
            assert p in original_predictions
            
    for k, v in predictions_combination_limit5_exclude_converted.items():
        assert set(v['gold']) == set(predictions_combination_limit5_exclude[k]['gold'])
        assert set(v['pred']) == set(predictions_combination_limit5_exclude[k]['pred'])
        
        original_predictions = predictions_combination_limit5_exclude[k]['pred']
        for p in v['pred']:
            assert p in original_predictions


    
    # test-2: pronouns should not be in the predictions for exclude cases
    pronouns = {'i', 'me', 'myself', 'we', 'us', 'ourselves', 'he', 'him', 'himself', 'she', 'her', 'herself',
                'it', 'itself', 'they', 'them', 'themselves', 'you', 'yourself'}
    count = 0
    for mention_info in data:
        if mention_info['mention_span'].lower() in pronouns:
            assert mention_info['annot_id'] not in predictions_combination_wo_limit_exclude.keys()
            assert mention_info['annot_id'] not in predictions_combination_limit5_exclude.keys()
            
            assert mention_info['annot_id'] not in predictions_combination_wo_limit_exclude_converted.keys()
            assert mention_info['annot_id'] not in predictions_combination_limit5_exclude_converted.keys()
            continue
        count += 1

    assert count == len(predictions_combination_wo_limit_exclude_converted)
    assert count == len(predictions_combination_limit5_exclude_converted)
    assert count == 1210
    
    
    assert 1998 == len(predictions_combination_wo_limit_wo_exclude_converted)
    assert 1998 == len(predictions_combination_limit5_wo_exclude_converted)
