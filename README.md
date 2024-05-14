# fake_new_detection
 sahte haber tespiti
Sistemin gerçeklenmesi için gerekli olan iç politika, veri toplanacağı platform olarak Twitter, toplama zamanını ise ülkemizin iç siyasetinin ekonomik şartlar ve yönetim biçimlerindeki değişkenlikleri dikkate alarak 2020'nin başından günümüze kadar belirlendi.

Algoritmanın entegrasyonu sağlandı ve 2.159 haberle veri seti %75 öğrenme, %25 test verisi olarak ayrıldı.

B. Yazılımın Kullanımı:

Yazılım 3 modülden oluşur ve kullanılabilirliği artırmak için modüller içinde metodlara ayrılmıştır:

scraper.py: Veri çekmek için tasarlanmıştır. Kullanıcıdan anahtar kelime, hashtag veya kullanıcı adı, verilerin toplanacağı başlangıç tarihi ve toplanacak tweet sayısı alır. Çıktı olarak belirtilen sayıda tweet içeren bir .csv dosyası verir.

after_scrape.py: Ham veriyi alır ve NLP teknikleriyle işleyerek sonraki aşamaya hazır hale getirir.

random_forest.py: İşlenmiş veriyi alarak kullanıcının isteğine göre yeni bir haberin doğruluğunu test eder. Opsiyonel olarak veri kümesine ait doğruluk değerlerini döndürebilir.

Her modülün görevleri açıklandıktan sonra kullanım aşaması daha rahat anlaşılabilir.

scraper.py kullanımı için Twitter API erişim izni gereklidir. API erişimi için Twitter Developer programına katılınmalı, bir proje oluşturulmalı ve proje için secret/consumer_key ve secret/access_token bilgileri edinilmelidir.

scraper.py dosyasında belirtilen fonksiyonu çağırmak için gerekli parametreler verilmelidir:

• search_words = "anahtar_kelime1 OR anahtar_kelime2 OR ..."
• date_since = '2020-01-01'
• numTweets = 5000
• numRuns = 1
• username = 'kullanıcı_adı'

Parametreler belirlendikten sonra fonksiyon çağrılmalıdır.

after_scrape.py modülü herhangi bir parametre ayarı gerektirmez. Çalıştırıldığında final.csv adında temizlenmiş veriyi içeren bir .csv dosyası oluşturur.

random_forest.py dosyası için de herhangi bir parametre ayarı yapılmasına gerek yoktur. Çalıştırıldığında kullanıcı tercihlerine göre yönetilerek çıktılar verir.