# YZ ile Çalışma Günlüğü

Bu dosyada **Uçuş Eğitim Kayıt ve Saat Takip Sistemi** geliştirilirken kullanılan beş ana prompt, yapay zekâ yanıtlarının özeti ve bu yanıtlarla ilgili değerlendirmeler yer almaktadır. Her aşamada yapay zekâ tarafından önerilen içerik kontrol edilmiş; uygun bulunan kısımlar kabul edilmiş, gerekli görülen kısımlar düzenlenerek kullanılmıştır.

## Prompt 1 – Problem ve kapsam

**Prompt:**

“Pilotaj eğitimi alan bir öğrenci için Python'un temel konularını gösteren, komut satırında çalışan bir mini uygulama fikri öner. En az üç kullanıcı girdisi, iki karar yapısı, bir döngü, üç fonksiyon, liste veya sözlük ve CSV dosyasına kaydetme koşullarını karşılasın. Gerçek uçuş operasyonlarında kullanılmayacak şekilde eğitim kaydı odaklı olsun.”

**YZ yanıtının özeti:**

Yapay zekâ, uçuş eğitim oturumlarının tarih, eğitim türü, süre ve ders konusu bilgileriyle kaydedildiği bir takip uygulaması önerdi. Uygulamanın komut satırından çalışması ve kayıtları CSV dosyasında saklaması planlandı.

**Karar ve gerekçe:**

Öneri kabul edildi. Seçilen konu pilotaj eğitimiyle doğrudan ilişkiliydi ve ödevde istenen temel Python konularının kullanılmasına imkân veriyordu. Uygulamanın yalnızca eğitim kayıtlarını tutacağı, gerçek uçuş operasyonlarında veya operasyonel kararlarda kullanılmayacağı açıkça belirtildi.

## Prompt 2 – Girdi doğrulama

**Prompt:**

“Python'da tarih, eğitim türü, süre ve ders konusu girdilerini doğrulayan fonksiyonlar yaz. Hatalı girdide program kapanmasın; kullanıcıdan tekrar girdi alsın. Ondalık sürelerde nokta veya virgül kabul edilsin.”

**YZ yanıtının özeti:**

Yapay zekâ, tarih, eğitim türü, süre ve ders konusu için ayrı doğrulama fonksiyonları ile hatalı girişte kullanıcıya yeniden soru soran ortak bir fonksiyon tasarladı.

**Karar ve gerekçe:**

Öneri düzenlenerek kabul edildi. Her girdi için ayrı fonksiyon kullanılması kodun okunabilirliğini ve test edilebilirliğini artırdı. Süre alanı için sıfırdan büyük ve en fazla sekiz saatlik bir uygulama-verisi sınırı belirlendi. Bu sınırın gerçek bir uçuş süresi kuralı veya havacılık mevzuatı olmadığı kodda ve raporda açıklandı. Ondalık sayıların hem nokta hem virgülle girilebilmesi sağlandı.

## Prompt 3 – CSV kaydı

**Prompt:**

“Kayıtları standart kütüphanedeki csv modülüyle UTF-8 bir dosyaya yazan ve program açılırken dosyadan tekrar okuyan fonksiyonları ekle. Dosya yoksa boş listeyle başlasın.”

**YZ yanıtının özeti:**

Yapay zekâ, CSV dosyasını okumak için `csv.DictReader`, dosyaya yazmak için `csv.DictWriter` kullanan fonksiyonlar önerdi. Kayıt dosyası bulunmadığında uygulamanın boş bir kayıt listesiyle başlaması planlandı.

**Karar ve gerekçe:**

Öneri kabul edildi. Kayıtların program kapatıldıktan sonra da saklanabilmesi için CSV dosyası kullanıldı. Ayrıca dosyada bozuk veya geçersiz bir satır bulunmasının diğer geçerli kayıtların okunmasını engellememesi amacıyla satır bazında doğrulama yapıldı.

## Prompt 4 – Test ve hata ayıklama

**Prompt:**

“Bu uygulama için unittest ile en az sekiz test yaz. Geçerli süre, virgül ile ondalık, sıfır, izin verilen aralık dışı süre, geçersiz kategori, boş konu, CSV kaydetme-okuma ve özet hesaplamasını test et.”

**YZ yanıtının özeti:**

Yapay zekâ, girdi doğrulama, CSV dosya işlemleri ve toplam süre hesaplamasını kapsayan birim testleri önerdi. Testlerin `unittest` modülüyle çalıştırılması planlandı.

**Karar ve gerekçe:**

Öneri düzenlenerek kabul edildi. Dosya işlemlerinin test edilmesi sırasında gerçek proje kayıtlarının etkilenmemesi için geçici klasör ve geçici CSV dosyası kullanıldı. İlk test kapsamı daha sonra kayıt ekleme, kayıt silme, hatalı girdiler ve dosya yazma hatası gibi ek durumları da kapsayacak şekilde genişletildi.

## Prompt 5 – Kod inceleme ve sınırlar

**Prompt:**

“Kodu ödev gereksinimlerine göre incele: üç farklı girdi, iki karar yapısı, döngü, üç fonksiyon, liste/sözlük, biçimli ekran çıktısı, TXT/CSV kaydı ve hatalı girdide dayanıklılık. Eksikleri ve operasyonel kullanım açısından yanlış anlaşılabilecek kısımları belirt.”

**YZ yanıtının özeti:**

Yapay zekâ, uygulamanın ödevdeki temel gereksinimlerini kontrol etmeye yönelik bir inceleme sundu. Ayrıca eğitim kayıtları için belirlenen sınırların gerçek uçuş kuralları veya operasyonel kullanım onayı gibi anlaşılmaması gerektiğini vurguladı.

**Karar ve gerekçe:**

Öneri kabul edildi. Uygulamanın eğitim amaçlı olduğu ve gerçek uçuş planlaması, performans hesabı, uçuşa elverişlilik veya operasyonel karar desteği sağlamadığı README dosyasına, rapora ve programın açılış mesajına eklendi. Kodun gereksinimlere uygunluğu testlerle kontrol edildi.

## Yakalanan YZ eksiği ve yapılan son kontroller

İlk taslakta, kullanıcının süreyi `1,5` biçiminde girmesi durumunda Python'un standart `float()` dönüşümünün hata verebileceği gözden kaçabilirdi. Bu durum ayrı bir test senaryosuyla kontrol edildi. `parse_duration()` fonksiyonunda virgül nokta biçimine dönüştürülerek ondalık virgül girişi desteklendi ve ilgili testle doğrulandı.

Ek kontrollerde, `0.001` gibi çok küçük pozitif bir sürenin iki ondalık basamağa yuvarlandığında sıfıra dönüşebileceği fark edildi. Sıfıra yuvarlanan sürelerin kabul edilmemesi sağlandı. CSV dosyasının yazma işlemi sırasında yarım veya bozuk kalma riskini azaltmak için geçici dosyaya yazma ve ardından dosyayı atomik olarak değiştirme yöntemi kullanıldı.

Son olarak, önceki terminal ekran görüntüsündeki menü seçenekleri güncel kodla karşılaştırıldı. Görseldeki menü güncel kodla eşleşmediği için ekran görüntüsü beş seçenekli son menüyü gösterecek şekilde yenilendi.

Bu son kontroller, yukarıdaki beş ana prompttan ayrı yeni bir prompt olarak sayılmamaktadır. Yapay zekâ çıktılarının test edilmesi, hataların belirlenmesi ve uygulamanın son hâlinin doğrulanması sürecini açıklamaktadır.
