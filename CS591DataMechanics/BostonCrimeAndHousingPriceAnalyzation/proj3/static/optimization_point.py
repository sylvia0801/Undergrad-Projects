import geojson

features = []
properties = {'specific point': "Safest Point in Boston",
			  'acheiving way': "k-means",
			  'coordinates': [
			    -71.0831821237185, 
			    42.3211059996542
			  ]
			  }
geometry = geojson.Point([-71.08318212371852, 42.32110599965421])
features.append(geojson.Feature(geometry=geometry, properties=properties))


open('optimization.geojson', 'w').write(geojson.dumps(geojson.FeatureCollection(features)))