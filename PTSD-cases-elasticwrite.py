# Imports of import.
import json
import os

from datetime import datetime
from elastic_search_wrapper import ElasticSearchWrapper

# https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html



def elasticsearch_publish(data_path, eurl):


    es = ElasticSearchWrapper(esurl)
    # es.smoketest()


    caseIndex = 'la-case'
    es.delete_index(caseIndex)

    paragraphIndex = 'la-paragraph'
    es.delete_index(paragraphIndex)
    
    sentenceIndex = 'la-sentence'
    es.delete_index(sentenceIndex)

    ## NOTE: can't merge a non object mapping 
    ##The error message means that you are trying to change an existing mapping. However, that is not possible in Elasticsearch. Once a mapping has been created, it cannot be changed.
    ## https://stackoverflow.com/questions/44435624/can-t-merge-a-non-object-mapping-with-an-object-mapping-error-in-machine-learnin
    
    # Getting the list of files in <data_path>:
    list_of_files = os.listdir(data_path)

    # ...and creating new lists for the texts of the sentences...
    sentenceCount = 0
    paragraphCount = 0
    caseCount = 0

                
    # print(list_of_files)
    # Using a for-loop to iterate over the filenames...
    for filename in list_of_files:
        # print ( f"{data_path}/{filename}" )
        if ( filename.find('.json') == -1):
            continue
        
        print ( f"")

        # ... and opening the given filename...
        file = open(f"{data_path}/{filename}", encoding="utf8")
        print ( f"working on case  {data_path}/{filename}" )

        data = json.load(file)
        data['ruleTree'] = {}
        
        sentence_lookup = dict()

        try:

# "probability": {
#     "author": "enriched",
#     "rhetClass": 91
# }, 
            # loop through and fix  probability.rhetClass  issue
            if data.get('sentences') is None:
                print('sentences is None', filename)
                continue   
        
            sentences =  data['sentences']
            for sentence in sentences:
                probability = sentence.get('probability')
                if probability is not None:
                    rhetClass = probability.get('rhetClass')
                    if isinstance(rhetClass, int):
                        #print(type(rhetClass),rhetClass) 
                        rhetClass = float(rhetClass)
                        #print(type(rhetClass),rhetClass) 
                        probability['rhetClass'] = rhetClass         
                 
            # ...and adding the sentences to those new lists...
            sentences =  data['sentences']
            for sentence in sentences:
                sentID = sentence['sentID']
                sentence_lookup[sentID] = sentence


                enrichment = sentence['enrichmentSet']

                rhetClass = enrichment.get('rhetClass')
                if rhetClass is None:
                    rhetClass = {}
                   
                polarity = enrichment.get('polarity')
                if polarity is None:
                    polarity = {}
                    polarity['classification'] = 'unknown'


# "ruleID": {
#     "text": "(d)  Opine whether it is at least as likely as not (50 percent or greater probability) that a diagnosis of PTSD is related to a fear of hostile military or terrorist activity during service.",
#     "classification": "SC_1.2",
#     "predictions": {
#         "SC_1": "0.14995848",
#         "SC_1.1": "0.15441038",
#         "SC_1.2": "0.4503781",
#         "SC_1.3": "0.24525304"
#     }
# }
                

                ruleID = enrichment.get('ruleID')
                if ruleID is None:
                    ruleID = {}
                    ruleID['classification'] = 'unknown'
                else:
                    pred = ruleID['predictions'];
                    ruleID['predictions'] = {}          # it does not like the "SC_1.1"  as a name for prediction key
                    ruleID['predictions']['SC_1'] = pred['SC_1']
                    ruleID['predictions']['SC_1_1'] = pred['SC_1.1']
                    ruleID['predictions']['SC_1_2'] = pred['SC_1.2']
                    ruleID['predictions']['SC_1_3'] = pred['SC_1.3']

                sentence['rhetClass'] = rhetClass['classification']
                sentence['polarity'] = polarity['classification']
                sentence['ruleID'] = ruleID['classification']
                        
                enrichment['rhetClass'] = rhetClass
                enrichment['polarity'] = polarity
                enrichment['ruleID'] = ruleID 
                
                res = es.add_item(sentenceIndex, sentenceCount, sentence)
                
                sentenceCount += 1
                ## print(F"Sentence count {sentenceCount}")

        except Exception as ex:
            print('Sentence EXCEPTION', ex, filename)


        try:

            # after some mods then replace sentences
            data['sentences'] = sentences
            res = es.add_item(caseIndex, caseCount, data)
            caseCount += 1

            print(F"case count {caseCount}  sentence count: {sentenceCount}")
        except Exception as ex:
            print('Case EXCEPTION', ex, filename)

          

        if data.get('paragraphs') is None:
            print('...no paragraphs')
            continue   
                
        paragraphs = data['paragraphs']  
        for paragraph in paragraphs:

            try:
                paraID = paragraph['paraID']
                sentIDList = paragraph['sentIDList']
                paragraph['sentences'] = []
                for sentID in sentIDList:
                    sentence = sentence_lookup[sentID]
                    if sentence is not None:
                        paragraph['sentences'].append(sentence)


                res = es.add_item(paragraphIndex, paragraphCount, paragraph)
                paragraphCount += 1

                ## print(F"para count {paragraphCount} {paraID} {filename}")

            except Exception as ex:
                 print('paragraph EXCEPTION', ex, filename)  
     
     
if __name__ == "__main__":                
    # Getting the list of files in <data_path>:
    data_path = './1-The_FS-PTSD_Dataset'
    data_path = './PTSD-Paragraph-cases'
    
    #  https://elasticsearch-py.readthedocs.io/en/master/
    # by default we connect to localhost:9200
    esurl = 'http://localhost:9200'
    
    data_path = './3-The_Curated_SRS_Dataset'
    esurl = 'https://legalapprenticedb.azurewebsites.net'
    
    elasticsearch_publish(data_path, esurl)



# python PTSD-cases-elasticwrite.py
#  docker run -d -p 9200:9200 --name elasticsearch elasticsearch
#  use this for persistent storage
#  docker run -d -p 9200:9200 -p 9300:9300 -v data:/usr/share/elasticsearch/data --name elasticsearch elasticsearch
