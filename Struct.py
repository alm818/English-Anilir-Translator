from copy import deepcopy
class Phone:
	def __init__(self, phono, ortho):    
		self.phono = phono
		self.ortho = ortho

class Vowel(Phone):
	def __init__(self, phono, ortho):
		super().__init__(phono, ortho)

class Conso(Phone):
	def __init__(self, phono, ortho, isNonEnd):
		super().__init__(phono, ortho)
		self.isNonEnd = isNonEnd
	def addAllophone(self, allop):
		self.allop = allop
	def isAllop(self):
		return hasattr(self, 'allop')
	def isNonEnd(self):
		return self.isNonEnd

class Alphabet:
	def __init__(self):
		self.ɑ = Vowel('ɑ', 'a')
		self.ə = Vowel('ə', 'k')
		self.ɪ = Vowel('ɪ', 'i')
		self.e = Vowel('e', 'e')
		self.o = Vowel('o', 'o')
		self.u = Vowel('u', 'u')

		self.VOWEL = [self.ɑ, self.ə, self.ɪ, self.e, self.o, self.u]

		self.b = Conso('b', 'b', False)
		self.b.addAllophone('bʰ')
		self.k = Conso('k', 'c', False)
		self.d = Conso('d', 'd', False)
		self.ð = Conso('ð', 'x', True)
		self.t = Conso('t', 't', False)
		self.v = Conso('v', 'v', False)
		self.g = Conso('g', 'g', False)
		self.h = Conso('h', 'h', False)
		self.ħ = Conso('ħ', 'f', True)
		self.dʒ = Conso('dʒ', 'j', False)
		self.l = Conso('l', 'l', False)
		self.m = Conso('m', 'm', False)
		self.m.addAllophone('ᵐb')
		self.n = Conso('n', 'n', False)
		self.n.addAllophone('ŋ')
		self.p = Conso('p', 'p', False)
		self.p.addAllophone('pʰ')
		self.r = Conso('r', 'r', False)
		self.w = Conso('w', 'w', True)
		self.z = Conso('z', 'z', False)
		self.ɹ = Conso('ɹ', 'q', True)
		self.ʃ = Conso('ʃ', 's', False)

		self.CONSO = [self.b, self.k, self.d, self.ð, self.t, self.v,
			self.g, self.h, self.ħ, self.dʒ, self.l, self.m, self.n, 
			self.p, self.r, self.w, self.z, self.ɹ, self.ʃ]

		self.CONSOS = [[x] for x in self.CONSO] + [[self.b, self.l], [self.g, self.l], [self.t, self.l], [self.v, self.l],
			[self.p, self.l], [self.d, self.r], [self.g, self.r], [self.p, self.r], [self.w, self.r]
			]

class Basis:
	def __init__(self):
		self.abc = Alphabet()
		self.Article = Basis.Article(self.abc)
		self.Pronoun = Basis.Pronoun(self.abc)
		self.TenseParticle = Basis.TenseParticle(self.abc)
		self.WH_Word = Basis.WH_Word(self.abc)
		self.Verb = Basis.Verb(self.abc)
	class Article:
		def __init__(self, abc):
			self.EXIST = [abc.ɑ, abc.l]
			self.NEXIST = [abc.ɪ, abc.l]
			self.NEUTRAL = [abc.e, abc.l]
	class Pronoun:
		def __init__(self, abc):
			self.I = [abc.ɪ]
			self.YOU = [abc.u]
			self.IT = [abc.e]
			self.WE = [abc.n, abc.ɪ]
			self.YOUS = [abc.n, abc.u]
			self.THEY = [abc.n, abc.e]
			self.DP = [abc.z, abc.ɪ] # This, That, These, Those
			self.EX = [abc.g, abc.o] # There
	class TenseParticle:
		def __init__(self, abc):
			self.PAST = [abc.m, abc.u]
			self.PRES = [abc.m, abc.ɑ]
			self.FUTR = [abc.m, abc.o]
	class WH_Word:
		def __init__(self, abc):
			self.WHAT = [abc.h, abc.e, abc.v]
			self.IS = [abc.ʃ, abc.ɪ]
			self.THAT = [abc.r, abc.ɑ]
	class Verb:
		def __init__(self, abc):
			self.DO = [abc.d, abc.ə, abc.v, abc.ɑ]
			self.GO = [abc.d, abc.ə, abc.k, abc.o]
			self.HAVE = [abc.d, abc.ə, abc.b, abc.ə]
			self.BE = [abc.d, abc.ə, abc.r, abc.ɪ]
			self.CAUSE = [abc.d, abc.ə, abc.ʃ, abc.ɑ]
			self.ADV = [abc.k, abc.e]
			self.COM = [abd.k, abc.o]