import requests
import datetime
import json
import gzip
import os
from bs4 import BeautifulSoup
from io import BytesIO


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
    print(soup)
    links = [a['href'] for a in soup.find_all('a', href=True) if a.text.endswith('.gz')]

    # Process each file
    for link in links:
        if is_within_time_bounds(link, start_dt, end_dt):
            data = download_and_extract(currurl + link)
            if data:
                # Filter only specific fields in aircraft data
                print('Filtering data...')
                filtered_aircraft = [
                    {
                        'hex': ac.get('hex'),
                        'flight': ac.get('flight'),
                        'alt_baro': ac.get('alt_baro'),
                        'alt_geom': ac.get('alt_geom'),
                        'gs': ac.get('gs'),
                        'track': ac.get('track'),
                        'baro_rate': ac.get('baro_rate'),
                        'lat': ac.get('lat'),
                        'lon': ac.get('lon'),
                    } for ac in data.get('aircraft', []) if 'lat' in ac and 'lon' in ac and is_within_geobound(ac['lat'], ac['lon'], geobound)
                ]

                if filtered_aircraft:
                    data['aircraft'] = filtered_aircraft
                    json.dump(data, fid_out, indent=4)