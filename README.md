# cmpt353-project
Repo of CMPT353 Final Project

# Extra packages requirement (assuming you are running with Anaconda)
1) pip install gpsphoto
2) pip install exifread
3) pip install piexif
4) pip install geojson

# Running main application
1) open terminal with path to the "code" folder
2) run: py main.py ImageFileName travelMode
Sample code:
python .\main.py img2.jpg walk  (Input image 2, travel mode is walk)
python .\main.py img15.jpg bike (Input image 15, travel mode is bike)
python .\main.py img12.jpg drive (Input image 12, travel mode is car)

Note: 
 - ImageFileName: 
   - Can be any image file name from the sample_images folder, or any personal image with geotaggged copy to the sample_images folder
 - travelMode:
   - Can be walk, bike or drive
 
# Viewing the result from main application 
1) in terminal:
 - will print out a list of places that the program suggest the user to visit
2) viewing in map with direction 
 - in the result folder, can open the result file by using this link 'https://geojson.io/'

# Running stats analysis 
1) open terminal with path to the "code" folder
2) run: py bench_cluster.py
3) run: py statsAna.py
 


