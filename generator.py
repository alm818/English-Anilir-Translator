from Struct import Alphabet
from random import randint
import csv

class Generator:
	def __init__(self):
		self.abc = Alphabet()
		self.vowel = list('aeouiy')
	def count_sound(self, word):
		count = 0
		countable = True
		for c in word.lower():
			if c in self.vowel and countable: 
				count += 1
				countable = False
			else:
				countable = True
		return count
	def rvowel(self):
		return [self.abc.VOWEL[randint(0, len(self.abc.VOWEL) - 1)]]
	def rconso(self):
		return self.abc.CONSOS[randint(0, len(self.abc.CONSOS) - 1)]
	def make_word(self, count):
		if 4 >= count >= 3:
			rcount = randint(count - 1, count + 1)
		elif 5 <= count:
			rcount = randint(count - 2, count)
		else:
			rcount = randint(count, count + 1)
		word = []
		first_conso = randint(0, 1)
		if first_conso:
			word += self.rconso()
		for t in range(rcount - 1):
			word += self.rvowel() + self.rconso()
		word += self.rvowel()
		last_conso = randint(0, 1)
		if last_conso:
			while True:
				conso = self.rconso()
				if len(conso) == 1:
					break
			word += conso
		return word
	def represent(self, word):
		s = ''
		for char in word:
			s += char.ortho
		return s
	def phonorepr(self, ortho):
		s = ''
		for c in ortho:
			for vowel in self.abc.VOWEL:
				if vowel.ortho == c:
					s += vowel.phono
					break
			for conso in self.abc.CONSO:
				if conso.ortho == c:
					s += conso.phono
					break
		return s
if __name__ == '__main__':
	f = open('dictionary.csv', 'r')
	reader = csv.DictReader(f)
	dic = {}
	for line in reader:
		dic[line['word']] = line['translation']
	fi = open('word_needed.txt', 'r')
	gen = Generator()
	for line in fi:
		word = line.strip().lower()
		if word in dic:
			pass
			#print(dic[word])
		else:
			new = gen.make_word(gen.count_sound(word))
			res = gen.represent(new)
			dic[word] = res
			print(word.lower(), res)
	fw = open('dictionary.csv', 'w')
	fw.write('word,translation,phonology\n')
	for word in sorted(dic):
		fw.write(word.lower() + ',' + dic[word] + ',' + gen.phonorepr(dic[word]) + '\n')