
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from pygbif import occurrences as occ

load_dotenv()

GBIF_USER = os.getenv("GBIF_USER")
GBIF_PWD = os.getenv("GBIF_PWD")
GBIF_EMAIL = os.getenv("GBIF_EMAIL")

DOWNLOAD_DIR = Path("datasets/gbif_indonesia")

def download(download_key):
    if not download_key:
        raise ValueError("Download key harus diisi!")

    # Cek status sebelum download
    status = cek_status(download_key)

    if status != "SUCCEEDED":
        print("\nDownload dibatalkan.")
        print("GBIF masih memproses data. Silakan coba lagi nanti.")
        return

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nMemulai download: {download_key}")

    result = occ.download_get(
        key=download_key,
        path=str(DOWNLOAD_DIR)
    )

    print("\nDownload selesai!")
    print(f"Lokasi: {DOWNLOAD_DIR.resolve()}")
    print(result)

def cek_status(download_key):
    result = occ.download_meta(key=download_key)

    status = result.get("status", "UNKNOWN")

    print(f"\nDownload key : {download_key}")
    print(f"Status       : {status}")

    if status == "SUCCEEDED":
        print(f"Total records: {result.get('totalRecords')}")
        print("Data siap diunduh!")

    elif status in ["PREPARING", "RUNNING"]:
        print("GBIF masih memproses permintaan.")

    else:
        print("Periksa detail respons GBIF:")
        print(result)

    return status

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pengajuan dan download data biodiversitas GBIF"
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument("--ajukan", action="store_true")
    mode.add_argument("--status", type=str, metavar="DOWNLOAD_KEY")
    mode.add_argument("--download", type=str, metavar="DOWNLOAD_KEY")

    args = parser.parse_args()

    if args.ajukan:
        ajukan()

    elif args.status:
        cek_status(args.status)

    elif args.download:
        download(args.download)
    