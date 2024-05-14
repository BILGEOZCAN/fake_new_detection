from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import pandas as pd
import csv

tüketici_anahtarı = ""
tüketici_sırrı = ""

erişim_tokenı = ""
erişim_tokenı_sırrı = ""

doğrulama = tweepy.OAuthHandler(tüketici_anahtarı, tüketici_sırrı) 
doğrulama.set_access_token(erişim_tokenı, erişim_tokenı_sırrı)
api = tweepy.API(doğrulama, wait_on_rate_limit=True)

def tweetleri_al(kullanıcı_adı, arama_kelimeleri, tarih_tarihi, tweet_sayısı):
    db_tweetler = pd.DataFrame(columns = ['kullanıcı_adı', 'tweet_oluşturma_tarihi', 'metin', 'etiketler'])


    tweetler = tweepy.Cursor(api.user_timeline, id=kullanıcı_adı, q=arama_kelimeleri, lang="tr", since=tarih_tarihi, tweet_mode='extended').items(tweet_sayısı)
    tweet_listesi = [tweet for tweet in tweetler]

    for tweet in tweet_listesi:
        kullanıcı_adı = tweet.user.screen_name
        tweet_oluşturma_tarihi = tweet.created_at
        etiketler = tweet.entities['hashtags']

        try:
            metin = tweet.retweeted_status.full_text
        except AttributeError:  # Retweet değilse
            metin = tweet.full_text
        
        ith_tweet = [kullanıcı_adı, tweet_oluşturma_tarihi, metin, etiketler]
        db_tweetler.loc[len(db_tweetler)] = ith_tweet
  
    print('Veri çekme işlemi tamamlandı.')
        
    dosya_adı = 'output.csv'
    db_tweetler.to_csv(dosya_adı, index=False)

arama_kelimeleri = "anahtar kelimeler"
tarih_tarihi = "2017-01-01"
tweet_sayısı = 5000
kullanıcı_adı = 'zekiahmetbayar'
tweetleri_al(kullanıcı_adı, arama_kelimeleri, tarih_tarihi, tweet_sayısı)
