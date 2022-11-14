from os import system

#for windows, change to 'cls'.
#for linux/mac, change to 'clear' (mac not tested).
#this is for easy cross-platform console clearing.
CLS = "clear"

#here we have location variables, so we can tell where the player is.
p_X = 0
p_Y = 0

#here we have some gameplay data, like day number and hunger.
day = 0
hunger = False
tutorial_active = True
tutorial_fire_active = False
cot_deployed = False
moved_today = False
current_item = "none"

#what about the player's inventory? let's use a dictionary.
inv = {
	"gold": 5,
	"coal": 25,
	"meals": 3
}

#for carried tools and utilities, use a list.
tools = ["satchel", "cot", "tinderbox"]


#define what a city is
class City:
	#default city is in the centre of the world
	#is named error

	#Inns will provide a place to get good rest and
	# weather protection for cold nights.
	#inn types table:
	# 0 : No Inn (have to sleep outside)
	# 1 : Cheap Inn (yay)
	# 2 : Expensive Inn (eh, it's something)
	# 3 : Cheap Inn with food (double yay)
	# 4 : Expensive Inn with food (better be worth the price)

	#Markets will provide a source of food for money,
	# and income for selling what you have.
	#market types table:
	# 0 : No Market (what the hell, how do they eat)
	# 1 : Food Market (they sell food, but only food)
	# 2 : Open Market (you can sell whatever, whenever)
	# 3 : Controlled Market (you can sell if you have a license)

	#Depending on the affiliation, a town may decide
	# to reject strangers or people who are not affiliated
	# with the king of a domain. Some towns may require a
	# citizenship, which you can obtain by being a good guest.
	#welcome types table:
	# 0 : Free Entry (no affliation)
	# 1 : Entry for Camelcaam's friends (camelcaam's domain)
	# 2 : Entry only for citizens or visa (need citizenship or visa card)
	# 3 : No Entry

	X = 0
	Y = 0
	cityname = "error"
	inn_type = 0
	market_type = 0
	welcome_type = 0
	def __init__(self, posX, posY, data):
		self.X = posX
		self.Y = posY
		self.cityname = data["name"]
		self.inn_type = data["inn_type"]
		self.market_type = data["market_type"]
		self.welcome_type = data["welcome_type"]



#here we define some useful functions
#
def sleep():
	global day
	global moved_today
	moved_today = False
	day = day + 1

#list items for 'help' screen
def list_items():
	out = ""
	for i in range(len(tools)):
		out = out + "'" + tools[i] + "' "
	return out

#use satchel, print out inventory
def use_satchel():
	print('Looking into your satchel, you find:')
	items_list = list(inv)
	items_counts = list(inv.values())
	for i in range(len(inv)):
		print(items_list[i] + " (" + str(items_counts[i]) + ")")

#this function will get a yes/no answer.
def get_yesno():
	while True:
		test = input("y/n? ->")
		if test.upper() == "Y":
			return True
		elif test.upper() == "N":
			return False
		else:
			print('Your answer should be either a "Y" or an "N".')

#parse commands
def read_action(act, context, env_data = {}):
	#define global variables (we will need these)
	global tutorial_fire_active
	global tutorial_active
	global cot_deployed
	global inv
	global tools
	global hunger
	global p_Y
	global p_X
	global moved_today

	print()
	#context table
	# 0 : Tutorial
	# 1 : On the Road
	# 2 : Camp
	# 3 : In a City (env_data useful here)
	# 4 : Post-Tutorial Center
	# 5 : Outside a Locked City (env_data useful here too)
	#try:
	if True: #uncomment this line if you get unknown errors in this block.
		if act == "help":
			if context == 4:
				print('\n===[ ENVIRONMENT')
				#returning to the center of the world
				print('You are in a clearing of a lightly populated forest. In the center of the clearing, there is a white, marble obelish with something engraved into it. You recognise this place.')
				print('\n===[ OPTIONS')
				print('You can interact with things that you are currently carrying. Here are your items:')
				print(list_items())
			if context == 1:
				print('\n===[ ENVIRONMENT')
				#on the road
				print('You are on the road. The terrain is neither steep nor flat, and neither densely wooded nor plain. You can tell where you are with your map.')
				print('\n===[ OPTIONS')
				print('You can interact with things that you are currently carrying. Here are your items:')
				print(list_items())
			if context == 0:
				print('Welcome to the Tutorial!')
				print('\n===[ ENVIRONMENT')
				#tutorial mode, the story is as follows:
				#	Player is in X0Y0, the center of the world. Her mind is blank,
				#		due to a sudden strike of amnesia. It is getting dark, and
				#		tonight is going to be cold. The player must make a fire using
				#		her tinderbox and coal, and then set a bed.
				print('You are in a clearing within a lightly populated forest. In the center of the clearing, there is a white, marble obelisk with something engraved into it.')
				
				#depending on the state of the world, display one of these two messages.
				if env_data["fire_active"]:
					print('The moon is beginning to show now, through the clouds above. The world around you is frigid, but the fire you have made keeps you warm.')
				else:
					print('You cannot seem to recall anything about who you are or why you are here. The sun is sinking at this time, and already it is rather cold. You are wearing a satchel with something in it, and a utility belt with a tinderbox attached. On your back is a folded cot.')

				#	If the player is pre-fire, then tell her how to start a fire.
				#	If the player is post-fire, then tell her to set a bed.
				# The player has a cot on her back, with a tinderbox on her hip and
				#		a satchel to store items.
				print('\n===[ OPTIONS')
				print('You can interact with things that you are currently carrying. In the tutorial, you only have three items:')
				print(list_items())
				print('You can type \'use satchel\', for instance to view your inventory.')
				if env_data["fire_active"] == False:
					print('You may want to start a fire. I recommend that you \'use tinderbox with coal\'')
		else:
			cmd_list = act.split(" ")
			#print(cmd_list) #debug thing
			if cmd_list[0] == "move":
				if context != 0:
					if moved_today:
						print('You have moved today already.')
					else:
						if cmd_list[1] == "north":
							p_Y = p_Y + 1
							moved_today = True
				else:
					print('Hold on! You should finish the tutorial first!')
			elif cmd_list[0] == "use":
				if cmd_list[1] in tools:
					#here we go through all the tools expected to be here
					if cmd_list[1] == "satchel":
						use_satchel()
					elif cmd_list[1] == "tinderbox":
						if context == 1:
							print('You should not be making fires on the road unless you are camping here.')
						elif context == 0:
							try:
								if cmd_list[2] == "with":
									if cmd_list[3] == "coal":
										print('You strike your flintstones together. The sparks light your kindling and you add a coal lump to the fire. You pile up 9 more lumps on the ground, and cover them with sticks and branches. You use the tinderbox to light the fuel, and soon you have a warm fire.')
										inv["coal"] = inv["coal"] - 10
										tutorial_fire_active = True
									else:
										print('What do you want to use in your tinderbox?')
								else:
									print('What do you want to do with the tinderbox?')
							except:
								print('What should you use the tinderbox with?')
					elif cmd_list[1] == "cot":
						if context == 0: #For the tutorial segment
							if env_data["fire_active"]:
								if env_data["cot_deployed"]:
									print('Your cot is deployed by the fire. Do you want to lay down and sleep?')
									if get_yesno():
										print('You get into the cot, and fall asleep.')
										tutorial_active = False
										sleep()
									else:
										print('You delay sleep for now.')
								else:
									print('You take the folded cot off your back, and you lay it down. You begin to unfold it.')
									print('The cot is now deployed!')
									cot_deployed = True
							else:
								if env_data["cot_deployed"]:
									print('You have deployed the cot. It is too cold to think about sleep, however. You need to make a fire.')
								else:
									print('You take the folded cot off your back, and you lay it down. You begin to unfold it, but the cold is becoming worse. You will not be able to sleep without a fire.')
									print('The cot is now deployed!')
									cot_deployed = True
					else:
						print('That item... does not seem to do anything?')
				else:
					print('You do not have that item.')
					
#	except:
#		print('Woah! Something went wrong!')



#define cities
solitude = City(0, 1, {"name" : "Solitude", "inn_type" : 3, "market_type" : 2, "welcome_type" : 0})
cities_list = [solitude]



#mainloop function
print('hello.')
while tutorial_active:
	print()
	read_action(input(' ->'), 0, {"fire_active": tutorial_fire_active, "cot_deployed": cot_deployed})
while True:
	print()
	#if in a city, then context is either 3 or 5.
	current_city = None
	for i in range(len(cities_list)):
		if cities_list[i].X == p_X and cities_list[i].Y == p_Y:
			current_city = cities_list[i]
	if current_city == None:
		if (p_X == 0 and p_Y == 0):
			read_action(input(' ->'), 4, {})
		else:
			read_action(input(' ->'), 1, {})
	else:
		if current_city.welcome_type in [2, 3, 4]:
			read_action(input(' ->'), 5, {current_city})
		else:
			read_action(input(' ->'), 1, {current_city})
