import sys
import os
import settingsjsonactions
import cmd
#import dronecontrol2
#location of settings file for each environment
airsim_settings = {}
weather_settings = {}
other_settings = {}
unreal_environments = []
current_environment = ""
settings = {}
master_settings_path = "./settingsTest.json"
airsim_settings_path = "./settings.json"

class DroneControl(cmd.Cmd):
    prompt = "Enter command (start/settings/quit) or help for list of commands: "
    def __init__(self,settingsPath, airsimPath):
        super().__init__()
        self.settingsPath = settingsPath
        self.airsimPath = airsimPath
        self.settings = {}
        self. airsimSettings = {}
    def do_preloop(self):
        self.settings = settingsjsonactions.readSettings(self.settingsPath)
        self.airsimSettings = settingsjsonactions.readSettings(self.airsimPath)

    def do_postloop(self):
        settingsjsonactions.writeSettings(self.settingsPath,self.settings)
    def do_start(self, arg):
        print("Starting simulation")
        #load current settings into respective locations
        #start simulation unreal
    def do_settings(self, arg):
        #call settings subprocess with settings
        settings_page = DroneSettings(self.settings)
        settings_page.cmdloop()
        settings_page.do_postloop()
    def do_quit(self, arg):
        return True

    def default(self, arg):
        print("Invalid command")


class DroneSettings(cmd.Cmd):
    prompt = "Select setting/category or list to view categories (type back to go back): "

    def __init__(self,settings):
        super().__init__()
        self.settings = settings
    def do_select(self, arg):
        arg = int(arg)
        options = list(self.settings.keys())
        if arg < len(self.settings):
            if type(self.settings[options[arg]]) == dict:
                DroneSettings(self.settings[options[arg]]).cmdloop()
            else:
                print(f"Current setting: {self.settings[options[arg]]}")
                new_setting = input("Enter new setting: ")
                self.settings[options[arg]] = new_setting
        else:
            print(arg)
            print("Invalid setting")
    def do_back(self, arg):
        return True

    def do_list(self, arg):
        categories = list(self.settings.keys())
        for x in range(0,len(categories)):
            if type(self.settings[categories[x]]) == dict:
                print(f"({x}) {categories[x]}")
            else:
                print(f"({x}) {categories[x]}: {self.settings[categories[x]]}")

    def do_postloop(self):
        for setting in self.settings.keys():
            if setting == "Airsim":
                settingsjsonactions.writeAirsimSettings(airsim_settings_path,self.settings[setting])
            elif setting == "Weather":
                pass
            else:
                pass



    def default(self, arg):
        print("Invalid command")


if __name__ == "__main__":
    drone_control = DroneControl(master_settings_path,airsim_settings_path)
    drone_control.do_preloop()
    drone_control.cmdloop()
    drone_control.do_postloop()









'''def main():
    while True:
        command = input("Enter command (start/settings/quit): ")
        if command == "start":
            print("Starting simulation")
            #start simulation unreal

        elif command == "settings":
            settings = settingsjsonactions.readSettings(master_settings_path)
            for x in range(0,len(settings)):
                categories = list(settings.keys())
                print(f"({x}): {categories[x]}")
                while True:
                    command = input("Enter category or quit: ")
                    if command == "quit":
                        break
                    elif int(command) >= len(categories):
                        print("Invalid command")
                    else:
                        current_environment = categories[int(command)]
                        print(f"Current environment: {current_environment}")

        elif command == "quit":
            sys.exit()
        else:
            print("Invalid command")






if __name__ == "__main__":
    main()'''