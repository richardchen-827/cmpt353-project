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
    


park_path = "../dataset/parks.json"

van_park_dataset = pd.read_json(park_path,orient = 'records')
#print(van_park_dataset)
van_park_dataset['park_name'] = (van_park_dataset.apply(get_park_name,axis=1))
van_park_dataset['park_location'] = (van_park_dataset.apply(get_park_loc,axis=1))
van_park_dataset['park_str'] = (van_park_dataset.apply(get_park_strname,axis=1))
clean_van_park_dataset = van_park_dataset[['park_name', 'park_location','park_str']]

# print(van_park_dataset['name'])
print(clean_van_park_dataset)
#print(osm_dataset)