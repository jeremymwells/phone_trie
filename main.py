import trie
import sys

def main(phone_number):

	all_words_tuple = trie.get_words_for(phone_number)

	for i, (number, concatenated_word, parts) in enumerate(all_words_tuple):
		print str(i) + ') ' + str(number) + ' ' + concatenated_word + ' ' + str(parts) + '\n'
	
	return 0

def handle_args(args):
	if len(args)>1:
		clean_args = args[1].replace('1','').replace('0','')
		if clean_args:
			return main(clean_args)

	return print_error()
		
def print_error():
	print '[error] no arguments received - remember 1\'s and 0\'s are ignored'
	print '[info] call script with a phone number, eg: python main.py 7627245'
	return 1

if __name__ == "__main__":
	handle_args(sys.argv)

	