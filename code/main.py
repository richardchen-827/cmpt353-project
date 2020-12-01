#main file to run our program

from distance_calculate import distance_formula,distance_formula_row
from extract_gps import extractGPS
import pandas as pd
#pd.set_option('display.max_rows', None)

#get the image file exif info 
coordinate = (extractGPS('../sample_images/img5.jpg'))
#print(coordinate)
# user_lat = coordinate[0]
# user_lon = coordinate[1]

dataset_path = "../dataset/all.json.gz"
osm_dataset = pd.read_json(dataset_path,compression = 'gzip',lines=True)

osm_dataset = osm_dataset.assign(user_lat=coordinate[0])
osm_dataset = osm_dataset.assign(user_lon=coordinate[1])


osm_dataset['distance'] = osm_dataset.apply(distance_formula_row,axis = 1)

filter_osm_dataset = osm_dataset[osm_dataset['distance'] < 1000]
filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])

filter_osm_dataset = filter_osm_dataset[['amenity','name','tags','distance']]
filter_osm_dataset = (filter_osm_dataset[filter_osm_dataset['amenity'] != 'bench'])
print(filter_osm_dataset)
result_output_path = "../dataset/result.json"
filter_osm_dataset.to_json(result_output_path, orient = 'records',lines=True) 
#distance = distance_formula(user_lat,user_lon)
#park = osm_dataset[osm_dataset['amenity'] == 'park']

#print(park)