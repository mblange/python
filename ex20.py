# import the argv function from the sys library
from sys import argv

# define the arguments
script, input_file = argv

# define a function called "print_all" that requires an argument "f"
# the fuction reads the argument f and then prints the result
def print_all(f):
	print f.read()

# define a function called "rewind" that takes an argument "f"
# the fucntion sends the current pointer to the byte 0
def rewind(f):
	f.seek(0)

# define a function that takes two arguments, "f" and "line_count"
# the fuction prints the linecount and currnet line of "f"
def print_a_line(line_count, f):
	print line_count, f.readline()

# define variable "current_file" as the result of opening "input_file"
# "input_file" is entered as an argument when calling the script
current_file = open(input_file)

# print a line
print "First let's print the whole file:\n"

# run the fuction "print_all" with "current_file" as the argument
print_all(current_file)

# print a line
print "Now let's rewind, kind of like a tape."

# run fuction "rewind" with "current_file" as argument
rewind(current_file)

#print a line
print "Let's print three lines:"

#define variable "current_line"
current_line = 1
print_a_line(current_line, current_file)

current_line = current_line + 1
print_a_line(current_line, current_file)

current_line = current_line + 1
print_a_line(current_line, current_file)
