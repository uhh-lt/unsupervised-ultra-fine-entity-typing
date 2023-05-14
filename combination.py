import json
import argparse


def combine(predictions_first, predictions_second, limit_number=None):
    predictions_combination = {}
    if limit_number and limit_number > 0:
        for k, v in predictions_first.items():
            predictions_combination[k] = {}
            
            assert set(v['gold']) == set(predictions_second[k]['gold'])
            predictions_combination[k]['gold'] = v['gold']
            
            # use the first n predictions
            combination_pred = [p for p in v['pred'][:limit_number]]
            combination_pred.extend([p for p in predictions_second[k]['pred'][:limit_number]])
            predictions_combination[k]['pred'] = combination_pred
    else:
        for k, v in predictions_first.items():
            predictions_combination[k] = {}
            
            assert set(v['gold']) == set(predictions_second[k]['gold'])
            predictions_combination[k]['gold'] = v['gold']
            
            # use all predictions
            combination_pred = [p for p in v['pred']]
            combination_pred.extend([p for p in predictions_second[k]['pred']])
            predictions_combination[k]['pred'] = combination_pred
            
    return predictions_combination


def exclude_pronouns(data, predictions):
    # https://github.com/HKUST-KnowComp/MLMET/blob/a05d3f7adeacaa057ec3bcc488214fe8ac8ba270/prep.py#L9
    # Wikipedia -- https://en.wikipedia.org/wiki/English_pronouns#Full_list
    # it seems they take a reference for Nominative	Accusative	Reflexive
    # we also add 'yourself' and 'itself' for completion
    pronouns = {'i', 'me', 'myself', 'we', 'us', 'ourselves', 'he', 'him', 'himself', 'she', 'her', 'herself',
                'it', 'itself', 'they', 'them', 'themselves', 'you', 'yourself'}
    
    predictions_excluded = {}
    for k, v in predictions.items():
        mention = [m for m in data if m['annot_id'] == k]
        assert len(mention) == 1

        if mention[0]['mention_span'].lower() not in pronouns:
            predictions_excluded[k] = v
            
    return predictions_excluded
    

def get_parameters():
    parser = argparse.ArgumentParser(description='Performs Combination of Predictions from \
                                     Unsupervised Knowledge-Free Ultra Fine Entity \
                                     Typing using JoBimText and from UFET model provided by (Choi et al., 2018).')
    
    parser.add_argument('--jobimtext-predictions-file-path', dest='predictions_jobimtext', 
                        default="predictions_jobimtext/\
                        predictions_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim.json",
                        type=str,
                        help='determines the path for the predictions derived from using jobimtext \
                        (default is local path for the dev set \
                        -- on model headword_prepro_includeisas_inclmentionsim )') 
    
    parser.add_argument('--ufet-predictions-file-path', dest='predictions_ufet', 
                        default="../open_type/best_model/dev.json", type=str,
                        help='determines the path for the best model predictions file \
                        provided by open type (Choi et al., 2018) \
                        -- https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html \
                        (default is local path on dev set -- for best_model/dev.json)')
    
    parser.add_argument('--limit-number', dest='limit_number', default=0, type=int,
                        help='determines how many predictions from each file will be combined \
                        (default 0 means all predictions in each file will be used)')
    
    parser.add_argument('--file-path', dest='file_path', 
                        default="../open_type/release/crowd/dev.json", type=str,
                        help='determines the path for test or dev file provided by open type (Choi et al., 2018) \
                        -- https://www.cs.utexas.edu/~eunsol/html_pages/open_entity.html, which will be only used \
                        if pronouns are exluded in order to check the mention span is pronoun or not \
                        (default is local path for file release/crowd/dev.json)')
    
    exclude_pronouns_ = parser.add_mutually_exclusive_group(required=False)
    exclude_pronouns_.add_argument('--exclude-pronouns', dest='exclude_pronouns_', action='store_true',
                                  help='determines if the predictions of the pronoun mentions are excluded or not')
    exclude_pronouns_.add_argument('--not-exclude-pronouns', dest='exclude_pronouns_', action='store_false',
                                  help='determines if the predictions of the pronoun mentions are excluded or not')
    parser.set_defaults(exclude_pronouns_=False)
    
    parser.add_argument('--output-file-path', dest='output_file_path', 
                        default='predictions_combined_open_type_with_jobimtext.json', type=str,
                        help='determines the file path to store the combined predictions \
                        (default is "predictions_combined_open_type_with_jobimtext.json")')
    
    return parser.parse_args()
    
    
if __name__ == '__main__':
    args = get_parameters()
    print(args)
    
    with open(args.predictions_jobimtext, 'r') as f:
        predictions_jobimtext = json.load(f)
    
    with open(args.predictions_ufet, 'r') as f:
        predictions_ufet = json.load(f)
    
    if args.exclude_pronouns_:
        with open(args.file_path, "r") as f:
            data_lines = f.readlines()
        data_ = [json.loads(sent.strip()) for sent in data_lines]
        
        predictions_jobimtext = exclude_pronouns(data=data_, predictions=predictions_jobimtext)
        predictions_ufet = exclude_pronouns(data=data_, predictions=predictions_ufet)
            
    predictions_ = combine(predictions_first=predictions_jobimtext, predictions_second=predictions_ufet,
                           limit_number=args.limit_number)
    
    with open(args.output_file_path, "w") as f:
        json.dump(predictions_, f)
