from collections import defaultdict
import requests
import bs4 as bs
import re
from nltk.corpus import stopwords

class ScrappingAndIndexing:
    def __init__(self):
        self.urls = []
        self.postings = defaultdict(lambda: defaultdict(int))
        self.tfd = defaultdict(lambda: defaultdict(int))
        self.terms = []
        self.number_of_terms = 0

    def ExtractDocuments(self, url):
        try:
            response = requests.get(url);
            if response.status_code != 200:
                text = ''
            else:
                text = bs.BeautifulSoup(response.content, 'html.parser').text
        except:
            text = ''

        word_tokens = re.split('\W+', text)
        stop_words = set(stopwords.words('english'))
        words = []
        for word in word_tokens:
            if word and word not in stop_words:
                words.append(word.lower())
        
        if len(words) == 0:
            return
        self.urls.append(url)
        
        document_number = len(self.urls)
        
        for word in words:
            if word not in self.terms:
                self.terms.append(word)
                self.number_of_terms += 1
                
            self.tfd[document_number][word] += 1
            doc_list = self.postings[word]
            doc_list[document_number] += 1
            self.postings[word] = doc_list

    def PrintPostings(self):
        for word in self.postings:
            print('Word:', word)
            for document in self.postings[word]:
                print("Document : ",document," Frequency : ",self.postings[word][document])

if __name__ == "__main__":
    
    links = open("Links.txt", 'r').read()
    links=links.split('\n')[:20]
    obj = ScrappingAndIndexing()
    for link in links:
        obj.ExtractDocuments(link)
    obj.PrintPostings()
