#file that can extract the exif info from a camera
#reference https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
#https://towardsdatascience.com/grabbing-geodata-from-your-photos-library-using-python-60eb0462e147

#libray need
# ExifRead
# piexif
#input: an image with GPS infomation
#return a (latitude,longitude) tuple

from GPSPhoto import gpsphoto

def extractGPS(filename):
    data = gpsphoto.getGPSData(filename)
    #print(data)
    latitude = data['Latitude']
    longitude = data['Longitude']
    return (latitude,longitude)
    


# print(extractGPS('../sample_images/img4.jpg'))