from nltk.corpus import wordnet
class SynSetFinder:

	def __init__(self, word):
		self.word = word #initializes  Synsetfinder class with word
	
	def list_all_synsets(self):
		synset_list = wordnet.synsets(self.word, pos='n')
		return synset_list
		

