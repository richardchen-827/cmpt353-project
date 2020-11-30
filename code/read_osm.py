import pandas as pd
def combine_lat_lon(row):
    return (row['lat'],row['lon'])
    
osm_path = "../dataset/amenities-vancouver.json.gz"
osm_dataset = pd.read_json(osm_path,compression = 'gzip',lines=True)
osm_dataset['loc'] = osm_dataset.apply(combine_lat_lon, axis = 1)
print(osm_dataset)