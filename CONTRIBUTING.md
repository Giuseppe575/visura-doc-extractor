# 🤝 Contributing to Document Extractor

Grazie per il tuo interesse nel contribuire a Document Extractor! 

## Come Contribuire

### Segnalare Bug

Se trovi un bug, apri un [Issue](https://github.com/TUO_USERNAME/document-extractor/issues) includendo:

- **Descrizione del problema**: Cosa ti aspettavi e cosa è successo invece
- **Passi per riprodurre**: Come possiamo replicare il bug
- **Ambiente**: Sistema operativo, versione Python, versione Tesseract
- **Screenshot**: Se applicabile
- **File di esempio**: Se possibile (rimuovi dati sensibili!)

### Proporre Nuove Funzionalità

Hai un'idea per migliorare l'app? Fantastico!

1. Controlla prima nelle [Issues](https://github.com/TUO_USERNAME/document-extractor/issues) se qualcuno l'ha già proposta
2. Se no, apri una nuova Issue con:
   - Descrizione della funzionalità
   - Perché sarebbe utile
   - Come dovrebbe funzionare

### Contribuire con Codice

#### Setup Ambiente di Sviluppo

```bash
# Clona il repository
git clone https://github.com/TUO_USERNAME/document-extractor.git
cd document-extractor

# Crea un virtual environment
python -m venv venv

# Attiva il virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

#### Flusso di Lavoro

1. **Fork** del repository
2. Crea un **branch** per la tua feature: `git checkout -b feature/nome-feature`
3. **Sviluppa** e testa le tue modifiche
4. **Commit** con messaggi descrittivi: `git commit -m "Add: nuova funzionalità X"`
5. **Push** al tuo fork: `git push origin feature/nome-feature`
6. Apri una **Pull Request**

#### Linee Guida per il Codice

- **PEP 8**: Segui le convenzioni Python
- **Commenti**: Commenta codice complesso
- **Docstrings**: Documenta funzioni e classi
- **Test**: Testa le tue modifiche prima di committare
- **Italiano**: Mantieni commenti e UI in italiano per coerenza

#### Convenzioni Commit

Usa prefissi descrittivi:

- `Add:` - Nuove funzionalità
- `Fix:` - Correzioni bug
- `Update:` - Aggiornamenti
- `Remove:` - Rimozioni
- `Docs:` - Documentazione
- `Style:` - Formattazione codice
- `Refactor:` - Ristrutturazione codice

Esempio: `Fix: corretto problema estrazione P.IVA da visure PDF`

## Aree di Contributo

### 🐛 Bug Fix
- Correzione problemi di estrazione
- Miglioramento compatibilità OCR
- Fix interfaccia grafica

### ✨ Nuove Funzionalità
- Supporto per nuovi tipi di documenti
- Integrazione con altri formati (JSON, XML)
- Export in altri formati
- Validazione dati estratti

### 📚 Documentazione
- Migliorare README
- Aggiungere tutorial
- Traduzione in altre lingue
- Video tutorial

### 🧪 Testing
- Creare test automatizzati
- Test con diversi formati documenti
- Test cross-platform

### 🎨 UI/UX
- Migliorare interfaccia grafica
- Aggiungere temi
- Migliorare accessibilità

## Priorità

**Alta priorità**:
- 🔴 Miglioramento accuratezza estrazione dati
- 🔴 Supporto per più formati di visura
- 🔴 Validazione campi estratti

**Media priorità**:
- 🟡 Interfaccia più moderna
- 🟡 Export in più formati
- 🟡 Logging e debugging

**Bassa priorità**:
- 🟢 Temi personalizzabili
- 🟢 Internazionalizzazione
- 🟢 Plugin system

## Codice di Condotta

- Sii rispettoso
- Accetta critiche costruttive
- Focalizzati su ciò che è meglio per il progetto
- Mostra empatia verso gli altri

## Domande?

Non esitare a:
- Aprire una [Issue](https://github.com/TUO_USERNAME/document-extractor/issues)
- Partecipare alle [Discussions](https://github.com/TUO_USERNAME/document-extractor/discussions)

---

**Grazie per il tuo contributo! 🙏**
