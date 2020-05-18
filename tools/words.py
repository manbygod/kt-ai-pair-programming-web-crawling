from konlpy.tag import Kkma
from . import singleton

class WordsTool(metaclass=singleton.Singleton):
 
    def __init__(self):
        self.kkma = Kkma()
        
    def getWordCount(self, words):
        words = words.strip()
        words = self.kkma.pos(words)            
        words = [w[0] for w in words if w[1] in ['NNG', 'NNP']]
        
        word_tup_list = [(w, words.count(w)) for w in set(words)]
        word_tup_list = sorted(word_tup_list, key = lambda x : x[1], reverse=True)
        
        return word_tup_list