import requests
import logging
import time


# for a query mention and cluster type, returns a response from jobimtext api
# -- http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
# http://ltmaggie.informatik.uni-hamburg.de/jobimtext/jobimviz-web-demo/api-and-demo-documentation/#API
# -- term operations
def get_senses_from_jobimtext(mention, cluster_type):
    # there are 3 clustering options in JoBimText
    assert cluster_type in ["200,200", "200,50", "50,50"]
    
    if len(mention.split()) > 1:
        r_url = 'http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws/api/ccDepNEMWE/jo/senses/' \
                 + mention + '%23MWE' + '?sensetype=CW(' + cluster_type + ')&format=json'
    else:
        r_url = 'http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws/api/ccDepNEMWE/jo/senses/' \
                 + mention + '%23NN' + '?sensetype=CW(' + cluster_type + ')&format=json'
    response = requests.get(r_url)
    
    try:
        return response.json()['result']
    except:
        logging.info('No result from API call of ' + mention +
                     ' --- response status code: ' + str(response.status_code))
        if response.status_code == 200:
            logging.info('response json: ' + str(response.json()))
        # from logging, I recognized sometimes 502, although everything seems ok.
        # for them, I tried 10 times until I get a response.
        if response.status_code != 200:
            for i in range(10):
                logging.info(str(i+1) + '. try for status code: ' + str(response.status_code))
                time.sleep(3)
                response = requests.get(r_url)
                try:
                    return response.json()['result']
                except:
                    logging.info('did not work once more: ' + str(response.status_code))
        # for two mentions, exception from API -- for dev
        # EXCEPT: EEC/EC interior and justice ministers
        # EXCEPT: Catholics
        # for test -- EXCEPT: the Richard Rodgers/Stephen Sondheim
        # print('EXCEPT:', mention)
        return []
        
        
# TODO: the same function as preprocess in preprocess.py -- write them in common utils in one function.
# singularize the label
def postprocess(label, inflect_engine, nlp):
    singular_label = inflect_engine.singular_noun(label)

    # for the cases like "actress" or "a focus", cross-check with stanza's feats of 'Number=Plur'
    feats = nlp(label).sentences[0].words[-1].feats
    if (label[-1] == 's' or label[-1] == 'S') and feats and 'Number=Plur' in feats.split('|') and \
            singular_label:
        return singular_label
    elif label[-1] != 's' and label[-1] != 'S' and singular_label:
        return singular_label

    return label


# since 'thing' is the most common, we thought it is noisy.
def process_jobimtext_result(result, noisy_isas, number_of_cluster_terms=None, number_of_isas=None,
                             apply_postprocess=False, nlp=None, inflect_engine=None, types=None):
    sense_terms = result['senses']
    
    # take only terms, since we do not need tag information
    # remove the sense terms starting with "^" 
    splitted = [s.split('#')[0] for s in sense_terms if not s.startswith('^')]
    pruned = []
    for i in splitted:
        # not add already added ones
        if i not in pruned:
            pruned.append(i)
            
    # limiting the term number
    if number_of_cluster_terms:
        senses = pruned[:number_of_cluster_terms]
    else:
        senses = pruned
    
    isas = result['isas']
    if isas:
        # take only isas words, since we do not use frequency information
        isas = [i.split(':')[0] for i in isas if i.split(':')[0] not in noisy_isas]

        if apply_postprocess and isas:
            isas_new = []
            for label in isas:
                # 1-step: singularize
                singular_label = postprocess(label=label, inflect_engine=inflect_engine, nlp=nlp)
                # 2-step: if the label multi token, put underscore
                underscored_label = singular_label.replace(' ', '_')
                # 3-step: lowerize the label
                lowerized_label = underscored_label.lower()
                if lowerized_label not in isas_new and lowerized_label not in noisy_isas:
                    # 4-step: if it is in type set, include it.
                    # it is done here, since the number of isas limited here
                    if types:
                        if lowerized_label in types:
                            isas_new.append(lowerized_label)
                    else:
                        isas_new.append(lowerized_label)

            isas = isas_new

        # limiting the isas number
        if number_of_isas:
            isas = isas[:number_of_isas]
    
    return senses, isas
