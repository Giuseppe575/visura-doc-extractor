# 🚀 Deploy su Streamlit Cloud - Guida Completa

## 🌐 Cos'è Streamlit Cloud?

Streamlit Cloud è una piattaforma **GRATUITA** per deployare applicazioni Streamlit direttamente da GitHub. 

**Vantaggi:**
- ✅ Completamente gratuito
- ✅ Deploy automatico da GitHub
- ✅ HTTPS incluso
- ✅ Dominio gratuito (.streamlit.app)
- ✅ Aggiornamenti automatici ad ogni commit
- ✅ Nessuna configurazione server necessaria

---

## 📋 Requisiti

1. **Account GitHub** (gratuito)
2. **Account Streamlit Cloud** (gratuito)
3. **Repository su GitHub** con il codice

---

## 🎯 GUIDA PASSO-PASSO

### PASSO 1: Carica il Codice su GitHub

Se non l'hai già fatto, segui la guida in [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md)

**File necessari per Streamlit** (già presenti):
```
document-extractor/
├── streamlit_app.py              ← App principale
├── requirements-streamlit.txt     ← Dipendenze Python
├── packages.txt                   ← Dipendenze sistema (Tesseract)
└── .streamlit/
    └── config.toml                ← Configurazione
```

---

### PASSO 2: Crea Account Streamlit Cloud

1. Vai su **https://streamlit.io/cloud**
2. Clicca su **"Sign up"**
3. Scegli **"Continue with GitHub"**
4. Autorizza Streamlit ad accedere a GitHub
5. Conferma l'email

**Hai 3 app gratuite** con l'account free!

---

### PASSO 3: Deploy dell'App

#### Opzione A: Deploy dalla Dashboard

1. **Accedi a Streamlit Cloud**: https://share.streamlit.io/
2. Clicca su **"New app"**
3. Compila i campi:
   - **Repository**: `tuousername/document-extractor`
   - **Branch**: `main` (o `master`)
   - **Main file path**: `streamlit_app.py`
   - **App URL**: scegli un nome (es: `document-extractor`)
4. Clicca su **"Deploy!"**

#### Opzione B: Deploy Diretto (URL magico)

Vai direttamente su:
```
https://share.streamlit.io/[USERNAME]/document-extractor/main/streamlit_app.py
```

Sostituisci `[USERNAME]` con il tuo username GitHub.

---

### PASSO 4: Attendi il Deploy

Il primo deploy richiede 5-10 minuti perché deve:
- ✅ Clonare il repository
- ✅ Installare Python e dipendenze
- ✅ Installare Tesseract OCR
- ✅ Configurare l'ambiente
- ✅ Avviare l'app

**Vedrai i log in tempo reale!**

---

### PASSO 5: App Online! 🎉

Una volta completato, vedrai:
```
🎈 Your app is live!
URL: https://tuousername-document-extractor-streamlit-app-xxxxx.streamlit.app
```

**L'app è online e accessibile da chiunque!**

---

## 🔧 Configurazione Avanzata

### Secrets Management

Se hai API keys o credenziali:

1. Dashboard → La tua app → **Settings** → **Secrets**
2. Aggiungi secrets in formato TOML:
```toml
[passwords]
admin = "password123"

[api_keys]
openai = "sk-..."
```

3. Accedi nel codice:
```python
import streamlit as st
password = st.secrets["passwords"]["admin"]
```

### Variabili d'Ambiente

Nel file `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
```

---

## 🔄 Aggiornamenti Automatici

**Ogni volta che fai un commit su GitHub, l'app si aggiorna automaticamente!**

```bash
# Modifica il codice
git add streamlit_app.py
git commit -m "Update: migliorata UI"
git push

# Streamlit Cloud rileva il cambiamento e rideploya
```

---

## 🎨 Personalizza il Dominio

### Domini Disponibili

**Gratuito:**
- `tuousername-document-extractor-xxxxx.streamlit.app`

**A Pagamento** (Team Plan - $250/mese):
- Dominio custom: `extractor.tuosito.com`

Per la maggior parte degli usi, il dominio gratuito è più che sufficiente!

---

## 📊 Monitoraggio

### Dashboard Streamlit Cloud

Nella dashboard puoi vedere:
- **Logs**: Errori e output dell'app
- **Analytics**: Visite e utilizzo (se abilitato)
- **Metrics**: CPU, memoria, traffico
- **Settings**: Configurazione e secrets

### Accesso ai Logs

1. Dashboard → La tua app → **Manage app**
2. Tab **Logs** per vedere output in tempo reale
3. Utile per debugging!

---

## 🐛 Risoluzione Problemi

### Errore: "ModuleNotFoundError"

**Soluzione**: Aggiungi il modulo a `requirements-streamlit.txt`
```bash
# Aggiungi la libreria mancante
echo "nome-libreria==versione" >> requirements-streamlit.txt
git add requirements-streamlit.txt
git commit -m "Fix: aggiunta dipendenza"
git push
```

### Errore: "Tesseract not found"

**Soluzione**: Verifica che `packages.txt` contenga:
```
tesseract-ocr
tesseract-ocr-ita
```

### App Lenta o Timeout

**Cause comuni:**
- File troppo grandi (limite: 200MB)
- Troppe elaborazioni contemporanee
- OCR su immagini molto grandi

**Soluzioni:**
- Aggiungi caching con `@st.cache_data`
- Ridimensiona immagini prima dell'OCR
- Limita dimensione upload

### Errore: "App failed to load"

**Soluzioni:**
1. Controlla i logs nella dashboard
2. Verifica che `streamlit_app.py` sia nella root del repo
3. Testa in locale: `streamlit run streamlit_app.py`
4. Verifica che tutte le dipendenze siano corrette

---

## 💰 Limiti Free Plan

| Risorsa | Limite Free | Note |
|---------|-------------|------|
| App | 3 app pubbliche | Sufficienti per test |
| Memoria | 1 GB RAM | OK per uso normale |
| CPU | Condivisa | Performance OK |
| Upload | 200 MB | Per singolo file |
| Traffico | Illimitato | 🎉 |
| Storage | No persistenza | Usa database esterno se serve |

**Per uso professionale intensivo**: considera l'upgrade a Team ($250/mese)

---

## 🔒 Privacy e Sicurezza

### Dati Sensibili

**IMPORTANTE**: I file caricati dagli utenti vengono elaborati sul server Streamlit!

**Best Practices:**
- ✅ Avvisa gli utenti di NON caricare documenti reali in produzione
- ✅ Usa per test e demo
- ✅ Per dati reali, deploya su server privato (vedi sezione Docker)
- ✅ Non salvare file caricati dagli utenti

### Autenticazione

Streamlit Cloud non ha autenticazione built-in. Opzioni:

1. **Streamlit-authenticator** (libreria community)
2. **Google OAuth** (tramite secrets)
3. **Password semplice** (per uso interno)

Esempio password semplice:
```python
password = st.text_input("Password", type="password")
if password != st.secrets["passwords"]["admin"]:
    st.stop()
```

---

## 🚀 Alternative a Streamlit Cloud

Se Streamlit Cloud non è adatto:

### 1. **Heroku** (Free tier rimosso, da $5/mese)
- Pro: Più controllo, database incluso
- Contro: A pagamento, setup più complesso

### 2. **Railway** (Free $5 credito/mese)
- Pro: Facile come Streamlit, più risorse
- Contro: Credito limitato

### 3. **Render** (Free plan disponibile)
- Pro: Gratuito, buone performance
- Contro: Sleeping dopo inattività

### 4. **Docker su VPS** (da $5/mese - DigitalOcean, Linode)
- Pro: Massimo controllo, privacy totale
- Contro: Richiede conoscenze DevOps

---

## 📱 Test in Locale Prima del Deploy

**Sempre testa in locale prima!**

```bash
# Installa dipendenze
pip install -r requirements-streamlit.txt

# Installa Tesseract (vedi README.md per il tuo OS)

# Avvia l'app
streamlit run streamlit_app.py

# Apri browser su http://localhost:8501
```

---

## 🎯 Checklist Pre-Deploy

Verifica prima di deployare:

- [ ] `streamlit_app.py` testato in locale
- [ ] `requirements-streamlit.txt` completo
- [ ] `packages.txt` con Tesseract
- [ ] `.streamlit/config.toml` configurato
- [ ] Repository su GitHub aggiornato
- [ ] Branch `main` o `master` esistente
- [ ] README.md aggiornato con URL app
- [ ] File di test preparati

---

## 📖 Risorse Utili

- **Documentazione Streamlit**: https://docs.streamlit.io/
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **Gallery (Esempi)**: https://streamlit.io/gallery
- **GitHub Issues**: Per bug di Streamlit stesso

---

## 🎊 Dopo il Deploy

### Cosa fare dopo che l'app è online:

1. **Testa tutte le funzionalità**
   - Carica file di test
   - Prova export Excel e CSV
   - Verifica elaborazione batch

2. **Condividi il link**
   - Con colleghi per feedback
   - Su LinkedIn/Twitter per visibilità
   - Nel tuo portfolio

3. **Monitora i logs**
   - Controlla per errori
   - Ottimizza performance se necessario

4. **Aggiungi al README**
   - Badge "Deploy on Streamlit"
   - Link all'app live

5. **Raccogli feedback**
   - Crea form per suggerimenti
   - GitHub Issues per bug reports

---

## 🎁 Badge per il README

Aggiungi al README.md:

```markdown
## 🌐 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tuousername-document-extractor.streamlit.app)

Prova l'app online: [document-extractor.streamlit.app](https://tuousername-document-extractor.streamlit.app)
```

---

## ✅ Conclusione

Con Streamlit Cloud hai:
- ✅ App web professionale
- ✅ Hosting gratuito
- ✅ Deploy automatico
- ✅ HTTPS e dominio inclusi
- ✅ Zero configurazione server

**Perfetto per demo, prototipi e progetti personali!**

Per uso aziendale con dati sensibili, considera il deploy Docker su server privato.

---

**Buon Deploy! 🚀**

*Se hai problemi, controlla prima i logs nella dashboard Streamlit Cloud.*
