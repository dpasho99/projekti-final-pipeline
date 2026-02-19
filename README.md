# Projekti Përfundimtar – Laborator i Integruar
## Web Scraping + API + Data Processing + Security + Database

## Çfarë bën ky projekt?
Ky projekt mbledh të dhëna nga një website me **Web Scraping**, i pasuron ato me të dhëna shtesë nga një **API**, i përpunon, i siguron me **encryption/hashing** dhe i ruan në një **database SQLite**.

## Si funksionon (me pak fjalë)
Pipeline punon kështu:

1) Merr të dhëna nga website (Scraping)  
2) I pasuron me informacione nga një API  
3) I pastron dhe llogarit statistika  
4) Enkripton dhe hashohet një pjesë e të dhënave  
5) I ruan në SQLite dhe i eksporton në CSV  


## Burimi i të dhënave
### Website për scraping
- https://books.toscrape.com/

Merren të dhëna si:
- Titulli i librit
- Çmimi
- Rating
- Disponueshmëria në stok
- Linku i librit

### API e përdorur për pasurim
- https://restcountries.com/

Merren të dhëna si:
- Region
- Population
- Currency


## Çfarë bën çdo modul?
- **scraper.py** → merr të dhëna nga website (me headers, timeout, retry)
- **client.py** → merr të dhëna nga API (enrichment)
- **transform.py** → pastron dhe përpunon të dhënat
- **crypto.py** → bën encryption (Fernet) dhe hashing (SHA-256)
- **db.py** → ruan të dhënat në SQLite
- **main.py** → i lidh të gjitha bashkë dhe ekzekuton pipeline

---

## Siguria (Encryption dhe Hashing)
Ky projekt përdor:
- **Encryption simetrik (Fernet)** për të enkriptuar linkun `source_url`
- **SHA-256 hashing** për të ruajtur një identifikues të sigurt të linkut

Çelësi i encryption ruhet në `.env` dhe nuk publikohet në GitHub.

---

# Si ekzekutohet projekti (Hap pas Hapi)

## 1) Shkarko projektin nga GitHub
```bash
git clone https://github.com/USERNAME/projekti-final-pipeline.git
cd projekti-final-pipeline

## 2) Krijo Virtual Environment

Windows

py -m venv .venv
.venv\Scripts\activate

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate

## 3) Instalo libraritë
pip install -r requirements.txt

## 4) Krijo file-in .env

Krijo një file .env në root të projektit (ose kopjo .env.example) dhe vendos këtë format:

FERNET_KEY=PASTE_YOUR_KEY_HERE
HTTP_TIMEOUT=15
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProjektiFinal/1.0

Si gjenerohet FERNET_KEY

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Kopjo key-n dhe vendose te .env.

## 5) Ekzekuto projektin

python -m src.main

## 6) Ku dalin rezultatet?

Pas ekzekutimit krijohen këto file:

data/processed/books_enriched.csv

data/processed/metrics.csv

data/processed/books.sqlite

Folderi data/ nuk ngarkohet në GitHub sepse është në .gitignore.

