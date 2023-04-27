
# How to create Elastic Search for the 450 PTSD-cases that were extracted from the 10000 BVA cases

- First you need to start elastic search 
  
use this command to build a container  (you may need sudo)

  docker build -t elasticsearch -f elasticsearch.Dockerfile .

use this command to start the elastic search container  (you may need sudo)

  docker run -d -p 9200:9200 --name elasticsearch elasticsearch


now that elasticsearch is running on port 9200   you can run the python program to load elastic

the program for all 450 cases is PTSD-cases-elasticwrite.py

type the command in the terminal



 docker run -d -p 9200:9200 --name elasticsearch elasticsearch

    python PTSD-cases-elasticwrite.py 