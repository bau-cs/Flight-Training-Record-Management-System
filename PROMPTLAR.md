# YZ ile Calisma Gunlugu - Prompt Taslagi

> **Ogrenci notu:** Asagidaki kayitlar bu projenin gelistirme adimlarini belgelemek icin hazirlanmis ornek prompt gunlugudur. Teslimden once, kendi gercek ChatGPT/Claude oturumunuzdaki promptlari ve aldiginiz cevaplari kontrol ederek metni kendi surecinize gore duzenleyin. Kullanmadiginiz bir promptu gercekten kullanmis gibi gostermeyin.

## Prompt 1 - Problem ve kapsam

**Prompt:** "Pilotaj egitimi alan bir ogrenci icin Python'un temel konularini gosteren, komut satirinda calisan bir mini uygulama fikri oner. En az uc kullanici girdisi, iki karar yapisi, bir dongu, uc fonksiyon, liste veya sozluk ve CSV dosyasina kaydetme kosullarini karsilasin. Gercek ucus operasyonlarinda kullanilmayacak sekilde egitim kaydi odakli olsun."

**YZ yanitinin ozeti:** Ucus egitim oturumlarinin tarih, egitim turu, sure ve ders konusu ile kaydedildigi bir takip uygulamasi onerildi.

**Karar:** Kabul edildi. Fikir, pilotaj alaniyla ilgili ve odevin teknik kosullariyla uyumluydu. Uygulamanin gercek operasyonel karar araci olmadigi siniri eklendi.

## Prompt 2 - Girdi dogrulama

**Prompt:** "Python'da tarih, egitim turu, sure ve ders konusu girdilerini dogrulayan fonksiyonlar yaz. Hatali girdide program kapanmasin; kullanicidan tekrar girdi alsin. Ondalik surelerde nokta veya virgul kabul edilsin."

**YZ yanitinin ozeti:** Her girdi turu icin ayri dogrulama fonksiyonu ve tekrar soran ortak bir fonksiyon tasarlandi.

**Karar:** Duzenlenerek kabul edildi. Fonksiyonlarin ayri tutulmasi test yazmayi kolaylastirdi. Sure icin 0'dan buyuk ve en fazla 8 saatlik uygulama-verisi siniri belirlendi; bunun gercek ucus limiti olmadigi kod yorumuna eklendi.

## Prompt 3 - CSV kaydi

**Prompt:** "Kayitlari standart kutuphanedeki csv moduluyle UTF-8 bir dosyaya yazan ve program acilirken dosyadan tekrar okuyan fonksiyonlari ekle. Dosya yoksa bos listeyle baslasin."

**YZ yanitinin ozeti:** `csv.DictReader` ve `csv.DictWriter` kullanan okuma/yazma fonksiyonlari olusturuldu.

**Karar:** Kabul edildi. Buna ek olarak bozuk bir CSV satirinin diger gecerli satirlarin okunmasini engellememesi icin satir bazli dogrulama eklendi.

## Prompt 4 - Test ve hata ayiklama

**Prompt:** "Bu uygulama icin unittest ile en az sekiz test yaz. Gecerli sure, virgul ile ondalik, sifir, izin verilen aralik disi sure, gecersiz kategori, bos konu, CSV kaydetme-okuma ve ozet hesaplamasini test et."

**YZ yanitinin ozeti:** Girdi dogrulama, dosya islemleri ve ozet hesaplamasini kapsayan birim testleri olusturuldu.

**Karar:** Duzenlenerek kabul edildi. Dosya testi icin gecici klasor kullanildi; boylece testler proje klasorundeki gercek kayit dosyasina bagimli olmadi.

## Prompt 5 - Kod inceleme ve sinirlar

**Prompt:** "Kodu odev gereksinimlerine gore incele: uc farkli girdi, iki karar yapisi, dongu, uc fonksiyon, liste/sozluk, bicimli ekran ciktisi, TXT/CSV kaydi ve hatali girdide dayaniklilik. Eksikleri ve operasyonel kullanim acisindan yanlis anlasilabilecek kisimlari belirt."

**YZ yanitinin ozeti:** Uygulama gereksinimlerinin kodda karsilandigi kontrol edildi; uygulama-verisi sinirinin gercek ucus kurali gibi sunulmamasi gerektigi belirtildi.

**Karar:** Kabul edildi ve guvenli kullanim aciklamasi README'ye, rapora ve program acilis ekranina eklendi.

## Yakalanan / kontrol edilen olasi YZ eksigi

Ilk taslaklarda kullanici sureyi `1,5` biciminde yazdiginda standart `float()` donusumunun hata verebilecegi gozden kacabilirdi. Kod calistirilirken bu girdi ayri bir test olarak ele alindi; `parse_duration()` fonksiyonuna virgul-nokta normalizasyonu eklendi ve `test_decimal_comma_is_supported` testiyle kontrol edildi. Boylece yalnizca YZ ciktisini kabul etmek yerine davranis testle dogrulandi.
