import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy

# functions implemented from lecture notes
def union(R, S):
    return R + S

def difference(R, S):
    return [t for t in R if t not in S]

def intersect(R, S):
    return [t for t in R if t in S]

def project(R, p):
    return [p(t) for t in R]

def select(R, s):
    return [t for t in R if s(t)]
 
def product(R, S):
    return [(t,u) for t in R for u in S]

def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k,v) in R if k == key])) for key in keys]

def map(f, R):
    return [t for (k,v) in R for t in f(k,v)]
    
def reduce(f, R):
    keys = {k for (k,v) in R}
    return [f(k1, [v for (k2,v) in R if k1 == k2]) for k1 in keys]


class fld_crime(dml.Algorithm):
    contributor = "pt0713_silnuext"
    reads = ["pt0713_silnuext.fld",
            "pt0713_silnuext.crime"]
    writes = ["pt0713_silnuext.fld_crime"]

    @staticmethod
    def execute(trial = False):
        """Retrieve some data sets (not using the API here for the sake of simplicity)."""
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate("pt0713_silnuext", "pt0713_silnuext")
        repo.dropCollection("fld_crime")
        repo.createCollection("fld_crime")

        # import fld data
        client = sodapy.Socrata("data.mass.gov", None)
        response = client.get("x99p-b88k", limit=9787, offset=0)
        s = json.dumps(response, sort_keys=True, indent=2)
   

        fld_city_data = project(response, lambda t: (t["date_received"], [t.get("business_city")]))
        fld_city_month = [int(boston[0][6]) for boston in fld_city_data if boston[0][:4] == "2015" and boston[1] == ['Boston'] and boston[0][5] != 1]
        fld12 = [num for num in fld_city_month if num == 1 or num == 2]
        fld34 = [num for num in fld_city_month if num == 3 or num == 4]
        fld56 = [num for num in fld_city_month if num == 5 or num == 6]
        fld78 = [num for num in fld_city_month if num == 7 or num == 8]
        print("the number of complaints in 2015 Jan + Feb: " , len(fld12))
        print("the number of complaints in 2015 Mar + Apr: " , len(fld34))
        print("the number of complaints in 2015 May + Jun: " , len(fld56))
        print("the number of complaints in 2015 Jul + Aug: " , len(fld78))
        
        repo["pt0713_silnuext.fld_crime"].insert_many(response)
        repo["pt0713_silnuext.fld_crime"].metadata({"complete":True})
        print(repo["pt0713_silnuext.fld_crime"].metadata())


        # import crime data
        client1 = sodapy.Socrata("data.cityofboston.gov", None)
        response1 = []
        limits = [0, 50001, 100001, 150001, 200001, 250001]
        for limit in limits:
            response1 += client1.get("crime", limit=50000, offset=limit)
        s = json.dumps(response1, sort_keys=True, indent=2)

        crime_month = project(response1, lambda x: (x["year"], x["month"]))
        crime_month2015 = [crime_2015month for crime_2015month in crime_month if crime_2015month[0] == "2015"]
        crime12 = [crime12_2015 for crime12_2015 in crime_month2015 if crime12_2015[1] == '1' or crime12_2015[1] == '2']
        print("The crime number happens in Jan and Feb in 2015 is: ", len(crime12))
        crime34 = [crime34_2015 for crime34_2015 in crime_month2015 if crime34_2015[1] == '3' or crime34_2015[1] == '4']
        print("The crime number happens in Mar and Apr in 2015 is: ", len(crime34))
        crime56 = [crime56_2015 for crime56_2015 in crime_month2015 if crime56_2015[1] == '5' or crime56_2015[1] == '6']
        print("The crime number happens in May and Jun in 2015 is: ", len(crime56))
        crime78 = [crime78_2015 for crime78_2015 in crime_month2015 if crime78_2015[1] == '7' or crime78_2015[1] == '8']
        print("The crime number happens in Jul and Aug in 2015 is: ", len(crime78))

        repo["pt0713_silnuext.fld_crime"].insert_many(response1)
        repo["pt0713_silnuext.fld_crime"].metadata({"complete":True})
        print(repo["pt0713_silnuext.fld_crime"].metadata())

        print("The percentage of fld complaint / crime in Jan and Feb is: ", len(fld12) / len(crime12))
        print("The percentage of fld complaint / crime in Mar and Apr is: ", len(fld34) / len(crime34))
        print("The percentage of fld complaint / crime in May and Jun is: ", len(fld56) / len(crime56))
        print("The percentage of fld complaint / crime in Jul and Aug is: ", len(fld78) / len(crime78))


        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        """
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            """

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate("pt0713_silnuext", "pt0713_silnuext")
        doc.add_namespace("alg", "http://datamechanics.io/algorithm/") # The scripts are in <folder>#<filename> format.
        doc.add_namespace("dat", "http://datamechanics.io/data/") # The data sets are in <user>#<collection> format.
        doc.add_namespace("ont", "http://datamechanics.io/ontology#") # "Extension", "DataResource", "DataSet", "Retrieval", "Query", or "Computation".
        doc.add_namespace("log", "http://datamechanics.io/log/") # The event log.
        doc.add_namespace("bdp", "https://data.cityofboston.gov/resource/")
        doc.add_namespace('aaa', 'https://data.mass.gov/dataset')

        this_script = doc.agent("alg:pt0713_silnuext#fld_crime", {prov.model.PROV_TYPE:prov.model.PROV["SoftwareAgent"], "ont:Extension":"py"})
        resource1 = doc.entity("bdp:wc8w-nujj", {"prov:label":"crime", prov.model.PROV_TYPE:"ont:DataResource", "ont:Extension":"json"})
        resource2 = doc.entity("aaa:x99p-b88k", {"prov:label":"fld", prov.model.PROV_TYPE:"ont:DataResource", "ont:Extension":"json"})

        get_fld_crime = doc.activity("log:uuid"+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_fld_crime, this_script)

        doc.usage(get_fld_crime, resource1, startTime, None,
                  {prov.model.PROV_TYPE:"ont:Retrieval",})

        doc.usage(get_fld_crime, resource2, startTime, None,
                  {prov.model.PROV_TYPE:"ont:Retrieval",})

                  

        crime = doc.entity("dat:pt0713_silnuext#fld_crime", {prov.model.PROV_LABEL:"crime", prov.model.PROV_TYPE:"ont:DataSet"})
        doc.wasAttributedTo(crime, this_script)
        doc.wasGeneratedBy(crime, get_fld_crime, endTime)
        doc.wasDerivedFrom(crime, resource1, get_fld_crime, get_fld_crime, get_fld_crime)

        fld = doc.entity("dat:pt0713_silnuext#fld_crime", {prov.model.PROV_LABEL:"fld", prov.model.PROV_TYPE:"ont:DataSet"})
        doc.wasAttributedTo(fld, this_script)
        doc.wasGeneratedBy(fld, get_fld_crime, endTime)
        doc.wasDerivedFrom(fld, resource2, get_fld_crime, get_fld_crime, get_fld_crime)


        repo.logout()
                  
        return doc

# fld_crime.execute()
# doc = fld_crime.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof