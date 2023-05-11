import snscrape.modules.twitter as sntwitter
import re
import csv

tweets_cocacola = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('#colacola lang:en').get_items()):
    if i >= 1000:
        break
    text = tweet.content.replace('\n', ' ') # usuwanie znaków nowej linii
    text = text.replace('\r', ' ') # usuwanie znaków powrotu karetki
    tweets_cocacola.append(text)

# Wyświetlenie listy tweetów w oczekiwanej formie


tweet_count = len(tweets_cocacola)
if tweet_count == 1000:
    print("Pobrano 1000 tweetów.")
else:
    print(f"Pobrano {tweet_count} tweetów, zamiast 1000.")


# Otwarcie pliku CSV w trybie zapisu


with open('tweets_cocacola1.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)