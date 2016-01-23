from sys import argv

script, number, inc = argv

# Convert arguments to integers
number = int(number)
inc = int(inc)

def print_numbers():
	i = 0
	numbers = []
	for i in range(0, number, inc):
		print "At the top i is %d" % i
		numbers.append(i)
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i 


	print "The numbers: "

	for num in numbers:
		print num

def print_numbers_loop():
	nums = [1,2,3,4,5]
	numbers = []
	for i in nums:
		print "At the top i is %d" % i
		numbers.append(i)
		
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % (i + 1)
	
	print "The Numbers: "

	for num in numbers:
		print num

# print_numbers_loop()
print_numbers()
