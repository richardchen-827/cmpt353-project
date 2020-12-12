import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sklearn.cluster import KMeans

seaborn.set()

#Since in the giving dataset, there are many benches records, we removed them for our main project, since we think for 
#tourism purpose, people will not too interested in visiting benches.

#However, for those removed benches, we actually want to know, over the range of Metro Vancouver, which area has relatively more 
#benches, are those benches can beformed into a cluster so that we can probably make a conclusion for those benches in 
#different region


def get_lat(row):
    return row['loc'][0]

def get_lon(row):
    return row['loc'][1]

#import the dataframe
data_path = "../dataset/all.json.gz"

all_data = pd.read_json(data_path,lines=True,compression="gzip")

#print(all_data)

#only keep those amentity that are bench
bench_data = all_data[all_data['amenity'] == "bench"]
bench_data = bench_data.copy()
bench_data['lat'] = bench_data.apply(get_lat,axis=1)
bench_data['lon'] = bench_data.apply(get_lon,axis=1)
#print(bench_data)
plt.scatter(bench_data['lon'],bench_data['lat'])
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Metro Vancouver Benches Distribution 10 Clusters")
#plt.show()


#try to use KMeans cluster to group those benches
# bench_loc = bench_data['loc'].values
# print(bench_loc)
model = KMeans()
y_kmeans  = model.fit_predict(bench_data[['lat', 'lon']])
#print((y_kmeans))
bench_data['label'] = model.labels_
#print(bench_data)

plt.scatter(bench_data['lon'],bench_data['lat'], c=bench_data['label'])

#maybe add the cluster center for it
#seaborn.scatterplot('lon', 'lat', data=bench_data, hue='label')

plt.show()