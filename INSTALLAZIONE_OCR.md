# Guida Installazione Strumenti OCR (Opzionali)

Questa guida spiega come installare Tesseract OCR e Poppler per migliorare l'estrazione da documenti scansionati o di bassa qualità.

**NOTA**: Questi strumenti sono **OPZIONALI**. Lo script funziona già per PDF con testo selezionabile. Installa questi strumenti solo se:
- Hai molti documenti scansionati (immagini JPG/PNG)
- I PDF non contengono testo selezionabile
- L'estrazione base non funziona per i tuoi documenti

## 1. Installazione Tesseract OCR

Tesseract è necessario per riconoscere il testo nelle immagini.

### Download e Installazione

1. **Scarica l'installer**:
   - Vai a: https://github.com/UB-Mannheim/tesseract/wiki
   - Scarica: `tesseract-ocr-w64-setup-5.x.x.exe` (versione più recente)

2. **Installa Tesseract**:
   - Esegui l'installer scaricato
   - **IMPORTANTE**: Durante l'installazione:
     - Seleziona "Additional language data (download)"
     - Assicurati di selezionare **Italian (ita)** nella lista delle lingue
   - Installa in: `C:\Program Files\Tesseract-OCR`

3. **Aggiungi al PATH** (metodo semplice):
   - Premi `Win + R`
   - Digita: `sysdm.cpl` e premi Invio
   - Vai su "Avanzate" → "Variabili d'ambiente"
   - Nella sezione "Variabili di sistema", trova "Path" e clicca "Modifica"
   - Clicca "Nuovo" e aggiungi: `C:\Program Files\Tesseract-OCR`
   - Clicca OK su tutte le finestre
   - **Riavvia il computer**

4. **Verifica installazione**:
   ```cmd
   tesseract --version
   ```

### Configurazione Alternativa (se non vuoi modificare il PATH)

Se preferisci non modificare il PATH di sistema, modifica lo script:

1. Apri `visura_extractor.py`
2. Trova la riga 19 (attualmente commentata):
   ```python
   # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
3. Rimuovi il `#` all'inizio:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## 2. Installazione Poppler (per pdf2image)

Poppler è necessario per convertire PDF in immagini quando serve OCR.

### Download e Installazione

1. **Scarica Poppler per Windows**:
   - Vai a: https://github.com/oschwartz10612/poppler-windows/releases
   - Scarica l'ultimo file `Release-XX.XX.X-X.zip`

2. **Estrai e Installa**:
   - Estrai il file ZIP in `C:\Program Files\poppler`
   - Dovresti avere la struttura: `C:\Program Files\poppler\Library\bin\`

3. **Aggiungi al PATH**:
   - Premi `Win + R`
   - Digita: `sysdm.cpl` e premi Invio
   - Vai su "Avanzate" → "Variabili d'ambiente"
   - Nella sezione "Variabili di sistema", trova "Path" e clicca "Modifica"
   - Clicca "Nuovo" e aggiungi: `C:\Program Files\poppler\Library\bin`
   - Clicca OK su tutte le finestre
   - **Riavvia il computer**

4. **Verifica installazione**:
   ```cmd
   pdftoppm -h
   ```

## 3. Test Completo

Dopo aver installato entrambi gli strumenti:

1. Riavvia il computer
2. Apri il terminale/PowerShell
3. Vai nella cartella del progetto:
   ```cmd
   cd "C:\Users\atisg\OneDrive - giuseppe strifezza\Desktop\prova estrazione"
   ```
4. Esegui lo script:
   ```cmd
   python visura_extractor.py
   ```

Ora lo script dovrebbe:
- Estrarre testo da immagini JPG/PNG
- Usare OCR su PDF quando il testo non è selezionabile
- Non mostrare più errori "tesseract is not installed" o "poppler installed"

## Risoluzione Problemi

### "tesseract is not installed or it's not in your PATH"

**Soluzione 1**: Verifica che Tesseract sia nel PATH
```cmd
echo %PATH%
```
Dovresti vedere `C:\Program Files\Tesseract-OCR`

**Soluzione 2**: Usa la configurazione manuale nello script (vedi sopra)

**Soluzione 3**: Riavvia il computer dopo aver modificato il PATH

### "Unable to get page count. Is poppler installed and in PATH?"

**Soluzione 1**: Verifica che Poppler sia nel PATH
```cmd
where pdftoppm
```
Dovrebbe mostrare il percorso di pdftoppm.exe

**Soluzione 2**: Reinstalla Poppler nella directory corretta

**Soluzione 3**: Riavvia il computer dopo aver modificato il PATH

### L'OCR è lento

L'OCR è più lento dell'estrazione diretta del testo. Per documenti con testo selezionabile, non verrà usato l'OCR.

**Suggerimenti per velocizzare**:
- Usa PDF con testo selezionabile quando possibile
- Riduci la risoluzione DPI nel codice (attualmente 300)
- Processa solo le cartelle necessarie

### L'OCR non riconosce bene il testo

**Suggerimenti per migliorare**:
- Aumenta la qualità delle scansioni (minimo 300 DPI)
- Assicurati che i documenti siano dritti e ben illuminati
- Usa documenti originali quando possibile
- Verifica che il pacchetto lingua italiana sia installato in Tesseract

## Alternative Senza Installazione

Se non vuoi installare Tesseract e Poppler:

1. **Converti i PDF scansionati in PDF con testo**:
   - Usa Adobe Acrobat Pro
   - Usa servizi online come Smallpdf o PDF24

2. **Converti le immagini in PDF con testo**:
   - Usa Microsoft Office Lens (app mobile)
   - Usa Adobe Scan (app mobile)
   - Salva come PDF con livello testo

3. **Usa lo script solo per PDF con testo selezionabile**:
   - Lo script funziona perfettamente senza OCR per questi documenti
   - È molto più veloce

## Riepilogo

| Strumento | Necessario per | Alternativa |
|-----------|---------------|-------------|
| Tesseract | Immagini JPG/PNG, PDF scansionati | Converti in PDF con testo |
| Poppler | OCR su PDF (conversione in immagini) | Usa solo PDF con testo |
| Entrambi | Massima compatibilità | Preprocessing manuale |

**Raccomandazione**: Se la maggior parte dei tuoi documenti sono già PDF con testo selezionabile, **non è necessario installare** questi strumenti. Lo script funziona già perfettamente!
