-dronecontrol.py: deprecated file used for initial testing

drone.py: contains the drone class and all of the initialization, movement commands, etc
-Functions:
	__init__:initializes drone, sets its x,y,z, and commands drone to take off
	move: deprecated move command used before switching to movegps
	update: updates drones positional arguments, needs to be updated with latitude/longitude
	movegps: move to a specified longitude/latitude. Once fixed, threshold will be calculated using euclidian distance
	orbit: command to orbit a fixed distance around a point, needs to either be deleted or updated to use gps coordinates
-Current issues:
	-movegps does not have threshold checking as of right now, must move exactly to specified point
	-movegps does not allow multiple drones to move at the same time as of this moment
	-update position commands not properly used/not updated to use longitude/latitude
	-issue with the drone not moving to next position still occurs occasionally
-Future improvements:
	-move command can be changed to command drone to move x meters in a direction from its current location, makes more sense than trying to tell it to move 1 meter using gps commands
	-update drone attributes (x,y,z,longitude,latitude,etc)


extractjson.py: file containing function that turns raw adsb json into useable data
-Functions:
	extract_json: takes json file and returns it in a usable format
	get_data: takes output from extract_json and filters data to only what is currently used for movement
	get_commands_list: calls extract_json and get_data
-Current issues:
	-doesn't handle null data well, must be filtered out prior
-Future improvements:
	-improve error handling


-dronecontrol2.py: file containing main function and functions needed for asynchronous running
-Functions:
	async run_commands: asynchronously runs each command from command file
	async run_commands_test/asnyc run_commands_test2: modified run functions for testing/demonstration
	async main: contains main bulk of code used for running, including prompting user and calling other functions
-Current issues:
	-code has to be commented out repeatedly if different number of drones are desired on the map or commanded
	-not sure how well our current file format would allow multiple drones to be used with the way it is formatted, needs further investigating
	-lots of commented out code from testing, might not be clear to other people what stuff does if they try to look at/modify code
	-zero comments
-Future improvements:
	-put command file in github repository so command path does not have to be altered as much
	-add code to add/remove drones