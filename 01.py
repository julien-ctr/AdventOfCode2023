def islettersnumber(txt, i):
	d = {"0": "zero",
		 "1": "one",
		 "2": "two",
		 "3": "three",
		 "4": "four",
		 "5": "five",
		 "6": "six",
		 "7": "seven",
		 "8": "eight",
		 "9": "nine"}
		 
	for key, val in d.items():
		j = i
		while j < len(txt) and j-i < len(val) and txt[j] == val[j-i]:
			j += 1
		if j-i == len(val):
			return key 
	return None

sum = 0

with open("inputs/01-input.txt", "r", encoding="utf-8") as f:
	t = []
	for line in f:
		i = 0
		j = len(line)-1
		while i < j and not line[i].isnumeric() and islettersnumber(line, i) is None:
			i += 1
		while i < j and not line[j].isnumeric() and islettersnumber(line, j) is None:
			j -= 1
		
		x = line[i]
		y = line[j]
		u = islettersnumber(line, i)
		v = islettersnumber(line, j)
		
		if u is not None:
			x = u
		if v is not None:
			y = v 
			
		sum += int(x+y)
		t.append(int(x+y))
