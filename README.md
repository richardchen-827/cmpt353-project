# cmpt353-project
Repo of CMPT353 Final Project

# extra packages requirement (assuming you are running with Anaconda)
1) pip install gpsphoto
2) pip install exifread
3) pip install piexif
4) pip install geojson

# running main application
1) open terminal with path to the "code" folder
2) run: py main.py ImageFileName travelMode
note: 
 - ImageFileName: 
   - Can be any image file name from the sample_images folder, or any personal image with geotaggged copy to the sample_images folder
 - travelMode:
   - Can be walk, bike or drive
 
# viewing the result from main application 
1) in terminal:
 - will print out a list of places that the program suggest the user to visit
2) viewing in map with direction 
 - in the result folder, can open the result file by using this link 'https://geojson.io/#map=2/20.0/0.0'

# running stats analysis 
1) open terminal with path to the "code" folder
2) run: py statsAna.py

# running the bench cluster 
1) open terminal with path to the "side_question" folder
2) run: py bench_cluster.py 
