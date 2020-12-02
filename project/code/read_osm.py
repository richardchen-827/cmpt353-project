import pandas as pd
def combine_lat_lon(row):
    return (row['lat'],row['lon'])
    
osm_path = "../dataset/amenities-vancouver.json.gz"
osm_dataset = pd.read_json(osm_path,compression = 'gzip',lines=True)
osm_dataset['loc'] = osm_dataset.apply(combine_lat_lon, axis = 1)
osm_dataset = osm_dataset.drop(columns=['timestamp','lat','lon'])
osm_output_path = "../dataset/clean_osm.json.gz"
osm_dataset.to_json(osm_output_path, orient = 'records',lines=True,compression = 'gzip') 

# osm_path = "../dataset/clean_osm.json.gz"
# osm_dataset = pd.read_json(osm_path,compression = 'gzip',lines=True)

#print(osm_dataset.iloc[0]['tags']['cuisine'])