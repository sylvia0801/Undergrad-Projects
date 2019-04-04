import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy


# https://data.cityofboston.gov/dataset/Property-Assessment-2014/qz7u-kb7x
# https://data.cityofboston.gov/resource/jsri-cpsq.json

class property_2014(dml.Algorithm):
    contributor = 'pt0713_silnuext'
    reads = ['pt0713_silnuext.property_2014']
    writes = ['pt0713_silnuext.property_2014']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')

        client = sodapy.Socrata("data.cityofboston.gov", None)
        response = client.get("jsri-cpsq", limit=164091, offset=0)
        s = json.dumps(response, sort_keys=True, indent=2)
        repo.dropCollection("property_2014")
        repo.createCollection("property_2014")
        repo['pt0713_silnuext.property_2014'].insert_many(response)
        repo['pt0713_silnuext.property_2014'].metadata({'complete':True})
        print(repo['pt0713_silnuext.property_2014'].metadata())

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

        this_script = doc.agent('alg:pt0713_silnuext#2014property(citygov)', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('bdp:jsri-cpsq', {'prov:label':'property14', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_property_2014 = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_property_2014, this_script)

        doc.usage(get_property_2014, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',})

        property_2014 = doc.entity('dat:pt0713_silnuext#property_2014', {prov.model.PROV_LABEL:'property_2014', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(property_2014, this_script)
        doc.wasGeneratedBy(property_2014, get_property_2014, endTime)
        doc.wasDerivedFrom(property_2014, resource, get_property_2014, get_property_2014, get_property_2014)


        repo.logout()
                  
        return doc

# property_2014.execute()
# doc = property_2014.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof