import pickle
import pandas as pd
import numpy as np

from trnlp import TrnlpWord
from trnlp import SpellingCorrector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

adım0_doğruluk = 0
adım1_doğruluk = 0

getbase_word = TrnlpWord()
corrector = SpellingCorrector()

def temel_kelimeyi_al(metin):
    kelimeler = list()
    ret_metin = " "
    kelimeler = metin.split()
    
    for i in range(0,len(kelimeler)):
        
        getbase_word.setword(kelimeler[i])
        temp = kelimeler[i]
        kelimeler[i] = getbase_word.get_base 
        if kelimeler[i] == '':
            kelimeler[i] = temp
    
    return ret_metin.join(kelimeler) + '\n'

def duzeltileni_al(metin):
    kelimeler = list()
    gerçek_kelimeler = list()
    ret_metin = " "
    kelimeler = metin.split()

    for i in range(0,len(kelimeler)):
        corrector.settext(kelimeler[i])
        gerçek_kelimeler = corrector.correction(deasciifier=True)
        kelimeler[i] = gerçek_kelimeler[0][0]
    
    return ret_metin.join(kelimeler) + '\n'

def rastgele_orman(data_yolu, test_verisi, adım):
    veri = pd.read_csv(data_yolu, header=None, dtype=str)
    
    veri['Etiket'] = veri[1] # Etiket sütununu seç.
    veri.drop([1], axis=1, inplace=True)

    tweetler = np.array(veri.drop(['Etiket'], axis=1), dtype='<U13') # Metinlerin sütununu al
    tweet_etiketleri = np.array(veri['Etiket']) # Etiket sütununu al

    tweetler = tweetler[1:] # Başlıkları sil
    tweet_etiketleri = tweet_etiketleri[1:] # Başlıkları sil

    kf = kf = KFold(n_splits=2)
    kf.get_n_splits(tweetler)
    tweet_etiketleri = list(map(int, tweet_etiketleri)) # Etiket değerlerini integer'a çevir ve list haline getir

    # tweetler_Eğitim > Öğrenme verisi
    # tweetler_Test > Test verisi
    # etiket_Eğitim > Öğrenme verisi ETİKET
    # etiket_Test > Test verisi ETİKET

    tweetler_Eğitim, tweetler_Test, etiket_Eğitim, etiket_Test = train_test_split(tweetler, tweet_etiketleri,test_size=0.30, random_state= 100)
    
    tweetler_Eğitim = list(tweetler_Eğitim) # Eğitim verisi list haline geldi
    temiz_tweetler_Eğitim = list()
    for eğitim_tweet in tweetler_Eğitim:
        for eğitim_tweet2 in eğitim_tweet:
            temiz_tweetler_Eğitim.append(eğitim_tweet2) # Asıl verileri alır
            
    tweetler_Test = list(tweetler_Test)
    temiz_tweetler_Test = list()
    for test_tweet in tweetler_Test:
        for test_tweet2 in test_tweet:
            temiz_tweetler_Test.append(test_tweet2) # Asıl verileri alır
            
    say_vect = CountVectorizer(lowercase=False)
    tweet_eğitim_sayıları = say_vect.fit_transform(temiz_tweetler_Eğitim)
    tweet_test_sayıları = say_vect.transform(temiz_tweetler_Test)

    test_girişi = test_verisi
    test_girişi_sayı = say_vect.transform(test_girişi)

    rastgele_ormanModeli = RandomForestClassifier()
    rastgele_ormanModeli.fit(tweet_eğitim_sayıları, etiket_Eğitim) # Öğrenme aşaması
    etiket_tahmini = rastgele_ormanModeli.predict(tweet_test_sayıları) # Test verisi

    test_sonuç_1 = rastgele_ormanModeli.predict(test_girişi_sayı) # Test verisi
    doğruluk = accuracy_score(etiket_Test, etiket_tahmini) # Karşılaştır

    if adım == 0:
        global adım0_doğruluk 
        adım0_doğruluk = float("{0:.2f}".format(doğruluk*100))
    
    if adım == 1:
        global adım1_doğruluk
        adım1_doğruluk = float("{0:.2f}".format(doğruluk*100))

    dosya_adı = 'finalized_model.sav'
    pickle.dump(rastgele_ormanModeli, open(dosya_adı, 'wb'))

    return test_sonuç_1

kullanıcı_girişi =  input('Veri seti doğruluk oranlarını görmek için 0, Haberinizi test etmek için 1 tuşlaması yapınız!\nSeçiminiz: ')

if kullanıcı_girişi == '1':
    kullanıcı_yeni = input('Test haberi giriniz!\nHaber: ')
    kullanıcı_yeni = duzeltileni_al(kullanıcı_yeni)
    print('Mesajın doğrulaştırılmış hali: ' + kullanıcı_yeni)
    kullanıcı_yeni = temel_kelimeyi_al(kullanıcı_yeni)
    print('Mesajın köklerine ayrılmış hali: ' + kullanıcı_yeni)
    kullanıcı_yeni = kullanıcı_yeni.lower()
    print('Mesajın tekrar küçük harfe dönüştürülmüş hali: ' + kullanıcı_yeni)
    test_verisi_listesi = [kullanıcı_yeni]
    sonuç = rastgele_orman('data.csv', test_verisi_listesi, 0)

    if sonuç == 0:
        sahte_sonuç = rastgele_orman('fakedata.csv', test_verisi_listesi, 1)

        if sahte_sonuç == 0:
            print('Karar: Bilinçsiz Yanlış!')

        if sahte_sonuç == 1:
            print('Karar: Bilinçli Yanlış!')
            
    else:
        sahte_sonuç = rastgele_orman('fakedata.csv', test_verisi_listesi, 1)
        print('Karar: Haber doğru!')

if kullanıcı_girişi == '0':
    test_verisi_listesi = ['']
    sıfır_giriş = rastgele_orman('data.csv', test_verisi_listesi, 0)
    print('Doğru/Yanlış haber ayırt etme doğruluğu: {} '.format(adım0_doğruluk))

    test_verisi_listesi = ['']
    sıfır_giriş = rastgele_orman('fakedata.csv', test_verisi_listesi, 1)
    print('Bilinçli/Bilinçsiz haber ayırt etme doğruluğu: {} '.format(adım1_doğruluk))

if kullanıcı_girişi == 'q':
    exit 
