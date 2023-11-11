# Imports of import.
import json
import os
import csv



def computestats(data_path):


    # Getting the list of files in <data_path>:
    list_of_files = os.listdir(data_path)

    # ...and creating new lists for the texts of the sentences...
    sentenceCount = 0

    with open('sentences.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sentenceID','labels.rhetClass', 'enrichmentSet.rhetClass', 'text' ])

          
        # print(list_of_files)
        # Using a for-loop to iterate over the filenames...
        for filename in list_of_files:
            print ( f"{data_path}/{filename}" )
            if ( filename.find('.json') == -1):
                continue
            
            print ( f"")

            # ... and opening the given filename...
            file = open(f"{data_path}/{filename}", encoding="utf8")
            print ( f"working on case  {data_path}/{filename}" )

            data = json.load(file)
        
        
            if data.get('sentences') is None:
                print('sentences is None', filename)
                continue   
        
            sentences =  data['sentences']        
    
            for sentence in sentences:
                try:
                    sentence_id = sentence['sentID']
                    sentence_text = sentence['text']
                    
                    labels_rhet_class = ''
                    if 'labels' in sentence:
                        labels_rhet_class = sentence['labels']['rhetClass']
                        
                    enrichment_rhet_class = ''    
                    if 'enrichmentSet' in sentence:
                        enrichment_rhet_class = sentence['enrichmentSet']['rhetClass']['classification']
                    
                    writer.writerow([sentence_id, labels_rhet_class, enrichment_rhet_class, sentence_text])
                            
                    sentenceCount += 1
                    print(F"Sentence count {sentenceCount}")

                except Exception as ex:
                    print('Sentence EXCEPTION', ex, filename)


if __name__ == "__main__":                
    # Getting the list of files in <data_path>:
    data_path = './1-The_FS-PTSD_Dataset'
    data_path = './PTSD-Paragraph-cases'
    data_path = './3-The_Curated_SRS_Dataset'
    
    computestats(data_path)



# python PTSD-cases-elasticwrite.py
#  docker run -d -p 9200:9200 --name elasticsearch elasticsearch
#  use this for persistent storage
#  docker run -d -p 9200:9200 -p 9300:9300 -v data:/usr/share/elasticsearch/data --name elasticsearch elasticsearch
