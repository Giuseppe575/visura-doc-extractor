# Guida Elaborazione Batch

## Introduzione

Lo script `batch_processor.py` permette di elaborare automaticamente tutti i documenti presenti in una cartella, senza bisogno di selezionarli uno per uno.

## Vantaggi

- ✅ Elaborazione automatica di decine o centinaia di documenti
- ✅ Un unico file Excel/CSV con tutti i dati
- ✅ Ogni documento su una riga separata
- ✅ Riconoscimento automatico del tipo di documento
- ✅ Log degli errori per documenti non elaborabili

## Utilizzo

### Passo 1: Prepara i documenti

Crea una cartella con tutti i documenti da elaborare:

```
documenti/
├── visura1.pdf
├── visura2.pdf
├── carta_identita1.jpg
├── carta_identita2.png
└── patente.pdf
```

### Passo 2: Esegui lo script

**Windows:**
```bash
python batch_processor.py documenti risultati
```

**Linux/macOS:**
```bash
python3 batch_processor.py documenti risultati
```

Dove:
- `documenti` è la cartella contenente i file
- `risultati` è il nome dei file di output (senza estensione)

### Passo 3: Raccogli i risultati

Lo script creerà due file:
- `risultati.xlsx` - File Excel
- `risultati.csv` - File CSV

## Formato Output

Ogni documento viene salvato su una **riga separata** con tutte le informazioni estratte:

```
| Nome_File      | Tipo_File         | Denominazione | Partita_IVA | Nome  | Cognome | ... |
|----------------|-------------------|---------------|-------------|-------|---------|-----|
| visura1.pdf    | Visura Camerale   | ABC SRL       | 12345678901 |       |         | ... |
| carta1.jpg     | Documento Identità|               |             | Mario | Rossi   | ... |
| visura2.pdf    | Visura Camerale   | XYZ SPA       | 98765432109 |       |         | ... |
```

## Colonne Aggiuntive

Lo script aggiunge automaticamente:
- **Nome_File**: Nome del file elaborato
- **Tipo_File**: Tipo di documento riconosciuto
- **Data_Elaborazione**: Data e ora dell'elaborazione

## Esempi Pratici

### Esempio 1: Elaborare visure camerali

```bash
# Cartella con 50 visure camerali
python batch_processor.py ./visure_2024 visure_gennaio

# Output: visure_gennaio.xlsx e visure_gennaio.csv
```

### Esempio 2: Elaborare documenti identità

```bash
# Cartella con carte d'identità
python batch_processor.py ./documenti_identita anagrafica_clienti

# Output: anagrafica_clienti.xlsx e anagrafica_clienti.csv
```

### Esempio 3: Mix di documenti

```bash
# Cartella con vari tipi di documenti
python batch_processor.py ./archivio_2024 tutti_documenti

# Output: tutti_documenti.xlsx e tutti_documenti.csv
```

### Esempio 4: Output con timestamp automatico

```bash
# Senza specificare nome output
python batch_processor.py ./documenti

# Output: risultati_20250129_143022.xlsx e risultati_20250129_143022.csv
```

## Formati Supportati

- **PDF**: .pdf, .PDF
- **Immagini**: .jpg, .JPG, .jpeg, .JPEG, .png, .PNG

## Gestione Errori

Se un documento non può essere elaborato:
- Viene stampato un messaggio di errore
- Gli altri documenti continuano ad essere elaborati
- Il documento problematico non appare nel file di output

## Suggerimenti

1. **Organizza i documenti per tipo** in cartelle separate per risultati più puliti

2. **Verifica la qualità** prima dell'elaborazione batch:
   - Testa alcuni documenti con l'app grafica
   - Assicurati che le immagini siano leggibili

3. **Backup dei dati**: Conserva sempre i documenti originali

4. **File molto grandi**: Per centinaia di documenti, l'elaborazione può richiedere tempo

## Monitoraggio Progresso

Durante l'elaborazione, lo script mostra:
```
Trovati 10 documenti da elaborare

[1/10] Elaborazione: visura1.pdf
  ✓ Completato

[2/10] Elaborazione: carta_identita.jpg
  ✓ Completato

[3/10] Elaborazione: documento_corrotto.pdf
  ✗ Errore: File danneggiato

...

✓ Dati esportati in Excel: risultati.xlsx
✓ Dati esportati in CSV: risultati.csv

Totale documenti elaborati: 9
```

## Personalizzazione

Puoi modificare lo script per:
- Aggiungere nuovi pattern di estrazione
- Filtrare documenti per data
- Aggiungere validazioni personalizzate
- Modificare il formato di output

## Confronto: App Grafica vs Batch

| Caratteristica | App Grafica | Batch Script |
|----------------|-------------|--------------|
| Documenti singoli | ✓ | ✓ |
| Elaborazione multipla | Manuale | Automatica |
| Interfaccia | Grafica | Linea comando |
| Velocità | Lenta | Veloce |
| Ideale per | 1-10 documenti | 10+ documenti |

## Requisiti

Gli stessi della app grafica:
- Python 3.8+
- Tesseract OCR
- Dipendenze in requirements.txt

## Troubleshooting

**Errore: "No such file or directory"**
- Verifica che il percorso della cartella sia corretto
- Usa percorsi assoluti se necessario: `C:\Users\Nome\documenti`

**Nessun documento trovato**
- Verifica che i file abbiano le estensioni supportate
- Controlla che la cartella non sia vuota

**Errore Tesseract**
- Assicurati che Tesseract OCR sia installato
- Verifica che il language pack italiano sia presente

**Memoria insufficiente**
- Elabora i documenti in lotti più piccoli
- Riduci la risoluzione delle immagini prima dell'elaborazione
