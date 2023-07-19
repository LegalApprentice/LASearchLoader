# Imports of import.
import json
import os

from datetime import datetime




def extract_publish(data_path):


    
    # Getting the list of files in <data_path>:
    list_of_files = os.listdir(data_path)



                
    # print(list_of_files)
    # Using a for-loop to iterate over the filenames...
    for filename in list_of_files:
        # print ( f"{data_path}/{filename}" )
        
        print ( f"")

        # ... and opening the given filename...
        fileread = open(f"{data_path}/{filename}", encoding="utf8")
        print ( f"working on case  {data_path}/{filename}" )

        data = json.load(fileread)
        fileread.close()
        
        text = data['text']  
         
        newname = filename.replace('.json', '.txt')
        filewrite = open(f"{data_path}/{newname}", "w")
        filewrite.write(text)
        
        filewrite.close()
        print ( f"Writing case  {data_path}/{newname}" )
     
     
if __name__ == "__main__":                

    
    data_path = './3-The_Curated_SRS_Dataset'
    
    extract_publish(data_path)



# python PTSD-cases-elasticwrite.py
#  docker run -d -p 9200:9200 --name elasticsearch elasticsearch
#  use this for persistent storage
#  docker run -d -p 9200:9200 -p 9300:9300 -v data:/usr/share/elasticsearch/data --name elasticsearch elasticsearch
