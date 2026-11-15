# YZ ile Çalışma Günlüğü

Bu dosyada uygulama geliştirilirken kullanılan beş ana prompt, YZ yanıtlarının özeti ve her yanıtla ilgili kararlar yer almaktadır.

## Prompt 1 – Problem ve kapsam

**Prompt:** “Pilotaj eğitimi alan bir öğrenci için Python'un temel konularını gösteren, komut satırında çalışan bir mini uygulama fikri öner. En az üç kullanıcı girdisi, iki karar yapısı, bir döngü, üç fonksiyon, liste veya sözlük ve CSV dosyasına kaydetme koşullarını karşılasın. Gerçek uçuş operasyonlarında kullanılmayacak şekilde eğitim kaydı odaklı olsun.”

**YZ yanıtının özeti:** Uçuş eğitim oturumlarının tarih, eğitim türü, süre ve ders konusu ile kaydedildiği bir takip uygulaması önerildi.

**Karar:** Kabul edildi. Fikir pilotaj alanıyla ilgili ve ödevin teknik koşullarıyla uyumluydu. Uygulamanın gerçek operasyonel karar aracı olmadığı sınırı eklendi.

## Prompt 2 – Girdi doğrulama

**Prompt:** “Python'da tarih, eğitim türü, süre ve ders konusu girdilerini doğrulayan fonksiyonlar yaz. Hatalı girdide program kapanmasın; kullanıcıdan tekrar girdi alsın. Ondalık sürelerde nokta veya virgül kabul edilsin.”

**YZ yanıtının özeti:** Her girdi türü için ayrı doğrulama fonksiyonları ve tekrar soran ortak bir fonksiyon tasarlandı.

**Karar:** Düzenlenerek kabul edildi. Fonksiyonların ayrı tutulması test yazmayı kolaylaştırdı. Süre için 0'dan büyük ve en fazla 8 saatlik uygulama-verisi sınırı belirlendi; bunun gerçek uçuş limiti olmadığı kod yorumuna ve rapora eklendi.

## Prompt 3 – CSV kaydı

**Prompt:** “Kayıtları standart kütüphanedeki csv modülüyle UTF-8 bir dosyaya yazan ve program açılırken dosyadan tekrar okuyan fonksiyonları ekle. Dosya yoksa boş listeyle başlasın.”

**YZ yanıtının özeti:** `csv.DictReader` ve `csv.DictWriter` kullanan okuma/yazma fonksiyonları oluşturuldu.

**Karar:** Kabul edildi. Bozuk bir CSV satırının diğer geçerli satırların okunmasını engellememesi için satır bazlı doğrulama eklendi.

## Prompt 4 – Test ve hata ayıklama

**Prompt:** “Bu uygulama için unittest ile en az sekiz test yaz. Geçerli süre, virgül ile ondalık, sıfır, izin verilen aralık dışı süre, geçersiz kategori, boş konu, CSV kaydetme-okuma ve özet hesaplamasını test et.”

**YZ yanıtının özeti:** Girdi doğrulama, dosya işlemleri ve özet hesaplamasını kapsayan birim testleri oluşturuldu.

**Karar:** Düzenlenerek kabul edildi. Dosya testi için geçici klasör kullanıldı; testler proje klasöründeki gerçek kayıt dosyasına bağlı kalmadı. Sonraki kontrollerde kayıt ekleme, silme ve hata senaryoları da kapsama alındı.

## Prompt 5 – Kod inceleme ve sınırlar

**Prompt:** “Kodu ödev gereksinimlerine göre incele: üç farklı girdi, iki karar yapısı, döngü, üç fonksiyon, liste/sözlük, biçimli ekran çıktısı, TXT/CSV kaydı ve hatalı girdide dayanıklılık. Eksikleri ve operasyonel kullanım açısından yanlış anlaşılabilecek kısımları belirt.”

**YZ yanıtının özeti:** Uygulama gereksinimlerinin kodda karşılandığı ve uygulama-verisi sınırının gerçek uçuş kuralı gibi sunulmaması gerektiği belirtildi.

**Karar:** Kabul edildi ve güvenli kullanım açıklaması README'ye, rapora ve program açılış ekranına eklendi.

## Prompt 6 – Son tutarlılık ve hata düzeltme

**Prompt:** “Ekran görüntüsünü oluştur ve dosyalardaki tüm hataları düzelt. Python kodu, testler, README, prompt günlüğü ve rapor birbiriyle tutarlı olsun.”

**YZ yanıtının özeti:** Önceki ekran görüntüsünde dört menü seçeneği görünürken güncel kodda beş seçenek bulunduğu saptandı. README'deki eksik silme seçeneği, eksik test/destek dosyaları ve kaynakça biçimi de kontrol edildi.

**Karar:** Düzenlenerek kabul edildi. Ekran görüntüsü son kod gerçek örnek verilerle çalıştırılarak yeniden üretildi; 34 otomatik test, atomik CSV yazımı ve ek uç girdilerle doğrulandı.

## Yakalanan / kontrol edilen olası YZ eksiği

İlk taslaklarda kullanıcı süreyi `1,5` biçiminde yazdığında standart `float()` dönüşümünün hata verebileceği gözden kaçabilirdi. Bu girdi ayrı bir test olarak ele alındı; `parse_duration()` fonksiyonuna virgül-nokta normalizasyonu eklendi ve `test_decimal_comma_is_supported` testiyle kontrol edildi. Ayrıca önceki örnek terminal görselindeki menü dört seçenek gösterirken son kodda beş seçenek bulunuyordu. Ekran görüntüsü son kod çalıştırılarak yeniden üretildi. Sürenin 0.001 gibi bir değerle girilmesi durumunda iki ondalığa yuvarlandığında sıfır üretmesi de ek bir uç durum olarak ele alındı; sıfıra yuvarlanan süreler reddedildi. CSV dosyasının yazma sırasında bozulmasını önlemek için geçici dosya ve atomik değiştirme yöntemi kullanıldı.
