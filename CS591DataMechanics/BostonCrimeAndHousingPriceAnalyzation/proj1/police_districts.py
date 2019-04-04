import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy

#prov check

# http://bostonopendata-boston.opendata.arcgis.com/datasets/9a3a8c427add450eaf45a470245680fc_5?selectedAttributes%5B%5D=DISTRICT&chartType=bar&uiTab=table
# http://bostonopendata-boston.opendata.arcgis.com/datasets/9a3a8c427add450eaf45a470245680fc_5.geojson

class police_districts(dml.Algorithm):
    contributor = 'pt0713_silnuext'
    reads = ['pt0713_silnuext.police_districts']
    writes = ['pt0713_silnuext.police_districts']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')

        url = "http://bostonopendata-boston.opendata.arcgis.com/datasets/9a3a8c427add450eaf45a470245680fc_5.geojson"
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        r = [r['features'][i]['properties'] for i in range(11)]
        print(json.dumps(r))
       
        repo.dropCollection("police_districts")
        repo.createCollection("police_districts")
        repo['pt0713_silnuext.police_districts'].insert_many(r)
        repo['pt0713_silnuext.police_districts'].metadata({'complete':True})
        print(repo['pt0713_silnuext.police_districts'].metadata())

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('aaa','http://bostonopendata-boston.opendata.arcgis.com/datasets/')

        this_script = doc.agent('alg:pt0713_silnuext#policeDistrcts(opendata)', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('aaa:9a3a8c427add450eaf45a470245680fc_5', {'prov:label':'police_district', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'geojson'})
        get_police_districts = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_police_districts, this_script)

        doc.usage(get_police_districts, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',})

        police_districts = doc.entity('dat:pt0713_silnuext#police_districts', {prov.model.PROV_LABEL:'police_districts', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(police_districts, this_script)
        doc.wasGeneratedBy(police_districts, get_police_districts, endTime)
        doc.wasDerivedFrom(police_districts, resource, get_police_districts, get_police_districts, get_police_districts)


        repo.logout()
                  
        return doc

# police_districts.execute()
# doc = police_districts.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof