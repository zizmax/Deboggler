#####################################
#Boggle solver by Nate and Ryn  	#
#Early January 2019					#
#Below are user settings			#
#####################################


debug = False #Debug mode prints out a TON of details, very messy
showResults = False #prints out all of the words found
loop = False #Will infinitely run the solver as a simulation with randomly generated boards
present = True #Presentation mode includes an ASCII print out of the board

# TODO Fix Q/Qu??
# TODO Is it possible to incorporate starts variable into findValids itself???
# TODO Is it possible to eliminate 2D board list by instead incorporating this info into the Dice.location
# TODO Change printing of board to be based off boardstring, not 2D list

import random
import time

boardstring = "serspatglinesers" # Super high scoring board: 1389 ()
boardstring = "perslatgsineters" # Another high scorer: 1265 (http://www.danvk.org/wp/2014-01-25/what-up-with-boggle/index.html)
boardstring = "nektesoonmltecye"
boardstring = "hnuhlajpudigorln"
boardstring = "zdysiaioyarewheh"
boardstring = "serspatglinesers"

dice = ["aaeegn", "elrtty", "aoottw", "abbjoo",
	"ehrtvw", "cimotu", "distty", "eiosst",
	"delrvy", "achops", "himnqu", "eeinsu",
	"eeghnw", "affkps", "hlnnrz", "deilrx"]
#the one Q character is actually Qu in the real game. The U next to it is a separate side

best = [0,""] #Top score from all loops, and its associated boardstring
loops = 0 #Number of cycles of randomly generated boards

#Init for unique Dice for each die on physical board
class Dice:
	def __init__(self, alpha, location, neighbors):
		self.alpha = alpha
		self.location= location
		self.neighbors = getNeighbors(location)

	def __init__(self, alpha, location):
		self.alpha = alpha
		self.location= location

def getNeighbors(location, boggle):
	"""Returns all neighboring tiles of a given tile.

	Neighbors are defined as tiles that are directly
	adjacent diagonally or in the cardinal directions.
	For tiles at the edge of the board, the theoretical neighbors
	that are off the board are ignored.
	"""
	neighbors = []
	x = location[0]
	y = location[1]
	if (x>0 and y>0):
		neighbors.append(boggle[x - 1][y - 1])
	if y>0:
		neighbors.append(boggle[x    ][y - 1])
	if (x<3 and y>0):
		neighbors.append(boggle[x + 1][y - 1])
	if x>0:
		neighbors.append(boggle[x - 1 ][y   ])
	if (x<3):
		neighbors.append(boggle[x + 1][y    ])
	if (x>0 and y<3):
		neighbors.append(boggle[x - 1][y + 1])
	if (y<3):
		neighbors.append(boggle[x    ][y + 1])
	if (x<3 and y<3):
		neighbors.append(boggle[x + 1][y + 1])
	return neighbors

def printNeighbors(die):
	print("Neighbors of '" + str(die.alpha) + "' at " + str(die.location) + " are: ")
	for neighbor in die.neighbors:
		print(neighbor.alpha)

def findValids(current, used, count, word, letters):
	"""
	Does some convoluted magic to find if a word exists on the boards

	This needs to be commented/explained better, and also needs to be modified
	into more of an isValid() function to just boolean check if word exists and return True/False

	"""
	if debug:
		print("Target: ===> " + word)
		print("Looking for letter: " + word[count] + " next to " + current.alpha)
		print(current.alpha + " is at " + str(current.location))
	for neighbor in current.neighbors:
		if neighbor not in used:
			if neighbor.alpha == word[count]:
				used.append(neighbor)
				letters.append(word[count])
				if ''.join(letters) == word:
					break
					return True
				if count < len(word)-1:
					findValids(neighbor, used, count+1, word, letters)
	#print("[" + word + "]")
	#print("> " + str(letters))
	return letters
	# TODO: Make this return a boolean so that we can say:
	# if findValids(word):
		#found.append(word)

#Loads dictionary file from disk
file = open("scrabble.txt", 'r')
lines = file.readlines()
file.close()

#Sanitizes raw text by converting to lowercase and removing newline char
dictionary = []
for line in lines:
	dictionary.append(line[:-1].lower())
print ("Words loaded: " + str(len(lines)))

def crunch(boardstring):
	print ("Boardstring: " + boardstring)

	#Converts simple boardstring to 2D list of letters
	print("Making board")
	board = [[0] * 4 for i in range(4)]
	for column in range (0,4):
		for row in range (0,4):
			board[column][row] = boardstring[(column)+(row*4)]

	#Creates 2D list of Dice objects
	print("Making dice")
	boggle = [[0] * 4 for i in range(4)]
	for x in range(0,4):
			for y in range(0,4):
				die = Dice(board[x][y],[x,y])
				boggle[x][y]=die

	#Sets neighbors for each Dice object on board
	print("Setting neighbors")
	for x in range(0,4):
			for y in range(0,4):
				boggle[x][y].neighbors=getNeighbors([x,y], boggle)

	#Removes words that cannot be made with the letters in the board
	print("Trimming dictionary")
	words = dictionary.copy() #Copies to new list to keep master dictionary static across loops
	for i in reversed(range(0,len(words))): #Iterates in reverse to avoid issues with pop()
		for letter in words[i]:
			if letter not in boardstring:
				words.pop(i)
				break #Adding this made it ~2x faster!!! Duh

	print ("Possible words: " + str(len(words)))

	found = []
	used = []

	for word in words:
		#Finds all the tiles a word could start and runs findValids() on each until a valid is found
		starts = [] #Contains each occurence of the first letter of the target word
		first = word[0]
		for x in range(len(boggle)):
			for y in range(len(boggle[x])):
				if boggle[x][y].alpha == first:
					starts.append(boggle[x][y])
		for start in starts:

			result = findValids(start, [start], 1, word, [first])
			if debug:
				print(result)
			if ''.join(result)[:len(word)] == word:
				if debug:
					print(">" + word)
					print("%" + ''.join(result))
					print("#" + ''.join(result)[:len(word)]+"\n")
				if debug:
					print("FOUND: " + word)
				found.append(word)
				break #This break stops it from looking for the same word twice

	#found = list(set(found)) #Removes duplicate words. No duplicates unless the above break is uncommented
	print("Solutions found: " + str(len(found)))
	file = open("successes.txt", 'w')

	#Finds and prints longest words
	longest_length = max(len(x) for x in found)
	print([x for x in found if len(x) == longest_length])

	#Prints and saves results to file on disk
	for success in found:
		if showResults:
			print(success)
		if not loop:
			file.write(success+"\n")
	if loop:
		loops += 1
		if best[0] < len(found):
			best[1] = boardstring
			best[0] = len(found)
		print("Top score: " + str(best[0]) + " Board: " + str(best[1]))
		print("Loops: " + str(loops))

	#Prints out visual representation of physical board
	if present:
		print("- - - - - -")
		for row in range (0,4):
			print ("| "+ board[0][row]+" "+board[1][row]+" "+board[2][row]+" "+board[3][row] + " |")
		print("- - - - - -")
	if not loop:
		pass

	#Generates random board before looping through simulation again
	string = ""
	for die in dice:
		string += random.choice(die)
	string = list(string)
	random.shuffle(string)
	boardstring = ''.join(string)
	#time.sleep(2)
	return found, board
