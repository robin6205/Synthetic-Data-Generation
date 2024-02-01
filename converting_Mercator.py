import requests
import datetime
import json
import gzip
import os
from bs4 import BeautifulSoup
from io import BytesIO
import math

#This will need scaling before it can be used in unreal engine
#This approach usses the mercator projection which is the projection of the 3D world to a 2D map.

# def download_and_extract(url):
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         with gzip.open(BytesIO(response.content), 'rt') as f:
#             return json.loads(f.read())
#     return None
def download_and_extract(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # with gzip.open(BytesIO(response.content), 'rt', encoding='utf-8') as f:
        #     return json.loads(f.read())
        return json.loads(response.content)
    return None

def is_within_time_bounds(file_name, start_dt, end_dt):
    file_dt = datetime.datetime.strptime(file_name[:6], '%H%M%S')
    return start_dt <= file_dt < end_dt


def is_within_geobound(lat, lon, geobound):
    return geobound[1][0] <= lat <= geobound[0][0] and geobound[0][1] <= lon <= geobound[1][1]


# Parameters
baseurl = 'https://samples.adsbexchange.com/readsb-hist/'
output_dir = ''  # Make sure this directory exists
year = '2023'
month = '08'
day = '01'
start_time = '130000'
end_time = '200000'
start_dt = datetime.datetime.strptime(start_time, '%H%M%S')
end_dt = datetime.datetime.strptime(end_time, '%H%M%S')

# Geographical Boundary
geobound = [(40 + 41.8628 / 60, -(87 + 37.1774 / 60)),  # NW
            (40 + 7.5751 / 60, -(85 + 44.0839 / 60))]  # SE

# Create output file
fn_out = f"{year}{month}{day}-{start_time}_{end_time}.json"
output_file = os.path.join(output_dir, fn_out)
with open(output_file, 'w') as fid_out:
    # Get list of files
    currurl = f"{baseurl}{year}/{month}/{day}/"
    print("Getting list of files from", currurl)
    # show request progress
    response = requests.get(currurl, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    links = [a['href'] for a in soup.find_all('a', href=True) if a.text.endswith('.gz')]


    # Mercator projection function
    def lat_lng_to_xy(latitude, longitude):
        R = 6371000  # Earth's radius in meters
        x = R * math.radians(longitude)
        y = R * math.log(math.tan(math.pi / 4 + math.radians(latitude) / 2))
        return x, y


    # Process each file
    for link in links:
        if is_within_time_bounds(link, start_dt, end_dt):
            data = download_and_extract(currurl + link)
            if data:
                # Filter only aircraft data containing lat and lon keys
                print('Filtering data...')
                filtered_aircraft = [ac for ac in data['aircraft'] if
                                     'lat' in ac and 'lon' in ac and is_within_geobound(ac['lat'], ac['lon'], geobound)]
                if filtered_aircraft:
                    data['aircraft'] = filtered_aircraft

                    for aircraft in filtered_aircraft:
                        latitude = aircraft['lat']
                        longitude = aircraft['lon']
                        z = aircraft.get('alt_geom', 'N/A')
                        hex_code = aircraft.get('hex', 'N/A')
                        vel = aircraft.get('gs') * 0.5144 if aircraft.get('gs') is not None else 0, #convert knotts to m/s
                        heading = aircraft.get('track'),

                        # Convert lat, lon to x, y
                        x, y = lat_lng_to_xy(latitude, longitude)

                        print(f"Hex: {hex_code}, Velocity {vel}, X: {x}, Y: {y}, Z: {z}")