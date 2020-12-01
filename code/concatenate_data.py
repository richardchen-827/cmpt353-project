import pandas as pd
osm_path = "../dataset/clean_osm.json.gz"
osm_dataset = pd.read_json(osm_path,compression = 'gzip',lines=True)

park_osm_path = "../dataset/clean_park.json.gz"
park_dataset = pd.read_json(park_osm_path,compression = 'gzip',lines=True)

#print(osm_dataset)
#print(park_dataset)

all_data = osm_dataset.append(park_dataset,ignore_index=True)

all_data_output_path = "../dataset/all.json.gz"
all_data.to_json(all_data_output_path, orient = 'records',lines=True,compression = 'gzip') 
#print(all_data)