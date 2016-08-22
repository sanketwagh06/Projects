from nltk.corpus import wordnet
from SynSetFinder import *
class NounData:
	def __init__(self, noun):
		self.count           = 0
        	self.synset_list     = []
       		self.hypernym_list   = []
       		self.hyponym_list    = []
        	self.meronym_list    = []
        	self.antonym_list    = []	
		self.noun = noun 
		self.__calculate_all_data(noun)
		self.count += 1
	
	def __get_hyponyms(self, synsets):
			hyponym_list_p = []
			for syn_set in synsets:
				hyponym_list_p.append(syn_set.hyponyms())
			return hyponym_list_p

	def __get_hypernyms(self, synsets):
		hypernym_list_p = []
		for syn_set in synsets:
			hypernym_list_p.append(syn_set.hypernyms())
		return hypernym_list_p

	def __get_antonyms(self, synsets):
		antonym_list_p = []
		for syn_set in synsets:
			for lemma_word in syn_set.lemmas():
				antonym_list_each_lm = [lemma_word.antonyms()] 
				antonym_list_p.append(antonym_list_each_lm)
		return antonym_list_p


		
	def __calculate_all_data(self, noun):
		synsetFinder = SynSetFinder(noun)
		synsets = synsetFinder.list_all_synsets()
		self.synset_list.append(synsets)
		self.hypernym_list.append(self.__get_hypernyms(synsets))
		self.hyponym_list.append(self.__get_hyponyms( synsets))
		self.antonym_list.append(self.__get_antonyms(synsets))

	def increase_count_value(self):
		self.count += 1
