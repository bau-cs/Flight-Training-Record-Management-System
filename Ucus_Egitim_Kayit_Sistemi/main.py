"""Ucus Egitim Kayit ve Saat Takip Sistemi.

Bu mini uygulama yalnizca egitim amacli kayit tutar. Gercek ucus
operasyonlari, ucus planlamasi veya ucusa elverislilik kararlari icin
kullanilamaz.
"""

from __future__ import annotations

import csv
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable


DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "ucus_egitim_kayitlari.csv"
DATA_FILE = Path(os.environ.get("FLIGHT_LOG_DATA", str(DEFAULT_DATA_FILE)))
FIELDNAMES = ["date", "duration", "hours", "topic"]
CATEGORIES = {
    "1": "Dual Flight",
    "2": "Solo Flight",
    "3": "Simulator",
}
MAX_SESSION_HOURS = 8.0  # Yalnizca uygulamanin veri girisi siniridir; operasyonel limit degildir.


class ValidationError(ValueError):
    """Kullanici girdisi belirlenen kurallara uymadiginda olusan hata."""


def parse_duration(value: str) -> float:
    """Sureyi saat cinsinden sayiya cevirir ve gecerli araligi denetler."""
    normalized = value.strip().replace(",", ".")
    try:
        duration = float(normalized)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Sure sayisal olmalidir. Ornek: 1.5") from exc

    if not 0 < duration <= MAX_SESSION_HOURS:
        raise ValidationError("Sure 0'dan buyuk ve 8 saatten fazla olmamalidir.")

    rounded_duration = round(duration, 2)
    if rounded_duration <= 0:
        raise ValidationError("Sure en az 0.01 saat olmalidir.")
    return rounded_duration


def parse_category(value: str) -> str:
    """1-3 arasindaki secimi egitim turune donusturur."""
    choice = value.strip()
    if choice not in CATEGORIES:
        raise ValidationError("Gecersiz secim. 1, 2 veya 3 giriniz.")
    return CATEGORIES[choice]


def parse_date(value: str) -> str:
    """Tarihi YYYY-MM-DD biciminde dogrular ve standartlastirir."""
    cleaned = value.strip()
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d")
    except (TypeError, ValueError) as exc:
        raise ValidationError(
            "Tarih YYYY-AA-GG biciminde olmali. Ornek: 2026-11-14"
        ) from exc
    return parsed.strftime("%Y-%m-%d")


def parse_topic(value: str) -> str:
    """Ders konusunun bos olmadigini ve uzunlugunu denetler."""
    topic = " ".join(value.split())
    if len(topic) < 3:
        raise ValidationError("Ders konusu en az 3 karakter olmalidir.")
    if len(topic) > 80:
        raise ValidationError("Ders konusu en fazla 80 karakter olabilir.")
    return topic


def build_record(
    date_value: str,
    category_value: str,
    duration_value: str,
    topic_value: str,
) -> dict:
    """Dogrulanmis alanlardan tek bir kayit sozlugu olusturur."""
    return {
        "date": parse_date(date_value),
        "duration": parse_category(category_value),
        "hours": parse_duration(duration_value),
        "topic": parse_topic(topic_value),
    }


def load_records(file_path: Path = DATA_FILE) -> list[dict]:
    """CSV kayitlarini yukler; dosya yoksa bos liste dondurur.

    Hatalı/eksik satirlar atlanir. Okuma hatasinda kullaniciya uyari verilir.
    """
    if not file_path.exists():
        return []

    records: list[dict] = []
    try:
        with file_path.open("r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    duration_type = (row.get("duration") or row.get("category") or "").strip()
                    hours_value = row.get("hours") or row.get("duration_hours") or ""
                    record = {
                        "date": parse_date(row.get("date") or ""),
                        "duration": duration_type,
                        "hours": parse_duration(str(hours_value)),
                        "topic": parse_topic(row.get("topic") or ""),
                    }
                    if record["duration"] not in CATEGORIES.values():
                        continue
                    records.append(record)
                except (ValidationError, AttributeError):
                    # Bozuk tek bir satir, diger gecerli kayitlarin okunmasini engellemez.
                    continue
    except (OSError, csv.Error, UnicodeError) as exc:
        print(f"Uyari: Kayit dosyasi okunamadi: {exc}")
    return records


def save_records(records: list[dict], file_path: Path = DATA_FILE) -> None:
    """Tum kayitlari UTF-8 CSV dosyasina guvenli/atomik bicimde yazar.

    Once ayni klasorde gecici dosya olusturulur. Yazma tamamlanirsa hedef
    dosyanin yerine gecirilir; yazma hatasinda onceki CSV korunur.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as csv_file:
            temporary_path = Path(csv_file.name)
            writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
            csv_file.flush()
            os.fsync(csv_file.fileno())
        os.replace(temporary_path, file_path)
    except OSError:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise


def summarize_records(records: list[dict]) -> dict:
    """Toplam sureyi, kayit sayisini ve egitim turu bazli sureleri hesaplar."""
    category_hours = {category: 0.0 for category in CATEGORIES.values()}
    total_hours = 0.0

    for record in records:
        hours = float(record["hours"])
        total_hours += hours
        duration_type = record["duration"]
        if duration_type in category_hours:
            category_hours[duration_type] += hours

    return {
        "record_count": len(records),
        "total_hours": round(total_hours, 2),
        "category_hours": {
            category: round(hours, 2)
            for category, hours in category_hours.items()
        },
    }


def display_records(records: list[dict]) -> None:
    """Kayitlari konsolda duzenli bir tablo halinde gosterir."""
    if not records:
        print("\nHenuz kayit bulunmuyor.\n")
        return

    print("\n" + "-" * 88)
    print(f"{'DATE':<14} {'DURATION':<18} {'HOURS':>10}  TOPIC")
    print("-" * 88)
    for record in records:
        print(
            f"{record['date']:<14} {record['duration']:<18} "
            f"{float(record['hours']):>10.2f}  {record['topic']}"
        )
    print("-" * 88 + "\n")


def display_summary(records: list[dict]) -> None:
    """Genel ve egitim turu bazli sure ozetini ekrana yazdirir."""
    summary = summarize_records(records)
    print("\n===== EGITIM OZETI =====")
    print(f"Toplam kayit sayisi : {summary['record_count']}")
    print(f"Toplam egitim suresi: {summary['total_hours']:.2f} saat")
    for category, hours in summary["category_hours"].items():
        print(f"{category:<18}: {hours:.2f} saat")
    print("=======================\n")


def ask_until_valid(
    prompt: str,
    parser: Callable[[str], object],
    input_fn: Callable[[str], str] = input,
) -> object:
    """Girdi dogru olana kadar sorar; hatali girdide uygulamayi kapatmaz."""
    while True:
        raw_value = input_fn(prompt)
        try:
            return parser(raw_value)
        except ValidationError as error:
            print(f"Hata: {error} Lutfen tekrar deneyin.")


def add_record_interactively(
    records: list[dict],
    input_fn: Callable[[str], str] = input,
    file_path: Path = DATA_FILE,
) -> None:
    """Dort alani alir, dogrular, listeye ekler ve CSV'ye kaydeder."""
    print("\n--- YENI EGITIM KAYDI ---")
    date_value = ask_until_valid("Tarih (YYYY-AA-GG): ", parse_date, input_fn)
    print("Egitim turu: 1) Dual Flight  2) Solo Flight  3) Simulator")
    category_value = ask_until_valid("Seciminiz (1-3): ", parse_category, input_fn)
    duration_value = ask_until_valid("Sure (saat, ornek 1.5): ", parse_duration, input_fn)
    topic_value = ask_until_valid("Ders konusu: ", parse_topic, input_fn)

    record = {
        "date": date_value,
        "duration": category_value,
        "hours": duration_value,
        "topic": topic_value,
    }
    records.append(record)
    try:
        save_records(records, file_path)
    except OSError as error:
        records.pop()  # Dosyaya yazilamazsa bellek listesini de geri al.
        print(f"Uyari: Kayit dosyaya yazilamadi: {error}\n")
        return
    print("Kayit basariyla eklendi ve CSV dosyasina kaydedildi.\n")


def delete_record_interactively(
    records: list[dict],
    input_fn: Callable[[str], str] = input,
    file_path: Path = DATA_FILE,
) -> None:
    """Secilen kaydi onayla siler; iptal veya dosya hatasinda kaydi korur."""
    if not records:
        print("\nSilinecek kayit bulunmuyor.\n")
        return

    print("\n--- UCUS EGITIM KAYDI SIL ---")
    display_records(records)

    while True:
        selection = input_fn(
            f"Silmek istediginiz kayit numarasi (1-{len(records)}) veya iptal icin 0: "
        ).strip()
        try:
            record_number = int(selection)
        except ValueError:
            print("Lutfen gecerli bir kayit numarasi giriniz.")
            continue

        if record_number == 0:
            print("Silme islemi iptal edildi.\n")
            return
        if not 1 <= record_number <= len(records):
            print(f"Lutfen 1 ile {len(records)} arasinda bir numara giriniz.")
            continue

        record_index = record_number - 1
        selected_record = records[record_index]
        print("\nSecilen kayit:")
        print(
            f"Tarih: {selected_record['date']} | "
            f"Tur: {selected_record['duration']} | "
            f"Sure: {float(selected_record['hours']):.2f} saat | "
            f"Konu: {selected_record['topic']}"
        )

        while True:
            confirmation = input_fn("Bu kaydi silmek istiyor musunuz? (E/H): ").strip().lower()
            if confirmation in ("e", "evet"):
                deleted_record = records.pop(record_index)
                try:
                    save_records(records, file_path)
                except OSError as error:
                    records.insert(record_index, deleted_record)
                    print(f"Uyari: Kayit dosyasi guncellenemedi; kayit korundu: {error}\n")
                    return
                print(
                    f"'{deleted_record['date']} - {deleted_record['topic']}' kaydi silindi.\n"
                )
                return
            if confirmation in ("h", "hayir", "hayır"):
                print("Silme islemi iptal edildi.\n")
                return
            print("Lutfen E (evet) veya H (hayir) giriniz.")


def print_menu() -> None:
    """Ana menu seceneklerini ekrana yazar."""
    print("===== UCUS EGITIM KAYIT SISTEMI =====")
    print("1. Yeni egitim kaydi ekle")
    print("2. Kayitlari listele")
    print("3. Egitim suresi ozetini goster")
    print("4. Ucus egitim kaydi sil")
    print("5. Cikis")


def main(
    input_fn: Callable[[str], str] = input,
    file_path: Path = DATA_FILE,
) -> None:
    """Ana menu dongusunu, kullanici cikis secene kadar calistirir."""
    records = load_records(file_path)
    print("Ucus Egitim Kayit ve Saat Takip Sistemine hos geldiniz.")
    print("Not: Bu uygulama yalnizca egitim amacli kayit tutar.\n")

    while True:
        print_menu()
        choice = input_fn("Islem seciniz (1-5): ").strip()
        if choice == "1":
            add_record_interactively(records, input_fn, file_path)
        elif choice == "2":
            display_records(records)
        elif choice == "3":
            display_summary(records)
        elif choice == "4":
            delete_record_interactively(records, input_fn, file_path)
        elif choice == "5":
            print("Programdan cikiliyor. Iyi calismalar!")
            break
        else:
            print("Gecersiz menu secimi. Lutfen 1, 2, 3, 4 veya 5 giriniz.\n")


if __name__ == "__main__":
    main()
