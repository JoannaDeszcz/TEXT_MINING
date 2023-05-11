
import csv
import re
import requests
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords
from collections import Counter


# wczytanie danych
with open('tweets_bmw.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dane1 = [row[0] for row in reader]
with open('tweets_audi.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dane2 = [row[0] for row in reader]
# połączenie tekstu
dane = dane1 + dane2

# czyszczenie tekstu
def czysc_tekst(dane):
    temp = re.sub("\s{2,}", " ", dane)
    temp = re.sub('http\S+', '', temp)
    temp = re.sub("(\r\n|\r|\n)", " ", temp) 
    temp = re.sub('\s+', ' ', temp)
    temp = temp.lower() 
    temp = re.sub("rt", "", temp) 
    temp = re.sub("&amp", "", temp) 
    temp = re.sub("#[a-z,A-Z]*", "", temp)
    temp = re.sub("@\w+", "", temp) 
    temp = re.sub("(f|ht)(tp)([^ ]*)", "", temp) 
    temp = re.sub("http(s?)([^ ]*)", "", temp)
    temp = re.sub("[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", " ", temp) 
    temp = re.sub("\d", "", temp) 
    temp = re.sub("\s{2,}", " ", temp) 
    temp = re.sub(":\w+:", "", temp) # usuwanie emotikonów w formacie ":nazwa_emotki:"
    temp = re.sub("<[\/]?[a-z]*>", "", temp)
    temp = re.sub('[^\w\s]|_', '', temp)
    temp = re.sub("[\u3131-\uD79D]","",temp)
    temp = re.sub("\b\w{1,2}\b", '', temp) # usuwanie słów, które nie są słowami
    temp = re.sub("[^\x00-\x7F]+", '', temp)
    temp = re.sub("\b\S{1,3}\b", '', temp)
    temp = re.sub(r"\s+[a-zA-Z]\s+", " ", temp)

    return temp

czysty = [czysc_tekst(el) for el in dane]
print(czysty)
czysty_set = list(set(czysty))

czysty_dict = list(dict.fromkeys(czysty))
czysty=czysty_dict
# Tokenizacja 
tokeny = [re.split("\s", el) for el in czysty]

# Stop lista
stopwords = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an", "and", "any", "are", "as", "at", "be", "because", "been", "but", "by", "can", "cannot", "could", "dear", "did", "do", "does", "either", "else", "ever", "every", "for", "from", "get", "got", "had", "has", "have", "he", "her", "hers", "him", "his", "how", "however", "i", "if", "in", "into", "is", "it", "its", "just", "least", "let", "like", "likely", "may", "me", "might", "most", "must", "my", "neither", "no", "nor", "not", "of", "off", "often", "on", "only", "or", "other", "our", "own", "rather", "said", "say", "says", "she", "should", "since", "so", "some", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "tis", "to", "too", "twas", "us", "wants", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", "yet", "you", "your"]

stopwords = stopwords + ["ya", "yeeeee", "yo", "ummm","ama","amaz","upsa","a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "mi","mr","th","sta","re","dr","tnr","bs","xi","ev","cs","ix","co","ve","bs","ag","sq","eg","xxmm","rr","pre","xm","ac","tr","nj","wd","hey","usb","inc","ah","lsm","ga"]

#streaming
stemmer = SnowballStemmer("english")

termy_bmw = [stemmer.stem(t) for el in tokeny[:len(dane1)] for t in el if t not in stopwords]
termy_audi = [stemmer.stem(t) for el in tokeny[len(dane2):] for t in el if t not in stopwords]

#Zliczanie wystąpień

# termy, które pojawiają się w obu zbiorach jednocześnie
wspolne_termy = set(termy_bmw).intersection(set(termy_audi))

unikaty= list(set(wspolne_termy)) 

# utworzenie słownika z częstością wystąpień poszczególnych termów

bow = {unikat: termy_bmw.count(unikat) + termy_audi.count(unikat) for unikat in unikaty}
# usunięcie termów, które nie pojawiają się w obu zbiorach jednocześnie

czestosci = {k: v for k, v in bow.items() if k in unikaty}

bow_naj = {unikat: liczba for unikat, liczba in bow.items() if liczba >= 2}

bow_naj_sort = {unikat: liczba for unikat, liczba in sorted(bow_naj.items(), key=lambda el: el[1])}

# generowanie chmury słów
wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", width=800, height=800, max_words=50).generate_from_frequencies(bow_naj_sort)

# wyświetlenie chmury słów
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Termy wspólne dla BMW i Audi")
plt.show()




