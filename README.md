# 📄 Estrattore Dati Documenti

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

Applicazione Python professionale per l'estrazione automatica di dati da **Visure Camerali** e **Documenti d'Identità**, con esportazione in Excel e CSV su una singola riga.

🎯 **Perfetta per**: Studi professionali, uffici pubblici, aziende, consulenti

---

## 📸 Screenshot

![App Interface](https://via.placeholder.com/800x500/4A90E2/ffffff?text=Interface+Screenshot)

*Interfaccia grafica intuitiva con visualizzazione dati in tempo reale*

---

## 🚀 Quick Start

### Opzione 1: App Web Streamlit (⭐ CONSIGLIATO per test online)

**Deploy gratuito su Streamlit Cloud in 5 minuti!**

```bash
# Clona il repository
git clone https://github.com/tuousername/document-extractor.git
cd document-extractor

# Test in locale
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py

# Deploy su Streamlit Cloud (vedi STREAMLIT_DEPLOY.md)
```

🌐 **[Demo Live](https://tuousername-document-extractor.streamlit.app)** (sostituisci con il tuo URL dopo il deploy)

### Opzione 2: App Desktop (Tkinter)

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python document_extractor.py
```

### Opzione 3: Docker (per server privati)

```bash
# Con Docker Compose
docker-compose up -d

# Accedi su http://localhost:8501
```

**Nota**: Tutte le opzioni richiedono [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installato sul sistema.

---

## Caratteristiche

### 🖥️ Versione Desktop (Tkinter)
- ✅ Interfaccia grafica intuitiva
- ✅ Estrazione da file singoli
- ✅ Elaborazione batch automatica
- ✅ Visualizzazione dati in tempo reale
- ✅ Esporta in Excel e CSV
- ✅ Cross-platform (Windows, macOS, Linux)

### 🌐 Versione Web (Streamlit)
- ✅ Accessibile da browser
- ✅ Interfaccia moderna e responsive
- ✅ Upload drag & drop
- ✅ Preview documenti
- ✅ Elaborazione batch con progress bar
- ✅ Download diretto risultati
- ✅ Nessuna installazione per utenti finali
- ✅ Deploy gratuito su Streamlit Cloud

### 🐳 Deploy Opzioni
- ✅ **Streamlit Cloud**: Gratuito, automatico, HTTPS incluso
- ✅ **Docker**: Privacy totale, controllo completo
- ✅ **Desktop**: Uso offline, nessun server necessario

## Dati Estratti

### Dalla Visura Camerale:
- Denominazione/Ragione Sociale
- Partita IVA
- Codice Fiscale
- Numero REA
- Forma Giuridica
- Sede Legale
- CAP
- Comune
- Provincia
- Data di Costituzione
- Capitale Sociale
- Stato Attività

### Dal Documento d'Identità:
- Nome
- Cognome
- Data di Nascita
- Luogo di Nascita
- Codice Fiscale
- Numero Documento
- Data di Rilascio
- Data di Scadenza
- Tipo Documento

## Requisiti di Sistema

### Windows

1. **Python 3.8 o superiore**
   - Scarica da: https://www.python.org/downloads/
   - Durante l'installazione, seleziona "Add Python to PATH"

2. **Tesseract OCR**
   - Scarica da: https://github.com/UB-Mannheim/tesseract/wiki
   - Installa l'eseguibile
   - Aggiungi il percorso di Tesseract al PATH (es: `C:\Program Files\Tesseract-OCR`)
   - Scarica il language pack italiano durante l'installazione

### macOS

```bash
# Installa Homebrew (se non già installato)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installa Python
brew install python

# Installa Tesseract con supporto italiano
brew install tesseract tesseract-lang
```

### Linux (Ubuntu/Debian)

```bash
# Installa Python e pip
sudo apt update
sudo apt install python3 python3-pip

# Installa Tesseract con supporto italiano
sudo apt install tesseract-ocr tesseract-ocr-ita
```

## Installazione

1. **Scarica i file dell'applicazione** in una cartella

2. **Apri il terminale/prompt dei comandi** nella cartella dell'applicazione

3. **Installa le dipendenze Python:**

```bash
pip install -r requirements.txt
```

oppure:

```bash
pip3 install -r requirements.txt
```

## Utilizzo

1. **Avvia l'applicazione:**

```bash
python document_extractor.py
```

oppure:

```bash
python3 document_extractor.py
```

2. **Estrai dati dalla Visura Camerale:**
   - Clicca su "Sfoglia" nella sezione "Visura Camerale"
   - Seleziona il file PDF della visura
   - Clicca su "Estrai Dati"

3. **Estrai dati dal Documento d'Identità:**
   - Clicca su "Sfoglia" nella sezione "Documento d'Identità"
   - Seleziona l'immagine o PDF del documento
   - Clicca su "Estrai Dati"

4. **Visualizza i dati estratti:**
   - I dati appaiono nella tabella centrale

5. **Esporta i dati:**
   - Clicca su "Esporta in Excel" per salvare in formato .xlsx
   - Clicca su "Esporta in CSV" per salvare in formato .csv
   - **I dati vengono salvati su una singola riga con colonne multiple**

6. **Pulisci i dati:**
   - Clicca su "Pulisci Dati" per iniziare una nuova estrazione

## Formato di Esportazione

I dati vengono esportati su **una singola riga** con le seguenti colonne:

### Excel (.xlsx):
```
| Denominazione | Partita_IVA | Codice_Fiscale | Nome | Cognome | ... |
|---------------|-------------|----------------|------|---------|-----|
| ABC SRL       | 12345678901 | 12345678901    | Mario| Rossi   | ... |
```

### CSV (.csv):
```
Denominazione;Partita_IVA;Codice_Fiscale;Nome;Cognome;...
ABC SRL;12345678901;12345678901;Mario;Rossi;...
```

## Suggerimenti per Migliori Risultati

### Per le Visure Camerali:
- Usa file PDF originali (non scansioni)
- Assicurati che il testo sia selezionabile nel PDF

### Per i Documenti d'Identità:
- Usa immagini ad alta risoluzione (minimo 300 DPI)
- Assicurati che l'immagine sia ben illuminata
- Evita riflessi e ombre
- Il documento deve essere piatto e non piegato
- Preferisci immagini a colori

## Risoluzione Problemi

### Errore "Tesseract not found"
- **Windows**: Aggiungi `C:\Program Files\Tesseract-OCR` al PATH
- **macOS/Linux**: Installa tesseract usando i comandi sopra indicati

### Dati non estratti correttamente
- Verifica la qualità dell'immagine/PDF
- Assicurati che il testo sia leggibile
- Per le visure, prova con il PDF originale dalla Camera di Commercio

### Errore nell'installazione delle dipendenze
```bash
# Prova con pip aggiornato
pip install --upgrade pip
pip install -r requirements.txt
```

## Personalizzazione

L'applicazione può essere personalizzata modificando il file `document_extractor.py`:

- Aggiungere nuovi pattern di estrazione nella funzione `parse_visura_camerale()`
- Modificare i pattern regex per adattarli a formati specifici
- Aggiungere nuovi campi da estrarre

## Licenza

Questo software è fornito "così com'è", senza garanzie di alcun tipo.

## Supporto

Per problemi o domande, verifica prima:
1. Di aver installato tutte le dipendenze
2. Di aver installato Tesseract OCR
3. Che i file siano nel formato corretto

## Note Tecniche

- L'applicazione usa **OCR (Optical Character Recognition)** per leggere testo dalle immagini
- La precisione dipende dalla qualità dei documenti forniti
- Formati supportati: PDF, JPG, JPEG, PNG
- I dati vengono elaborati localmente (nessun invio a server esterni)
