import string
import numpy
import sys


def bubble_sort(A, B, C):

    swapped = True
    while swapped:
        swapped = False
        for i in range(len(A) - 1):
            if A[i] < A[i + 1]:

                A[i], A[i + 1] = A[i + 1], A[i]
                B[i], B[i + 1] = B[i + 1], B[i]
                C[i], C[i + 1] = C[i + 1], C[i]

                swapped = True

class Indexer:

    def __init__(self):
        self.dictionary = dict()
        self.pages = dict()

    def get_clean_terms(self, text):
        clean_text = text.replace(". ", " ")
        clean_text = clean_text.replace(", ", " ")
        signs = "?!@#$%^&*()-_=+"
        for char in signs:
            clean_text = clean_text.replace(char, "")
        clean_text = clean_text.replace("  ", " ")
        clean_text = clean_text.replace('"', "")
        clean_text = clean_text.replace("'", "")

        terms = clean_text.split(" ")
        return terms

    def update(self, title, url, text):
        if self.pages.keys().__contains__(url):
            print("Page: " + url + " is already indexed")
        else:
            terms = self.get_clean_terms(text)
            self.pages.update({url: (title, len(terms))})

            for term in terms:
                if term[len(term) - 1] == '.':
                    term = term[:-1]
                if self.dictionary.keys().__contains__(term.lower()):
                    value = self.dictionary.get(term.lower())
                    found = False
                    for i in range(len(value)):
                        d, f = value[i]
                        if d == url:
                            self.dictionary.get(term.lower())[i] = (d, f+1)
                            found = True
                    if not found:
                        self.dictionary.get(term.lower()).append((url, 1))
                else:
                    self.dictionary.update({term.lower(): [(url, 1)]})

    def top_k(self, k, q):
        N = len(self.pages.keys())
        S = dict()
        terms = self.get_clean_terms(q)
        for term in terms:
            if term == '':
                continue

            if term[len(term) - 1] == '.':
                term = term[:-1]

            if self.dictionary.keys().__contains__(term.lower()):
                n = len(self.dictionary.get(term.lower()))
                idf = numpy.log(1 + N/n)
                for pair in self.dictionary.get(term.lower()):
                    d, f = pair
                    if not S.keys().__contains__(d):
                        S.update({d: 0})
                    tf = 1 + numpy.log(f)
                    S[d] = S[d] + tf * idf
        titles = []
        for d in S.keys():
            t, l = self.pages.get(d)
            S[d] = S[d] / l
            titles.append(t)
        urls = []
        scores = []
        for i in S.keys():
            urls.append(i)
            scores.append(S.get(i))
        bubble_sort(scores, urls, titles)
        for i in range(k):
            try:
                print("Page " + str(i+1) + ": " + titles[i] + " - " + urls[i])

            except IndexError:
                print("No more results..")
                break

#paradeigmataki

i = Indexer()
i.update("MALAKAS","www.malakas.gr", "When I was a young boy, my father took me into the city, to see a marching band!")
i.update("MALAKAS2", "www.malakas2.gr", "He said 'son, when you grow up, would you be the saviour of the broken, the beaten and the damned'")
i.top_k(int(sys.argv[1]), sys.argv[2])



