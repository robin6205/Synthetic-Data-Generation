import json
import pandas as pd
import numpy as np
import scipy


def extract_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


def get_data(data):
    flights = {}
    for timestep in data:
        for flight in timestep["aircraft"]:
            id = flight["hex"]
            if flight["alt_baro"] == 'ground':
                flight["alt_baro"] = 0
            alt_in_meters = int(flight["alt_baro"] or 0)  # Convert feet to meters
            if id in flights.keys():
                flights[id].append((flight["lon"], flight["lat"], alt_in_meters))
            else:
                flights[id] = [(flight["lon"], flight["lat"], alt_in_meters)]
    return flights


def convert_to_dataframes(commands):
    dataframes = {}
    for flight_id, data in commands.items():
        df = pd.DataFrame(data, columns=['Longitude', 'Latitude', 'Height'])
        df.insert(0, 'Row', range(1, 1 + len(df)))
        dataframes[flight_id] = df
    return dataframes


def smooth_spline(data_points, smoothing_factor=100):
    longitudes, latitudes, altitudes = zip(*data_points)

    # Generating smoothed data
    smoothed_data = []
    x = np.arange(len(data_points))
    x_new = np.linspace(0, len(data_points) - 1, smoothing_factor)
    longitudes_smooth = spline(x, longitudes, x_new)
    latitudes_smooth = spline(x, latitudes, x_new)
    altitudes_smooth = spline(x, altitudes, x_new)

    for i in range(smoothing_factor):
        smoothed_data.append((longitudes_smooth[i], latitudes_smooth[i], altitudes_smooth[i]))

    return smoothed_data


def get_commands_list(data, smoothing_factor=100):
    data = extract_json(data)
    commands = get_data(data)

    # Smooth the splines for each aircraft
    for flight_id, data_points in commands.items():
        smoothed_data = smooth_spline(data_points, smoothing_factor)
        commands[flight_id] = smoothed_data

    return commands


def export_data_to_json(commands, folder_path):
    for flight_id, data_points in commands.items():
        file_path = f"{folder_path}/{flight_id}.json"
        with open(file_path, 'w') as f:
            json.dump(data_points, f)


# Usage example
data_location = "C:/Users/LocalUser/Desktop/folder/scream.json"
commands = get_commands_list(data_location)
dataframes = convert_to_dataframes(commands)
folder_path = "C:/Users/LocalUser/Desktop/folder/testisabel"
export_data_to_json(dataframes, folder_path)

