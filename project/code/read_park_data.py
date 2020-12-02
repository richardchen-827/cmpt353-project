import pandas as pd
#pd.set_option('display.max_columns', None)

def get_park_name(row):
    park_name = row['fields']['name']
    return park_name

def get_park_loc(row):
    park_gps = row['fields']['googlemapdest']

    return (park_gps[0],park_gps[1])

def get_park_strname(row):
    park_street = row['fields']['streetname']
    return park_street

def make_tag(row):
    tags = {}
    tags['addr:street'] = row['fields']['streetname']
    return tags
    


park_path = "../dataset/parks.json"

van_park_dataset = pd.read_json(park_path,orient = 'records')
#print(van_park_dataset)
van_park_dataset['name'] = (van_park_dataset.apply(get_park_name,axis=1))
van_park_dataset['loc'] = (van_park_dataset.apply(get_park_loc,axis=1))
van_park_dataset['tags'] = (van_park_dataset.apply(make_tag,axis=1))
clean_van_park_dataset = van_park_dataset[['name', 'loc','tags']]
clean_van_park_dataset = clean_van_park_dataset.assign(amenity='park')
# clean_van_park_dataset['amenity'] = 'park'



# print(van_park_dataset['name'])
#print(clean_van_park_dataset)
park_output_path = "../dataset/clean_park.json.gz"
clean_van_park_dataset.to_json(park_output_path, orient = 'records',lines=True,compression = 'gzip') 
#print(osm_dataset)