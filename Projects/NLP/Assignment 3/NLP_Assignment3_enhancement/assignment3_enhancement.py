__author__ = 'Bharath'
from nltk import *
import nltk
from collections import Counter
import io
import re
from nltk.corpus import wordnet as wn
import itertools

def readfile(filename):
    txt = io.open(filename, encoding='utf8').readlines()
    return " ".join(txt)

def tokenize(text):
    tokens = re.findall(r'\w+', text)
    return tokens

def get_nouns(tagged_text):
    noun_text = []
    tags =  ['NN']
    for i in tagged_text:
        if (i[1] in tags):
            noun_text.append(i[0])
    return noun_text

def count_words(token):
    x = {}
    c = Counter()
    c.update(token)
    x = dict(c)
    return x


def get_synset(noun_dict):
    noun_synset = {}
    for noun in noun_dict:
        synset = wn.synsets(noun)
        noun_synset[noun] = synset

    return noun_synset

def get_hypernyms(noun_synset):
    noun_hypernym = {}
    for i in noun_synset:
        hypernym = []
        if noun_synset[i]:
            for j in noun_synset[i]:
                hypernym.append(j.hypernyms())
                merged = list(itertools.chain(*hypernym))
            noun_hypernym[i] = merged
    return noun_hypernym

def get_hyponyms(noun_synset):
    noun_hyponym = {}
    for i in noun_synset:
        hyponym = []
        if noun_synset[i]:
            for j in noun_synset[i]:
                hyponym.append(j.hyponyms())
                merged = list(itertools.chain(*hyponym))
            noun_hyponym[i] = merged
    return noun_hyponym

def get_meronyms(noun_synset):
    noun_meronym = {}
    for i in noun_synset:
        meronym = []
        if noun_synset[i]:
            for j in noun_synset[i]:
                meronym.append(j.part_meronyms())
                merged = list(itertools.chain(*meronym))
            noun_meronym[i] = merged
    return noun_meronym

def merge_dictionary(noun_dict,synset,hypernym,hyponym,meronym):
    merged_dict ={}
    for i in noun_dict:
        terms = []
        x =synset[i]
        if x:
            terms.append(synset[i])
        if i in hypernym:
            terms.append(hypernym[i])
        if i in hyponym:
            terms.append(hyponym[i])
        if i in meronym:
            terms.append(meronym[i])
        merged = list(itertools.chain(*terms))
        merged_dict[i] = merged
    return merged_dict

def get_lemma(merged_dict):
    lemma_word = {}
    for i in merged_dict:
        word_list = []
        for j in range(len(merged_dict[i])):
            y = merged_dict[i][j].lemma_names()
            word_list.append(y)
        merged = list(itertools.chain(*word_list))
        lemma_word[i] = list(set(merged))
    return lemma_word

filename = 'input.txt'
input_text = readfile(filename)

tokens = tokenize(input_text)
text_tagged = nltk.pos_tag(tokens)
noun_text = get_nouns(text_tagged)

noun_dictionary = count_words(noun_text)

#get synset for each noun
noun_synsets = get_synset(noun_dictionary)

#get hypernym for each synset
noun_hypernyms = get_hypernyms(noun_synsets)

#get hyponym for each synset
noun_hyponyms = get_hyponyms(noun_synsets)

noun_meronyms = get_meronyms(noun_synsets)

merge_synsets = merge_dictionary(noun_dictionary,noun_synsets,noun_hypernyms,noun_hyponyms,noun_meronyms)

lemma_words = get_lemma(merge_synsets)


test = {}
for i in lemma_words:
    test1 =[]
    for j in lemma_words:
        if i != j:
            for x in lemma_words[i]:
                if x in lemma_words[j]:
                    test1.append(j)
    test[i] = list(set(test1))

test_chain = {}
for i in test:
    x = test[i]
    x.insert(0,i)
    test_chain[i] = x

noun_text_o = []
for i in noun_text:
    if i not in noun_text_o:
        noun_text_o.append(i)

lex_chain = {}
for i in noun_text_o:
    test1 =[]

    for j in noun_text_o:
        if i != j:
            flag = False
            count = 0
            while(flag == False):
                if count >= len(lemma_words[i]):
                    flag = True
                elif (lemma_words[i][count] in set(lemma_words[j])) and count < len(lemma_words[i]):
                    test1.append(j)
                    flag = True
                else:
                    count = count + 1
    lex_chain[i] = list(set(test1))

test_chain2 = []
for i in lex_chain:
    x = lex_chain[i]
    x.insert(0,i)
    test_chain2.append(x)

test_chain_copy = test_chain2

test_chain3 =[]
for i in noun_text_o:
    flag = False
    for j in test_chain3:
        if i in set(j):
            flag = True
    if flag == False:
        xx = []
        for j in test_chain_copy:
            if i in set(j):
                xx.append(j)
                test_chain_copy.remove(j)
        merged = list(itertools.chain(*xx))
        test_chain3.append(list(set(merged)))

test_chain_copy2 = test_chain3
for i in test_chain_copy2:
    for j in i:
        for x in test_chain_copy2:
            if i != x:
                for m in x:
                    if j == m:
                        x.remove(j)

print test_chain_copy2
final_list = []
for x in test_chain_copy2:
    temp = []
    for y in x:
        temp.append((y,(noun_dictionary[y])))
    final_list.append(temp)

for i in range(len(final_list)):
    print "Chain %d : " %(i+1),final_list[i]