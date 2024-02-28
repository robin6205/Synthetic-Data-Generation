import json


def extract_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data
'''def get_data(data):
    vehicles = {}
    for id in data:
        single_drone = []
        for command in data[id]:
            single_drone.append(command)
        vehicles[id] = single_drone
    return vehicles'''
def get_data(data):
    #print(data)
    flights = {}
    for timestep in data:
        #print(timestep)
        for flight in timestep["aircraft"]:
            #print(flight)
            id = flight["hex"]
            #print(id)
            #print(flight)
            if flight["alt_baro"] == 'ground':
                flight["alt_baro"] = 0
            if id in flights.keys():
                flights[id].append((flight["lat"],flight["lon"],int(flight["alt_baro"] or 0)/3.2808399))
            else:
                flights[id] = [(flight["lat"],flight["lon"],int(flight["alt_baro"] or 0)/3.2808399)]
    return flights



def get_commands_list(data):
    data = extract_json(data)
    commands = get_data(data)
    return commands





#data_location = "C:/Users/LocalUser/Desktop/20230801-130000_200000.json"
#commands = get_commands_list(data_location)

#print(commands)
#with open("C:/Users/LocalUser/Desktop/Synthetic-Data-Generation/file.json","w") as f:
    #json.dump(commands,f)




