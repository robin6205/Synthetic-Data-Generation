import json


def extract_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data
def get_data(data):
    vehicles = {}
    for id in data:
        single_drone = []
        for command in data[id]:
            single_drone.append(command)
        vehicles[id] = single_drone
    return vehicles

def get_commands_list(data):
    data = extract_json(data)
    commands = get_data(data)
    return commands

filepath = "C:/Users/aleca/Desktop/test.json"

commands = get_commands_list(filepath)