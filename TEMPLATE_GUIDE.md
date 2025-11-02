# Guida Template Formato Import

## Nuova Funzionalità: Supporto Template Personalizzato

L'app Streamlit ora supporta l'export dei dati in un formato template personalizzato per facilitare l'importazione in altri sistemi.

## Come Funziona

### 1. Template Rilevato Automaticamente

Quando avvii l'app Streamlit, il sistema rileva automaticamente il file `format_import_template.xlsx` e ti mostra un avviso:

```
📋 Template formato import rilevato - I dati saranno esportati nel formato personalizzato
```

### 2. Estrazione Dati

Procedi normalmente con l'estrazione:

1. **Carica la Visura Camerale** (PDF)
   - Clicca su "Estrai Dati Visura"

2. **Carica il Documento d'Identità** (PDF/JPG/PNG)
   - Clicca su "Estrai Dati Documento"

### 3. Combina i Dati

Dopo aver estratto sia la visura che il documento, clicca sul pulsante:

```
🔄 Combina Visura e Documento nel Formato Template
```

### 4. Visualizza e Scarica

Vai alla tab **"Risultati"** per:

- Vedere le statistiche dei dati estratti
- Visualizzare i campi principali
- Scaricare il file Excel nel formato template

## Campi Mappati

### Dalla Visura Camerale → Template

| Dato Estratto | Colonna Template |
|--------------|------------------|
| Denominazione | Ragionesociale, Intestazione |
| Codice Fiscale | Codfisc Azienda |
| Partita IVA | Partita Iva Azienda |
| Numero REA | Cciaa |
| Forma Giuridica | Natura Giuridica |
| Sede Legale | Indirizzo Sede |
| Comune | Comune Sede |
| CAP | Cap Sede |
| Provincia | Prov Sede |
| Data Costituzione | Data Ini Rapporto |

### Dal Documento d'Identità → Template

| Dato Estratto | Colonna Template |
|--------------|------------------|
| Nome | Nome 1, Tit 1 Nome |
| Cognome | Cognome 1, Tit 1 Cognome |
| Codice Fiscale | Codfisc 1, Tit 1 Codfisc |
| Sesso | Sesso 1, Tit 1 Sesso |
| Data Nascita | Data Nas 1, Tit 1 Datanas |
| Luogo Nascita | Comune Nas 1, Tit 1 Comunenas |
| Provincia Nascita | Provincia Nas 1, Tit 1 Provincia Nas |
| Residenza | Indirizzo Res 1 |
| Comune Residenza | Comune Res 1 |
| Tipo Documento | Tipo Doc, Tit 1 Tipodoc |
| Numero Documento | Num Doc, Tit 1 Numdoc |
| Data Rilascio | Data Doc |
| Data Scadenza | Scadenza Doc, Tit 1 Scad Doc |
| Comune Rilascio | Autorita Doc, Tit 1 Rilasc Da |

### Campi Predefiniti

Alcuni campi vengono compilati automaticamente:

- **Pers Soc**: "S" (società) o "P" (persona)
- **Stato Sede**: "ITALIA"
- **Stato Nas 1**: "ITALIA"
- **Stato Res 1**: "ITALIA"
- **Prest Prof**: "Tenuta della Contabilità"
- **Tipo Ident**: "Diretta"
- **Data Ident**: Data corrente
- **Pep**: "NO"
- **Carica 1**: "TITOLARE" o "RAPPRESENTANTE LEGALE"

## Struttura File Excel

Il file Excel generato contiene:

- **149 colonne totali** (tutte le colonne del template)
- **1 riga di dati** (una riga per ogni combinazione visura+documento)
- **Campi compilati**: Solo i campi per cui sono stati estratti dati
- **Campi vuoti**: Le colonne rimanenti sono presenti ma vuote

## Esempio di Utilizzo

### Workflow Completo

1. **Apri l'app Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Tab "Carica Documento"**:
   - Carica PDF visura camerale → Estrai Dati
   - Carica PDF/foto documento identità → Estrai Dati
   - Clicca "Combina nel Formato Template"

3. **Tab "Risultati"**:
   - Verifica campi compilati e percentuale completamento
   - Visualizza anteprima dati principali
   - Scarica file Excel o CSV

4. **Usa il file**:
   - Il file Excel è pronto per essere importato nel tuo sistema
   - Tutte le colonne del template sono presenti
   - I dati sono su una singola riga

## Elaborazione Batch

Puoi anche processare più documenti contemporaneamente:

1. Nella sezione "Elaborazione Batch", carica più file
2. Clicca "Elabora Tutti i Documenti"
3. Il sistema elabora automaticamente visure e documenti
4. Scarica i risultati nella tab "Risultati"

**Nota**: Il batch crea un file con i dati separati per ogni documento. Per il formato template combinato, usa il caricamento individuale.

## Fallback

Se il file `format_import_template.xlsx` non viene trovato:

- L'app funziona normalmente
- I dati vengono esportati nel formato standard (colonne separate)
- Nessuna funzionalità viene persa

## File Template

Il file `format_import_template.xlsx` deve:

- Trovarsi nella stessa cartella di `streamlit_app.py`
- Avere le colonne nella prima riga
- Non deve necessariamente contenere dati

Il template viene usato solo per leggere la struttura delle colonne.

## Personalizzazione

Per modificare il mapping dei campi, edita la funzione `map_data_to_template()` in `streamlit_app.py` alle righe 228-297.

Esempio per aggiungere un nuovo campo:

```python
row['Tua_Nuova_Colonna'] = visura_data.get('Campo_Estratto', '')
```

## Supporto

Per problemi o domande:

- Apri una issue su GitHub
- Consulta la documentazione principale nel README.md
- Controlla che il template sia nella posizione corretta

## Versione

Template support added in version 2.1 - 2025
