import requests
import datetime
import json
import gzip
import os
from bs4 import BeautifulSoup
from io import BytesIO
import math

#this will need some type of scale factor when used in Unreal engine
#This approach usues the wgs84 ellipsoid to convert spherical (lat long alt) to cartesian coordinates
def download_and_extract(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return json.loads(response.content)
    return None

def is_within_time_bounds(file_name, start_dt, end_dt):
    file_dt = datetime.datetime.strptime(file_name[:6], '%H%M%S')
    return start_dt <= file_dt < end_dt

def is_within_geobound(lat, lon, geobound):
    return geobound[1][0] <= lat <= geobound[0][0] and geobound[0][1] <= lon <= geobound[1][1]

def wgs84_parameters():
    # WGS 84 parameters
    a = 6378137.0  # semi-major axis in meters
    b = 6356752.3142  # semi-minor axis in meters
    f = (a - b) / a  # flattening
    e = math.sqrt(f * (2 - f))  # eccentricity
    return a, b, f, e

def geodetic_to_ecef(latitude, longitude, altitude):
    a, b, _, e = wgs84_parameters()

    # Convert latitude and longitude to radians
    phi = math.radians(latitude)
    lam = math.radians(longitude)

    # Radius of curvature in the prime vertical
    N = a / math.sqrt(1 - e ** 2 * math.sin(phi) ** 2)

    # ECEF coordinates
    X = (N + altitude) * math.cos(phi) * math.cos(lam)
    Y = (N + altitude) * math.cos(phi) * math.sin(lam)
    Z = ((b ** 2 / a ** 2) * N + altitude) * math.sin(phi)

    return X, Y, Z

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
fn_out = f"{year}{month}{day}-{start_time}_{end_time}_formatted.json"
output_file = os.path.join(output_dir, fn_out)
with open(output_file, 'w') as fid_out:
    # Get list of files
    currurl = f"{baseurl}{year}/{month}/{day}/"
    print("Getting list of files from", currurl)

    response = requests.get(currurl, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a.text.endswith('.gz')]

    # Process each file
    for link in links:
        if is_within_time_bounds(link, start_dt, end_dt):
            data = download_and_extract(currurl + link)
            if data:
                # Process each aircraft in the data
                formatted_aircraft = []
                for aircraft in data.get('aircraft', []):
                    if 'lat' in aircraft and 'lon' in aircraft and is_within_geobound(aircraft['lat'], aircraft['lon'], geobound):
                        X, Y, Z = geodetic_to_ecef(aircraft['lat'], aircraft['lon'], aircraft.get('alt_geom', 0))

                        # Check if the 'hex' identifier matches 'aaf0a1'
                        if aircraft.get('hex') == 'aaf0a1':
                            formatted_aircraft.append({
                                'hex': aircraft.get('hex'),
                                'x': X,
                                'y': Y,
                                'z': Z,
                                'velocity': aircraft.get('gs') * 0.5144 if aircraft.get('gs') is not None else 0,
                                'heading': aircraft.get('track'),
                                'delay': 5
                            })

                if formatted_aircraft:
                    # Print formatted data
                    for ac_data in formatted_aircraft:
                        print(json.dumps(ac_data, indent=4))

                    # Save formatted data to the output file
                    json.dump({'aircraft': formatted_aircraft}, fid_out, indent=4)
                    print(f"Formatted data saved to '{output_file}'")