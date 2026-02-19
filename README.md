# Projekti Përfundimtar – Laborator i Integruar
## Web Scraping + API + Data Processing + Security + Database

---

## Çfarë bën ky projekt?
Ky projekt realizon një pipeline të plotë për mbledhjen dhe përpunimin e të dhënave.

Pipeline:
1. Merr të dhëna nga një website me Web Scraping  
2. I pasuron të dhënat me një API të jashtme  
3. I pastron dhe llogarit statistika  
4. Aplikon encryption dhe hashing për siguri  
5. I ruan në SQLite dhe i eksporton në CSV  

---

## Burimi i të dhënave

### Website për scraping
https://books.toscrape.com/

Të dhënat që merren:
- Titulli i librit
- Çmimi
- Rating
- Disponueshmëria
- Linku i produktit

### API për pasurim
https://restcountries.com/

Të dhëna shtesë:
- Region
- Population
- Currency

---

## Struktura e projektit

projekti-final-pipeline/
│
├── src/
│   ├── main.py
│   ├── scraping/scraper.py
│   ├── api/client.py
│   ├── processing/transform.py
│   ├── security/crypto.py
│   ├── storage/db.py
│   └── utils/logging_config.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

---

## Çfarë bën çdo modul?

scraper.py  
→ Mbledh të dhëna nga website me headers, timeout dhe retry logic.

client.py  
→ Merr të dhëna nga API dhe trajton gabimet.

transform.py  
→ Pastron të dhënat dhe llogarit statistika.

crypto.py  
→ Enkripton të dhënat me Fernet dhe gjeneron hash me SHA-256.

db.py  
→ Krijon database SQLite dhe ruan rekordet.

main.py  
→ Lidh të gjitha modulet dhe ekzekuton pipeline.

---

## Siguria (Encryption dhe Hashing)

Ky projekt përdor:

- Encryption simetrik (Fernet) për të enkriptuar linkun `source_url`
- SHA-256 hashing për të ruajtur një identifikues të sigurt të linkut

Çelësi i encryption ruhet në `.env` dhe nuk publikohet në GitHub.

---

# Si ekzekutohet projekti (Hap pas Hapi)

## 1) Shkarko projektin nga GitHub

Hap terminalin dhe shkruaj:

git clone https://github.com/dpasho99/projekti-final-pipeline.git  
cd projekti-final-pipeline

---

## 2) Krijo Virtual Environment

Windows:

py -m venv .venv  
.venv\Scripts\activate  

macOS/Linux:

python3 -m venv .venv  
source .venv/bin/activate  

---

## 3) Instalo libraritë

pip install -r requirements.txt  

---

## 4) Krijo file-in .env

Krijo një file `.env` në root të projektit (ose kopjo `.env.example`) dhe vendos:

FERNET_KEY=PASTE_YOUR_KEY_HERE  
HTTP_TIMEOUT=15  
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProjektiFinal/1.0  

Si gjenerohet FERNET_KEY:

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Kopjo key-n që del dhe vendose te `.env`.

---

## 5) Ekzekuto projektin

python -m src.main  

---

## 6) Ku dalin rezultatet?

Pas ekzekutimit krijohen këto file:

data/processed/books_enriched.csv  
data/processed/metrics.csv  
data/processed/books.sqlite  

