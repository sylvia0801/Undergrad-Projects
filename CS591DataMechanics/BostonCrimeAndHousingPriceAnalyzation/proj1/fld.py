import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy

# PROV CHECK
# https://data.mass.gov/dataset/FLD-Complaints/c5kv-hee8
# https://data.mass.gov/resource/x99p-b88k.json

class fld(dml.Algorithm):
    contributor = 'pt0713_silnuext'
    reads = ['pt0713_silnuext.fld']
    writes = ['pt0713_silnuext.fld']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')

        client = sodapy.Socrata("data.mass.gov", None)
        response = client.get("x99p-b88k", limit=9787, offset=0)
        s = json.dumps(response, sort_keys=True, indent=2)
        repo.dropCollection("fld")
        repo.createCollection("fld")
        repo['pt0713_silnuext.fld'].insert_many(response)
        repo['pt0713_silnuext.fld'].metadata({'complete':True})
        print(repo['pt0713_silnuext.fld'].metadata())

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
        doc.add_namespace('bdp', 'https://data.mass.gov/dataset')

        this_script = doc.agent('alg:pt0713_silnuext#FLD(massdata)', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('bdp:x99p-b88k', {'prov:label':'fld', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_fld = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_fld, this_script)

        doc.usage(get_fld, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',})

        fld = doc.entity('dat:pt0713_silnuext#fld', {prov.model.PROV_LABEL:'fld', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(fld, this_script)
        doc.wasGeneratedBy(fld, get_fld, endTime)
        doc.wasDerivedFrom(fld, resource, get_fld, get_fld, get_fld)


        repo.logout()
                  
        return doc

# fld.execute()
# doc = fld.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof