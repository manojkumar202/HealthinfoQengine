from math import log
import nltk
from nltk.corpus import stopwords
import re
from phase_1 import ScrappingAndIndexing
import math
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup 

class QueryRanking:
    def __init__(self):
        self.Documents={}
        self.links = open("Links.txt", 'r').read()
        self.links=self.links.split('\n')[:20]
        self.obj = ScrappingAndIndexing()
        self.urltitle={}
        c=1
        
        for link in self.links:
            try:
                self.Documents[c]=link
                hdr = {'User-Agent': 'Mozilla/5.0'}
                req = Request(link,headers=hdr)
                page = urlopen(req)
                title =BeautifulSoup(page,features="lxml").title.get_text()
                self.urltitle[link]=title
                self.obj.ExtractDocuments(link)
                c=c+1
            except:
                print()
    
        self.Document_vectors=self.CreateDocumentVector(self.obj,self.links)
    def ImprovedSqrtCosineSimilarity(self,query,doc):
        dot_product=0
        norm_query=0
        norm_doc=0
        for i in range(len(query)):
            #print(query[i],'     *****    ',doc[i])
            dot_product=dot_product+math.sqrt(query[i]*doc[i])
            norm_query=norm_query+query[i]
            norm_doc=norm_doc+doc[i]
        if norm_doc==0 or norm_query==0:
            return 0
        denominator=(norm_query**0.5)*(norm_doc**0.5)
        return dot_product/denominator
    
    def VectorBasedRanking(self,query_vector):
        out=[]
        n_doc=len(self.links)
        for doc in range(n_doc):
            #print('Document : ',doc)
            sim=self.ImprovedSqrtCosineSimilarity(query_vector,self.Document_vectors[doc+1])
            out.append((sim,doc+1))
        out.sort(reverse=True)
        return out
    
    def CreateDocumentVector(self,obj,links):
        d_dict={}
        print('Creatdoc')
        for doc in range(len(links)):
            vector_list=[]
            for term in obj.terms:
                term_frequency=obj.tfd[doc+1][term]
                dft =len(obj.postings[term])
                vector_list.append( term_frequency * log(len(links) / dft ))
            d_dict[doc+1]=vector_list
        return d_dict
        
    def CreateQueryVetor(self,query):
        word_tokens = re.split('\W+', query)
        stop_words = set(stopwords.words('english'))
        words = []
        for word in word_tokens:
            if word and word not in stop_words:
                words.append(word.lower())
        query=words
        query_vector=[]
        for term in self.obj.terms:
            term_frequency=query.count(term)
            dft =len(self.obj.postings[term])
            if term_frequency==0:
                query_vector.append(0)
            else:
                query_vector.append( term_frequency * log(len(self.links)/dft))
        return query_vector
    
    def AppRanking(self,query):
    
        #query="healthy foods weight loss"
        query_vector=self.CreateQueryVetor(query)
        rank=self.VectorBasedRanking(query_vector)
        front_output=[]
        for i in range(len(rank)):
            #print("Rank:",i+1,"\tDocument url:",Documents[rank[i][1]])
            if rank[i][0]!=0:
                front_output.append([str(i+1) +'.\t'  +self.urltitle[self.Documents[rank[i][1]]],self.Documents[rank[i][1]]])
            
        return front_output
    
    
    