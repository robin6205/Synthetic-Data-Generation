import sys
import os

#location of settings file for each environment
airsim_settings_path = "Path/To/Setting"
airsim_settings = {}
weather_settings = {}
unreal_environments = []
current_environment = ""




def main():
    while True:
        command = input("Enter command (start/settings/quit): ")
        if command == "start":
            print("Starting simulation")
            #start simulation unreal

        elif command == "settings":
            #clear console command
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Settings")
            #print settings
            for setting in airsim_settings.keys():
                print(f'{setting}: {airsim_settings[setting]}')
            for setting in weather_settings.keys():
                print(f'{setting}: {weather_settings[setting]}')
            while True:
                command = input("Enter setting to change or quit: ")
                if command == "quit":

                    break
                elif command in airsim_settings.keys():
                    new_setting = input(f"Enter new value for {command}: ")
                    airsim_settings[command] = new_setting
                elif command in weather_settings.keys():
                    new_setting = input(f"Enter new value for {command}: ")
                    weather_settings[command] = new_setting
                else:
                    print("Invalid setting")
        elif command == "quit":
            sys.exit()
        else:
            print("Invalid command")






if __name__ == "__main__":
    main()