import shapefile
import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy
import rtree
import json
import geojson
import geopy.distance
import shapely.geometry
from tqdm import tqdm
from geojson import Polygon, LineString
from shapely.geometry import Polygon
from pyproj import Proj, transform
from random import shuffle
from math import sqrt

    
# implementation of functions from course notes

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

def dist(p, q):
    (x1,y1) = p
    (x2,y2) = q
    return (x1-x2)**2 + (y1-y2)**2

def plus(args):
    p = [0,0]
    for (x,y) in args:
        p[0] += x
        p[1] += y
    return tuple(p)

def scale(p, c):
    (x,y) = p
    return (x/c, y/c)

def permute(x):
    shuffled = [xi for xi in x]
    shuffle(shuffled)
    return shuffled

def avg(x): # Average
    return sum(x)/len(x)

def stddev(x): # Standard deviation.
    m = avg(x)
    return sqrt(sum([(xi-m)**2 for xi in x])/len(x))

def cov(x, y): # Covariance.
    return sum([(xi-avg(x))*(yi-avg(y)) for (xi,yi) in zip(x,y)])/len(x)

def corr(x, y): # Correlation coefficient.
    if stddev(x)*stddev(y) != 0:
        return cov(x, y)/(stddev(x)*stddev(y))

def p(x, y):
    c0 = corr(x, y)
    corrs = []
    for k in range(0, 2000):
        y_permuted = permute(y)
        corrs.append(corr(x, y_permuted))
    return len([c for c in corrs if abs(c) > c0])/len(corrs)
    

class optimization(dml.Algorithm):
    contributor = 'pt0713_silnuext'
    reads = ['pt0713_silnuext.property_2015', 'pt0713_silnuext.crime']
    writes = ['pt0713_silnuext.optimization']

    @staticmethod
    def execute(trial = True):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pt0713_silnuext', 'pt0713_silnuext')
        crime = repo.pt0713_silnuext.crime.find()
        property_2015 = repo.pt0713_silnuext.property_2015.find()
        repo.dropCollection("optimization")
        repo.createCollection("optimization")

        # getting zipcode data from local directory/internet

        myshp = open("pt0713_silnuext/zipcodes_nt/ZIPCODES_NT_POLY.shp", "rb")
        mydbf = open("pt0713_silnuext/zipcodes_nt/ZIPCODES_NT_POLY.dbf", "rb")
        r = shapefile.Reader(shp=myshp, dbf=mydbf)
        shapes = r.shapes()

        zipcode = [x[0] for x in r.records()]
        coor = [x.points for x in shapes]

        inProj = Proj(init='epsg:26986')
        outProj = Proj(init='epsg:4326')
        zip_to_coor = {}

        for i in range(len(zipcode)):
            for j in range(len(coor[i])):
                x1, y1 = coor[i][j][0], coor[i][j][1]
                x2, y2 = transform(inProj, outProj, x1, y1)
                coor[i][j] = [y2, x2]
                zip_to_coor[zipcode[i]] = coor[i]


        # getting coordination of crimes happened in 2015
        crime_coordination = project(crime, lambda x:(x["year"], x["month"], x["location"]["latitude"],x["location"]["longitude"]))     
        crime_15 = [crime_2015 for crime_2015 in crime_coordination if crime_2015[0] == "2015" and crime_2015[1] == "8"]
        crime_15coordination = [(float(latitude), float(longitude)) for (year, month, latitude, longitude) in crime_15]

        # getting coordination of properties that in the dataset of property assessment of 2015
        property15_price_coordination = project(property_2015, lambda x: (int(x["av_total"]), eval(str(x.get("location")))))


        print("Because our crime dataset is too large to run for k-means, we make it smaller by only taking a certain month of crime data.")
        print()
        print()
        print()

        # property r-tree
        def property_zipcode():
            zip_shapes = [(int(zipcode), Polygon(zip_to_coor[zipcode])) for zipcode in zip_to_coor]
            property_zip = {}
            rtidx = rtree.index.Index()
            for i in range(len(zip_shapes)):
                (zipcode, shape) = zip_shapes[i]
                rtidx.insert(zipcode, shape.bounds)

            for i in range(len(property15_price_coordination)):
                if property15_price_coordination[i][1] != 0 and property15_price_coordination[i][1] != None:
                    (lon, lat) = property15_price_coordination[i][1]
                    nearest = list(rtidx.nearest((lon, lat, lon, lat), 1))[0]
                    zipcode = '0' + str(nearest)
                if zipcode not in property_zip:
                    property_zip[zipcode] = [property15_price_coordination[i][0]]
                else:
                    property_zip[zipcode] += [property15_price_coordination[i][0]]

            return property_zip

        property_zipcode = property_zipcode()

        # crime r-tree
        def crime_zipcode():
            zip_shapes = [(int(zipcode), Polygon(zip_to_coor[zipcode])) for zipcode in zip_to_coor]
            crime_zip = {}
            rtidx = rtree.index.Index()
            for i in range(len(zip_shapes)):
                (zipcode, shape) = zip_shapes[i]
                rtidx.insert(zipcode, shape.bounds)

            for i in range(len(crime_15coordination)):
                (lon, lat) = crime_15coordination[i]
                nearest = list(rtidx.nearest((lon, lat, lon, lat), 1))[0]
                zipcode = '0' + str(nearest)
                if zipcode not in crime_zip:
                    crime_zip[zipcode] = [crime_15coordination[i]]
                else:
                    crime_zip[zipcode] += [crime_15coordination[i]]

            return crime_zip

        crime_zipcode = crime_zipcode()


        # k-means function to find two properties that is furthest from crime reporting places
        # initialize two random locations        
        M = [(42,-71),(41,-70)]

        def k_means(P,M):
            OLD = []
            while OLD != M:
                OLD = M

                MPD = [(m, p, dist(m,p)) for (m, p) in product(M, P)]
                PDs = [(p, dist(m,p)) for (m, p, d) in MPD]
                PD = aggregate(PDs, max)
                MP = [(m, p) for ((m,p,d), (p2,d2)) in product(MPD, PD) if p==p2 and d==d2]
                MT = aggregate(MP, plus)

                M1 = [(m, 1) for ((m,p,d), (p2,d2)) in product(MPD, PD) if p==p2 and d==d2]
                MC = aggregate(M1, sum)

                M = [scale(t,c) for ((m,t),(m2,c)) in product(MT, MC) if m == m2]

            return sorted(M)

        print("We are going to find the property that is closest to the coordinate(s): ")
        k_means_result = k_means(crime_15coordination,M)
        print(k_means_result)
        print()

        # put result get from k-means into r tree to find which zipcode is the best place to live that is as far as possible from crime areas
        def kmeans_zipcode():
            zip_shapes = [(int(zipcode), Polygon(zip_to_coor[zipcode])) for zipcode in zip_to_coor]
            rtidx = rtree.index.Index()
            for i in range(len(zip_shapes)):
                (zipcode, shape) = zip_shapes[i]
                rtidx.insert(zipcode, shape.bounds)

            (lon, lat) = k_means_result[1]
            nearest = list(rtidx.nearest((lon, lat, lon, lat), 1))[0]
            zipcode = '0' + str(nearest)
            return zipcode

        print("The zipcode that is the best place to live and is as far away as crime areas is: ")
        print(kmeans_zipcode())

 
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
        

        this_script = doc.agent('alg:pt0713_silnuext#optimization', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        crimedata = doc.entity('bdp:crime', {'prov:label':'crime', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        property2015data = doc.entity('bdp:n7za-nsjh', {'prov:label':'property_2015', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        
        k_means = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(k_means, this_script)

        doc.usage(k_means, property2015data, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Computation',})

        best_zipcode = doc.entity("dat:pt0713_silnuext#best_zipcode", {prov.model.PROV_LABEL:"Best Zipcode of Living with Least Crime Numbers Around", prov.model.PROV_TYPE:"ont:DataSet"})
        doc.wasAttributedTo(best_zipcode, this_script)
        doc.wasGeneratedBy(best_zipcode, k_means, endTime)
        doc.wasDerivedFrom(best_zipcode, crimedata, k_means, k_means, k_means)

        repo.logout()
                  
        return doc

optimization.execute()
doc = optimization.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
