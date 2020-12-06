import pandas as pd 

dataset_path = "../dataset/result.json"
visit_place_df = pd.read_json(dataset_path,lines=True)
#print(visit_place_df)

def get_loc_string(row):
    loc = row['loc']
    loc_string = str(loc[0])+","+str(loc[1])
    return loc_string

def parse_loc(travel_mode,img_coordinate,visit_place_df):
    visit_place_df['loc_str'] = visit_place_df.apply(get_loc_string,axis=1)
    way_points_list = visit_place_df['loc_str'].tolist()
    
    #print(way_points_list)
    api_url = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = "origin="+img_coordinate+"&"
    destination = "destination="+way_points_list[-1]+"&"
    #remove the last item in the list
    way_points_list = way_points_list[:-1]
    waypoints = "waypoints="
    for points in way_points_list:
        waypoints = waypoints + points + "|"
    setup = "&mode=" + travel_mode
    lang = "&language=en"
    apikey = "&key=AIzaSyC_OqhNkCgXZJlg5O3JEIGN4kHlF7YxKKo"

    request_url = api_url + origin + destination + waypoints + setup + lang + apikey
    return request_url



#url = parse_loc("bicycling","49.288452138888886,-123.11507413888889",visit_place_df)
#print(url)

# https://maps.googleapis.com/maps/api/directions/json?
# origin=49.288452138888886,-123.11507413888889&destination=49.285911,-123.120948
# &waypoints=49.2887562,-123.1150926|49.2893832,-123.117621|49.288042,-123.119169|49.2875974,-123.1191416|
# &mode=bicycling&language=en&key=AIzaSyC_OqhNkCgXZJlg5O3JEIGN4kHlF7YxKKo

#https://maps.googleapis.com/maps/api/directions/json?origin=49.288452138888886,-123.11507413888889&destination=49.285911,-123.120948&waypoints=49.2887562,-123.1150926|49.2893832,-123.117621|49.288042,-123.119169|49.2875974,-123.1191416|&mode=bicycling&language=en&key=AIzaSyC_OqhNkCgXZJlg5O3JEIGN4kHlF7YxKKo
