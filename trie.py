import marisa_trie
import words
import phone
import itertools

_words = None #['rob','sail','sob','pail','robs','bsa','pailer','sobuca']

def _create(words):
	trie_load_iterations = 0 
	numbered_words = []
	bytes_words = []
	for word in words: 
		numbered_word = ''
		for letter in phone.safe_word(word):
			trie_load_iterations+=1
			numbered_word += phone.dial[letter]
		if numbered_word: 
			numbered_words.append(unicode(numbered_word))
			bytes_words.append(bytes(word))

	return marisa_trie.BytesTrie(zip(numbered_words, bytes_words))

def get_bounded_radix_dict(phone_number, trie):
	#this whole thing is hacky, but avoids stack problems-->
	#tail recursion would be easier to read
	indexed_result_words = dict()
	all_radixes = [get_next_radix_level(phone_number, 0, trie, indexed_result_words)]
	while all_radixes:
		i =0
		if all_radixes:
			cur_radix = all_radixes.pop(0)
			for word in cur_radix:
				i+=len(word)
				next_radix_level = get_next_radix_level(phone_number, i, trie, indexed_result_words)
				if next_radix_level: 
					all_radixes.append(next_radix_level)

			#pop extra-->
			if all_radixes: cur_radix = all_radixes.pop(0)

	return indexed_result_words

def get_cleaned_cartesian_results_from_radix_dict(phone_number, indexed_result_words):
	tuples = [tuple(indexed_result_words[key]) for key in indexed_result_words]
	cartesian = list(itertools.product(*tuples))
	no_spaces = [(''.join(map(str,t)),t) for t in cartesian]
	cleaned_cartesian = [(convert_word_to_numbers(word), word, tup) for word, tup in no_spaces if convert_word_to_numbers(word) in phone_number or phone_number in convert_word_to_numbers(word)]
	return cleaned_cartesian

def get_next_radix_level(phone_number, phone_index, trie, indexed_result_words):
	phone_num_slice = phone_number[phone_index:len(phone_number)]
	for outer_i, outer_num in enumerate(phone_num_slice):
		key = ''
		for inner_num in phone_num_slice[outer_i:len(phone_number)]:
			key+=inner_num
			u_key = unicode(key)		
			if u_key in trie: 
				for val in trie[u_key]:
					if phone_index in indexed_result_words:
						indexed_result_words[phone_index] = list(set(indexed_result_words[phone_index]) | set(trie[u_key]))
					else:
						indexed_result_words[phone_index] = set(trie[key])
		
		break
	return indexed_result_words[phone_index] if phone_index in indexed_result_words else []

def convert_word_to_numbers(word):
	return ''.join([number for number in [phone.dial[letter] for letter in phone.safe_word(word)]])

def add_overflow_keys(phone_number, cartesian, trie):
	tuples = []
	for (num, word, tup) in cartesian:

		whole_word_keys = [prefix for prefix in trie.keys(unicode(phone_number)) if prefix[0:len(phone_number)] == phone_number]
		if whole_word_keys:
			for wrds in [trie[key] for key in whole_word_keys]:
				for word_for_key in wrds:
					final_num = convert_word_to_numbers(word_for_key)
					final_word = word_for_key
					final_tup = (word_for_key,)
					final = (final_num, final_word, final_tup)
					if final not in tuples:
						tuples.append(final)

		remainder = phone_number.replace(num,'')
		if remainder:
			remainder_keys = trie.keys(unicode(remainder))
			if remainder_keys:
				for wrds in [trie[key] for key in remainder_keys]:
					for word_for_key in wrds:
						final_num = num + convert_word_to_numbers(word_for_key)
						final_word = word + word_for_key
						final_tup = tuple(list(tup) + [word_for_key])
						final = (final_num, final_word, final_tup)
						if final not in tuples:
							tuples.append(final)

		new_tup = (num,word,tup)
		if new_tup not in tuples:
				tuples.append(new_tup)

	return tuples


def get_words_for(phone_number):

	print '[begin] getting words from web and creating trie'	
	word_trie = _create(_words if _words != None else words.get())
	print '[done]'

	print '[begin] getting radix levels that are in the bounds of the phone number'
	bounded_radix = get_bounded_radix_dict(phone_number, word_trie)
	print '[done]'
	

	print '[begin] to massage bounded radix into cartesian'
	cartesian = get_cleaned_cartesian_results_from_radix_dict(phone_number, bounded_radix)
	print '[done]'
	

	print '[begin] add all keys/words that overrun phone number bounds/length'
	final = add_overflow_keys(phone_number, cartesian, word_trie)
	print '[done]'
	
	return final


