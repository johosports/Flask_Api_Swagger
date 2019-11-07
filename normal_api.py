from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

es = Elasticsearch()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    results = es.get(index='xinpei', doc_type='house',id=10)
    return jsonify(results['_source'])


#新北市男生可租
@app.route('/search/xinpei/<house_gender>', methods=['GET'])
def search(house_gender): 
    body = {
        "query": {
            "match": {
                "house_gender": house_gender
            }
        }
    }

    res = es.search(index='xinpei', body=body)

    return jsonify(res['hits'])



# #聯絡電話查詢
# @app.route('/search/<house_phone>', methods=['GET'])
# def test_phone(house_phone):
#     body = {
#         "query": {
#             "match_phrase":{
#                 "house_phone":house_phone
            
#             }
#         }
#     }

#     res = es.search(index='xinpei', body=body)

#     return jsonify(res['hits']['hits'])



@app.route('/search/nickname/<nick_name>', methods=['GET'])
def nick_search(nick_name):
    body = {
        "query": {
            "match_phrase":{
                "nick_name":nick_name
            
            }
        }
    }

    res = es.search(index='xinpei', body=body)

    return jsonify(res['hits']['hits'])


@app.route('/search/taipei/<linkman>', methods=['GET'])
def linkman_search(linkman):
    body = {
        "query": {
            "match_phrase":{
                "linkman":linkman
            
            }
        }
    }
    res = es.search(index='taipei', body=body)

    return jsonify(res['hits']['hits'])

@app.route('/search/taipei/<house_gender>/<linkman>', methods=['GET'])
def all_search(house_gender,linkman):
    body = {    
        "query": {      
                "bool":{
                    "must":[
                        {"match_phrase":{"house_gender":house_gender}},
                        {"match_phrase":{"linkman":linkman}}                        
                    ]            
                }
            }
        }

    res = es.search(index='taipei', body=body)
    return jsonify(res['hits']['hits'])


app.run(port=5000, debug=True)