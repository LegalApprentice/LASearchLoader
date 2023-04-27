from datetime import datetime
from elasticsearch import Elasticsearch


# https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html






def elasticsearch_query():

    #  https://elasticsearch-py.readthedocs.io/en/master/
    # by default we connect to localhost:9200
    es = Elasticsearch()

    #url = 'https://cdb55929da7544268b1880b042fcf11c.eastus2.azure.elastic-cloud.com:9243'
    #es = Elasticsearch(hosts=[url],http_auth=('elastic','mwm4q0n3QUhm3ixBwgR4OI9y'))

    indexName = 'la-50attrib-cases'
    documentIndex = 'la-document'
    sentenceIndex = 'la-sentence'


    # OR:   This query searches the "text" field for ANY of the words ("OR"); number of hits = 2024
    query = {
        "query": {
            "match": {
                "text": {
                     "query": "service Vietnam combat"
                }
            }
        }
    }

    # AND:   This query searches the "text" field for ALL of the words ("AND"), but in any order; number of hits = 7
    query = {
        "query": {
            "match": {
                "text": {
                     "query": "service Vietnam combat",
                     "operator": "and"
                }
            }
        }
    }


    # RHETCLASS:   This query searches the "rhetClass" field for "FindingSentence"; number of hits = 487
    query = {
        "query": {
            "match": {
                "rhetClass": {
                     "query": "FindingSentence"
                }
            }
        }
    }


    # OR + RHETCLASS:   This query combines an "OR" search of text with a "rhetClass" match for "FindingSentence"; number of hits = 361
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "rhetClass": {
                            "query" : "FindingSentence"
                        }
                    }
                    },
                    {"match": {
                        "text": {
                            "query": "service Vietnam"
                        }
                    }
                    }
                ]
            }
        }
    }

    # AND + RHETCLASS:   This query combines an "AND" search of text with a "rhetClass" match for "FindingSentence"; number of hits = 3
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "rhetClass": {
                            "query" : "FindingSentence"
                        }
                    }
                    },
                    {"match": {
                        "text": {
                            "query": "service Vietnam",
                            "operator": "and"
                        }
                    }
                    }
                ]
            }
        }
    }


    # EXACT PHRASE:   This query does an exact match on a phrase
    query = {
        "query": {
            "match_phrase": {
                "text": {
                     "query": "psychiatric problem"
                     }
                }
            }
    }

    # EXACT PHRASE + RHETCLASS:   This query combines an exact-phrase search of text with a "rhetClass" match for "FindingSentence"; number of hits = 3
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "rhetClass": {
                            "query" : "FindingSentence"
                        }
                    }
                    },
                    {"match_phrase": {
                        "text": {
                            "query": "Cambodia and Vietnam"
                        }
                    }
                    }
                ]
            }
        }
    }



    # AND NOT:   This query combines a search of text with a "rhetClass" match for "FindingSentence", but then excludes text that contains ANY of a list of words; number of hits before the exclusion = 361 ;number of hits with exclusion = 325
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "rhetClass": {
                            "query" : "FindingSentence"
                        }
                    }
                    },
                    {"match": {
                        "text": {
                            "query": "service Vietnam"
                        }
                    }
                    }
                ],
                "must_not": {
                    "match": {
                        "text": {
                            "query": "Cambodia stressor sexual"
                        }
                    }
                }
            }
        }
    }



    # VARIABLES for "query" fields; same results as without use of variables (N = 325) [AVOID "filter" as variable name, because it is a boolean parameter name]
    sentClass = "FindingSentence"
    inclusion = "service Vietnam"
    exclusion = "Cambodia stressor sexual"
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "rhetClass": {
                            "query" : sentClass
                        }
                    }
                    },
                    {
                    "match": {
                        "text": {
                            "query": inclusion
                        }
                    }
                    }
                ],
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    # VARIABLES for "query" fields, but with the "rhetClass" in a "filter" parameter (not included in scoring), and "exclusion" empty; same results as just OR+RHETCLASS, hits = 361; "sentClass" and "inclusion" must not be empty, because they are in the search query "must" [also, AVOID "filter" as variable name, because it is a boolean parameter name]
    sentClass = "FindingSentence"
    inclusion = "service Vietnam"
    exclusion = ""
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text": {
                            "query": inclusion
                        }
                    }
                },
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClass
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }


    # POSSIBLE UGLY SOLUTION FOR CHECKING MULTIPLE EXCLUSIVE sentClass CATEGORIES, hits for sentClass1 = 361, hits for sentClass2 = 656, hits for both combined sentClass3 = 1017; VARIABLES for "query" fields, but with the "rhetClass" in a "filter" parameter (not included in scoring), and "exclusion" empty; same results as just OR+RHETCLASS, hits = 361; "sentClass" and "inclusion" must not be empty, because they are in the search query "must" [also, AVOID "filter" as variable name, because it is a boolean parameter name]
    sentClass = "FindingSentence EvidenceSentence"
    inclusion = "service Vietnam"
    exclusion = ""
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text": {
                            "query": inclusion
                        }
                    }
                },
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClass
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }


    # FINAL GENERALIZED QUERY; hits for sentClass1 = 361, hits for sentClass2 = 656, hits for both combined sentClass3 = 1017; VARIABLES for "query" fields, but with the "rhetClass" in a "filter" parameter (not included in scoring), and "exclusion" empty; same results as just OR+RHETCLASS, hits = 361; "sentClass" and "inclusion" must not be empty, because they are in the search query "must" [also, AVOID "filter" as variable name, because it is a boolean parameter name]
    # Variables to trigger strings for filter combinations; they have values of 0 or 1; if checkboxes on UI, I ASSUME CHECKED = 1 AND UNCHECKED = 0
    fBox = 1
    eBox = 0
    rBox = 0
    lBox = 0
    cBox = 0
    # this is a python tuple of all SIX types of sentence (including "Other" as "Sentence")
    sentTypes = ("FindingSentence", "EvidenceSentence", "ReasoningSentence", "LegalRuleSentence", "CitationSentence", "Sentence")
    # if no boxes are checked, the default search is all SIX types of sentence (including "Other" as "Sentence")
    sentClasses = " ".join(sentTypes)
    # subsets of pairs
    pair1 = (sentTypes[0], sentTypes[1])
    pair2 = (sentTypes[0], sentTypes[2])
    pair3 = (sentTypes[0], sentTypes[3])
    pair4 = (sentTypes[0], sentTypes[4])
    pair5 = (sentTypes[1], sentTypes[2])
    pair6 = (sentTypes[1], sentTypes[3])
    pair7 = (sentTypes[1], sentTypes[4])
    pair8 = (sentTypes[2], sentTypes[3])
    pair9 = (sentTypes[2], sentTypes[4])
    pair10 = (sentTypes[3], sentTypes[4])
    # subsets of triples
    trip1 = (sentTypes[0], sentTypes[1], sentTypes[2])
    trip2 = (sentTypes[0], sentTypes[1], sentTypes[3])
    trip3 = (sentTypes[0], sentTypes[1], sentTypes[4])
    trip4 = (sentTypes[0], sentTypes[2], sentTypes[3])
    trip5 = (sentTypes[0], sentTypes[2], sentTypes[4])
    trip6 = (sentTypes[0], sentTypes[3], sentTypes[4])
    trip7 = (sentTypes[1], sentTypes[2], sentTypes[3])
    trip8 = (sentTypes[1], sentTypes[2], sentTypes[4])
    trip9 = (sentTypes[1], sentTypes[3], sentTypes[4])
    trip10 = (sentTypes[2], sentTypes[3], sentTypes[4])
    # subsets of quadruples
    quad1 = (sentTypes[0], sentTypes[1], sentTypes[2], sentTypes[3])
    quad2 = (sentTypes[0], sentTypes[1], sentTypes[2], sentTypes[4])
    quad3 = (sentTypes[0], sentTypes[1], sentTypes[3], sentTypes[4])
    quad4 = (sentTypes[0], sentTypes[2], sentTypes[3], sentTypes[4])
    quad5 = (sentTypes[1], sentTypes[2], sentTypes[3], sentTypes[4])
    # only 1 quintuple (all FIVE boxes checked)
    full = (sentTypes[0], sentTypes[1], sentTypes[2], sentTypes[3], sentTypes[4])
    # logic tree to select the appropriate sub-tuple
    if fBox == 1:
        if eBox == 1:
            if rBox == 1:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(full)
                    elif cBox == 0:
                        sentClasses = " ".join(quad1)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(quad2)
                    elif cBox == 0:
                        sentClasses = " ".join(trip1)
            elif rBox == 0:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(quad3)
                    elif cBox == 0:
                        sentClasses = " ".join(trip2)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(trip3)
                    elif cBox == 0:
                        sentClasses = " ".join(pair1)
        elif eBox == 0:
            if rBox == 1:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(quad4)
                    elif cBox == 0:
                        sentClasses = " ".join(trip4)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(trip5)
                    elif cBox == 0:
                        sentClasses = " ".join(pair2)
            elif rBox == 0:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(trip6)
                    elif cBox == 0:
                        sentClasses = " ".join(pair3)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(pair4)
                    elif cBox == 0:
                        sentClasses = sentTypes[0]
    if fBox == 0:
        if eBox == 1:
            if rBox == 1:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(quad5)
                    elif cBox == 0:
                        sentClasses = " ".join(trip7)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(trip8)
                    elif cBox == 0:
                        sentClasses = " ".join(pair5)
            elif rBox == 0:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(trip9)
                    elif cBox == 0:
                        sentClasses = " ".join(pair6)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(pair7)
                    elif cBox == 0:
                        sentClasses = sentTypes[1]
        elif eBox == 0:
            if rBox == 1:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(trip10)
                    elif cBox == 0:
                        sentClasses = " ".join(pair8)
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = " ".join(pair9)
                    elif cBox == 0:
                        sentClasses = sentTypes[2]
            elif rBox == 0:
                if lBox == 1:
                    if cBox == 1:
                        sentClasses = " ".join(pair10)
                    elif cBox == 0:
                        sentClasses = sentTypes[3]
                elif lBox == 0:
                    if cBox == 1:
                        sentClasses = sentTypes[4]

    # 7 queries are needed: (1) "Any" ("any of these words", OR) by itself; (2) "All" ("all of these words", AND) by itself; (3) "AnyAll" (both Any and All fields) together; (4) "Exact" ("this exact phrase") by itself; (5) "AnyExact" (both Any and Exact) without All; (6) "AllExact" (both All and Exact) without Any; (7) AnyAllExact (all three, Any, All, Exact). NOTICE that the variable "exclusion" ("and not any of these words") is included in every query, can be an empty string, and is interpreted as an OR (not any of these words)
    inclusionAny = "service Vietnam"
    inclusionAll = "finds Board"
    exactPhrase = "that the"
    exclusion = "evidence"

    #(1) this is the "any" search by itself, with the inclusionAny variable; use this query if only the "Any" has an entry, but no entries for "All" or "Exact Phrase"
    # test: inclusionAny = "service Vietnam", sentClasses = FindingSentences only, exclusion = "", hits = 361; exclusion = "stressor", hits = 333
    queryAny = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text": {
                            "query": inclusionAny
                        }
                    }
                },
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(2) this is the "all" search by itself, with the inclusionAll variable; use this query if only the "All" has an entry, but no entries for "Any" or "Exact Phrase"
    # test: inclusionAll = "finds Board", sentClasses = FindingSentences only, exclusion = "", hits = 131; exclusion = "evidence", hits = 48
    queryAll = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text": {
                            "query": inclusionAll,
                            "operator": "and"
                        }
                    }
                },
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(3) this is the "AnyAll" search, with string values for BOTH the inclusionAny and inclusionAll variables, but no entry for exactPhrase
    # test: inclusionAny = "service Vietnam", inclusionAll = "finds Board", sentClasses = FindingSentences only, exclusion = "", hits = 94; exclusion = "evidence", hits = 38
    queryAnyAll = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": {
                                "query": inclusionAny
                            }
                        }
                    },
                    {
                        "match": {
                            "text": {
                                "query": inclusionAll,
                                "operator": "and"
                            }
                        }
                    }
                ],
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(4) this is the "Exact Phrase" search by itself, without the inclusionAny or inclusionAll variables; use this query only is the "Any" and "All" search fields have no entries
    # test: exactPhrase = "psychiatric disorder", sentClasses = FindingSentences only, exclusion = "", hits = 92; exclusion = "evidence", hits = 39
    queryExact = {
        "query": {
            "bool": {
                "must": {
                    "match_phrase": {
                        "text": {
                            "query": exactPhrase
                        }
                    }
                },
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(5) this is the "AnyExact" search, with string values for BOTH the inclusionAny and exactPhrase variables, but no entry for inclusionAll
    # test: inclusionAny = "service Vietnam", exactPhrase = "psychiatric disorder", sentClasses = FindingSentences only, exclusion = "", hits = 89; exclusion = "evidence", hits = 37
    queryAnyExact = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": {
                                "query": inclusionAny
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "text": {
                                "query": exactPhrase
                            }
                        }
                    }
                ],
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(6) this is the "AllExact" search, with string values for BOTH the inclusionAll and exactPhrase variables, but no entry for inclusionAny
    # test: inclusionAll = "finds Board", exactPhrase = "psychiatric disorder", sentClasses = FindingSentences only, exclusion = "", hits = 19; exclusion = "evidence", hits = 7
    queryAllExact = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": {
                                "query": inclusionAll,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "text": {
                                "query": exactPhrase
                            }
                        }
                    }
                ],
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }

    #(7) this is the "AnyAllExact" search, with string values for the inclusionAny, inclusionAll and exactPhrase variables
    # test: inclusionAny = "service Vietnam", inclusionAll = "finds Board", exactPhrase = "that the", sentClasses = FindingSentences only, exclusion = "", hits = 57; exclusion = "evidence", hits = 15
    queryAnyAllExact = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": {
                                "query": inclusionAny
                            }
                        }
                    },
                    {
                        "match": {
                            "text": {
                                "query": inclusionAll,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "text": {
                                "query": exactPhrase
                            }
                        }
                    }
                ],
                "filter": {
                    "match": {
                        "rhetClass": {
                            "query" : sentClasses
                        }
                    }
                },
                "must_not": {
                    "match": {
                        "text": {
                            "query": exclusion
                        }
                    }
                }
            }
        }
    }


    res = es.search(index=sentenceIndex, body=query)
    print(res)

    for hit in res['hits']['hits']:
        print(hit["_source"])

# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html

    print("Got %d Hits:" % res['hits']['total']['value'])
     
elasticsearch_query()