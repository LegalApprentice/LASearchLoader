# Imports of import.
import json
import os

from datetime import datetime
from elastic_search_wrapper import ElasticSearchWrapper

# https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html



def elasticsearch_publish():

    #  https://elasticsearch-py.readthedocs.io/en/master/
    # by default we connect to localhost:9200
    es = ElasticSearchWrapper()



    es.create_index('bva-index')  # ignore if exist
    
    documentIndex = 'la-document'
    sentenceIndex = 'la-sentence'
    infoIndex = 'la-info'

    es.delete_index(documentIndex)
    es.delete_index(sentenceIndex)
    es.delete_index(infoIndex)
    

    
    # Getting the list of files in <data_path>:
    data_path = './data/LAWeb-Converted-50BVAs'
    list_of_files = os.listdir(data_path)

    # ...and creating new lists for the texts of the sentences...
    sentenceCount = 0
    documentCount = 0
    
    print(list_of_files)
    # Using a for-loop to iterate over the filenames...
    for filename in list_of_files:
        print ( f"{data_path}/{filename}" )

        # ... and opening the given filename...
        file = open(f"{data_path}/{filename}", encoding="utf8")
        
        try:
            # ...using the json file loader to translate the json data...
            data = json.load(file)
            data['caseID'] = data['caseNumber']

            info = data['caseInfo']
            res = es.add_item(infoIndex, documentCount, info)

            res = es.add_item(documentIndex, documentCount, data)

            documentCount += 1

            # ...and adding the sentences to those new lists...
            sentences = data['sentences']
            for sentence in sentences:
                sentID = sentence['sentID']
                caseNumber = sentence['caseNumber']
                paragraphNumber = sentence['paragraphNumber']

                context = f"{caseNumber}P{paragraphNumber}"
                sentence['context'] = context
                #print(f"context {sentence['context']}")
                
                if 'rhetRole' in sentence:
                    sentence.pop('rhetRole', None)
                    #print(f"deleted {sentID}")

                res = es.add_item(sentenceIndex, sentenceCount, sentence)
                
                sentenceCount += 1

        except Exception as ex:
            print(ex)
            
elasticsearch_publish()
