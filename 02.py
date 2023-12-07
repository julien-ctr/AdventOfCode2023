MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

games_id = []

"""
with open("02-input.txt", "r", encoding = "utf-8") as f:
	for i, line in enumerate(f) :
		game = line.split(":")[1:][0].split(";")
		game = ",".join(game)
		
		if game[-1:] == '\n':
			game = game[:-1]
			
		count = 0
		
		for sample in game.split(","):
			number = int(sample.split(" ")[1])
			if sample.split(" ")[2] == "blue" and number > MAX_BLUE:
				break
			elif sample.split(" ")[2] == "green" and number > MAX_GREEN:
				break
			elif sample.split(" ")[2] == "red" and number > MAX_RED:
				break
			count += 1
			
		if count == len(game.split(",")):
			games_id.append(i+1)

print(games_id)
print(sum(games_id))
"""

#================PARTIE 2=======================

game_powers = []

with open("02-input.txt", "r", encoding = "utf-8") as f:
	for i, line in enumerate(f) :
		game = line.split(":")[1:][0].split(";")
		game = ",".join(game)
		
		if game[-1:] == '\n':
			game = game[:-1]
			
		count = 0
		
		mr, mg, mb = (0, 0, 0)
		
		for sample in game.split(","):
			number = int(sample.split(" ")[1])
			if sample.split(" ")[2] == "blue" and number > mb:
				mb = number
			elif sample.split(" ")[2] == "green" and number > mg:
				mg = number
			elif sample.split(" ")[2] == "red" and number > mr:
				mr = number
			
		game_powers.append(mr*mb*mg)

print(sum(game_powers))
