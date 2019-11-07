
from flask import Flask, jsonify, request
from flask_restplus import Resource, Api
from elasticsearch import Elasticsearch

es = Elasticsearch()

app = Flask(__name__)
api = Api(app, title="house_information", description="house_information_api.")



ns = api.namespace('591house/api', description='api_Docs')


@ns.route('/')
class Api_test(Resource):

    def get(self):
        results = es.get(index='xinpei', doc_type='house',id=10)
        return jsonify(results['_source'])


@ns.route('/<string:house_gender>')
@api.response(404, 'result not found.')
class get_house_gender(Resource):

    def get(self, house_gender):
        body = {
            "query": {
                "match": {
                    "house_gender": house_gender
                }
            }
        }

        res = es.search(index='xinpei', body=body)

        return jsonify(res['hits'])

@ns.route('/xinpei/<string:house_phone>')
@api.response(404, 'result not found.')
class get_house_phone(Resource):

    def get(self,house_phone):
        body = {
            "query": {
                "match_phrase":{
                    "house_phone":house_phone
                
                }
            }
        }

        res = es.search(index='xinpei', body=body)

        return jsonify(res['hits'])

@ns.route('/taipei/<string:linkman>')
@api.response(404, 'result not found.')
class get_house_linkman(Resource):

    def get(self,linkman):
        body = {
            "query": {
                "match_phrase":{
                    "linkman":linkman
                
                        }
                    }
                }
        res = es.search(index='taipei', body=body)

        return jsonify(res['hits']['hits'])


@ns.route('/taipei/<house_gender>/<linkman>')
@api.response(404, 'result not found.')
class get_house_linkman(Resource):

    def get(self,house_gender,linkman):
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



if __name__ == '__main__':
    app.run(port=5100, debug=True)