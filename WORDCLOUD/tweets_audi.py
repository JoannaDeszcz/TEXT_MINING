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

with open('tweets_audi.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dane = [row for row in reader]

dane1 = [element for podlista in dane for element in podlista]

def czysc_tekst(dane1):
    
    temp = re.sub("\s{2,}", " ", dane1)
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
    temp = re.sub(r"\s+[a-zA-Z]\s+", " ", temp)
    temp = re.sub(r'\b\w\b', '', temp)

    return temp

czysty = [czysc_tekst(el) for el in dane1]

czysty_set = list(set(czysty))

czysty_dict = list(dict.fromkeys(czysty))
czysty=czysty_dict

#Tokenizacja 
tokeny = [re.split("\s", el) for el in czysty]

#Stop lista
stopwords = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an", "and", "any", "are", "as", "at", "be", "because", "been", "but", "by", "can", "cannot", "could", "dear", "did", "do", "does", "either", "else", "ever", "every", "for", "from", "get", "got", "had", "has", "have", "he", "her", "hers", "him", "his", "how", "however", "i", "if", "in", "into", "is", "it", "its", "just", "least", "let", "like", "likely", "may", "me", "might", "most", "must", "my", "neither", "no", "nor", "not", "of", "off", "often", "on", "only", "or", "other", "our", "own", "rather", "said", "say", "says", "she", "should", "since", "so", "some", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "tis", "to", "too", "twas", "us", "wants", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", "yet", "you", "your"]

sciezka = "https://www.textfixer.com/tutorials/common-english-words.txt"

response = requests.get(sciezka)
stopwords = response.text.split(",")

# stopwords

termy = [[t for t in el if t not in stopwords] for el in tokeny]

#streaming


stemmer = SnowballStemmer("english")


termy_stem = [[stemmer.stem(t) for t in el] for el in termy]


#Zliczanie wystąpień

termy = [term for el in termy_stem for term in el] #wszystkie unikatowe

unikaty = list(set(termy)) # tylko raz

print(f'Wszystkich termów jest {len(termy)} ale unikatowych jest {len(unikaty)}')

bow = {unikat: termy.count(unikat) for unikat in unikaty} #liczba wystąpień
bow_naj = {unikat: liczba for unikat, liczba in bow.items() if liczba >= 2} #co najmniej 2 razy

bow_naj_sort = {unikat: liczba for unikat, liczba in sorted(bow_naj.items(), key=lambda el: el[1])} #, reverse = True
print(bow_naj_sort)

#Wizualizacja

plt.barh(range(len(bow_naj_sort)), bow_naj_sort.values(), align='center')
plt.yticks(range(len(bow_naj_sort)), list(bow_naj_sort.keys()))


# Utwórz obiekt WordCloud
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=STOPWORDS,max_words=50).generate_from_frequencies(bow_naj_sort)

# Wyświetl chmurę słów
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Audi")
plt.tight_layout(pad=0)
plt.show()

#-----------------------------------------------------------------------


