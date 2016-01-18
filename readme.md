#Phone Trie

`main.py` gets all words from [here](http://www.mieliestronk.com/corncob_lowercase.txt), loads them all into a marisa trie, then iterates over the phone number/input. The input is iterated in the manner of a radix/prefix trie, getting each level of words/prefixes and continuing on to the next within the bounds of the length of the phone number/input.

If the phone number/input itself is, or is part of a word, any/all matches are added to results.

If the branch length is less than the length of the phone number/input, any/all matches for the remaining digits are added. This is the case when words/phrases overrun the length of the phone number/input.

##To run

`python main.py [phone_number]`

eg: `python main.py 7627245`

##Output

input `7627245`

```
1) 76272457225 rocsagkraal ('roc', 'sag', 'kraal')

2) 76272457238 rocsagkraft ('roc', 'sag', 'kraft')

3) 7627245743477435 rocsagkriegspiel ('roc', 'sag', 'kriegspiel')

4) 76272457455 rocsagkrill ('roc', 'sag', 'krill')

5) 7627245736546 rocsagkremlin ('roc', 'sag', 'kremlin')

... 

20567) 7627245797866 rocsagkrypton ('soc', 'rag', 'krypton')
```