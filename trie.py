import cPickle as pickle

class Trie:
    def __init__(self):
        self.trie_obj={}
    
    def add_term(self, term, value):
        curr_obj = self.trie_obj
        term_size = len(term)
        last_index = term_size - 1
        for index, char in enumerate(term):
            if char not in curr_obj:
                if index == last_index:
                    curr_obj[char]= {'*':[value]}
                else:
                    curr_obj[char] = {term[index+1]:{}}
            else:
                if index == last_index:
                    if '*' in curr_obj[char] and curr_obj[char]['*']:
                        curr_obj[char]['*'].append(value)
                    else:
                        curr_obj[char]['*'] = [value]
            curr_obj = curr_obj[char]

    def get_item(self, term):
        curr_obj = self.trie_obj
        for letter in term:
            if letter in curr_obj:
                curr_obj = curr_obj[letter]
            else:
                return ""
        if '*' in curr_obj:
            return curr_obj['*']
        else:
            return ''

    def print_trie(self):
        print self.trie_obj
    
    def pickle_me(self, filename):
        myfile = open(filename, 'wb')
        pickle.dump(self.trie_obj, myfile, True)
        myfile.close()

    def unpickle_me(self, filename):
        myfile = open(filename, 'rb')
        self.trie_obj = pickle.load(myfile)
        myfile.close()

if __name__ == "__main__":
    mytrie = Trie()
    mytrie.unpickle_me('pickled_data')
    #mytrie.add_term('apple', 'a fruit')
    #mytrie.add_term('appletree', 'tree which has apple fruit')
    #mytrie.add_term('apply', 'an action')
    mytrie.print_trie()
    #mytrie.pickle_me('pickled_data')
    while 1:
        term = raw_input()
        if term == 'end': break
        print mytrie.get_item(term)
