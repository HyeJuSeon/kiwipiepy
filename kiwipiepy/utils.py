from kiwipiepy import Kiwi

class Stopwords:

    def load_stopwords(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            stopwords = f.readlines()
        for idx, stopword in enumerate(stopwords):
            stopword = stopword.strip()
            form, tag = stopword.split('/')
            stopwords[idx] = (form, tag)
        return stopwords

    def __init__(self, filename='kiwipiepy/corpus/stopwords.txt'):
        self.stopwords = self.load_stopwords(filename)

    def words(self):
        return self.stopwords

    def tag_exists(self, tag):
        tag_list = ['NNG', 'NNP', 'NNB', 'NR', 'NP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MM', 'MAG', 'MAJ', 'IC', 'JKS',
                    'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC', 'EP', 'EF', 'EC', 'ETN', 'ETM', 'XPN', 'XSN',
                    'XSV', 'XSA', 'XR', 'SF', 'SP', 'SS', 'SE', 'SO', 'SW', 'SL', 'SH', 'SN', 'UN', 'W_URL', 'W_EMAIL',
                    'W_HASHTAG', 'W_MENTION']
        if tag in tag_list:
            return True
        raise ValueError(f"'{tag}' is an invalid tag.")

    def token_exists(self, token):
        if token in self.stopwords:
            return True
        raise ValueError(f"'{token}' doesn't exist in stopwords")

    def add(self, tokens):
        if type(tokens) is str:
            self.stopwords.append((tokens, 'NNP'))
        elif type(tokens) is tuple and self.tag_exists(tokens[1]):
            self.stopwords.append(tokens)
        else:
            for token in tokens:
                if type(token) is str:
                    token = (token, 'NNP')
                    self.stopwords.append(token)
                    continue
                if self.tag_exists(token[1]):
                    self.stopwords.append(token)
        self.stopwords = list(set(self.stopwords))

    def remove(self, tokens):
        if type(tokens) is str and self.token_exists((tokens, 'NNP')):
            self.stopwords.remove((tokens, 'NNP'))
        elif type(tokens) is tuple and self.token_exists(tokens):
            self.stopwords.remove(tokens)
        else:
            for token in tokens:
                if type(token) is str:
                    token = (token, 'NNP')
                if self.token_exists(token):
                    self.stopwords.remove(token)
        self.stopwords = list(set(self.stopwords))

    def filter(self, tokens):
        filtered_tokens = tokens.copy()
        for token in tokens:
            form, tag = token.form, token.tag
            if (form, tag) in self.stopwords:
                filtered_tokens.remove(token)
        return filtered_tokens
