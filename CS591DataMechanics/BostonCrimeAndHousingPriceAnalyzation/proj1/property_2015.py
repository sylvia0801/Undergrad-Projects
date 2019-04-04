import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy

#prov check

# https://data.cityofboston.gov/Permitting/Property-Assessment-2015/yv8c-t43q
# https://data.cityofboston.gov/resource/n7za-nsjh.json

class property_2015(dml.Algorithm):
    contributor = 'pt0713_silnuext'
    reads = ['pt0713_silnuext.property_2015']
    writes = ['pt0713_silnuext.property_2015']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')

        client = sodapy.Socrata("data.cityofboston.gov", None)
        response = client.get("n7za-nsjh", limit=168115, offset=0)
        s = json.dumps(response, sort_keys=True, indent=2)
        repo.dropCollection("property_2015")
        repo.createCollection("property_2015")
        repo['pt0713_silnuext.property_2015'].insert_many(response)
        repo['pt0713_silnuext.property_2015'].metadata({'complete':True})
        print(repo['pt0713_silnuext.property_2015'].metadata())

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

        this_script = doc.agent('alg:pt0713_silnuext#2015property(citygov)', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('bdp:n7za-nsjh', {'prov:label':'property15', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_property_2015 = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_property_2015, this_script)

        doc.usage(get_property_2015, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',})

        property_2015 = doc.entity('dat:pt0713_silnuext#property_2015', {prov.model.PROV_LABEL:'property_2015', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(property_2015, this_script)
        doc.wasGeneratedBy(property_2015, get_property_2015, endTime)
        doc.wasDerivedFrom(property_2015, resource, get_property_2015, get_property_2015, get_property_2015)


        repo.logout()
                  
        return doc

# property_2015.execute()
# doc = property_2015.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof