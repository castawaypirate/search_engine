import string

class Indexer:

    def __init__(self):
        self.dictionary = dict()
        self.pages = []

    def update(self, url, text):
        if self.pages.__contains__(url):
            print("Page: " + url + " is already indexed")
        else:
            self.pages.append(url)
            clean_text = text.replace(". ",  " ")
            clean_text.replace(", ", " ")
            signs = "!@#$%^&*()-_=+"
            for char in signs:
                clean_text = clean_text.replace(char, "")
            clean_text = clean_text.replace("  ", " ")


            terms = clean_text.split(" ")

            for term in terms:
                if term[len(term) - 1] == '.':
                    term = term[:-1]
                if self.dictionary.keys().__contains__(term):
                    value = self.dictionary.get(term)
                    found = False
                    for i in range(len(value)):
                        d, f = value[i]
                        if d == url:
                            self.dictionary.get(term)[i] = (d, f+1)
                            found = True
                    if not found:
                        self.dictionary.get(term).append((url,1))
                else:
                    self.dictionary.update({term: [(url, 1)]})



