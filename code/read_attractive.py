import pandas as pd
import json

def get_loc_node(row):
    return (row['lat'],row['lon'])
def get_name_node(row):
    if 'name' in row['tags']:
        return row['tags']['name']
    else:
        return None
        




node_attractive_path = "../dataset/attractive_points_node.json"
way_attractive_path = "../dataset/attractive_points_way.json"
relation_attractive_path = "../dataset/attractive_points_relation.json"

#node tourism
node_data = json.load(open(node_attractive_path))
attractive_points_node_dataset = pd.DataFrame(node_data["elements"])

attractive_points_node_dataset['loc'] = attractive_points_node_dataset.apply(get_loc_node,axis= 1)
attractive_points_node_dataset['name'] = attractive_points_node_dataset.apply(get_name_node,axis= 1)
attractive_points_node_dataset = attractive_points_node_dataset.assign(amenity='tourism')
attractive_points_node_dataset = attractive_points_node_dataset[['amenity','name', 'loc','tags']]

#print(attractive_points_node_dataset)

def get_loc_way(row):
    return(row['center']['lat'],row['center']['lon'])

def get_name_way(row):
    if 'name' in row['tags']:
        return row['tags']['name']
    else:
        return None


#way tourism
way_data = json.load(open(way_attractive_path,'rb'))
attractive_points_way_dataset = pd.DataFrame(way_data["elements"])
attractive_points_way_dataset['loc'] = attractive_points_way_dataset.apply(get_loc_way,axis=1)
attractive_points_way_dataset['name'] = attractive_points_way_dataset.apply(get_name_way,axis=1)
attractive_points_way_dataset = attractive_points_way_dataset.assign(amenity='tourism')
attractive_points_way_dataset = attractive_points_way_dataset[['amenity','name', 'loc','tags']]
#print(attractive_points_way_dataset)




#relation tourism
relation_data = json.load(open(relation_attractive_path))
attractive_points_relation_dataset = pd.DataFrame(relation_data["elements"])
attractive_points_relation_dataset['loc'] = attractive_points_relation_dataset.apply(get_loc_way,axis=1)
attractive_points_relation_dataset['name'] = attractive_points_relation_dataset.apply(get_name_way,axis=1)
attractive_points_relation_dataset = attractive_points_relation_dataset.assign(amenity='tourism')
attractive_points_relation_dataset = attractive_points_relation_dataset[['amenity','name', 'loc','tags']]

#print(attractive_points_relation_dataset)

all_data = attractive_points_node_dataset.append(attractive_points_way_dataset,ignore_index=True)
all_data = all_data.append(attractive_points_relation_dataset,ignore_index=True)
#print(all_data)

attractive_output_path = "../dataset/clean_attractive.json"
all_data.to_json(attractive_output_path, orient = 'records',lines=True) 

# df = pd.DataFrame(data["elements"])
# # attractive_dataset = pd.read_json(attractive_path)
# # print(attractive_dataset)
# import json

# with open(attractive_path) as project_file:    
#     data = json.load(project_file)  

# df = pd.json_normalize(data)
# print(df)
# import json
# import pandas as pd
# data = json.load(open(attractive_path,'rb'))

# df = pd.DataFrame(data["elements"])
# print(df)