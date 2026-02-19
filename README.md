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
Hap terminalin dhe shkruaj:

```bash
git clone https://github.com/USERNAME/projekti-final-pipeline.git
cd projekti-final-pipeline