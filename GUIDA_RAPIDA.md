# GUIDA RAPIDA - Estrattore Dati Documenti

## 🚀 INSTALLAZIONE VELOCE

### Windows

1. **Scarica e installa Python**
   - Vai su: https://www.python.org/downloads/
   - Scarica Python 3.11 o superiore
   - IMPORTANTE: Durante l'installazione seleziona "Add Python to PATH"

2. **Scarica e installa Tesseract OCR**
   - Vai su: https://github.com/UB-Mannheim/tesseract/wiki
   - Scarica l'installer per Windows
   - Durante l'installazione, seleziona "Additional language data (download)" e scegli "Italian"

3. **Installa l'applicazione**
   - Estrai tutti i file in una cartella (es: C:\DocumentExtractor)
   - Fai doppio clic su `avvia_app.bat`
   - Le dipendenze verranno installate automaticamente

### macOS

1. **Apri il Terminale** (Cmd + Spazio, digita "Terminale")

2. **Installa Homebrew** (se non già installato):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Installa Python e Tesseract**:
   ```bash
   brew install python tesseract tesseract-lang
   ```

4. **Installa l'applicazione**:
   ```bash
   cd /percorso/alla/cartella
   chmod +x avvia_app.sh
   ./avvia_app.sh
   ```

### Linux (Ubuntu/Debian)

1. **Apri il Terminale**

2. **Installa Python e Tesseract**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-ita
   ```

3. **Installa l'applicazione**:
   ```bash
   cd /percorso/alla/cartella
   chmod +x avvia_app.sh
   ./avvia_app.sh
   ```

---

## 📱 PRIMO UTILIZZO

### Modalità Interfaccia Grafica

1. **Avvia l'applicazione**
   - Windows: doppio clic su `avvia_app.bat`
   - macOS/Linux: esegui `./avvia_app.sh` dal terminale

2. **Estrai dati dalla Visura Camerale**
   - Clicca "Sfoglia" nella sezione Visura Camerale
   - Seleziona il file PDF
   - Clicca "Estrai Dati"

3. **Estrai dati dal Documento d'Identità**
   - Clicca "Sfoglia" nella sezione Documento d'Identità
   - Seleziona l'immagine (JPG, PNG) o PDF
   - Clicca "Estrai Dati"

4. **Esporta i risultati**
   - Clicca "Esporta in Excel" o "Esporta in CSV"
   - Scegli dove salvare il file
   - **I dati vengono salvati su UNA SOLA RIGA con più colonne**

### Modalità Batch (Più Documenti)

1. **Prepara i documenti**
   - Crea una cartella con tutti i PDF e immagini da elaborare

2. **Esegui il processore batch**
   
   **Windows (Prompt dei comandi):**
   ```
   python batch_processor.py C:\percorso\documenti risultati
   ```

   **macOS/Linux (Terminale):**
   ```
   python3 batch_processor.py /percorso/documenti risultati
   ```

3. **Raccogli i risultati**
   - Troverai `risultati.xlsx` e `risultati.csv` nella stessa cartella
   - Ogni documento è su una riga separata

---

## 📊 FORMATO OUTPUT

### Excel (.xlsx)
```
Riga 1 (intestazioni): Denominazione | Partita_IVA | Codice_Fiscale | Nome | Cognome | ...
Riga 2 (dati):         ABC SRL      | 12345678901 | 12345678901    | Mario| Rossi   | ...
```

### CSV (.csv)
```
Denominazione;Partita_IVA;Codice_Fiscale;Nome;Cognome;...
ABC SRL;12345678901;12345678901;Mario;Rossi;...
```

---

## 🎯 CAMPI ESTRATTI

### Da Visura Camerale:
✓ Denominazione/Ragione Sociale
✓ Partita IVA
✓ Codice Fiscale
✓ Numero REA
✓ Forma Giuridica
✓ Sede Legale (Via)
✓ CAP
✓ Comune
✓ Provincia
✓ Data di Costituzione
✓ Capitale Sociale
✓ Stato Attività

### Da Documento d'Identità:
✓ Nome
✓ Cognome
✓ Data di Nascita
✓ Luogo di Nascita
✓ Codice Fiscale
✓ Numero Documento
✓ Data di Rilascio
✓ Data di Scadenza
✓ Tipo Documento

---

## ⚠️ RISOLUZIONE PROBLEMI COMUNI

### "Python non trovato"
→ Reinstalla Python e seleziona "Add Python to PATH"

### "Tesseract not found"
→ **Windows**: Aggiungi `C:\Program Files\Tesseract-OCR` al PATH di sistema
→ **macOS/Linux**: Reinstalla con `brew install tesseract` o `apt install tesseract-ocr`

### Dati non estratti correttamente
→ Verifica la qualità del PDF/immagine
→ Usa scansioni ad alta risoluzione (minimo 300 DPI)
→ Assicurati che il testo sia leggibile

### Errore nell'installazione dipendenze
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💡 SUGGERIMENTI PER MIGLIORI RISULTATI

### Per Visure Camerali:
- Usa PDF originali dalla Camera di Commercio
- Evita scansioni di bassa qualità
- Verifica che il testo sia selezionabile nel PDF

### Per Documenti d'Identità:
- Fotografia ben illuminata, senza ombre
- Documento piatto (non piegato)
- Risoluzione minima 300 DPI
- Formato preferito: JPG o PNG a colori
- Evita riflessi sulla plastica del documento

---

## 📞 SUPPORTO

### Controllare:
1. Versione Python: `python --version` (deve essere 3.8+)
2. Tesseract installato: `tesseract --version`
3. Dipendenze installate: `pip list`

### File di Log
In caso di errori, l'applicazione mostra messaggi nella finestra. 
Per il batch processor, gli errori vengono stampati nel terminale.

---

## 📁 STRUTTURA FILE

```
DocumentExtractor/
├── document_extractor.py    # App con interfaccia grafica
├── batch_processor.py        # Script elaborazione batch
├── requirements.txt          # Dipendenze Python
├── avvia_app.bat            # Avvio rapido Windows
├── avvia_app.sh             # Avvio rapido macOS/Linux
├── README.md                # Documentazione completa
├── BATCH_GUIDE.md           # Guida elaborazione batch
├── GUIDA_RAPIDA.md          # Questa guida
├── esempio_output.xlsx      # Esempio formato Excel
└── esempio_output.csv       # Esempio formato CSV
```

---

## 🔒 PRIVACY E SICUREZZA

✓ Tutti i dati vengono elaborati **localmente** sul tuo computer
✓ Nessun dato viene inviato a server esterni
✓ Nessuna connessione internet richiesta (dopo l'installazione)
✓ I tuoi documenti rimangono completamente privati

---

## 📈 CASI D'USO

### Studi Professionali
- Archiviazione rapida dati clienti
- Controllo documenti per compliance
- Gestione anagrafiche

### Uffici Pubblici
- Registrazione cittadini
- Gestione pratiche amministrative
- Digitalizzazione archivi

### Aziende
- Onboarding dipendenti
- Verifica fornitori
- Gestione documentale

### Uso Personale
- Organizzazione documenti familiari
- Backup digitale documenti importanti
- Database personale

---

## ✅ CHECKLIST INSTALLAZIONE

- [ ] Python 3.8+ installato
- [ ] Python aggiunto al PATH
- [ ] Tesseract OCR installato
- [ ] Language pack italiano installato
- [ ] Dipendenze Python installate (`pip install -r requirements.txt`)
- [ ] App avviata con successo
- [ ] Test con documento di prova completato

---

## 🎓 FORMAZIONE E ASSISTENZA

Per utilizzare al meglio questa applicazione nel contesto di:
- Sicurezza nei luoghi di lavoro
- Gestione ambientale
- Compliance normativa
- Gestione documentale aziendale

Considera la possibilità di integrare questo strumento nei processi di:
- Verifica documentazione fornitori
- Gestione anagrafiche clienti/dipendenti
- Archivi digitali certificati
- Procedure di audit e controllo

---

**Versione 1.0 - Ottobre 2025**
*Estrattore Dati Documenti - Strumento professionale per l'estrazione automatica di informazioni da documenti aziendali e personali*
