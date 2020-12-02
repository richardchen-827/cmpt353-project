#main file to run our program

from distance_calculate import distance_formula,distance_formula_row
from extract_gps import extractGPS
import pandas as pd
import numpy as np
import sys
import os 


def main(imgFileName,travelMode):

	#get the image file exif info 
	path = '../sample_images/'
	path = os.path.join(path,imgFileName)
	print(travelMode)
	coordinate = (extractGPS(path))

	#get data
	dataset_path = "../dataset/all.json.gz"
	osm_dataset = pd.read_json(dataset_path,compression = 'gzip',lines=True)

	osm_dataset = osm_dataset.assign(user_lat=coordinate[0])
	osm_dataset = osm_dataset.assign(user_lon=coordinate[1])

	#cleaning data
	osm_dataset = osm_dataset.dropna(subset=['name']) # remove all place that doesnt have a name

	#assign weight according to the attraction condition
	condition = [
				(osm_dataset['amenity'] == 'tourism'),
				(osm_dataset['amenity'] == 'cinema'),
				(osm_dataset['amenity'] == 'theatre'),
				(osm_dataset['amenity'] == 'park'),
				(osm_dataset['amenity'] == 'restaurant'),
				(osm_dataset['amenity'] == 'bar'),
				(osm_dataset['amenity'] == 'pub'),
				(osm_dataset['amenity'] == 'fast_food'),
				(osm_dataset['amenity'] == 'cafe'),
				(osm_dataset['amenity'] == 'nightclub'),
				(osm_dataset['amenity'] == 'casino')
				]
	values = [11,10,9,8,7,6,5,4,3,2,1]
	osm_dataset['weight'] = np.select(condition,values)
	
	#remove all the place that is not a restaurant or tourism attraction
	osm_dataset = osm_dataset[~(osm_dataset['weight'] < 1)]

	#calculate distance of each place from the image input
	osm_dataset['distance'] = osm_dataset.apply(distance_formula_row,axis = 1)

	#detect what the user might be interest in from the image input 
	possible_interest = osm_dataset[osm_dataset['distance'] < 100]
	possible_interest = possible_interest.weight.max()

	#assign search radius according to travel method
	search_radius = 0
	if (travelMode == 'walk'):
		search_radius = 1000
	elif(travelMode == 'bike'):
		search_radius = 2000
	else:
		search_radius = 3000

	#get a list of attraction base on the search radius
	filter_osm_dataset = osm_dataset[osm_dataset['distance'] <= search_radius]
	filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
	filter_osm_dataset = filter_osm_dataset[['amenity','name','tags','weight','distance','loc','user_lon','user_lat']]

	#base on the possible interest get the attraction within the search radius
	if (possible_interest > 7): #interest in tourism 
		#TODO using greedy algorithm to find the shortest D first 2T
		attrac_list = filter_osm_dataset[filter_osm_dataset['weight'] > 7]
		print(attrac_list)
		#TODO using greedy to find the restaurant with the shortest D from previous T
		#TODO using greedy to find 2T with shortest D from previous restaurant

	#else: #interest in food first


	
	result_output_path = "../dataset/result.json"
	filter_osm_dataset.to_json(result_output_path, orient = 'records',lines=True) 
	#distance = distance_formula(user_lat,user_lon)
	#park = osm_dataset[osm_dataset['amenity'] == 'park']

	#print(park)

if __name__=='__main__':
	imgFileName = sys.argv[1]
	travelMode = sys.argv[2]
	main(imgFileName,travelMode)