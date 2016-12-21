import nltk
from nltk.draw.tree import TreeView
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
from nltk.corpus import wordnet as wn
from enum import Enum
import copy
import os
import csv
from generator import Generator

class Constant:
	PRES = 'ma'
	PAST = 'mu'
	FUTR = 'mo'
	NEG = 'n'
	ADV = 'ce'
	COM = 'co'
	SUP = 'cu'
	NEUTRAL = 'el'
	PLURAL = 'n'
	REL = 'ra'
	WHAT = 'hev'
	IS = 'si'

def to_translate(word):
	if not word:
		return ''
	return '<' + word.lower() + '>'
main_verbs = {
		'love': ['dkbk', 'al', to_translate('affection')],
	'like': ['dkbk', 'al', to_translate('preference')],
	'need': ['dkbk', 'al', to_translate('need')],
	'want': ['dkbk', 'al', to_translate('desire')],
	'can': ['dkbk', 'al', to_translate('ability')],
	'could': ['dkbk', 'al', to_translate('ability')],
	'should': ['dkbk', 'al', to_translate('priority')],
	'shall': ['dkbk', 'al', to_translate('priority')],
	'must': ['dkbk', 'al', to_translate('obligation')],
	'may': ['dkbk', 'al', to_translate('possibility')],
	'might': ['dkbk', 'al', to_translate('possibility')],
	'will' : [],
	'would' : [],
	'did' : [],
	'go': ['dkco'],
	'cause': ['dksa'],
	'have': ['dkbk'],
	'be': ['dkri'],
	'do': ['dkva'],
	'does': [],
	'did': [],
	'are': [],
	"'re": [],
	'is': [],
	"'s": [],
	'am': [],
	"'m": [],
	'was': [],
	'were': [],
	'has': [],
	'have': [],
	'had': []
}
main_whs = {
	'what': [Constant.WHAT, to_translate('thing'), Constant.REL],
	'who': [Constant.WHAT, to_translate('person'), Constant.REL],
	'whom': [Constant.WHAT, to_translate('person'), Constant.REL],
	'where': [Constant.WHAT, to_translate('place'), Constant.REL],
	'why': [Constant.WHAT, to_translate('reason'), Constant.REL],
	'how_do': [Constant.WHAT, to_translate('mean'), Constant.REL],
	'how_be': [Constant.WHAT, to_translate('status'), Constant.REL]
}
class Tense(Enum):
	present = 0
	past = -1
	future = 1
class AuxV:
	class Be:
		sM = { 'value' : "'m", 'tense' : Tense.present}
		AM = { 'value' : 'am', 'tense' : Tense.present}
		IS = { 'value' : 'is', 'tense' : Tense.present}
		sS = { 'value' : "'s", 'tense' : Tense.present}
		ARE = { 'value' : 'are', 'tense' : Tense.present}
		sRe = { 'value' : "'re", 'tense' : Tense.present}
		WAS = { 'value' : 'was', 'tense' : Tense.past}
		WERE = { 'value' : 'were', 'tenes' : Tense.past}
	class Do:
		DOES = { 'value' : 'does', 'tense' : Tense.present}
		DO = { 'value' : 'do', 'tense' : Tense.present}
		DID = { 'value' : 'did', 'tense' : Tense.past}
	class Have:
		HAS = { 'value' : 'has', 'tense' : Tense.present}
		HAVE = { 'value' : 'have', 'tense' : Tense.present}
		HAD = { 'value' : 'had', 'tense' : Tense.past}
	class Modal:
		CAN = { 'value' : 'can', 'tense' : Tense.present}
		COULD = { 'value' : 'could', 'tense' : Tense.past}
		MAY = { 'value' : 'may', 'tense' : Tense.present}
		MIGHT = { 'value' : 'might', 'tense' : Tense.past}
		SHALL = { 'value' : 'shall', 'tense' : Tense.future}
		SHOULD = { 'value' : 'should', 'tense' : Tense.present}
		WILL = { 'value' : 'will', 'tense' : Tense.future}
		WOULD = { 'value' : 'would', 'tense' : Tense.past}
		MUST = { 'value' : 'must', 'tense' : Tense.present}
	def all():
		li = [AuxV.Be.sM, AuxV.Be.AM, AuxV.Be.sS, AuxV.Be.IS, AuxV.Be.sRe, AuxV.Be.ARE, AuxV.Be.WAS, AuxV.Be.WERE,
				AuxV.Do.DOES, AuxV.Do.DO, AuxV.Do.DID,
				AuxV.Have.HAS, AuxV.Have.HAVE, AuxV.Have.HAD,
				AuxV.Modal.CAN, AuxV.Modal.COULD, AuxV.Modal.MAY, AuxV.Modal.MIGHT,
				AuxV.Modal.SHALL, AuxV.Modal.SHOULD, AuxV.Modal.WILL, AuxV.Modal.WOULD, AuxV.Modal.MUST
			]
		return li
	def be():
		li = [AuxV.Be.sM, AuxV.Be.AM, AuxV.Be.sS, AuxV.Be.IS, AuxV.Be.sRe, AuxV.Be.ARE, AuxV.Be.WAS, AuxV.Be.WERE]
		return li
	def get_aux(aux):
		for v in AuxV.all():
			if aux.lower() == v['value']:
				return v
	def is_be(aux):
		for v in AuxV.be():
			if aux.lower() == v['value']:
				return True
		return False
class CFG:
	def init():
		auxV = 'AuxV -> ' + ' | '.join('"' + v['value'] + '"' for v in AuxV.all()) + '\n'
		CFG.statement += CFG.base + auxV
		CFG.question += CFG.base + auxV
	statement = """		
	S -> NP VP | NP AuxV RB VP | NP AuxV VP | S s
	"""
	question = """
	S -> AuxP | WRB AuxP | WDT NP AuxP | WDT AuxP | WP AuxP | S s
	AuxP -> AuxV RB NP VP | AuxV NP VP | AuxV DT | AuxV IN | AuxV NP | AuxV RB NP
	"""
	base = """
	VP -> VP CC VP | V | VP NP | VP PP | VP Adv | V VBG | VP TO VP | VP AP
	NP -> N | CD N | AP N | DT N | CD AP N | DT AP N | DT CD N | DT CD AP N | NP CC NP | PRP | NP PP | NP RelClause | DP
	RelClause -> Rel S | Rel VP | Rel AuxV VP | Rel AuxV RB VP
	Rel -> "who" | "that" | "which"
	PP -> PP P NP | P NP | P
	P -> IN | TO
	AP -> AP A | A | AP CC A
	Adv -> RB | RBR | RBS
	A -> JJ | JJR | JJS
	N -> NN | NNS | NNP | NNPS
	V -> VBD | VBN | VBP | VBZ | VB | VBG
	DP -> "that" | "this" | "these" | "those"
	"""
def levenshtein(s1, s2):
	if len(s1) < len(s2):
		return levenshtein(s2, s1)
	if len(s2) == 0:
		return len(s1)
	previous_row = range(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
	return previous_row[-1]
def adjectize(adv):
	max_value = 10 ** 9
	res = None
	for ss in wn.synsets(adv):
		for lemmas in ss.lemmas():
			for ps in lemmas.pertainyms():
				value = levenshtein(ps.name(), adv)
				if max_value > value:
					max_value = value
					res = ps.name()
	if res:
		return res
	else:
		return adv
def verbize(verb, need_base=True):
	lower = verb.lower()
	if lower in main_verbs:
		return main_verbs[lower]
	else:
		if need_base:
			return ['dkva'] + [to_translate(lower)]
		else:
			return [to_translate(lower)]
def normalize(sentence):
	lower = sentence.lower()
	res = ''
	for index, c in enumerate(lower):
		if c == 'i' and (lower[index - 1] in (' ', "'") or index == 0) and (lower[index + 1] in (' ', "'") or index == len(lower) - 1):
			res += 'I'
		else:
			res += c
	return res
class Translator:
	alter_name = {
		'WP$' : 'WPs',
		'.' : 's',
		'PRP$' : 'DT'
	}
	def __init__(self, sentence):
		CFG.init()
		self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
		self.lemmatizer.lemmatize('is', 'v')
		self.sentence = normalize(sentence)
		self.tokenized = nltk.word_tokenize(self.sentence)
		self.pos_tag = nltk.pos_tag(self.tokenized)
		self.remove_have()
		self.tagging()
		"""	VP -> VP CC VP | V | VP NP | VP PP | VP Adv | V VBG | VP TO VP | VP AP
	NP -> N | CD N | AP N | DT N | CD AP N | DT AP N | DT CD N | DT CD AP N | NP CC NP | PRP | NP PP | NP RelClause | DP
	RelClause -> Rel S | Rel VP | Rel AuxV VP | Rel AuxV RB VP
	Rel -> "who" | "that" | "which"
	PP -> PP P NP | P NP | P
	P -> IN | TO
	AP -> AP A | A | AP CC A
	Adv -> RB | RBR | RBS
	A -> JJ | JJR | JJS
	N -> NN | NNS | NNP | NNPS
	V -> VBD | VBN | VBP | VBZ | VB | VBG
	DP -> "that" | "this" | "these" | "those"
	"""
	def finalize(self):
		f = open('dictionary.csv', 'r')
		reader = csv.DictReader(f)
		dic = {}
		for line in reader:
			dic[line['word']] = line['translation']
		gen = Generator()
		# for line in fi:
		# 	word = line.strip().lower()
		# 	if word in dic:
		# 		pass
		# 		#print(dic[word])
		# 	else:
		# 		new = gen.make_word(gen.count_sound(word))
		# 		res = gen.represent(new)
		# 		dic[word] = res
		# 		print(word.lower(), res)
		self.gloss = ' '.join(self.res)
		self.res = ''
		st = None
		for index, c in enumerate(self.gloss):
			if st == None and c == '<':
				st = index
			elif st != None and c == '>':
				word = self.gloss[st+1:index]
				if word in dic:
					self.res += dic[word]
				else:
					new = gen.make_word(gen.count_sound(word))
					res = gen.represent(new)
					dic[word] = res
					self.res += dic[word]
					fw = open('dictionary.csv', 'w')
					fw.write('word,translation,phonology\n')
					for word in sorted(dic):
						fw.write(word.lower() + ',' + dic[word] + ',' + gen.phonorepr(dic[word]) + '\n')
				st = None
			elif st == None:
				self.res += c
		self.phonology = gen.phonorepr(self.res)
	def remove_have(self):
		is_start = None
		remove_index = []
		for index, (word, tag) in enumerate(self.pos_tag):
			if AuxV.get_aux(word) != None:
				is_start = False
			elif is_start == False and tag.startswith('V'):
				previous = index
				is_start = True
			elif is_start == True and tag.startswith('V'):
				previous_word = self.pos_tag[previous][0]
				if previous_word in ('have', 'be', 'been'):
					remove_index.append(previous)
				previous = index
			elif is_start == True and not tag.startswith('V'):
				is_start = None
		new_pos_tag = []
		new_tokenized = []
		for index in range(len(self.pos_tag)):
			if index not in remove_index:
				new_pos_tag.append(self.pos_tag[index])
				new_tokenized.append(self.tokenized[index])
		self.pos_tag = new_pos_tag
		self.tokenized = new_tokenized
		print(self.tokenized)
		print(self.pos_tag)
	def is_question(self):
		return self.tokenized[-1][0] == '?'
	def tagging(self):
		self.cfg_tag = ""
		dic = {}
		for word, tag in self.pos_tag:
			if tag in Translator.alter_name:
				tag = Translator.alter_name[tag]
			if tag not in dic:
				dic[tag] = []
			dic[tag].append(word)
		for tag in dic:
			self.cfg_tag += '\t' + tag + ' -> ' + ' | '.join(map(lambda x: '"' + x + '"', dic[tag])) + '\n'
	def translate(self):
		if self.is_question():
			self.question_tree()
		else:
			self.statement_tree()
	def cfg_parser(self, cfg):
		cfg_string = cfg + self.cfg_tag
		print(cfg_string)
		cfg = nltk.CFG.fromstring(cfg_string)
		parser = nltk.ChartParser(cfg)
		return parser
	def question_tree(self):
		parser = self.cfg_parser(CFG.question)
		self.res = None
		for tree in parser.parse(self.tokenized):
			tree.pretty_print()
			if self.res == None:
				self.res = self.question_translate(tree)
				print(self.res)
			else:
				print(self.question_translate(tree))
	def statement_tree(self):
		parser = self.cfg_parser(CFG.statement)
		self.res = None
		for tree in parser.parse(self.tokenized):
			tree.pretty_print()
			if self.res == None:
				self.res = self.statement_translate(tree)
				print(self.res)
			else:
				print(self.statement_translate(tree))
	def question_translate(self, tree):
		result = []
		auxP = None
		np = None
		wdt = None
		wrb = None
		wp = None
		is_be = None
		for index, child in enumerate(tree):
			label = child.label()
			if label == 's':
				result += [child[0]]
			elif label == 'S':
				result += self.question_translate(child)
			elif label == 'AuxP':
				auxP = self.auxP_translate(child)
			elif label == 'NP':
				np = self.np_translate(child)
			elif label == 'WRB':
				wrb = child[0].lower()
				is_be = AuxV.is_be(tree[index + 1][0][0])
			elif label == 'WDT':
				wdt = True
			elif label == 'WP':
				wp = child[0].lower()
		if wrb:
			if wrb != 'how':
				result += main_whs[wrb] + auxP
			elif is_be:
				result += main_whs['how_be'] + auxP
			else:
				result += main_whs['how_do'] + auxP
		elif wdt:
			if np == None:
				np = [to_translate('thing')]
			result += [Constant.WHAT] + np + [Constant.REL] + auxP
		elif wp:
			result += main_whs[wp] + auxP
		elif auxP != None:
			result += [Constant.IS, Constant.REL] + auxP
		return result
	def auxP_translate(self, tree):
		result = []
		neg = False
		aux = None
		np = None
		vp = None
		for child in tree:
			label = child.label()
			if label == 'NP':
				np = self.np_translate(child)
			elif label == 'VP':
				vp = self.vp_translate(child, aux, neg)
			elif label == 'AuxV':
				aux = AuxV.get_aux(child[0])
			elif label == 'RB':
				neg = True
		if vp != None:
			result += np + vp
		else:
			tense = aux['tense']
			if tense == Tense.present:
				article = Constant.PRES
			elif tense == Tense.past:
				article = Constant.PAST
			elif tense == Tense.future:
				article = Constant.FUTR
			if neg:
				article += Constant.NEG
			result += np + [article] + main_verbs['be']
		return result
	def statement_translate(self, tree, is_rel=False):
		result = []
		neg = False
		aux = None
		for child in tree:
			label = child.label()
			if label == 'S':
				result += self.statement_translate(child)
			elif label == 's':
				result += [child[0]]
			elif label == 'NP':
				result += self.np_translate(child)
				if is_rel:
					result += [Constant.REL]
			elif label == 'VP':
				result += self.vp_translate(child, aux, neg)
			elif label == 'AuxV':
				aux = AuxV.get_aux(child[0])
			elif label == 'RB':
				neg = True
		return result
	def vp_translate(self, tree, aux=None, neg=None, need_article=True, need_base=True):
		result = []
		article = None
		if aux != None:
			if aux['tense'] == Tense.present:
				article = Constant.PRES
			elif aux['tense'] == Tense.past:
				article = Constant.PAST
			elif aux['tense'] == Tense.future:
				article = Constant.FUTR
			if neg:
				article += Constant.NEG
			if aux['value'] == 'do':
				result += [article]
			else:
				result += [article] + verbize(aux['value'])
		for child in tree:
			label = child.label()
			if label == 'VP':
				if aux!= None and verbize(aux['value']):
					child_need_base = False
				else:
					child_need_base = True
				result += self.vp_translate(child, need_article=need_article and (aux == None), need_base=child_need_base)
			elif label == 'CC':
				result += [to_translate(child[0])]
			elif label == 'NP':
				result += self.np_translate(child)
			elif label == 'PP':
				result += self.pp_translate(child)
			elif label == 'AP':
				result += self.ap_translate(child)
			elif label == 'VBG':
				word = child[0]
				verb = self.lemmatizer.lemmatize(word, 'v')
				result += verbize(verb, False)
			elif label == 'Adv':
				word = child[0][0]
				adj = adjectize(word)
				result += [to_translate(adj) + Constant.ADV]
			elif label == 'V':
				v_label = child[0].label()
				word = child[0][0]
				verb = self.lemmatizer.lemmatize(word, 'v')
				if v_label in ('VBD', 'VBN'):
					tense = Tense.past
				elif v_label in ('VBG', 'VBP', 'VBZ'):
					tense = Tense.present
				else:
					tense = Tense.present
				if need_article and article == None:
					if tense == Tense.present:
						article = Constant.PRES
					elif tense == Tense.past:
						article = Constant.PAST
					elif tense == Tense.future:
						article = Constant.FUTR
					if neg:
						article += Constant.NEG
					result += [article] + verbize(verb)
				else:
					result += verbize(verb, need_base)
		return result
	def np_translate(self, tree):
		result = []
		ap = []
		cd = []
		dt = None
		n = None
		is_plural = None
		for child in tree:
			label = child.label()
			if label == 'RelClause':
				result += self.rel_translate(child)
			elif label == 'PRP' or label == 'CC':
				result += [to_translate(child[0])]
			elif label == 'NP':
				result += self.np_translate(child)
			elif label == 'AP':
				ap = self.ap_translate(child)
			elif label == 'PP':
				result += self.pp_translate(child)
			elif label == 'CD':
				cd = [to_translate(child[0])]
			elif label == 'DT' or label == 'DP':
				dt = child[0]
			elif label == 'N':
				n_label = child[0].label()
				word = child[0][0]
				if n_label == 'NN':
					is_plural = False
				elif n_label == 'NNS':
					is_plural = True
				n = [to_translate(self.lemmatizer.lemmatize(word, 'n'))]
		if n != None:
			if dt == None:
				result += cd + n + ap
			else:
				article = Constant.NEUTRAL
				if is_plural:
					article = Constant.PLURAL + Constant.NEUTRAL
				article += to_translate(dt)
				result += cd + [article] + n + ap
		elif dt != None:
			result += [to_translate(dt)]
		return result
	def rel_translate(self, tree):
		result = []
		neg = False
		aux = None
		for child in tree:
			label = child.label()
			if label == 'Rel':
				result += [Constant.REL]
			elif label == 'S':
				result += self.statement_translate(child)
			elif label == 'VP':
				result += self.vp_translate(child, aux, neg, aux == None)
			elif label == 'AuxV':
				aux = AuxV.get_aux(child[0])
			elif label == 'RB':
				neg = True
		return result
	def pp_translate(self, tree):
		result = []
		for child in tree:
			label = child.label()
			if label == 'PP':
				result += self.pp_translate(child)
			elif label == 'P':
				result += [to_translate(child[0][0])]
			elif label == 'NP':
				result += self.np_translate(child)
		return result
	def ap_translate(self, tree):
		result = []
		for child in tree:
			label = child.label()
			if label == 'AP':
				result += self.ap_translate(child)
			elif label == 'CC':
				result += [to_translate(child[0])]
			elif label == 'A':
				a_label = child[0].label()
				word = child[0][0]
				if a_label == 'JJ':
					a = to_translate(word)
				elif a_label == 'JJR':
					a = to_translate(self.lemmatizer.lemmatize(word, 'a')) + Constant.COM
				elif a_label == 'JJS':
					a = to_translate(self.lemmatizer.lemmatize(word, 'a')) + Constant.SUP
				result += [a]
		return result
if __name__ == '__main__':
	sent = input()
	trans = Translator(sent)
	trans.translate()