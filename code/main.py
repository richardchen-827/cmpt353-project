#main file to run our program
from distance_calculate import distance_formula,distance_formula_row
from extract_gps import extractGPS
from parse_loc import parse_loc
from read_google_json import out_put_geojson
from checkFamous import checkTags
from checkEmpty import checkEmp
import urllib.request
import geojson
import pandas as pd
import numpy as np
import sys
import os 


def main(imgFileName,travelMode):

	if ((travelMode != 'walk') and (travelMode != 'bike') and (travelMode != 'drive')):
		print("\nPlease input the right travel mode (walk, bike or drive)")
		return

	#get the image file exif info 
	path = '../sample_images/'
	path = os.path.join(path,imgFileName)
	coordinate = (extractGPS(path))
	print("\ncoordinate from the pic: " + str(coordinate) + "\n")

	#get data
	dataset_path = "../dataset/all.json.gz"
	osm_dataset = pd.read_json(dataset_path,compression = 'gzip',lines=True)

	osm_dataset = osm_dataset.assign(user_lat=coordinate[0])
	osm_dataset = osm_dataset.assign(user_lon=coordinate[1])

	#cleaning data
	osm_dataset = osm_dataset.dropna(subset=['name']) # remove all place that doesnt have a name

	#assign weight according to the attraction condition
	condition = [
				(osm_dataset['amenity'] == 'tourism'), 		#11
				(osm_dataset['amenity'] == 'park'),			#10
				(osm_dataset['amenity'] == 'cinema'), 		#9
				(osm_dataset['amenity'] == 'theatre'),		#8
				(osm_dataset['amenity'] == 'restaurant'),	#7
				(osm_dataset['amenity'] == 'bar'),			#6
				(osm_dataset['amenity'] == 'pub'),			#5
				(osm_dataset['amenity'] == 'fast_food'),	#4
				(osm_dataset['amenity'] == 'cafe'),			#3
				(osm_dataset['amenity'] == 'nightclub'),	#2
				(osm_dataset['amenity'] == 'casino')		#1
				]
	values = [11,10,9,8,7,6,5,4,3,2,1]
	osm_dataset['weight'] = np.select(condition,values)
	
	#remove all the place that is not a restaurant or tourism attraction
	osm_dataset = osm_dataset[~(osm_dataset['weight'] < 1)]

	#calculate distance of each place from the image input
	osm_dataset['distance'] = osm_dataset.apply(distance_formula_row,axis = 1)
	#print(osm_dataset.sort_values(by=['distance']))

	#detect what the user might be interested in first from the image input 
	possible_interest = osm_dataset[osm_dataset['distance'] < 100]
	# if cannot find anything make attraction as default
	if (possible_interest.empty): 
		possible_interest = 8 
	else:
		possible_interest = possible_interest.weight.max()

	if (possible_interest > 7):
		print("User interests in Tourism first\n")
	else:
		print("User interests in Restaurant first\n")

	#assign search radius according to travel method
	search_radius = 0
	if (travelMode == 'walk'):
		search_radius = 1000 #in meter
	elif(travelMode == 'bike'):
		search_radius = 10000
	else: 
		search_radius = 50000

	#get a list of attraction base on the search radius
	filter_osm_dataset = osm_dataset[osm_dataset['distance'] <= search_radius]
	filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])

	#remove the duplicate place
	filter_osm_dataset = filter_osm_dataset.drop_duplicates(subset=['name'],keep='first')
	
	#kept only the usefull column 
	filter_osm_dataset = filter_osm_dataset[['amenity','name','tags','user_lon','user_lat','distance','weight','loc']]
	
	#further filter out the attraction and food base on the travel mode
	if (travelMode == 'drive'):
		filter_osm_dataset['tourismTag'] = filter_osm_dataset['tags'].apply(checkTags)
		filter_osm_dataset = filter_osm_dataset[((filter_osm_dataset['tourismTag'] == 'true') | ((filter_osm_dataset['weight'] <= 7) & (filter_osm_dataset['weight'] >= 5) ))]
	elif (travelMode == 'bike'):
		#remove fake park
		filter_osm_dataset['tagsEmpty'] = filter_osm_dataset['tags'].apply(checkEmp)
		filter_osm_dataset = filter_osm_dataset[((filter_osm_dataset['tagsEmpty'] == False) & (filter_osm_dataset['amenity'] == 'park') ) | ((filter_osm_dataset['weight'] <= 4) & (filter_osm_dataset['weight'] >= 3))]
		#print(filter_osm_dataset[['name','weight']])


	#base on the possible interest get the attraction within the search radius
	visit_place = []
	#TODO
	#make different selection for drive, walk, and bike
	if (possible_interest > 7): #interest in tourism 
		#TODO using greedy algorithm to find the shortest D first 2T
		attrac_list_first = filter_osm_dataset[filter_osm_dataset['weight'] > 7]
		#print(filter_osm_dataset)
		#print(attrac_list)
		attrac_list_first = attrac_list_first.head(1)
		#print(attrac_list_first)
		attrac_list_first  =attrac_list_first[['amenity','name','tags','distance','weight','loc']]
		attrac_list_first_dic = attrac_list_first.to_dict('records')
		#print(filter_osm_dataset.shape[0])
		#print((attrac_list_first_two_dic))
		for places in attrac_list_first_dic:
			#add to the visit place
			visit_place.append(places)
			#remove from the orginal list ??????????????????? need to discuss (not too sure if there are duplicate)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		

		############ 2nd toursim ############
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		#set the new user lat and lon based on the last position
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		#print(visit_place)
		#print(filter_osm_dataset)

		
		attrac_list_second = filter_osm_dataset[filter_osm_dataset['weight'] > 7]
		attrac_list_second = attrac_list_second.head(1)
		attrac_list_second  =attrac_list_second[['amenity','name','tags','distance','weight','loc']]
		attrac_list_second_dic = attrac_list_second.to_dict('records')
		#print(filter_osm_dataset.shape[0])
		for places in attrac_list_second_dic:
			#add to the visit place
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]

		# print(visit_place)
		
		############ 3rd food ############
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		#set the new user lat and lon based on the last position
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		
		#add into our visit place list
		attrac_list_third = filter_osm_dataset[filter_osm_dataset['weight'] < 7]
		attrac_list_third = attrac_list_third.head(1)
		attrac_list_third = attrac_list_third[['amenity','name','tags','distance','weight','loc']]
		attrac_list_third_dic = attrac_list_third.to_dict('records')

		#add to the list 
		#print(filter_osm_dataset.shape[0])
		for places in attrac_list_third_dic:
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		#print(visit_place)
		#print(filter_osm_dataset)



		
		############ 4th toursim ############
		#assign the new location
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)
		#print(filter_osm_dataset[['user_lat','user_lon']])
		
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		#now only interesting in tourism
		attrac_list_fourth = filter_osm_dataset[filter_osm_dataset['weight'] >=8]
		#choose the closest tourism
		attrac_list_fourth = attrac_list_fourth.head(1)
		attrac_list_fourth = attrac_list_fourth[['amenity','name','tags','distance','weight','loc']]
		attrac_list_fourth_dic = attrac_list_fourth.to_dict('records')
		#print(attrac_list_fourth_dic)
		
		#print(filter_osm_dataset.shape[0])
		for places in attrac_list_fourth_dic:
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		#print(visit_place)
		#print(filter_osm_dataset)


		############ 5th toursim ############
		#assign the new location
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)
		#print(filter_osm_dataset[['user_lat','user_lon']])
		#return
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		#now only interesting in tourism
		attrac_list_fifth = filter_osm_dataset[filter_osm_dataset['weight'] >=8]
		#choose the closest tourism
		attrac_list_fifth = attrac_list_fifth.head(1)
		attrac_list_fifth = attrac_list_fifth[['amenity','name','tags','distance','weight','loc']]
		attrac_list_fifth_dic = attrac_list_fifth.to_dict('records')
		#print(attrac_list_fifth_dic)

		#print(filter_osm_dataset.shape[0])
		for places in attrac_list_fifth_dic:
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		
		#print(visit_place)
		#print(filter_osm_dataset.shape[0])
		visit_place_df = pd.DataFrame(visit_place)


	#else: #interest in food first
	else:	#interest in food
		############ 1st food ############
		attrac_list = filter_osm_dataset[(filter_osm_dataset['weight'] <=7) & (filter_osm_dataset['weight'] >=3)]
		attrac_list_first = attrac_list.head(1)
		attrac_list_first  =attrac_list_first[['amenity','name','tags','distance','weight','loc']]
		attrac_list_first_dic = attrac_list_first.to_dict('records')	
		#print(filter_osm_dataset)
		#print(attrac_list_first_two_dic)
		#print(filter_osm_dataset)
		for places in attrac_list_first_dic:
			#add to the visit place
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		#print(visit_place)
		#print(filter_osm_dataset[['user_lat','user_lon']])

		############ 2nd tourism ############
		############ 3rd tourism ############
		#set the new user lat and lon based on the last position
		for i in range(2):
			new_user_lat = visit_place[-1]['loc'][0]
			new_user_lon =  visit_place[-1]['loc'][1]
			filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
			filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)
			#print(filter_osm_dataset[['user_lat','user_lon']])
			#calculate the distance for each of the POI from the list
			filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
			filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
			#print(filter_osm_dataset.shape[0])
			attrac_list_second_third = filter_osm_dataset[filter_osm_dataset['weight']>=8]
			#print(attrac_list_second_third)
			attrac_list_second_third = attrac_list_second_third.head(1)
			attrac_list_second_third = attrac_list_second_third[['amenity','name','tags','distance','weight','loc']]
			attrac_list_second_third_dic  = attrac_list_second_third.to_dict('records')

			#print(filter_osm_dataset)
			for places in attrac_list_second_third_dic:
				visit_place.append(places)
				filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
			# print(visit_place)
			# print(filter_osm_dataset.shape[0])
		#print(visit_place)

			
		#print(filter_osm_dataset)
		#print(filter_osm_dataset['user_lat'])
		
		############ 4th food ############
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)	
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		#print(filter_osm_dataset)
		#choose the closest one restaurant
		attrac_list_fourth = filter_osm_dataset[(filter_osm_dataset['weight'] <=7) & (filter_osm_dataset['weight'] >=3)]
		#print(attrac_list_fourth)
		attrac_list_fourth = attrac_list_fourth.head(1)
		attrac_list_fourth = attrac_list_fourth[['amenity','name','tags','distance','weight','loc']]
		attrac_list_fourth_dic = attrac_list_fourth.to_dict('records')
		#print(attrac_list_fifth_dic)
		for places in attrac_list_fourth_dic:
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]


		############ 5th tourism ############
		new_user_lat = visit_place[-1]['loc'][0]
		new_user_lon =  visit_place[-1]['loc'][1]
		filter_osm_dataset = filter_osm_dataset.assign(user_lat=new_user_lat)
		filter_osm_dataset = filter_osm_dataset.assign(user_lon=new_user_lon)	
		#calculate the distance for each of the POI from the list range
		filter_osm_dataset['distance'] = filter_osm_dataset.apply(distance_formula_row,axis = 1)
		filter_osm_dataset = filter_osm_dataset.sort_values(by=['distance'])
		attrac_list_fifth = filter_osm_dataset[filter_osm_dataset['weight']>=8]
		attrac_list_fifth = attrac_list_fifth.head(1)
		attrac_list_fifth = attrac_list_fifth[['amenity','name','tags','distance','weight','loc']]
		attrac_list_fifth_dic = attrac_list_fifth.to_dict('records')
		# print(filter_osm_dataset.shape[0])
		for places in attrac_list_fifth_dic:
			visit_place.append(places)
			filter_osm_dataset = filter_osm_dataset[(filter_osm_dataset['distance']!=places['distance'])]
		# print(filter_osm_dataset.shape[0])
		# print(visit_place)
		# 		
		#print(filter_osm_dataset)
		visit_place_df = pd.DataFrame(visit_place)
		#print(visit_place_df)

	print("Your Travle list is:")
	print(visit_place_df[['amenity','name','distance']])
	result_output_path = "../dataset/result.json"
	visit_place_df.to_json(result_output_path, orient = 'records',lines=True) 
	#distance = distance_formula(user_lat,user_lon)
	#park = osm_dataset[osm_dataset['amenity'] == 'park']

	#################parse the location so that we can fit into the google api#################
	if(travelMode == 'walk'):
		api_mode = "walking" 
	elif(travelMode ==  'bike'):
		api_mode = "bicycling" 
	elif(travelMode ==  'drive'):
		api_mode = "driving" 
	
	img_coordinate = str(coordinate[0])+","+str(coordinate[1])
	#print(img_coordinate)
	request_url = parse_loc(api_mode,img_coordinate,visit_place_df)
	#print(request_url)


	#################put google api to result#################
	#TODO
	response = urllib.request.urlopen(request_url).read()
	result = out_put_geojson(visit_place_df,response)
	output_file = "../result/result_route.geojson"
	with open(output_file, 'w') as f:
		geojson.dump(result, f) 

	
	#print(park)

if __name__=='__main__':
	imgFileName = sys.argv[1]
	travelMode = sys.argv[2]
	main(imgFileName,travelMode)