import pandas as pd
import json
import geojson
from geojson import Point
from geojson import MultiPoint
from geojson import LineString
from geojson import MultiLineString
from geojson import GeometryCollection
import urllib.request




#google_route = "../dataset/route.json"
#output_file = "../result/result_route.geojson"
#url = "https://maps.googleapis.com/maps/api/directions/json?origin=49.288452138888886,-123.11507413888889&destination=49.285911,-123.120948&waypoints=49.2887562,-123.1150926|49.2893832,-123.117621|49.288042,-123.119169|49.2875974,-123.1191416|&mode=bicycling&language=en&key=AIzaSyC_OqhNkCgXZJlg5O3JEIGN4kHlF7YxKKo"

#response = urllib.request.urlopen(url).read()
def get_all_visit_point(row):
    lat = row['loc'][0]
    lng = row['loc'][1]
    point = (lng,lat)
    return point

def out_put_geojson(visit_place_df,google_response):
    visit_place_df['geojson_points'] = visit_place_df.apply(get_all_visit_point,axis = 1)
    visit_point_list = visit_place_df['geojson_points'].tolist()
    #print(visit_place_df['geojson_points'])
    #print(visit_point_list)
    
    node_data = json.loads(google_response)
    #print(len(node_data['routes'][0]['legs']))
    route = []
    start_location = (node_data['routes'][0]['legs'][0]['start_location']['lng'],
    node_data['routes'][0]['legs'][0]['start_location']['lat'])
    #print(start_location)
    route.append(start_location)

    for legs in node_data['routes'][0]['legs']:
        #print(len(legs['steps']))
        for steps in legs['steps']:
            end_location = (steps['end_location']['lng'],steps['end_location']['lat'])
            #print(end_location)
            route.append(end_location)
        #route.append("end")
        
    #print(route)
    #print(LineString(route))
    collection = []
    for points in visit_point_list:
        #print(points)
        geo_point_object = Point((points[0],points[1]))
        collection.append(geo_point_object)
    #print(collection)
    
    collection.append(LineString(route))

    #my_point = Point((-123.1151695, 49.2884587))
    #print(my_point)
    geo_collection = GeometryCollection(collection)
    return geo_collection
#print(geo_collection)

# print(response)
# result=out_put_geojson(response)
# print(result)

# with open(output_file, 'w') as f:
#     geojson.dump(result, f) 
#dump = geojson.dumps(my_point, sort_keys=True)
       


#google_route = pd.read_json(node_data['routes']['legs'],orient='records')
# google_route = pd.DataFrame(node_data['routes'][0]['legs'])
# print(google_route)
# result_output_path = "../dataset/parse_route.json"
# google_route.to_json(result_output_path, orient = 'records',lines=True) 
