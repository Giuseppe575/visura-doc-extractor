"""
Document Extractor - Streamlit Web App
Applicazione web per l'estrazione di dati da Visure Camerali e Documenti d'Identità
"""

import streamlit as st
import pandas as pd
import PyPDF2
from PIL import Image
import pytesseract
import re
from datetime import datetime
import io
import base64
from pathlib import Path

# Configurazione pagina
st.set_page_config(
    page_title="Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        margin: 1rem 0;
    }
    .data-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DocumentExtractor:
    """Classe per l'estrazione dati da documenti"""
    
    def __init__(self):
        self.data = {}
    
    def extract_text_from_pdf(self, file):
        """Estrae il testo da un file PDF"""
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Errore nell'estrazione dal PDF: {str(e)}")
            return ""
    
    def extract_text_from_image(self, image):
        """Estrae il testo da un'immagine usando OCR"""
        try:
            # Preprocessing dell'immagine per migliorare l'OCR
            # Converti in scala di grigi se necessario
            if image.mode != 'L':
                image = image.convert('L')

            # Configurazione OCR per migliore estrazione
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='ita', config=custom_config)
            return text
        except Exception as e:
            st.error(f"Errore nell'OCR: {str(e)}")
            st.warning("⚠️ Assicurati che Tesseract OCR sia installato sul server")
            return ""
    
    def extract_pattern(self, text, pattern):
        """Estrae un pattern dal testo usando regex"""
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if not match:
            return None
        # Prova tutti i gruppi e ritorna il primo non-None
        for i in range(1, len(match.groups()) + 1):
            if match.group(i):
                return match.group(i).strip()
        return None
    
    def parse_visura_camerale(self, text):
        """Analizza il testo della visura camerale ed estrae i dati"""
        data = {}

        # DENOMINAZIONE / RAGIONE SOCIALE (multipli pattern)
        denominazione_patterns = [
            r"(?:Denominazione|DENOMINAZIONE)[:\s]*\n?\s*([A-Z][A-Z\s'\.]+(?:S\.R\.L\.|SRL|S\.P\.A\.|SPA|S\.A\.S\.|SAS|SRLS|S\.R\.L\.S\.|SOCIETA'[^\n]+)?)",
            r"(?:Ragione\s+sociale|RAGIONE\s+SOCIALE)[:\s]*\n?\s*([A-Z][^\n]+)",
            r"^([A-Z][A-Z\s'\.]+(?:S\.R\.L\.|SRL|S\.P\.A\.|SOCIETA')[^\n]{0,100})",  # All'inizio del testo
            r"VISURA.*?\n+([A-Z][A-Z\s'\.]+(?:SOCIETA|S\.R\.L\.|SRL)[^\n]+)",
        ]
        for pattern in denominazione_patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match and not data.get('Denominazione'):
                denominazione = match.group(1).strip()
                # Pulisci eventuali artefatti
                denominazione = re.sub(r'\s+', ' ', denominazione)
                # Rimuovi caratteri speciali finali
                denominazione = re.sub(r'[,\.\-]+$', '', denominazione)
                if len(denominazione) > 3:
                    data['Denominazione'] = denominazione
                    break

        # PARTITA IVA (multipli pattern)
        piva_patterns = [
            r"(?:Partita\s+IVA|P\.?\s*IVA|PARTITA\s+IVA)[:\s]*\n?\s*(\d{11})",
            r"(?:P\.IVA|PIVA)[:\s]+(\d{11})",
            r"IVA[:\s]*(\d{11})",
        ]
        for pattern in piva_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Partita_IVA'):
                data['Partita_IVA'] = match.group(1)
                break

        # CODICE FISCALE (multipli pattern)
        cf_patterns = [
            r"(?:Codice\s+[Ff]iscale|C\.?\s*F\.?|CF)[:\s]*\n?\s*([A-Z0-9]{11,16})",
            r"(?:Codice\s+fiscale\s+e\s+n\.?\s*iscr)[^\n]*[:\s]*(\d{11})",
            r"(\d{11})(?:\s|$)",  # 11 cifre da sole
        ]
        for pattern in cf_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Codice_Fiscale'):
                cf = match.group(1)
                # Verifica che sia lungo 11 o 16 caratteri
                if len(cf) in [11, 16]:
                    data['Codice_Fiscale'] = cf
                    break

        # NUMERO REA (multipli pattern)
        rea_patterns = [
            r"(?:Numero\s+REA|N\.?\s*REA|REA)[:\s]*\n?\s*([A-Z]{2})[\s\-]*(\d+)",
            r"REA[:\s]*([A-Z]{2})\s*-\s*(\d+)",
            r"(?:Repertorio\s+[Ee]conomico)[^\n]*[:\s]*([A-Z]{2})\s*[\-\s]*(\d+)",
        ]
        for pattern in rea_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Numero_REA'):
                if len(match.groups()) == 2:
                    data['Numero_REA'] = f"{match.group(1)} - {match.group(2)}"
                else:
                    data['Numero_REA'] = match.group(1)
                break

        # FORMA GIURIDICA (multipli pattern)
        forma_patterns = [
            r"(?:Forma\s+giuridica|Natura\s+giuridica)[:\s]*\n?\s*([a-z\s']+(?:limitata|semplificata|per azioni|società|s\.r\.l\.|s\.p\.a\.)[^\n]*)",
            r"(?:FORMA\s+GIURIDICA)[:\s]*\n?\s*([^\n]+)",
            r"(società\s+a\s+responsabilità\s+limitata[^\n]*)",
            r"(SOCIETA'?\s+A\s+RESPONSABILITA'?\s+LIMITATA[^\n]*)",
        ]
        for pattern in forma_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Forma_Giuridica'):
                forma = match.group(1).strip()
                forma = re.sub(r'\s+', ' ', forma)
                if len(forma) > 3:
                    data['Forma_Giuridica'] = forma
                    break

        # SEDE LEGALE con indirizzo completo
        sede_patterns = [
            r"(?:Sede\s+legale|Indirizzo\s+[Ss]ede)[:\s]*\n?\s*([A-Z][^\n]+?)(?:CAP\s*\d{5}|\n|$)",
            r"(?:Indirizzo)[:\s]*([^\n]+?)(?:\d{5})",
            r"(?:VIA|VIALE|PIAZZA|CORSO)\s+([A-Z][^\n]+?)(?:\s+\d{5})",
        ]
        for pattern in sede_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Sede_Legale'):
                sede = match.group(1).strip()
                # Pulisci
                sede = re.sub(r'\s+', ' ', sede)
                sede = re.sub(r'CAP.*$', '', sede)
                if len(sede) > 5:
                    data['Sede_Legale'] = sede
                    break

        # CAP
        cap_patterns = [
            r"(?:CAP|Cap)[:\s]*(\d{5})",
            r"(?:^|\s)(\d{5})(?:\s+[A-Z][A-Za-z]+\s*\([A-Z]{2}\))",
        ]
        for pattern in cap_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match and not data.get('CAP'):
                data['CAP'] = match.group(1)
                break

        # COMUNE (multipli pattern)
        comune_patterns = [
            r"\d{5}\s*[-,]?\s*([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})(?:\s*\(|\s*[-,]?\s*\(?[A-Z]{2}\)?)",
            r"(?:Comune)[:\s]+([A-Z][A-Za-z\s]+?)(?:\s*\([A-Z]{2}\)|\n|$)",
            r"([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})\s*\([A-Z]{2}\)",
        ]
        for pattern in comune_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match and not data.get('Comune'):
                comune = match.group(1).strip()
                # Valida che non contenga parole non valide
                invalid = ['NUMERO', 'REPERTORIO', 'REA', 'AMMINISTRATIVO', 'ATTIVITA', 'REGISTRO']
                if not any(word in comune.upper() for word in invalid) and len(comune) > 2:
                    data['Comune'] = comune
                    break

        # PROVINCIA
        prov_patterns = [
            r"\(([A-Z]{2})\)",
            r"(?:Provincia|Prov\.?)[:\s]*\(?\s*([A-Z]{2})\s*\)?",
            r"(?:Sigla)[:\s]*([A-Z]{2})",
        ]
        for pattern in prov_patterns:
            match = re.search(pattern, text)
            if match and not data.get('Provincia'):
                data['Provincia'] = match.group(1)
                break

        # DATA COSTITUZIONE / ISCRIZIONE
        data_cost_patterns = [
            r"(?:Data\s+atto\s+di\s+costituzione|Data\s+costituzione)[:\s]*\n?\s*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
            r"(?:Data\s+iscrizione|Data\s+di\s+iscrizione)[:\s]*\n?\s*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
            r"(?:Costituita\s+il)[:\s]*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
        ]
        for pattern in data_cost_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Data_Costituzione'):
                data['Data_Costituzione'] = match.group(1)
                break

        # DATA INIZIO ATTIVITÀ
        data_inizio_patterns = [
            r"(?:Data\s+inizio\s+attività|Data\s+inizio\s+attivit[aà])[:\s]*\n?\s*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
            r"(?:Inizio\s+attività)[:\s]*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
        ]
        for pattern in data_inizio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Data_Inizio_Attivita'):
                data['Data_Inizio_Attivita'] = match.group(1)
                break

        # CAPITALE SOCIALE
        capitale_patterns = [
            r"(?:Capitale\s+sociale)[:\s]*\n?\s*(?:€|EUR|Euro)?\s*([\d\.,]+)",
            r"(?:Capitale)[:\s]+(?:€|EUR)?\s*([\d\.,]+)",
            r"(?:sottoscritto|versato)[:\s]*(?:€)?\s*([\d\.,]+)",
        ]
        for pattern in capitale_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Capitale_Sociale'):
                data['Capitale_Sociale'] = match.group(1)
                break

        # STATO ATTIVITÀ
        stato_patterns = [
            r"(?:Stato\s+attività|Stato)[:\s]*\n?\s*(ATTIVA|ATTIVO|CESSATA|CESSATO|SOSPESA|SOSPESO)",
            r"(?:stato)[:\s]+(attiva|cessata|sospesa)",
        ]
        for pattern in stato_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Stato_Attivita'):
                data['Stato_Attivita'] = match.group(1).upper()
                break

        # CODICE ATECO (IMPORTANTE!)
        ateco_patterns = [
            r"(?:Codice\s+ATECO|ATECO|Cod\.\s*ATECO)[:\s]*\n?\s*(\d{2}\.\d{2}\.\d{1,2})",
            r"(?:Attività\s+prevalente).*?(\d{2}\.\d{2}\.\d{1,2})",
            r"ATECO[:\s]+(\d{2}\.\d{2}\.\d{1,2})",
            r"(\d{2}\.\d{2}\.\d{1,2})",  # Pattern generico per codici
        ]
        for pattern in ateco_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match and not data.get('Codice_ATECO'):
                ateco = match.group(1)
                # Verifica che sia un formato valido (XX.XX.X o XX.XX.XX)
                if re.match(r'\d{2}\.\d{2}\.\d{1,2}', ateco):
                    data['Codice_ATECO'] = ateco
                    break

        # ATTIVITÀ PREVALENTE (descrizione)
        attivita_patterns = [
            r"(?:Attività\s+prevalente)[:\s]*\n?\s*([a-z][a-z\s,]+(?:prodotti|servizi|commercio|produzione|vendita|gestione)[^\n]{0,150})",
            r"(?:ATTIVITA'?\s+PREVALENTE)[:\s]*([^\n]+)",
            r"(?:Oggetto\s+sociale)[:\s]*([A-Z][^\n]{20,200})",
        ]
        for pattern in attivita_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Attivita_Prevalente'):
                attivita = match.group(1).strip()
                attivita = re.sub(r'\s+', ' ', attivita)
                if len(attivita) > 10:
                    data['Attivita_Prevalente'] = attivita[:200]  # Max 200 caratteri
                    break

        # AMMINISTRATORE / LEGALE RAPPRESENTANTE (NUOVO!)
        amministratore_patterns = [
            r"(?:Amministratore\s+[Uu]nico|AMMINISTRATORE\s+UNICO)[:\s]*\n?\s*([A-Z][A-Z\s]+)",
            r"(?:Legale\s+[Rr]appresentante|LEGALE\s+RAPPRESENTANTE)[:\s]*\n?\s*([A-Z][A-Z\s]+)",
            r"(?:Rappresentante\s+dell'?impresa)[:\s]*\n?\s*([A-Z][A-Z\s]+)",
            r"(?:Presidente)[:\s]*\n?\s*([A-Z][A-Z\s]+)",
        ]
        for pattern in amministratore_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match and not data.get('Amministratore'):
                amm = match.group(1).strip()
                # Pulisci da caratteri extra
                amm = re.sub(r'\s+', ' ', amm)
                # Estrai nome e cognome se possibile
                parts = amm.split()
                if len(parts) >= 2:
                    data['Amministratore'] = amm
                    data['Amministratore_Cognome'] = parts[0]
                    data['Amministratore_Nome'] = ' '.join(parts[1:])
                else:
                    data['Amministratore'] = amm
                break

        # SOCI / TITOLARI (NUOVO!)
        # Cerca pattern tipo "Soci e titolari: 1" o simili
        soci_numero_patterns = [
            r"(?:Soci\s+e\s+titolari)[^\n]*[:\s]+(\d+)",
            r"(?:Numero\s+soci)[:\s]+(\d+)",
        ]
        for pattern in soci_numero_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Numero_Soci'):
                data['Numero_Soci'] = match.group(1)
                break

        # Cerca nomi dei soci (più complesso)
        # Pattern per sezioni soci
        soci_section_pattern = r"(?:Soci\s+e\s+titolari|SOCI|Elenco\s+soci)(.*?)(?:\n\n|\Z)"
        match = re.search(soci_section_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            soci_text = match.group(1)
            # Cerca nomi (pattern approssimativo)
            soci_names = re.findall(r"([A-Z][A-Z]+)\s+([A-Z][a-z]+)", soci_text)
            if soci_names:
                data['Soci'] = '; '.join([f"{cognome} {nome}" for cognome, nome in soci_names[:5]])  # Max 5 soci

        return data
    
    def parse_documento_identita(self, text):
        """Analizza il testo del documento d'identità ed estrae i dati"""
        data = {}

        # Normalizza il testo per facilitare matching
        text_clean = text.replace('\n', ' ').replace('  ', ' ')

        # Pattern multipli per ogni campo (più flessibili)

        # CODICE FISCALE (priorità alta - più affidabile)
        cf_patterns = [
            r"([A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])",  # Standard
            r"(?:CF|C\.F\.|Codice\s*Fiscale)[:\s]*([A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])",
        ]
        for pattern in cf_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['CF_Persona'] = match.group(1) if len(match.groups()) == 1 else match.group(2)
                break

        # COGNOME (multipli pattern)
        cognome_patterns = [
            r"(?:Cognome|COGNOME|Surname)[:\s]+([A-Z][A-Z\s]+?)(?:\s+Nome|\s+NOME|\s+Name|\n)",
            r"(?:Cognome|COGNOME)[:\s]*\n+([A-Z][A-Z\s]+)",
            r"^([A-Z]{2,}(?:\s+[A-Z]{2,})*)\s+(?:[A-Z][a-z]+|NOME)",  # ROSSI Mario
        ]
        for pattern in cognome_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match and not data.get('Cognome'):
                data['Cognome'] = match.group(1).strip()
                break

        # NOME (multipli pattern)
        nome_patterns = [
            r"(?:Nome|NOME|Name)[:\s]+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)",
            r"(?:Cognome|COGNOME)[^\n]+\n+(?:Nome|NOME)[:\s]*\n*([A-Z][A-Za-z]+)",
            r"[A-Z]{2,}\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:nato|Nat)",  # ROSSI Mario nato
        ]
        for pattern in nome_patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match and not data.get('Nome'):
                data['Nome'] = match.group(1).strip()
                break

        # DATA DI NASCITA (molto flessibile)
        data_nascita_patterns = [
            r"(?:nat[oa]\s+il|Data\s+di\s+nascita|Date\s+of\s+birth)[:\s]*(\d{1,2}[/\.\-\s]\d{1,2}[/\.\-\s]\d{2,4})",
            r"(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",  # Qualsiasi data
            r"(?:il|del)\s+(\d{1,2}[/\.\-\s]\d{1,2}[/\.\-\s]\d{2,4})",
        ]
        for pattern in data_nascita_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Data_Nascita'):
                date_str = match.group(1).strip()
                # Normalizza la data
                date_str = re.sub(r'[/\.\-\s]+', '/', date_str)
                # Se anno a 2 cifre, converti a 4
                parts = date_str.split('/')
                if len(parts) == 3 and len(parts[2]) == 2:
                    year = int(parts[2])
                    parts[2] = f"19{year}" if year > 30 else f"20{year}"
                    date_str = '/'.join(parts)
                data['Data_Nascita'] = date_str
                break

        # LUOGO DI NASCITA
        luogo_patterns = [
            r"(?:nat[oa]\s+a|nato\s+il\s+\d+[/\-\.]\d+[/\-\.]\d+\s+a)\s+([A-Z][A-Za-z\s']+?)(?:\s*\([A-Z]{2}\)|$|\s+il|\s+\d)",
            r"(?:Luogo\s+di\s+nascita|Place\s+of\s+birth)[:\s]*([A-Z][A-Za-z\s']+?)(?:\s*\(|$|\n)",
            r"(?:Comune\s+di\s+nascita)[:\s]*([A-Z][A-Za-z\s']+)",
        ]
        for pattern in luogo_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Luogo_Nascita'):
                luogo = match.group(1).strip()
                # Rimuovi date se catturate per errore
                luogo = re.sub(r'\d+[/\-\.]\d+[/\-\.]\d+', '', luogo).strip()
                if luogo and len(luogo) > 2:
                    data['Luogo_Nascita'] = luogo
                break

        # PROVINCIA NASCITA
        prov_patterns = [
            r"(?:nat[oa]\s+a)[^\n]*\(([A-Z]{2})\)",
            r"([A-Z]{2})\s*\)\s*il\s+\d",
            r"\(\s*([A-Z]{2})\s*\)",
        ]
        for pattern in prov_patterns:
            match = re.search(pattern, text)
            if match and not data.get('Provincia_Nascita'):
                data['Provincia_Nascita'] = match.group(1)
                break

        # SESSO
        sesso_patterns = [
            r"(?:Sesso|Sex)[:\s]*([MF])",
            r"\b([MF])\b(?:\s+\d{3}\s+cm|\s+nat)",  # M 180 cm o M nato
        ]
        for pattern in sesso_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Sesso'):
                data['Sesso'] = match.group(1).upper()
                break

        # STATURA
        statura_patterns = [
            r"(?:Statura|Height)[:\s]*(\d{2,3})\s*(?:cm)?",
            r"([MF])\s+(\d{3})\s*cm",  # M 180 cm
            r"(\d{3})\s*cm",
        ]
        for pattern in statura_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Statura'):
                statura = match.group(2) if len(match.groups()) > 1 else match.group(1)
                data['Statura'] = statura
                break

        # CITTADINANZA
        if 'ITALIANA' in text.upper() or 'ITALY' in text.upper():
            data['Cittadinanza'] = 'ITALIANA'

        # RESIDENZA (pattern semplificato)
        residenza_patterns = [
            r"(?:Residenza|Residence)[:\s]*([A-Z][A-Za-z0-9\s,\.'-]+?)(?:\n\n|Rilasciat)",
            r"(?:Via|Viale|Piazza|Corso)\s+([A-Za-z0-9\s,\.'-]+?)(?:\d{5}|\n)",
        ]
        for pattern in residenza_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Residenza'):
                data['Residenza'] = match.group(1).strip()
                break

        # COMUNE RESIDENZA
        comune_res_patterns = [
            r"(?:Comune)[:\s]*([A-Z][A-Za-z\s]+?)(?:\s*\(|$|\n)",
            r"\d{5}\s+([A-Z][A-Za-z\s]+?)(?:\s*\([A-Z]{2}\)|$)",
        ]
        for pattern in comune_res_patterns:
            match = re.search(pattern, text)
            if match and not data.get('Comune_Residenza'):
                data['Comune_Residenza'] = match.group(1).strip()
                break

        # NUMERO DOCUMENTO (CI elettronica formato: CA12345AA o simili)
        numero_patterns = [
            r"(?:N\.|Numero|Nr)[:\s]*([A-Z]{2}\s*\d{5,7}\s*[A-Z]{0,2})",
            r"([A-Z]{2}\d{5,7}[A-Z]{0,2})",  # CA12345AA
            r"Carta\s+d[''i]?\s*identit[aà]\s+(?:N\.?|n\.?)\s*([A-Z0-9]{6,10})",
        ]
        for pattern in numero_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Numero_Documento'):
                numero = match.group(1).replace(' ', '')
                data['Numero_Documento'] = numero
                break

        # DATA RILASCIO
        rilascio_patterns = [
            r"(?:Rilasciat[oa]\s+il|Emess[oa]\s+il|Data\s+di\s+rilascio)[:\s]*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{2,4})",
            r"(?:del|il)\s+(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
        ]
        for pattern in rilascio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Data_Rilascio'):
                data['Data_Rilascio'] = re.sub(r'[/\.\-\s]+', '/', match.group(1))
                break

        # DATA SCADENZA
        scadenza_patterns = [
            r"(?:Scadenza|valida\s+fino\s+al)[:\s]*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{2,4})",
            r"(?:Valid until|Date of expiry)[:\s]*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{2,4})",
        ]
        for pattern in scadenza_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Data_Scadenza'):
                data['Data_Scadenza'] = re.sub(r'[/\.\-\s]+', '/', match.group(1))
                break

        # COMUNE RILASCIO
        comune_rilascio_patterns = [
            r"(?:Comune\s+di|Rilasciat[oa]\s+da)[:\s]*([A-Z][A-Za-z\s]+?)(?:\s*\n|$|il)",
            r"(?:Sindaco\s+del\s+Comune\s+di)[:\s]*([A-Z][A-Za-z\s]+)",
        ]
        for pattern in comune_rilascio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and not data.get('Comune_Rilascio'):
                data['Comune_Rilascio'] = match.group(1).strip()
                break

        # TIPO DOCUMENTO
        if any(keyword in text.upper() for keyword in ['CARTA', 'IDENTITA', 'IDENTITY']):
            data['Tipo_Documento'] = "CARTA D'IDENTITA"
        elif 'PATENTE' in text.upper():
            data['Tipo_Documento'] = 'PATENTE'
        elif 'PASSAPORTO' in text.upper() or 'PASSPORT' in text.upper():
            data['Tipo_Documento'] = 'PASSAPORTO'

        return data
    
    def is_visura_camerale(self, text):
        """Determina se il testo è di una visura camerale"""
        keywords = ['camera di commercio', 'visura', 'rea', 'partita iva']
        text_lower = text.lower()
        return sum(1 for keyword in keywords if keyword in text_lower) >= 2
    
    def is_documento_identita(self, text):
        """Determina se il testo è di un documento d'identità"""
        keywords = [
            'carta identita', 'identity card', 'patente', 'passaporto',
            'documento', 'rilasciato', 'luogo di nascita', 'data di nascita',
            'residenza', 'comune di', 'cittadinanza', 'codice fiscale'
        ]
        text_lower = text.lower()
        return sum(1 for keyword in keywords if keyword in text_lower) >= 2

def load_template():
    """Carica il template Excel"""
    template_path = Path(__file__).parent / "format_import_template.xlsx"
    try:
        if template_path.exists():
            df = pd.read_excel(template_path)
            return df.columns.tolist()
        return None
    except Exception as e:
        st.error(f"Errore nel caricamento del template: {e}")
        return None

def map_data_to_template(visura_data, documento_data):
    """Mappa i dati estratti alle colonne del template"""
    # Carica le colonne del template
    template_columns = load_template()

    # Se il template non esiste, usa il formato standard
    if not template_columns:
        # Combina i dati in formato standard
        combined = {**visura_data, **documento_data}
        return pd.DataFrame([combined])

    # Inizializza riga con tutte le colonne a None
    row = {col: None for col in template_columns}

    # Mappa dati della visura
    if visura_data:
        row['Pers Soc'] = 'S' if visura_data.get('Denominazione') else 'P'
        row['Ragionesociale'] = visura_data.get('Denominazione', '')
        row['Intestazione'] = visura_data.get('Denominazione', '')
        row['Natura Giuridica'] = visura_data.get('Forma_Giuridica', '')
        row['Codfisc Azienda'] = visura_data.get('Codice_Fiscale', '')
        row['Partita Iva Azienda'] = visura_data.get('Partita_IVA', '')
        row['Cciaa'] = visura_data.get('Numero_REA', '')
        row['Cod Ateco'] = visura_data.get('Codice_ATECO', '')  # AGGIUNTO
        row['Attivita'] = visura_data.get('Attivita_Prevalente', '')  # AGGIUNTO
        row['Indirizzo Sede'] = visura_data.get('Sede_Legale', '')
        row['Comune Sede'] = visura_data.get('Comune', '')
        row['Cap Sede'] = visura_data.get('CAP', '')
        row['Prov Sede'] = visura_data.get('Provincia', '')
        row['Stato Sede'] = 'ITALIA'
        row['Data Ini Rapporto'] = visura_data.get('Data_Costituzione', '')
        row['Prest Prof'] = 'Tenuta della Contabilità'
        row['Tipo Ident'] = 'Diretta'
        row['Data Ident'] = datetime.now().strftime('%Y-%m-%d')
        row['Pep'] = 'NO'

    # Mappa dati del documento
    if documento_data:
        row['Carica 1'] = 'TITOLARE' if visura_data else 'RAPPRESENTANTE LEGALE'
        row['Nome 1'] = documento_data.get('Nome', '')
        row['Cognome 1'] = documento_data.get('Cognome', '')
        row['Sesso 1'] = documento_data.get('Sesso', '')
        row['Data Nas 1'] = documento_data.get('Data_Nascita', '')
        row['Comune Nas 1'] = documento_data.get('Luogo_Nascita', '')
        row['Provincia Nas 1'] = documento_data.get('Provincia_Nascita', '')
        row['Stato Nas 1'] = 'ITALIA'
        row['Codfisc 1'] = documento_data.get('CF_Persona', '')
        row['Indirizzo Res 1'] = documento_data.get('Residenza', '')
        row['Comune Res 1'] = documento_data.get('Comune_Residenza', '')
        row['Prov Res 1'] = documento_data.get('Provincia_Nascita', '')
        row['Stato Res 1'] = 'ITALIA'
        row['Tipo Doc'] = documento_data.get('Tipo_Documento', '')
        row['Num Doc'] = documento_data.get('Numero_Documento', '')
        row['Data Doc'] = documento_data.get('Data_Rilascio', '')
        row['Scadenza Doc'] = documento_data.get('Data_Scadenza', '')
        row['Autorita Doc'] = documento_data.get('Comune_Rilascio', '')

        # Copia dati anche come Titolare 1
        row['Tit 1 Nome'] = documento_data.get('Nome', '')
        row['Tit 1 Cognome'] = documento_data.get('Cognome', '')
        row['Tit 1 Codfisc'] = documento_data.get('CF_Persona', '')
        row['Tit 1 Sesso'] = documento_data.get('Sesso', '')
        row['Tit 1 Datanas'] = documento_data.get('Data_Nascita', '')
        row['Tit 1 Comunenas'] = documento_data.get('Luogo_Nascita', '')
        row['Tit 1 Provincia Nas'] = documento_data.get('Provincia_Nascita', '')
        row['Tit 1 Stato Nas'] = 'ITALIA'
        row['Tit 1 Tipodoc'] = documento_data.get('Tipo_Documento', '')
        row['Tit 1 Numdoc'] = documento_data.get('Numero_Documento', '')
        row['Tit 1 Rilasc Da'] = documento_data.get('Comune_Rilascio', '')
        row['Tit 1 Scad Doc'] = documento_data.get('Data_Scadenza', '')

    # Se non c'è documento ma c'è amministratore dalla visura, usa quei dati
    elif visura_data and (visura_data.get('Amministratore_Nome') or visura_data.get('Amministratore_Cognome')):
        row['Carica 1'] = 'AMMINISTRATORE UNICO'
        row['Nome 1'] = visura_data.get('Amministratore_Nome', '')
        row['Cognome 1'] = visura_data.get('Amministratore_Cognome', '')
        row['Tit 1 Nome'] = visura_data.get('Amministratore_Nome', '')
        row['Tit 1 Cognome'] = visura_data.get('Amministratore_Cognome', '')

    return pd.DataFrame([row])

def create_download_link(df, filename, file_format):
    """Crea un link per il download del file"""
    if file_format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">📥 Scarica Excel</a>'
    else:  # CSV
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:text/csv;base64,{b64}" download="{filename}.csv">📥 Scarica CSV</a>'

def main():
    """Funzione principale dell'applicazione"""
    
    # Header
    st.markdown('<h1 class="main-header">📄 Document Extractor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Estrazione automatica dati da Visure Camerali e Documenti d\'Identità</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 📄 Document Extractor")
        st.markdown("---")
        
        st.markdown("### 📋 Informazioni")
        st.info("""
        **Documenti supportati:**
        - 📄 Visure Camerali (PDF)
        - 🆔 Carte d'Identità
        - 🚗 Patenti
        - 🛂 Passaporti
        
        **Formati supportati:**
        - PDF
        - JPG/JPEG
        - PNG
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Impostazioni")
        
        export_format = st.radio(
            "Formato esportazione:",
            ["Excel (.xlsx)", "CSV (.csv)", "Entrambi"],
            index=2
        )
        
        st.markdown("---")
        st.markdown("### 📊 Statistiche")
        if 'processed_docs' not in st.session_state:
            st.session_state.processed_docs = 0
        st.metric("Documenti elaborati", st.session_state.processed_docs)
        
        st.markdown("---")
        st.markdown("### 🔗 Link Utili")
        st.markdown("- [GitHub Repository](#)")
        st.markdown("- [Documentazione](#)")
        st.markdown("- [Segnala Bug](#)")
    
    # Tabs principale
    tab1, tab2, tab3 = st.tabs(["📤 Carica Documento", "📊 Risultati", "ℹ️ Guida"])
    
    with tab1:
        st.markdown("### Carica il tuo documento")

        # Info sul template
        template_exists = load_template() is not None
        if template_exists:
            st.info("📋 Template formato import rilevato - I dati saranno esportati nel formato personalizzato")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Visura Camerale")
            visura_file = st.file_uploader(
                "Carica file PDF della visura",
                type=['pdf'],
                key='visura',
                help="Carica il PDF della visura camerale ottenuto dalla Camera di Commercio"
            )

            if visura_file:
                st.success(f"✅ File caricato: {visura_file.name}")

                if st.button("🔍 Estrai Dati Visura", key='btn_visura'):
                    with st.spinner("Elaborazione in corso..."):
                        extractor = DocumentExtractor()
                        text = extractor.extract_text_from_pdf(visura_file)

                        if text:
                            # Debug: mostra testo estratto
                            with st.expander("🔍 Visualizza testo estratto dal PDF"):
                                st.text(text[:2000])  # Mostra primi 2000 caratteri

                            data = extractor.parse_visura_camerale(text)
                            data['Nome_File'] = visura_file.name
                            data['Tipo_Documento'] = 'Visura Camerale'
                            data['Data_Elaborazione'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            st.session_state.visura_data = data
                            st.session_state.processed_docs += 1

                            if len(data) > 3:  # Se ha estratto più di 3 campi
                                st.success("✅ Dati estratti con successo!")
                                st.balloons()
                            else:
                                st.warning("⚠️ Alcuni dati potrebbero non essere stati estratti. Verifica il formato del PDF.")

        with col2:
            st.markdown("#### 🆔 Documento d'Identità")
            doc_file = st.file_uploader(
                "Carica immagine o PDF del documento",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key='documento',
                help="Carica foto o scansione del documento d'identità"
            )

            if doc_file:
                st.success(f"✅ File caricato: {doc_file.name}")

                # Mostra preview dell'immagine
                if doc_file.type.startswith('image'):
                    image = Image.open(doc_file)
                    st.image(image, caption="Preview documento", use_column_width=True)

                if st.button("🔍 Estrai Dati Documento", key='btn_doc'):
                    with st.spinner("Elaborazione in corso..."):
                        extractor = DocumentExtractor()

                        if doc_file.type == 'application/pdf':
                            text = extractor.extract_text_from_pdf(doc_file)
                        else:
                            image = Image.open(doc_file)
                            text = extractor.extract_text_from_image(image)

                        if text:
                            # Debug: mostra testo estratto
                            with st.expander("🔍 Visualizza testo estratto dall'OCR"):
                                st.text(text)

                            data = extractor.parse_documento_identita(text)
                            data['Nome_File'] = doc_file.name
                            data['Tipo_Documento'] = 'Documento Identità'
                            data['Data_Elaborazione'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            st.session_state.documento_data = data
                            st.session_state.processed_docs += 1

                            if len(data) > 3:  # Se ha estratto più di 3 campi
                                st.success("✅ Dati estratti con successo!")
                                st.balloons()
                            else:
                                st.warning("⚠️ Alcuni dati potrebbero non essere stati estratti. Controlla la qualità dell'immagine.")

        # Pulsante per combinare i dati
        st.markdown("---")
        if 'visura_data' in st.session_state or 'documento_data' in st.session_state:
            if st.button("🔄 Combina Visura e Documento nel Formato Template", use_container_width=True):
                visura = st.session_state.get('visura_data', {})
                documento = st.session_state.get('documento_data', {})

                # Crea il DataFrame mappato al template
                st.session_state.combined_data = map_data_to_template(visura, documento)
                st.success("✅ Dati combinati nel formato template!")
                st.info("📊 Vai alla tab 'Risultati' per scaricare il file Excel")
        
        # Elaborazione Batch
        st.markdown("---")
        st.markdown("### 📦 Elaborazione Batch (Multipla)")
        st.info("Carica più documenti contemporaneamente per un'elaborazione veloce")
        
        batch_files = st.file_uploader(
            "Carica più file",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key='batch',
            help="Seleziona più file da elaborare in una volta"
        )
        
        if batch_files and st.button("🚀 Elabora Tutti i Documenti"):
            visure_data = []
            documenti_data = []
            unmatched_data = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            # Fase 1: Estrazione dati da tutti i file
            status_text.text("Fase 1/2: Estrazione dati dai documenti...")

            for idx, file in enumerate(batch_files):
                extractor = DocumentExtractor()

                try:
                    if file.type == 'application/pdf':
                        text = extractor.extract_text_from_pdf(file)
                    else:
                        image = Image.open(file)
                        text = extractor.extract_text_from_image(image)

                    if text:
                        if extractor.is_visura_camerale(text):
                            data = extractor.parse_visura_camerale(text)
                            data['Nome_File'] = file.name
                            data['Tipo_Documento'] = 'Visura Camerale'
                            visure_data.append(data)
                        elif extractor.is_documento_identita(text):
                            data = extractor.parse_documento_identita(text)
                            data['Nome_File'] = file.name
                            data['Tipo_Documento'] = 'Documento Identità'
                            documenti_data.append(data)
                        else:
                            unmatched_data.append({
                                'Nome_File': file.name,
                                'Tipo_Documento': 'Non Riconosciuto',
                                'Errore': 'Tipo documento non identificato'
                            })

                except Exception as e:
                    st.warning(f"⚠️ Errore con {file.name}: {str(e)}")
                    unmatched_data.append({
                        'Nome_File': file.name,
                        'Tipo_Documento': 'Errore',
                        'Errore': str(e)
                    })

                progress_bar.progress((idx + 1) / (len(batch_files) * 2))

            # Fase 2: Matching e creazione template
            status_text.text("Fase 2/2: Matching documenti e creazione formato template...")

            template_rows = []
            matched_visure = set()
            matched_documenti = set()

            # Strategia 1: Match per codice fiscale
            for i, visura in enumerate(visure_data):
                cf_azienda = visura.get('Codice_Fiscale', '')

                # Cerca documento con stesso CF
                for j, doc in enumerate(documenti_data):
                    cf_persona = doc.get('CF_Persona', '')

                    # Match se il CF azienda coincide con CF persona (impresa individuale)
                    # oppure se abbiamo altri criteri di matching
                    if cf_azienda and cf_persona and (cf_azienda == cf_persona):
                        # Crea riga template
                        template_df = map_data_to_template(visura, doc)
                        template_rows.append(template_df)
                        matched_visure.add(i)
                        matched_documenti.add(j)
                        break

            # Strategia 2: Match per nome file (pattern comune)
            for i, visura in enumerate(visure_data):
                if i in matched_visure:
                    continue

                # Estrai pattern dal nome file (es. partita IVA, codice fiscale)
                visura_file = visura.get('Nome_File', '').lower()

                for j, doc in enumerate(documenti_data):
                    if j in matched_documenti:
                        continue

                    doc_file = doc.get('Nome_File', '').lower()

                    # Cerca pattern comuni nei nomi dei file
                    # Es: entrambi contengono lo stesso codice fiscale o nome azienda
                    cf_visura = visura.get('Codice_Fiscale', '')
                    if cf_visura and cf_visura.lower() in doc_file:
                        template_df = map_data_to_template(visura, doc)
                        template_rows.append(template_df)
                        matched_visure.add(i)
                        matched_documenti.add(j)
                        break

            # Strategia 3: Abbinamento manuale per ordine (se caricati in coppia)
            remaining_visure = [v for i, v in enumerate(visure_data) if i not in matched_visure]
            remaining_docs = [d for j, d in enumerate(documenti_data) if j not in matched_documenti]

            # Se abbiamo lo stesso numero, abbiniamo per ordine
            if len(remaining_visure) == len(remaining_docs):
                for visura, doc in zip(remaining_visure, remaining_docs):
                    template_df = map_data_to_template(visura, doc)
                    template_rows.append(template_df)
                    matched_visure.add(visure_data.index(visura))
                    matched_documenti.add(documenti_data.index(doc))
            else:
                # Abbina quelli rimanenti singolarmente
                for visura in remaining_visure:
                    template_df = map_data_to_template(visura, {})
                    template_rows.append(template_df)

                for doc in remaining_docs:
                    template_df = map_data_to_template({}, doc)
                    template_rows.append(template_df)

            # Combina tutti i DataFrame template in uno unico
            if template_rows:
                batch_template_df = pd.concat(template_rows, ignore_index=True)
                st.session_state.batch_template_data = batch_template_df
            else:
                st.session_state.batch_template_data = None

            # Salva anche i dati non matchati per riferimento
            st.session_state.batch_unmatched = unmatched_data
            st.session_state.processed_docs += len(batch_files)

            progress_bar.progress(1.0)
            status_text.text("")

            # Statistiche finali
            st.success(f"✅ Elaborazione completata!")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Totale file", len(batch_files))
            with col2:
                st.metric("📋 Visure", len(visure_data))
            with col3:
                st.metric("🆔 Documenti", len(documenti_data))
            with col4:
                st.metric("✅ Righe template", len(template_rows) if template_rows else 0)

            if unmatched_data:
                st.warning(f"⚠️ {len(unmatched_data)} file non riconosciuti o con errori")
    
    with tab2:
        st.markdown("### 📊 Dati Estratti")

        # Visualizza dati combinati nel formato template
        if 'combined_data' in st.session_state and st.session_state.combined_data is not None:
            st.markdown("#### 📋 Dati nel Formato Template")
            st.success("✅ I dati sono stati mappati al formato import personalizzato")

            df_combined = st.session_state.combined_data

            # Statistiche
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                filled_cols = df_combined.notna().sum(axis=1).iloc[0]
                st.metric("📊 Campi compilati", int(filled_cols))
            with col2:
                total_cols = len(df_combined.columns)
                st.metric("📋 Totale colonne", total_cols)
            with col3:
                percentage = (filled_cols / total_cols * 100) if total_cols > 0 else 0
                st.metric("✅ Completamento", f"{percentage:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

            # Mostra alcune colonne chiave
            st.markdown("##### Anteprima Dati Principali")
            key_columns = ['Ragionesociale', 'Codfisc Azienda', 'Partita Iva Azienda',
                          'Nome 1', 'Cognome 1', 'Codfisc 1', 'Comune Sede']
            available_cols = [col for col in key_columns if col in df_combined.columns]
            if available_cols:
                st.dataframe(df_combined[available_cols], use_container_width=True)

            # Mostra tutti i dati
            with st.expander("🔍 Visualizza Tutti i Campi"):
                st.dataframe(df_combined, use_container_width=True)

            # Download
            st.markdown("#### 💾 Download Formato Template")
            col1, col2 = st.columns(2)

            with col1:
                if export_format in ["Excel (.xlsx)", "Entrambi"]:
                    st.markdown(create_download_link(df_combined, "dati_formato_import", "excel"), unsafe_allow_html=True)

            with col2:
                if export_format in ["CSV (.csv)", "Entrambi"]:
                    st.markdown(create_download_link(df_combined, "dati_formato_import", "csv"), unsafe_allow_html=True)

            st.markdown("---")

        # Visualizza dati singolo documento (visura o documento separato)
        if 'visura_data' in st.session_state or 'documento_data' in st.session_state:
            st.markdown("#### Dati Estratti Individuali")

            if 'visura_data' in st.session_state:
                with st.expander("📄 Visura Camerale"):
                    df_visura = pd.DataFrame([st.session_state.visura_data])
                    st.dataframe(df_visura, use_container_width=True)

            if 'documento_data' in st.session_state:
                with st.expander("🆔 Documento d'Identità"):
                    df_doc = pd.DataFrame([st.session_state.documento_data])
                    st.dataframe(df_doc, use_container_width=True)
        
        # Visualizza dati batch nel formato template
        if 'batch_template_data' in st.session_state and st.session_state.batch_template_data is not None:
            st.markdown("---")
            st.markdown("#### 📦 Elaborazione Batch - Formato Template")
            st.success("✅ Tutti i documenti batch sono stati mappati al formato import")

            df_batch = st.session_state.batch_template_data

            # Statistiche
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Righe totali", len(df_batch))
            with col2:
                total_cols = len(df_batch.columns)
                st.metric("📋 Colonne template", total_cols)
            with col3:
                # Media campi compilati per riga
                avg_filled = df_batch.notna().sum(axis=1).mean()
                st.metric("📈 Media campi/riga", f"{int(avg_filled)}")
            with col4:
                # Percentuale media completamento
                avg_percentage = (avg_filled / total_cols * 100) if total_cols > 0 else 0
                st.metric("✅ Completamento medio", f"{avg_percentage:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

            # Anteprima colonne chiave
            st.markdown("##### 🔍 Anteprima Dati Principali")
            key_columns = ['Ragionesociale', 'Codfisc Azienda', 'Partita Iva Azienda',
                          'Nome 1', 'Cognome 1', 'Codfisc 1', 'Comune Sede']
            available_cols = [col for col in key_columns if col in df_batch.columns]
            if available_cols:
                st.dataframe(df_batch[available_cols], use_container_width=True)

            # Tabella completa espandibile
            with st.expander("📋 Visualizza Tutte le Colonne del Template"):
                st.dataframe(df_batch, use_container_width=True)

            # Info su file non matchati
            if 'batch_unmatched' in st.session_state and st.session_state.batch_unmatched:
                with st.expander("⚠️ File Non Riconosciuti o con Errori"):
                    df_unmatched = pd.DataFrame(st.session_state.batch_unmatched)
                    st.dataframe(df_unmatched, use_container_width=True)

            # Download batch
            st.markdown("#### 💾 Download Batch Formato Template")
            col1, col2 = st.columns(2)

            with col1:
                if export_format in ["Excel (.xlsx)", "Entrambi"]:
                    st.markdown(create_download_link(df_batch, "batch_formato_import", "excel"), unsafe_allow_html=True)

            with col2:
                if export_format in ["CSV (.csv)", "Entrambi"]:
                    st.markdown(create_download_link(df_batch, "batch_formato_import", "csv"), unsafe_allow_html=True)

        if ('combined_data' not in st.session_state and
            'batch_template_data' not in st.session_state and
            'visura_data' not in st.session_state and
            'documento_data' not in st.session_state):
            st.info("👆 Carica ed elabora un documento nella tab **Carica Documento** per visualizzare i risultati qui")
    
    with tab3:
        st.markdown("### 📖 Guida all'uso")
        
        st.markdown("""
        #### 🚀 Come utilizzare l'applicazione
        
        **1. Carica il documento**
        - Scegli tra Visura Camerale o Documento d'Identità
        - Clicca su "Browse files" e seleziona il file
        - Formati supportati: PDF, JPG, PNG
        
        **2. Estrai i dati**
        - Clicca sul pulsante "Estrai Dati"
        - Attendi l'elaborazione (pochi secondi)
        - I dati verranno mostrati nella tab "Risultati"
        
        **3. Scarica i risultati**
        - Vai alla tab "Risultati"
        - Scegli il formato (Excel o CSV)
        - Clicca sul link di download
        - **I dati sono su una singola riga con colonne multiple**
        
        ---
        
        #### 📋 Dati estratti
        
        **Dalla Visura Camerale:**
        - Denominazione/Ragione Sociale
        - Partita IVA
        - Codice Fiscale
        - Numero REA
        - Forma Giuridica
        - Sede Legale, CAP, Comune, Provincia
        - Data di Costituzione
        - Capitale Sociale
        - Stato Attività
        
        **Dal Documento d'Identità:**
        - Nome e Cognome
        - Data e Luogo di Nascita (con Provincia)
        - Codice Fiscale
        - Residenza e Comune di Residenza
        - Numero Documento
        - Data di Rilascio e Scadenza
        - Comune di Rilascio
        - Sesso, Statura, Cittadinanza
        - Tipo Documento
        
        ---
        
        #### 💡 Suggerimenti per migliori risultati
        
        **Per le Visure:**
        - Usa PDF originali dalla Camera di Commercio
        - Evita scansioni di bassa qualità
        
        **Per i Documenti d'Identità:**
        - Fotografia ben illuminata
        - Documento piatto (non piegato)
        - Risoluzione minima 300 DPI
        - Evita riflessi
        
        ---
        
        #### ⚠️ Note importanti
        
        - Questa è una versione web dell'applicazione
        - Richiede Tesseract OCR installato sul server
        - I dati vengono elaborati localmente (privacy garantita)
        - Per uso professionale, considera il deploy su server dedicato
        
        ---
        
        #### 🔗 Risorse
        
        - [GitHub Repository](https://github.com/tuousername/document-extractor)
        - [Documentazione Completa](https://github.com/tuousername/document-extractor/blob/main/README.md)
        - [Segnala un Bug](https://github.com/tuousername/document-extractor/issues)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📄 Document Extractor v2.0 Web Edition | Sviluppato con ❤️ usando Streamlit</p>
        <p>🔒 I tuoi dati sono sicuri - Elaborazione locale | 🆓 Open Source - MIT License</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
