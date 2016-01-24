# Practice Game
import time
import sys

## Functions: ##

#fancy time clock
def clock():
	for i in ['-', '|', '/', '-', '\\']:
	      	sys.stdout.write(i)
	    	sys.stdout.write('\r')
	      	sys.stdout.flush()
        	time.sleep(.2)
	print "*******************************"
	print "*******************************"
	
# ask their name
def get_name():
	global name
	name = raw_input("What's your name?> ")
	print "Hi %s! Lets Play." % name
	clock()

# intro the game
def intro_game():
	print "%s, you are walking in the woods " % name
	print "and you approach a castle. You assume you "
	print "need to go inside and save the princess."
	print "you see a bridge and a ladder. Which do you choose?"
	clock()

# introduce options for the next room
def intro_room():
	global entry
	if location == 1:
		room = 'kitchen'
		entry = 'hole'
		print location
	elif location == 2:
		room = 'hall'
		entry = 'crack'
		print location
	elif location == 3:
		room = 'study'
		entry = 'tunnel'
		print location
	elif location == 4:
		room = 'library'
		entry = 'chute'
		print location
	elif location == 5:
		room = 'dungeon'
		entry = 'staircase'
		print location
	elif location == 6:
		room = 'basement'
		entry = 'princess'
		print location
	print "%s, you have enetered the %s." % (name, room)
	print "But you need to go further and save the princess."
	print "you see a door and a %s. Which do you choose?" % entry
	clock()

# define starting location
location = int(0)
# use this instead of 'choice1/2'?? 
# entry = 'ladder'

# enter the next room how?
def enter_room(choice1, choice2):
	global location
	global entry
	entry = raw_input(choice1 + ' or ' + choice2 + ' ?> ')
	if not (entry == choice1 or entry == choice2):
		print "Umm, %s was not an option %s... Try again." % (entry, name)
		enter_room(choice1, choice2)
	elif entry == choice1:
		print "OK, you chose %s" % entry
		location += 1
		clock()
		print location
		next_room()
	else:
		print "OK, you chose %s" % entry
		location += 2
		clock()
		print location
		next_room()

def next_room():	
	global entry
	if location == 1:
		print location
		intro_room()
		enter_room('door', 'hole')
	elif location == 2:
		print location
		intro_room()
		enter_room('door', 'crack')
	elif location == 3:
		print location
		intro_room()
		enter_room('door', 'tunnel')
	elif location == 4:
		print location
		intro_room()
		enter_room('door', 'chute')
	elif location == 5:
		print location
		intro_room()
		enter_room('door', 'staircase')
	elif location == 6:
		print location
		intro_room()
		enter_room('door', 'princess')
	elif entry == 'princess':
		clock()
		print "You have saved the pricess!!"
		print "you win!!!!!"
		print "******!!!!!!!!********"
		print " ---------------------"
		exit(0)
	else:
		print "Something's gone terribly wrong with your 'location' variable... fix it."
		print location
		exit(1)
# welcome player
print "Welcome to the Castle Game"

get_name()

intro_game()

enter_room('bridge', 'ladder')
