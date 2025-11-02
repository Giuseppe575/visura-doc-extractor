# Estrattore Dati Visure Camerali

Sistema automatico per l'estrazione di dati da **Visure Camerali** e **Documenti di Identità** con output nel formato Excel personalizzato.

## Caratteristiche

- Estrazione automatica da PDF e immagini (JPG, JPEG, PNG)
- Riconoscimento OCR per documenti scansionati
- Output diretto nel formato template Excel fornito
- Processamento batch di multiple cartelle
- Supporto per visure camerali italiane
- Estrazione dati da carte d'identità e documenti

## Requisiti

### Software necessario

1. **Python 3.8+** (già installato)
2. **Tesseract OCR** (per il riconoscimento ottico dei caratteri)

### Installazione Tesseract OCR (Windows)

1. Scarica Tesseract da: https://github.com/UB-Mannheim/tesseract/wiki
2. Esegui l'installer e installa in `C:\Program Files\Tesseract-OCR`
3. Durante l'installazione, assicurati di selezionare il language pack **Italiano**
4. Aggiungi Tesseract al PATH di sistema oppure modifica lo script

Se Tesseract non è nel PATH, modifica la riga 19 di `visura_extractor.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Librerie Python

Le librerie necessarie sono già state installate:
- openpyxl (gestione Excel)
- pytesseract (wrapper Python per Tesseract)
- pdf2image (conversione PDF in immagini)
- PyPDF2 (estrazione testo da PDF)
- pillow (gestione immagini)
- pandas (manipolazione dati)

## Struttura delle Cartelle

Il sistema si aspetta questa struttura:

```
prova estrazione/
├── format import.xlsx          # Template Excel (NON modificare)
├── visura_extractor.py         # Script principale
├── README.md                   # Questo file
├── CARTELLA AZIENDA 1/
│   ├── visura-camerale.pdf    # Visura (nome file deve contenere "visur")
│   └── documento.pdf           # Documento identità (nome deve contenere "doc")
├── CARTELLA AZIENDA 2/
│   ├── VISUORD-xxx.pdf
│   └── carta-identita.jpg
└── ...
```

## Come Usare

### Metodo 1: Doppio click

Semplicemente fai doppio click su `visura_extractor.py`

### Metodo 2: Da terminale

```bash
cd "C:\Users\atisg\OneDrive - giuseppe strifezza\Desktop\prova estrazione"
python visura_extractor.py
```

## Output

Lo script crea un file Excel con nome formato:
```
dati_estratti_YYYYMMDD_HHMMSS.xlsx
```

Il file conterrà:
- Una riga per ogni cartella processata
- Tutte le colonne del template originale
- Dati estratti dalle visure e documenti

## Dati Estratti

### Dalla Visura Camerale:
- Denominazione/Ragione Sociale
- Forma giuridica
- Codice Fiscale azienda
- Partita IVA
- Camera di Commercio e REA
- Sede legale (indirizzo, comune, CAP, provincia)
- Attività prevalente
- Codice ATECO
- Amministratori e cariche
- Date costituzione/inizio attività

### Dal Documento di Identità:
- Nome e Cognome
- Data e luogo di nascita
- Codice Fiscale
- Sesso
- Residenza completa
- Tipo documento
- Numero documento
- Autorità di rilascio
- Date rilascio e scadenza

## Convenzioni per i Nomi dei File

Per un riconoscimento ottimale:

**Visure camerali** - il nome deve contenere:
- "visur"
- "VISUR"
- "visuord"
- "VISUORD"

**Documenti di identità** - il nome deve contenere:
- "doc"
- "DOC"
- "identit"
- "carta"

## Risoluzione Problemi

### Tesseract non trovato
```
Error: Tesseract not found
```
**Soluzione**: Installa Tesseract OCR o modifica il path nello script

### Nessun dato estratto
**Possibili cause**:
- PDF protetto o criptato
- Qualità immagine troppo bassa
- Nome file non segue le convenzioni
- Formato visura non standard

**Soluzioni**:
- Verifica che i PDF siano leggibili
- Aumenta risoluzione scansioni (minimo 300 DPI)
- Rinomina i file seguendo le convenzioni
- Controlla i log dello script

### Errori di estrazione
**Soluzione**: Controlla il log dello script per dettagli specifici

## Personalizzazione

### Modificare i pattern di riconoscimento

I pattern regex per l'estrazione si trovano nei metodi:
- `extract_visura_data()` - riga 87
- `extract_documento_data()` - riga 167

### Aggiungere nuovi campi

Modifica il metodo `create_row_from_data()` alla riga 250

## Note Tecniche

- L'estrazione avviene prima tentando di leggere il testo dal PDF
- Se il testo è insufficiente, viene usato OCR
- I dati vengono validati con espressioni regolari
- Il formato date è italiano (GG/MM/AAAA)
- Supporto completo per caratteri accentati italiani

## Supporto

Per problemi o domande, contatta il supporto tecnico.

## Versione

1.0.0 - Prima release
