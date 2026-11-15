# Uçuş Eğitim Kayıt ve Saat Takip Sistemi

**Ders:** GEP1316 Kodlama Okuryazarlığı

**Ödev:** Ara Değerlendirme Ödevi 1

**Öğrenci:** Hüseyin Can Sevinç

## 1. Proje ne yapar?

Bu komut satiri uygulamasi, pilotaj egitimi sirasinda yapilan egitim oturumlarini kaydetmek ve toplam sureleri takip etmek icin hazirlanmistir. Her kayitta tarih (`date`), egitim turu (`duration`), saat degeri (`hours`) ve ders konusu (`topic`) tutulur. CSV dosyasinda bu dort alan ayri sutunlarda saklanir: `date,duration,hours,topic`. `duration` Dual Flight, Solo Flight veya Simulator degerini; `hours` sayisal sureyi tutar. Kayitlar CSV dosyasina yazilir; program yeniden acildiginda dosyadan okunur.

> **Onemli sinir:** Bu proje yalnizca ders/egitim kaydi ve Python programlama calismasi icindir. Gercek ucus planlamasi, yakit/performans hesabi, ucus izni, ucusa elverislilik veya operasyonel kararlar icin kullanilamaz.

## 2. Odev gereksinimleriyle eslesme

| Odev gereksinimi | Uygulamadaki karsiligi |
|---|---|
| En az 3 farkli girdi ve dogrulama | Tarih, egitim turu, sure ve ders konusu |
| En az 2 karar yapisi | Girdi araligi kontrolleri ve ana menu `if/elif/else` yapisi |
| En az 1 dongu | Ana menu ve hatali girdiyi tekrar isteyen `while` donguleri |
| En az 3 fonksiyon | `parse_duration`, `load_records`, `save_records`, `summarize_records` ve digerleri |
| Liste veya sozluk | Kayitlar listesi ve her kayit icin sozluk |
| Bicimli ekran ciktisi ve dosyaya kayit | Tablo/ozet ciktisi ve CSV dosyasi |
| En az 5 test senaryosu | `docs/TEST_SENARYOLARI.md` ve `tests/test_app.py` |
| GitHub dosyalari | Bu README, `PROMPTLAR.md`, kaynak kod ve rapor |

## 3. Kurulum ve calistirma

Python 3.10 veya daha yeni bir surum yeterlidir. Harici paket kurulumu gerekmez.

1. Bu klasoru bilgisayariniza indirin veya GitHub deposunu klonlayin.
2. Terminali bu klasorde acin.
3. Uygulamayi calistirin:

```bash
python main.py
```

4. Menu seceneklerini kullanin: yeni kayit ekleme, kayitlari listeleme, egitim suresi ozetini goruntuleme ve cikis.

Kayitlar varsayilan olarak `ucus_egitim_kayitlari.csv` dosyasinda saklanir. Uygulama dosyayi ilk kayit eklenirken olusturur.

## 4. Testleri calistirma

Proje klasorunde:

```bash
python -m unittest discover -s tests -v
```

Testler girdi dogrulama, CSV kaydetme/okuma ve toplam sure hesaplamasini kontrol eder.

## 5. Proje dosyalari

```text
Ucus_Egitim_Kayit_Sistemi/
├── main.py
├── README.md
├── PROMPTLAR.md
├── requirements.txt
├── tests/
│   └── test_app.py
├── docs/
│   ├── TEST_SENARYOLARI.md
│   └── akis_semasi.png
└── screenshots/
    └── uygulama_ornek_cikti.png
```

Ayrica teslim klasorunde 3 sayfalik `RAPOR.docx` ve `RAPOR.pdf`, ayrıca `TESLIM_ONCESI_KONTROL.md` bulunur.

## 6. Ekran goruntusu

Asagidaki goruntu, ornek komut satiri oturumundan alinmistir:

![Uygulama ornek ciktisi](screenshots/uygulama_ornek_cikti.png)

## 7. Veri ve gizlilik

Uygulama ad, telefon, ogrenci numarasi veya baska bir kisisel veri istemez. Kullanici sadece egitim kaydina ait tarih, tur, saat ve konu alanlarini girer. CSV sutunlari `date`, `duration`, `hours` ve `topic` seklindedir. CSV dosyasi yerel proje klasorunde tutulur.
