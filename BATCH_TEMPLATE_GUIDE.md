# Guida Elaborazione Batch con Template

## Nuova Funzionalità: Batch Processing con Formato Template

L'elaborazione batch ora supporta automaticamente il **mapping al template** con 149 colonne, esattamente come l'elaborazione singola.

## Come Funziona l'Elaborazione Batch

### Fase 1: Estrazione Dati
Il sistema estrae i dati da tutti i file caricati identificando automaticamente:
- **Visure Camerali** (PDF)
- **Documenti d'Identità** (PDF/JPG/PNG)
- **File non riconosciuti** (per report errori)

### Fase 2: Matching Intelligente

Il sistema usa **3 strategie di matching** per abbinare visure e documenti:

#### Strategia 1: Match per Codice Fiscale
- Confronta il **Codice Fiscale dell'azienda** dalla visura
- Con il **Codice Fiscale della persona** dal documento
- Perfetto per **imprese individuali** dove CF azienda = CF titolare

**Esempio**:
```
Visura: RSSMRA80A01H501Z (azienda individuale)
Documento: RSSMRA80A01H501Z (Mario Rossi)
✅ MATCH! Stessa persona
```

#### Strategia 2: Match per Nome File
- Cerca **pattern comuni** nei nomi dei file
- Identifica codici fiscali, partite IVA, nomi presenti in entrambi

**Esempio**:
```
Visura: "RSSMRA80A01H501Z-VISUORD-2025.pdf"
Documento: "doc-RSSMRA80A01H501Z.jpg"
✅ MATCH! Stesso codice fiscale nel nome
```

#### Strategia 3: Match per Ordine
- Se hai caricato **coppie ordinate** (es: visura1+doc1, visura2+doc2)
- Il sistema abbina automaticamente nell'ordine di caricamento

**Esempio**:
```
File caricati in ordine:
1. visura_azienda_A.pdf
2. documento_azienda_A.jpg
3. visura_azienda_B.pdf
4. documento_azienda_B.jpg

✅ Abbinamento: 1-2, 3-4
```

### Gestione Casi Speciali

**Visura senza documento**:
- Crea riga con solo dati azienda
- Campi persona lasciati vuoti

**Documento senza visura**:
- Crea riga con solo dati persona
- Campi azienda lasciati vuoti

**File non riconosciuti**:
- Vengono elencati separatamente
- Report errori disponibile

## Output Batch

### File Excel Generato

Il file contiene:
- **N righe** = numero di coppie/documenti processati
- **149 colonne** = tutte le colonne del template
- **Formato identico** al singolo documento

**Esempio Output**:
```
Riga 1: Azienda A + Titolare A (matched)
Riga 2: Azienda B + Titolare B (matched)
Riga 3: Azienda C (solo visura, nessun documento)
Riga 4: Persona D (solo documento, nessuna visura)
```

### Statistiche Mostrate

1. **Righe totali**: Quante righe nel file finale
2. **Colonne template**: 149 (sempre)
3. **Media campi/riga**: Media campi compilati per ogni riga
4. **Completamento medio**: % di completamento medio

## Workflow Completo Batch

### 1. Carica i File

Nella sezione "Elaborazione Batch (Multipla)":

```
📦 Elaborazione Batch (Multipla)
Carica più documenti contemporaneamente
```

Clicca "**Carica più file**" e seleziona:
- Tutte le visure (PDF)
- Tutti i documenti (PDF/JPG/PNG)
- In qualsiasi ordine

**Tip**: Usa nomi file con pattern comuni per matching automatico migliore!

### 2. Avvia Elaborazione

Clicca "**🚀 Elabora Tutti i Documenti**"

Vedrai:
- **Fase 1/2**: Estrazione dati dai documenti
- **Fase 2/2**: Matching documenti e creazione formato template
- Progress bar per seguire l'avanzamento

### 3. Verifica Statistiche

Dopo l'elaborazione vedrai:
```
✅ Elaborazione completata!
📄 Totale file: 10
📋 Visure: 5
🆔 Documenti: 5
✅ Righe template: 5
```

### 4. Visualizza Risultati

Vai alla tab "**📊 Risultati**":

- **Anteprima dati principali**: Colonne chiave (Ragione sociale, CF, P.IVA, Nome, Cognome, ecc.)
- **Visualizza tutte le colonne**: Espandi per vedere tutte le 149 colonne
- **File non riconosciuti**: Se presenti, report degli errori

### 5. Scarica Excel

Clicca "**📥 Scarica Excel**"

Il file sarà: `batch_formato_import_[data].xlsx`

## Suggerimenti per Matching Ottimale

### Naming Convention Consigliata

Per il miglior matching automatico, usa nomi file con pattern:

**Visure**:
```
[CF_AZIENDA]-visura.pdf
[PIVA]-VISUORD-[data].pdf
```

**Documenti**:
```
[CF_PERSONA]-documento.pdf
doc-[CF_PERSONA].jpg
[NOME]-[COGNOME]-CI.pdf
```

**Esempio Perfetto**:
```
✅ RSSMRA80A01H501Z-VISUORD-20250131.pdf
✅ documento-RSSMRA80A01H501Z.jpg
→ Match automatico garantito!
```

### Caricamento in Coppie

Se possibile, carica i file in coppie ordinate:
1. Visura Azienda A
2. Documento Azienda A
3. Visura Azienda B
4. Documento Azienda B
...

Il sistema userà l'ordine come fallback se gli altri match falliscono.

### Struttura Cartelle (Opzionale)

Se usi l'upload da cartelle locali, organizza così:
```
batch_upload/
├── AZIENDA_A/
│   ├── visura.pdf
│   └── documento.jpg
├── AZIENDA_B/
│   ├── visura.pdf
│   └── documento.pdf
```

## Vantaggi Batch con Template

✅ **Elaborazione Massiva**: 10, 20, 50+ documenti in una volta
✅ **Matching Automatico**: 3 strategie intelligenti
✅ **Formato Uniforme**: Sempre 149 colonne template
✅ **Pronto per Import**: File Excel diretto nel tuo sistema
✅ **Report Errori**: File non processati elencati separatamente
✅ **Statistiche Complete**: Completamento medio, campi compilati, ecc.
✅ **Anteprima Intelligente**: Solo colonne chiave mostrate di default

## Confronto Single vs Batch

| Feature | Singolo | Batch |
|---------|---------|-------|
| File per volta | 1 visura + 1 doc | N file |
| Matching | Manuale (clicca "Combina") | Automatico |
| Output | 1 riga | N righe |
| Formato | Template 149 col | Template 149 col |
| Velocità | Lenta (uno alla volta) | Veloce (tutti insieme) |
| Uso ideale | Test, verifica | Produzione, volume |

## Esempio Pratico

### Scenario: 10 Aziende da Importare

**File da processare**:
- 10 visure camerali (PDF)
- 10 documenti identità titolari (JPG)
- Totale: 20 file

**Workflow**:
1. Carica tutti i 20 file insieme
2. Clicca "🚀 Elabora Tutti"
3. Sistema fa matching automatico
4. Scarica 1 file Excel con 10 righe
5. Importa nel sistema

**Tempo**:
- Prima (manuale): ~30 minuti
- Ora (batch automatico): ~2 minuti

**Risultato**:
- File Excel pronto con 10 righe
- Tutte con 149 colonne template
- Pronto per import diretto

## Risoluzione Problemi

### "Poche righe generate"

**Causa**: Matching non riuscito per alcuni documenti

**Soluzione**:
1. Verifica naming dei file
2. Usa pattern comuni (CF, P.IVA)
3. Carica in coppie ordinate

### "File non riconosciuti"

**Causa**: OCR fallito o formato non supportato

**Soluzione**:
1. Verifica qualità immagini (min 300 DPI)
2. Usa PDF con testo selezionabile
3. Controlla che siano visure/documenti validi

### "Campi vuoti nel template"

**Causa**: Dati non estratti dal documento

**Soluzione**:
1. Verifica qualità del PDF/immagine
2. Alcuni campi potrebbero non essere presenti nel documento
3. Completa manualmente i campi mancanti nell'Excel

## Note Tecniche

- **Limite file**: Nessun limite teorico, ma consigliati max 100 file per upload
- **Timeout**: File molto grandi potrebbero richiedere più tempo
- **Memoria**: L'elaborazione avviene in-memory, file troppo grandi potrebbero dare problemi
- **Formato**: Il template è sempre lo stesso, indipendentemente dal numero di righe

## Versione

Batch Template Processing added in version 2.2 - 2025
