import pandas as pd
import numpy as np
import sys
import os 
from distance_calculate import distance_formula,distance_formula_row
from checkEmpty import checkEmp
from checkBackRest import checkBackRest
from scipy import stats




def main():
	dataset_path = "../dataset/all.json.gz"
	data = pd.read_json(dataset_path, compression = 'gzip',lines=True)

	#get all the bench that is within the 5km radius of Stanley park
	park = data[(data['amenity'] == 'park') & (data['name'] == 'Stanley Park')]
	park = park['loc']
	park_lat = park.iloc[0][0]
	park_long = park.iloc[0][1]
	park_bench = data[data['amenity'] == 'bench']
	park_bench = park_bench[['tags','loc']]
	park_bench = park_bench.assign(user_lat=park_lat)
	park_bench = park_bench.assign(user_lon=park_long)
	park_bench['distance'] = park_bench.apply(distance_formula_row,axis = 1)
	park_bench = park_bench[park_bench['distance'] <= 5000]
	park_bench = park_bench[['tags','distance']]

	#get total number of bench in park
	park_bench_total = len(park_bench['distance'])
	
	#get number of bench that does have back rest
	park_bench['backRest'] = park_bench['tags'].apply(checkBackRest)
	park_bench_withBR = len(park_bench[park_bench['backRest'] == True])
	
	#get number of bench that does not have back rest
	park_bench_noBR = park_bench_total - park_bench_withBR


	#get all the bench that is within the 5km radius of gotham restaurant (center of vancouver)
	city = data[(data['amenity'] == 'restaurant') & (data['name'] == 'Gotham')]
	city = city['loc']
	city_lat = city.iloc[0][0]
	city_long = city.iloc[0][1]	
	city_bench = data[data['amenity'] == 'bench']
	city_bench = city_bench[['tags','loc']]
	city_bench = city_bench.assign(user_lat=city_lat)
	city_bench = city_bench.assign(user_lon=city_long)
	city_bench['distance'] = city_bench.apply(distance_formula_row,axis = 1)
	city_bench = city_bench[city_bench['distance'] <= 5000]
	city_bench = city_bench[['tags','distance']]
	
	#get total number of bench in city
	city_bench_total = len(city_bench['distance'])
	
	#get number of bench that does have back rest
	city_bench['backRest'] = city_bench['tags'].apply(checkBackRest)
	city_bench_withBR = len(city_bench[city_bench['backRest'] == True])
	
	#get number of bench that does not have back rest
	city_bench_noBR = city_bench_total - city_bench_withBR

	#chi-square test (does the place you are in affect the type of bench you get)
	contingency = [[park_bench_withBR,park_bench_noBR],[city_bench_withBR,city_bench_noBR]]
	chi2,p,dof,expected = stats.chi2_contingency(contingency)
	print('\nThe p value that we got is: ' + str(p))
	
	if (p < 0.05):
		print('\nThus, the bench quality does matter on which area you are in')
	else:
		print('\nThus, the bench quality does not matter on which area you are in')






if __name__ == '__main__':
    main()