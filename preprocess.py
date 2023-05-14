import logging
# https://universaldependencies.org/docsv1/en/overview/tokenization.html
# https://github.com/UniversalDependencies/UD_English-EWT/issues/1
# LRB (Left Round Bracket) and RRB (Right Round Brackets)
# -- https://stackoverflow.com/questions/37536068/removing-special-characters-from-txt-file-give-lrb-lsb-rsb-lrb
# removed -LRB- and -RRB- by assuming, the above definitions are applied here as well.


# singularize the mention
def preprocess(mention, inflect_engine, nlp):
    singular_mention = inflect_engine.singular_noun(mention)

    # for the cases like "actress" or "a focus", cross-check with stanza's feats of 'Number=Plur'
    feats = nlp(mention).sentences[0].words[-1].feats
    if (mention[-1] == 's' or mention[-1] == 'S') and feats and 'Number=Plur' in feats.split('|') and \
            singular_mention:
        return singular_mention
    elif mention[-1] != 's' and mention[-1] != 'S' and singular_mention:
        return singular_mention

    return mention
    
    
# nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')    
# tried for n=1,2,3
def get_first_ngram_of_mentions(mentions, n, inflect_engine, nlp, apply_preprocess=True):
    # ngram search
    # based on the info here: https://stackoverflow.com/questions/13423919/computing-n-grams-using-python
    # https://stackoverflow.com/questions/32441605/generating-ngrams-unigrams-bigrams-etc-from-a-large-corpus-of-txt-files-and-t
    # I used nltk -- https://www.nltk.org/api/nltk.util.html#nltk.util.ngrams
    from nltk.util import ngrams 
    from string import punctuation
    
    processed_mentions = {}
    
    # 1) filter punctuations:   for mentions, like "the building , a violation of the Clean Air Act"
    # 2) -LRB-, -RRB-:   "the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"
    # 3) --:   "present Erwin Arnada -- now at large --"
    # 4) '':   "the percentage of Americans who do `` real exercise to build the heart ''"
    filter_list = [item for item in punctuation]
    filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
    
    mentions = set(mentions)
    count_less, count_assertion_err = 0, 0
    for mention in mentions:
        if len(mention.split()) == 1:
            search_token = mention
        # multi-token
        else:
            mention_ = [token for token in mention.split() if token not in filter_list]
            ngram_list = list(ngrams(mention_, n))
            
            if n == 1:
                # check if ngram_list is not empty, when n==1
                assert ngram_list
                assert len(ngram_list[-1]) == n
                # remove a-an-the to prevent that the search token is just "a/an/the", 
                # for the mentions like "the piano"
                # Note that [0] index is taken, since when n=1, the ngrams are like 
                # "golf gear" --> [('golf',), ('gear',)] 
                if not ngram_list[0][0] in ['a', 'an', 'the', 'A', 'An', 'The']:
                    search_token = ngram_list[0][0]
                else:
                    search_token = ngram_list[1][0]
            else:
                if n == 3 and not ngram_list:
                    # if n=3, and the mentions length is 2, we take the mention as it is.
                    search_token = ' '.join(mention_)
                    count_less += 1
                else:
                    # check if ngram_list is not empty, when n==2
                    assert ngram_list
                    assert len(ngram_list[0]) == n
                    search_token = ' '.join(ngram_list[0])
            try:
                assert len(search_token.split()) == n
            except AssertionError:
                count_assertion_err += 1
                
        # check if search_token is assigned
        assert search_token
        if apply_preprocess:
            search_token = preprocess(mention=search_token, inflect_engine=inflect_engine, nlp=nlp)
            
        processed_mentions[mention] = search_token
    
    assert len(processed_mentions) == len(mentions)
    assert count_assertion_err == count_less
    return processed_mentions


# nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
# tried for n=1,2,3
def get_last_ngram_of_mentions(mentions, n, inflect_engine, nlp, apply_preprocess=True):
    # ngram search
    # based on the info here: https://stackoverflow.com/questions/13423919/computing-n-grams-using-python
    # https://stackoverflow.com/questions/32441605/generating-ngrams-unigrams-bigrams-etc-from-a-large-corpus-of-txt-files-and-t
    # I used nltk -- https://www.nltk.org/api/nltk.util.html#nltk.util.ngrams
    from nltk.util import ngrams 
    from string import punctuation
    
    processed_mentions = {}
    
    # 1) filter punctuations for mentions, like 
    # "a parish church in the Church of England in Willoughby on the Wolds , Nottinghamshire , England"
    # 2) -LRB-, -RRB-, "the settlement Tubabodaga -LRB- '' village of the whites '' -RRB-"
    # 3) -- "present Erwin Arnada -- now at large --"
    # 4) '' "the percentage of Americans who do `` real exercise to build the heart ''"
    filter_list = [item for item in punctuation]
    filter_list.extend(["-LRB-", "-RRB-", "--", "''", "``"])
    
    mentions = set(mentions)
    count_less, count_assertion_err = 0, 0
    for mention in mentions:
        if len(mention.split()) == 1:
            search_token = mention
        # multi-token
        else:
            mention_ = [token for token in mention.split() if token not in filter_list]
            ngram_list = list(ngrams(mention_, n))
            
            if n == 1:
                # check if ngram_list is not empty, when n==1
                assert ngram_list
                assert len(ngram_list[-1]) == n
                search_token = ngram_list[-1][0]
            else:
                if n == 3 and not ngram_list:
                    # if n=3, and the mentions length is 2, we take the mention as it is.
                    search_token = ' '.join(mention_)
                    count_less += 1
                else:
                    assert ngram_list
                    assert len(ngram_list[-1]) == n
                    search_token = ' '.join(ngram_list[-1])
            try:  
                assert len(search_token.split()) == n
            except AssertionError:
                count_assertion_err += 1
        
        # check if search_token is assigned
        assert search_token        
        if apply_preprocess:
            search_token = preprocess(mention=search_token, inflect_engine=inflect_engine, nlp=nlp)

        processed_mentions[mention] = search_token
    
    assert len(processed_mentions) == len(mentions)
    assert count_assertion_err == count_less
    return processed_mentions


# nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
# tried for n=1,2,3
def get_first_ngram_of_mentions_sklearn(mentions, n, inflect_engine, nlp, apply_preprocess=True):
    # https://stackoverflow.com/questions/13423919/computing-n-grams-using-python
    # https://practicaldatascience.co.uk/machine-learning/how-to-use-count-vectorization-for-n-gram-analysis
    from sklearn.feature_extraction.text import CountVectorizer
    
    processed_mentions = {}
    
    vector = CountVectorizer(ngram_range=(n, n), lowercase=False)
    analyser = vector.build_analyzer()
    # since it can filter the punctuation itself, we did not add punctuation
    filter_list = ["-LRB-", "-RRB-"]
    
    mentions = set(mentions)
    count_less, count_more, count_assertion_err = 0, 0, 0
    for mention in mentions:
        if len(mention.split()) == 1:
            search_token = mention
        # multi-token
        else:
            mention_ = ' '.join([token for token in mention.split() if token not in filter_list])
            ngram_list = analyser(mention_)
            
            if n == 1:
                # check if ngram_list is not empty, when n==1
                assert ngram_list
                assert len(ngram_list[-1].split()) == n
                # remove an-the to prevent that the search token is just "an/the", 
                # note: "a" is already removed in sklearn, since its length < 2. 'token_pattern' -- 
                # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
                # for the mentions like "the piano"
                if not ngram_list[0] in ['an', 'the', 'An', 'The']:
                    search_token = ngram_list[0]
                else:
                    try:
                        search_token = ngram_list[1]
                    # for the mentions like 'the U.S.', U.S. removed and only 'the' remained
                    # for these cases, we take the mention as it is.
                    except IndexError:
                        search_token = mention_
                        count_more += 1
            else:
                if not ngram_list:
                    # if n=2,3, and no ngrams with this length is produced, we take the mention as it is.
                    search_token = mention_
                    # for cases, like 'a spot', 'the U.S.'; it may not return anything
                    if len(mention_.split()) == n:
                        count_less -= 1
                    count_less += 1
                else:
                    assert len(ngram_list[0].split()) == n
                    search_token = ngram_list[0]
            try:
                assert len(search_token.split()) == n
            except AssertionError:
                count_assertion_err += 1
                
        # check if search_token is assigned
        assert search_token
        if apply_preprocess:
            search_token = preprocess(mention=search_token, inflect_engine=inflect_engine, nlp=nlp)
            
        processed_mentions[mention] = search_token
    
    assert len(processed_mentions) == len(mentions)
    # we also need to take care of "count_more" due to IndexError
    assert count_assertion_err == count_less + count_more
    return processed_mentions


# nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
# tried for n=1,2,3
def get_last_ngram_of_mentions_sklearn(mentions, n, inflect_engine, nlp, apply_preprocess=True):
    # https://stackoverflow.com/questions/13423919/computing-n-grams-using-python
    # https://practicaldatascience.co.uk/machine-learning/how-to-use-count-vectorization-for-n-gram-analysis
    # https://datascience.stackexchange.com/questions/38167/how-to-use-build-analyzer-in-sklearn-feature-extraction
    from sklearn.feature_extraction.text import CountVectorizer
    
    processed_mentions = {}
    
    vector = CountVectorizer(ngram_range=(n, n), lowercase=False)
    analyser = vector.build_analyzer()
    # since it can filter the punctuation itself, we did not add punctuation
    filter_list = ["-LRB-", "-RRB-"]
    
    mentions = set(mentions)
    count_less, count_assertion_err = 0, 0
    for mention in mentions:
        if len(mention.split()) == 1:
            search_token = mention
        # multi-token
        else:
            mention_ = ' '.join([token for token in mention.split() if token not in filter_list])
            ngram_list = analyser(mention_)
            
            if n == 1:
                # check if ngram_list is not empty, when n==1
                assert ngram_list
                assert len(ngram_list[-1].split()) == n
                search_token = ngram_list[-1]
            else:
                if not ngram_list:
                    # if n=2,3, and no ngrams with this length is produced, we take the mention as it is.
                    search_token = mention_
                    # for cases, like 'a spot', 'the U.S.'; it may not return anything
                    if len(mention_.split()) == n:
                        count_less -= 1
                    count_less += 1
                else:
                    assert len(ngram_list[-1].split()) == n
                    search_token = ngram_list[-1]
            try:  
                assert len(search_token.split()) == n
            except AssertionError:
                count_assertion_err += 1
        
        # check if search_token is assigned
        assert search_token        
        if apply_preprocess:
            search_token = preprocess(mention=search_token, inflect_engine=inflect_engine, nlp=nlp)

        processed_mentions[mention] = search_token
    
    assert len(processed_mentions) == len(mentions)
    assert count_assertion_err == count_less
    return processed_mentions


# tried head words using stanza library
# nlp should be initialized: nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
# https://stanfordnlp.github.io/stanza/depparse.html
def get_headword_of_mentions(mentions, inflect_engine, nlp, apply_preprocess=True):
    processed_mentions = {}
    count_multiple_heads = 0
    
    mentions = set(mentions)
    for mention in mentions:
        doc = nlp(mention)
        root_word = [word for sent in doc.sentences for word in sent.words if word.head == 0]
        if len(root_word) > 1:
            count_multiple_heads += 1
            logging.info('More than one head word found, the first one is selected: ' + mention
                         + ' ' + root_word[0].text)
        assert root_word[0].deprel == "root"
        assert root_word[0].head == 0
        
        if apply_preprocess:
            # singularize
            processed_mentions[mention] = preprocess(mention=root_word[0].text, inflect_engine=inflect_engine, nlp=nlp)
        else:
            processed_mentions[mention] = root_word[0].text
            
    logging.info('Total number of mentions with more than one head is: ' + str(count_multiple_heads))
    return processed_mentions, count_multiple_heads
