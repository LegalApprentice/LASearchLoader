
from datetime import datetime
from elasticsearch import Elasticsearch

# https://elasticsearch-py.readthedocs.io/en/7.x/

class ElasticSearchWrapper:
    def __init__(self, url):

        # url = 'https://cdb55929da7544268b1880b042fcf11c.eastus2.azure.elastic-cloud.com:9243'
        # self.es = Elasticsearch(hosts=[url], http_auth=('elastic', 'mwm4q0n3QUhm3ixBwgR4OI9y'))
        if url is None:
            self.es = Elasticsearch()
        else:
            self.es = Elasticsearch(hosts=[url])
            
    def smoketest(self):
        index = 'smoke-index'
        doc_type="smoke-type"
        data = {"data": "smoketest", "timestamp": datetime.now()}
        id = 1
        try:
            self.delete_index(index)
            done = self.es.index(index=index, doc_type=doc_type, id=id, body=data)
            res = self.es.get(index=index, doc_type=doc_type, id=id)
            return res, done
        except Exception as message:
            res = self.es.get(index=index, doc_type=doc_type, id=id)
            return res, message
        
    def search(self, index, query):
        try:
            print(query)
            answer = self.es.search(index=index, body=query)
            hits = answer['hits']['hits']
           # print(hits)
            return hits
        except Elasticsearch.E as esError:
            raise  esError
            ## https://github.com/elastic/elasticsearch-py/blob/master/elasticsearch/exceptions.py
            ## https://elasticsearch-py.readthedocs.io/en/master/exceptions.html
            # print(esError)
            # res = [esError.error]
            # return res, esError.info
            
    def create_index(self, index):
        return self.es.indices.create(index=index, ignore=400)  # ignore if exist
    
    def delete_index(self, index):
        try:
            self.es.indices.delete(index=index, ignore=[400, 404])
        except:
            pass 
    
    def add_item(self, index, id, data):
        #print(data)
        res = self.es.index(index=index, id=id,  body=data)
        ## # print(res)
        return res

    def delete_item(self, index, id):
        res = self.es.delete(index=index, id=id)
        # # print(res)
        return res

    def delete_by_ids(self, index, ids):
        query = {"query": {"terms": {"_id": ids}}}
        res = self.es.delete_by_query(index=index, body=query)
        # # print(res)
        return res

    def stats(self, index):
        res = self.es.indices.stats(index=index)
        # # print(res)
        return res
        