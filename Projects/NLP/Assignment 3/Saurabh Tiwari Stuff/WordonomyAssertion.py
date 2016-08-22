class WordonomyAssertion:
	def __init__(self):
		pass


	def check_assertion(self, word, lexical_chain_dict, wdd_cpy):
		for key in lexical_chain_dict:
			list_lexical_chain = lexical_chain_dict[key]
			noun_data = wdd_cpy[key]

			#compares value existence in hypernym list
			for hypernym in noun_data.hypernym_list:
				for synsets in hypernym:
					for synset in synsets:
						for lemma in synset.lemmas():
							if word in lemma.name():
								list_lexical_chain.append(word)
								return True

			#compares value existence in hyponym list
			for hyponym in noun_data.hyponym_list:
				for synsets in hyponym:
					for synset in synsets:
						for lemma in synset.lemmas():
							if word in lemma.name():
								list_lexical_chain.append(word)
								return True

			#compares value from antonym list
			for antonym in noun_data.antonym_list:
				for synsets in antonym:
					for synset in synsets:
						for lemma in synset:
							if word in lemma.name():
								list_lexical_chain.append(word)
								return True

			#Compares value with a synset itself
			for synsets in noun_data.synset_list:
				for synset in synsets:
					for lemma in synset.lemmas():
						if word in lemma.name():
							list_lexical_chain.append(word)
							return True
	
		
