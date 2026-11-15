# Test Senaryoları

Testler `python -m unittest discover -s tests -v` komutuyla çalıştırılır. Otomatik testler geçici dosyalar kullanır; proje klasöründeki gerçek kullanıcı CSV dosyasını değiştirmez.

| # | Girdi / işlem | Beklenen sonuç | Test sonucu |
|---:|---|---|---|
| 1 | Tarih 2026-11-14, tür 1, süre 1.5, konu Traffic pattern | Kayıt oluşturulur ve CSV’ye yazılır | Başarılı |
| 2 | Süre 1,5 | Virgül ondalık ayırıcı olarak kabul edilir; sonuç 1.5 olur | Başarılı |
| 3 | Hatalı tarih 14-11-2026 | Tarih reddedilir | Başarılı |
| 4 | İmkânsız tarih 2026-02-30 | Tarih reddedilir | Başarılı |
| 5 | Süre 0 veya -1 | Süre reddedilir | Başarılı |
| 6 | Süre 8.1 | Uygulama veri giriş sınırını aştığı için reddedilir | Başarılı |
| 7 | Süre nan veya inf | Sonlu olmayan sayısal değer reddedilir | Başarılı |
| 8 | Süre 0.001 | 0.01 saate yuvarlanıp sıfır olacağı için reddedilir | Başarılı |
| 9 | Eğitim türü 9 | Geçersiz kategori reddedilir | Başarılı |
| 10 | Boş veya 80 karakterden uzun konu | Konu doğrulaması reddeder | Başarılı |
| 11 | CSV kaydet ve yeniden yükle | Dört alan aynı değerlerle okunur | Başarılı |
| 12 | Bozuk CSV satırı ve geçerli CSV satırı birlikte | Bozuk satır atlanır, geçerli satır okunur | Başarılı |
| 13 | Silme: geçerli sıra + E | Kayıt bellek listesinden ve CSV’den silinir | Başarılı |
| 14 | Silme: geçerli sıra + H | Kayıt korunur | Başarılı |
| 15 | Silme: metin/geçersiz sıra, ardından 0 | Yeniden sorulur ve silme iptal edilir | Başarılı |
| 16 | Silme onayı için geçersiz yanıt, ardından H | Geçersiz yanıt reddedilir; tekrar sorulur | Başarılı |
| 17 | Dosyaya ekleme veya silme sırasında yazma hatası | Bellek listesi eski durumuna döner | Başarılı |
| 18 | CSV kaydında atomik değiştirme hatası | Önceki CSV dosyası korunur; geçici dosya temizlenir | Başarılı |
| 19 | Menüde geçersiz seçim, ardından 5 | Uyarı gösterilir ve çıkış yapılır | Başarılı |

## Testlerin yorumu

Testler geçerli girdilerin yanı sıra hatalı ve uç girdileri de kapsar. Kayıt dosyası önce geçici dosyaya yazılır ve başarıyla tamamlanınca atomik biçimde hedef dosyanın yerine geçirilir. Yazma/değiştirme hatası oluşursa önceki CSV korunur ve bellekteki liste eski durumuna döndürülür.
