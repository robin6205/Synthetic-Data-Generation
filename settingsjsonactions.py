import json


def readSettings(settingsPath):
    with open(settingsPath, 'r') as settingsFile:
        settings = json.load(settingsFile)
    return settings
def writeSettings(settingsPath, settings):
    with open(settingsPath, 'w') as settingsFile:
        json.dump(settings, settingsFile)


def writeAirsimSettings(settingsPath, settings):
    airsim_file = readSettings(settingsPath)
    if settings["num_drones"] != len(airsim_file["Vehicles"]):
        airsim_file["Vehicles"] = {}
        template = readSettings("px4_drone_template.json")
        for i in range(int(settings["num_vehicles"])):
            #append drone template to airsim settings file
            airsim_file["Vehicles"]["Drone" + str(i)] = template
    writeSettings(settingsPath, airsim_file)



#settings = readSettings(file_path)
#print(list(settings.keys()))