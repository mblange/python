# Practice Game

## Functions: ##

# ask their name
def get_name():
	global name
	name = raw_input("What's your name?> ")
	print "Hi %s! Lets Play." % name

# intro the game
def intro_game():
	print "%s, you are walking in the woods " % name
	print "and you approach a castle. You assume you "
	print "need to go inside and save the princess."
	print "you see a bridge and a ladder. Which do you choose?"

# introduce options forthe next room
def intro_room():
	if location == 1:
		room = 'kitchen'
		entry = 'hole'
	elif location == 2:
		room = 'hall'
		entry = 'crack'
	elif location == 3:
		room = 'study'
		entry = 'tunnel'
	elif location == 4:
		room = 'library'
		entry = 'chute'
	print "%s, you have enetered the %s." % (name, room)
	print "But you need to go further and save the princess."
	print "you see a door and a %s. Which do you choose?" % entry

# define starting location
location = int(0)

# enter the next room how?
def enter_room(choice1, choice2):
	global location
	entry = raw_input(choice1 + ' or ' + choice2 + ' ?> ')
	if not (entry == choice1 or entry == choice2):
		print "Umm, %s was not an option %s... Try again." % (entry, name)
		enter_room(choice1, choice2)
	elif entry == choice1:
		print "OK, you chose %s" % entry
		location += 1
		next_room()
	else:
		print "OK, you chose %s" % entry
		location += 2
		next_room()
def next_room():	
	if location == 1:
		intro_room()
		enter_room('door', 'hole')
	elif location == 2:
		intro_room()
		enter_room('door', 'crack')
	elif location == 3:
		intro_room()
		enter_room('door', 'tunnel')
	elif location == 4:
		intro_room()
		enter_room('door', 'chute')
	else:
		print "Something's gone terribly wrong with your 'location' variable... fix it."
		exit(1)
# welcome player
print "Welcome to the Castle Game"

get_name()

intro_game()

enter_room('bridge', 'ladder')
