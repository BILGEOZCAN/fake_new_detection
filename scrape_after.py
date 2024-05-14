from string import digits
from trnlp import TrnlpWord
from trnlp import SpellingCorrector
import pandas as pd 
import csv,os,string,re
import logging
import emoji

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('log')
handler.setLevel(logging.DEBUG)

# logging format oluşturun
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# handler’i logger a kaydedin
logger.addHandler(handler)

getbase_kelime = TrnlpWord()
duzeltici = SpellingCorrector()

durdur_kelimeler = [  "bana", "bazı", "belki", "ben", "beni", "benim", "beri", "bile", "bir", "birçok",
    "biri", "birkaç", "biz", "bize", "bizi", "bizim","böyle", "böylece", "bu","buna", "bundan", "bunlar", "bunları", "bunların", 
    "bunu", "bunun", "burada", "çok", "çünkü", "da", "daha", "de","değildir","diğer", "diye", "dolayı", "dolayısıyla", "edecek", 
    "eden", "ederek", "edilmesi", "arada", "ama", "ancak","ayrıca","ediyor", "eğer", "etmesi", "etti", "ettiği", "ettiğini", "gibi","göre", 
    "halen", "hangi", "hatta", "hem", "henüz", "her", "herhangi", "herkesin", "hiç", "hiçbir", "için", "ile", "ilgili", "ise", "işte",
    "itibaren", "itibariyle", "kadar", "karşın", "kendi", "kendilerine", "kendini", "kendisi", "kendisine", "kendisini", "ki",
    "kim", "kimse", "mı", "mi",  "edilecek", "ediliyor","mu", "mü", "nasıl", "ne", "neden", "nedenle", "o", "olan", "olarak", "oldu", "olduğu", 
    "olduğunu", "olduklarını", "olmadı", "olmadığını", "olmak", "olması", "olmayan", "olmaz", "olsa", "olsun", "olup", "olur",
    "olursa", "oluyor", "ona", "onlar", "onları", "onların", "onu", "onun", "öyle", "oysa", "pek", "rağmen", "sadece", "siz",
    "şey", "şöyle", "şu", "şunları", "tarafından", "üzere", "var", "vardı", "ve", "veya", "ya", "yani", "yapacak", "yapılan",
    "yapılması", "yapıyor", "yapmak", "yaptı", "yaptığı", "yaptığını", "yaptıkları", "yerine", "yine", "yoksa", "zaten"]

def main():
    metin_sutununu_sec('cikti')
    anahtar_kelimeleri_ara()
    veriyi_temizle('cikti','son')

def metin_sutununu_sec(csv_adi):
    logger.info('Tweet dosyası okunuyor...')
    df = pd.read_csv(str(csv_adi)+'.csv')

    logger.info('Metin sütunu seçiliyor...')
    tweetler = df.loc[:, "metin"]

    logger.info('Seçilen sütun dosyaya yazılıyor...')
    dosya_adi = 'cikti.csv'
    tweetler.to_csv(dosya_adi, index = False)

def anahtar_kelimeleri_ara():
    tweetler = list()
    temiz_tweetler = list()

    logger.info('Anahtar kelime araması için dosya okunuyor...')
    with open('cikti.csv') as temiz_tweetler:
        tweetler = temiz_tweetler.readlines()
        anahtar_kelime_listesi = ["recep", "tayyip", "erdoğan", "akp", "bakan", "albayrak",
                        "siyaset", "siyasi", "meclis", "milletvekili", "mv.",
                        "saray"]

        logger.info('Anahtar kelime içeren tweetler ayrılıyor...')
        for i in tweetler:
            for j in anahtar_kelime_listesi:
                if j in i.lower():
                    temiz_tweetler.append(i)
    
    logger.info('Anahtar kelime içeren tweetler dosyaya yazılıyor...')
    with open('cikti.csv','w') as yeni:
        for i in range(len(temiz_tweetler)):
            yeni.write(temiz_tweetler[i])

def emojiyi_kaldir(text):
    yeni_metin = re.sub(emoji.get_emoji_regexp(), r"", text)
    return yeni_metin

def temel_kelimeyi_al(text):
    kelimeler = list()
    yeni_metin = " "
    kelimeler = text.split()
    
    for i in range(0,len(kelimeler)):
        
        getbase_kelime.setword(kelimeler[i])
        gecici = kelimeler[i]
        kelimeler[i] = getbase_kelime.get_base 
        if kelimeler[i] == '':
            kelimeler[i] = gecici
    
    return yeni_metin.join(kelimeler) + '\n'

def duzeltileni_al(text):
    kelimeler = list()
    dogru_kelimeler = list()
    yeni_metin = " "
    kelimeler = text.split()

    for i in range(0,len(kelimeler)):
        duzeltici.settext(kelimeler[i])
        dogru_kelimeler = duzeltici.correction(deasciifier=True)
        kelimeler[i] = dogru_kelimeler[0][0]
    
    return yeni_metin.join(kelimeler) + '\n'

def veriyi_temizle(girdi,cikti):
    with open(girdi + '.csv') as tweetler_dosyasi:
        tweetler_listesi = list()
        tweetler_listesi = tweetler_dosyasi.readlines()
        for i in range(0,len(tweetler_listesi)):

            logger.info('Linkler temizleniyor...')
            unlink = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweetler_listesi[i])
            tweetler_listesi[i] = unlink # Linkleri temizler.

            logger.info('Rakamlar temizleniyor...')
            remove_digits = str.maketrans('', '', digits)
            tweetler_listesi[i] = tweetler_listesi[i].translate(remove_digits) # Rakamları temizler

            logger.info('Noktalama işaretleri metinden çıkarılıyor...')
            tweetler_listesi[i] = tweetler_listesi[i].translate(str.maketrans('', '', string.punctuation)) # Noktalama işaretlerini temizler.

            logger.info('N karakterden az kelimeler siliniyor...')
            shortword = re.compile(r'\W*\b\w{1,3}\b')
            tweetler_listesi[i] = shortword.sub('', tweetler_listesi[i]) # N karakterden az kelimeleri temizler
            tweetler_listesi[i] = tweetler_listesi[i].lower()
            
            logger.info('Özel durumlar metinlerden siliniyor...')
            tweetler_listesi[i] = tweetler_listesi[i].replace('•', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('❞', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('❝', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('fotohaber', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('sporhaber', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('son', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('dakika', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('’', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('₺', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('”', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('“', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace('✘', '')
            tweetler_listesi[i] = tweetler_listesi[i].replace("'", '')
            
            logger.info('Emojiler metinlerden siliniyor...')
            tweetler_listesi[i] = emojiyi_kaldir(tweetler_listesi[i])

            logger.info('Yanlış yazılan kelimeler düzeltiliyor...')
            tweetler_listesi[i] = duzeltileni_al(tweetler_listesi[i])

            logger.info('Kelimeler köklerine ayrılıyor...')
            tweetler_listesi[i] = temel_kelimeyi_al(tweetler_listesi[i])
            tweetler_listesi[i] = tweetler_listesi[i].lower()
            tweetler_listesi[i] = tweetler_listesi[i].replace('i̇', 'i')
            tweetler_listesi[i] = tweetler_listesi[i].replace("'", '')

        logger.info('Durak kelimeler metinden çıkarılıyor...')
        for i in tweetler_listesi:
            for j in durdur_kelimeler:
                if i == j:
                    index = tweetler_listesi.index(i)
                    tweetler_listesi.pop(index)

        print("İşlem başarıyla tamamlandı.\nToplam veri sayısı : {} ".format(len(tweetler_listesi)))

        logger.info('Temizlenmiş metin dosyaya yazılıyor...')
        with open(cikti + '.csv','w') as yeni_tweetler_dosyasi:
            for i in range(len(tweetler_listesi)):
                yeni_tweetler_dosyasi.write(tweetler_listesi[i])
        
main()
