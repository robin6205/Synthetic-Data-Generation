import json


def readSettings(settingsPath):
    with open(settingsPath, 'r') as settingsFile:
        settings = json.load(settingsFile)
    return settings
def writeSettings(settingsPath, settings):
    with open(settingsPath, 'w') as settingsFile:
        json.dump(settings, settingsFile)


file_path = "C:/Users/aleca/OneDrive/Documents/GitHub/Synthetic-Data-Generation/settingsTest.json"

#settings = readSettings(file_path)
#print(list(settings.keys()))