import nltk
import spacy
from numpy.core.defchararray import isnumeric
import math
import pandas as pd
from nltk import ngrams
from collections import Counter
from numpy.core.defchararray import isnumeric
#execute on terminal spacy download fr_core_news_md
#spacy.load('fr_core_news_md')
class Cleaner:
    def __init__(self) -> None:
        nltk.download('stopwords')
        self.nlp=spacy.load('fr_core_news_md')
        self.stopwords = nltk.corpus.stopwords.words('french') + nltk.corpus.stopwords.words('english')+['avoir', 'être', 'pourcent', 'plus', 'aussi', 'tout', 'dh', 'milliard', 'autre', 'juin',
                            'entre', 'avril', 'selon', 'deux', 'mmdh', 'via', 'ha', 'dont', 'fois', 'œuvre', 'après',
                            'bien', 'afin', 'depuis', 'mdh', 'article','sous','vers','ainsi','cela','comme','sup','films',
                            'salle','maroc','casablanca','rapport','degré','faire','face','dirham','million','permettre','pouvoir',
                            'horaires','hors','eu','date','year','année','jour','mois','étage','habou','ville','météo','mettre',
                            'place','part','al','maghrib','maghreb','ligne','nouveau','fin','av','tour','fermer','accepter','alaoui',
                            'mehdi','zineb','hicham','nabyl','ryad','temps','afficher','institut','ami','annoncer','ben','bernoussi',
                            'iso','reda','dg','el','mou','abdullah','titre','tenir','contre','mai','économique']

    def is_pertinent_word(self,word):
        if word not in self.stopwords and not isnumeric(word) and word.isalpha() and len(word) > 1:
            return True
        return False
    
    def clean_document(self,document):
        cleaned_document=document
        cleaned_content=""
        for word in self.nlp(cleaned_document["content"]):
            if self.is_pertinent_word(word.lemma_.lower()):
                cleaned_content=cleaned_content+" "+word.lemma_.lower()
        cleaned_document["content"]=cleaned_content
        return cleaned_document

    def clean_documents(self,documents):
        cleaned_documents=[]
        for document in documents:
            cleaned_documents.append(self.clean_document(document))
        return cleaned_documents
