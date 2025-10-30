#!/bin/bash
# COMANDI RAPIDI PER UPLOAD SU GITHUB

# ==================================================
# PARTE 1: CREA IL REPOSITORY SU GITHUB
# ==================================================
# 1. Vai su: https://github.com/new
# 2. Repository name: document-extractor
# 3. Description: Applicazione per estrazione dati da Visure e Documenti
# 4. Public o Private (a tua scelta)
# 5. NON selezionare "Add a README file"
# 6. NON selezionare "Add .gitignore"
# 7. NON selezionare "Choose a license"
# 8. Clicca "Create repository"

# ==================================================
# PARTE 2: COLLEGA E CARICA (COPIA E INCOLLA QUESTI COMANDI)
# ==================================================

# Sostituisci TUO_USERNAME con il tuo username GitHub!

# Per Windows (PowerShell o CMD):
# --------------------------------
cd C:\percorso\document-extractor
git remote add origin https://github.com/TUO_USERNAME/document-extractor.git
git branch -M main
git push -u origin main


# Per macOS/Linux:
# ----------------
cd /percorso/document-extractor
git remote add origin https://github.com/TUO_USERNAME/document-extractor.git
git branch -M main
git push -u origin main


# ==================================================
# CREDENZIALI RICHIESTE
# ==================================================
# Username: TUO_USERNAME
# Password: IL_TUO_PERSONAL_ACCESS_TOKEN (NON la password!)

# ==================================================
# CREARE PERSONAL ACCESS TOKEN
# ==================================================
# 1. Vai su: https://github.com/settings/tokens
# 2. Click "Generate new token" → "Generate new token (classic)"
# 3. Nome: "Document Extractor Upload"
# 4. Expiration: 90 days (o No expiration)
# 5. Seleziona scope: ✅ repo (tutti i permessi sotto repo)
# 6. Click "Generate token"
# 7. COPIA IL TOKEN (lo vedrai solo questa volta!)
# 8. Salvalo in un posto sicuro

# ==================================================
# VERIFICA UPLOAD
# ==================================================
# Dopo aver pushato, vai su:
# https://github.com/TUO_USERNAME/document-extractor
# Dovresti vedere tutti i file!

# ==================================================
# COMANDI UTILI POST-UPLOAD
# ==================================================

# Vedere lo stato
git status

# Vedere i commit
git log --oneline

# Vedere il remote
git remote -v

# Aggiornare dopo modifiche
git add .
git commit -m "Descrizione modifiche"
git push

# ==================================================
# RISOLUZIONE PROBLEMI
# ==================================================

# Se "origin already exists":
git remote remove origin
git remote add origin https://github.com/TUO_USERNAME/document-extractor.git

# Se "permission denied":
# Usa il Personal Access Token come password!

# Se "repository not found":
# Verifica di aver creato il repository su GitHub
# Verifica l'URL: https://github.com/TUO_USERNAME/document-extractor

# ==================================================
# ALTRE OPZIONI
# ==================================================

# Opzione 1: GitHub Desktop (più facile)
# Scarica: https://desktop.github.com/
# 1. File → Add local repository
# 2. Seleziona questa cartella
# 3. Publish repository

# Opzione 2: GitHub CLI
gh repo create document-extractor --public --source=. --remote=origin --push

# ==================================================
# FINE
# ==================================================

echo "Repository pronto per l'upload!"
echo "Segui le istruzioni nel file GITHUB_UPLOAD.md per i dettagli completi"
