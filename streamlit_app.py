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

        patterns = {
            'Denominazione': r"(?:Denominazione|Ragione sociale)[:\s]*\n?\s*([A-Z][^\n]+)",
            'Partita_IVA': r"(?:P\.?\s*IVA|Partita\s+IVA)[:\s]*\n?\s*(\d{11})",
            'Codice_Fiscale': r"(?:Codice\s+Fiscale|C\.?\s*F\.?)[:\s]*\n?\s*([A-Z0-9]{11,16})",
            'Numero_REA': r"(?:REA|N\.?\s*REA|Numero\s+REA)[:\s]*\n?\s*([A-Z]{2}[\s\-]?\d+)",
            'Forma_Giuridica': r"(?:Forma\s+giuridica|Natura\s+giuridica)[:\s]*\n?\s*([^\n]+)",
            'Sede_Legale': r"(?:Sede\s+legale|Indirizzo)[:\s]*\n?\s*([^\n]+?)(?:\s*\d{5}|\n)",
            'CAP': r"(?:^|\s|-)(\d{5})(?:\s+[A-Z]|\s*-|\s*\()",
            'Comune': r"(?:\d{5}\s*[-,]?\s*|Comune[:\s]+)([A-Z][A-Za-z][A-Za-z\s\'\.]+?)(?:\s*[\(\-]|,?\s*(?:Provincia|Prov\.?)\s*[:\(]|\s+[A-Z]{2}\s*[\)\-])",
            'Provincia': r"(?:Provincia|Prov\.?|Sigla)[:\s]*\(?\s*([A-Z]{2})\s*\)?|(?:^|\s)\(([A-Z]{2})\)",
            'Data_Costituzione': r"(?:Data\s+costituzione|Costituita\s+il|Data\s+iscrizione)[:\s]*\n?\s*(\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{4})",
            'Capitale_Sociale': r"(?:Capitale\s+sociale|Capitale)[:\s]*\n?\s*(?:€|EUR|Euro)?\s*([\d\.,]+)",
            'Stato_Attivita': r"(?:Stato)[:\s]*\n?\s*(ATTIVA|ATTIVO|CESSATA|CESSATO|SOSPESA|SOSPESO)"
        }

        for key, pattern in patterns.items():
            value = self.extract_pattern(text, pattern)
            if value:
                # Pulizia del valore estratto
                cleaned_value = value.strip()
                # Rimuovi spazi multipli
                cleaned_value = re.sub(r'\s+', ' ', cleaned_value)
                # Pulizia specifica per il Comune (rimuovi virgole e trattini finali)
                if key == 'Comune':
                    cleaned_value = re.sub(r'[,\-\s]+$', '', cleaned_value)
                data[key] = cleaned_value

        return data
    
    def parse_documento_identita(self, text):
        """Analizza il testo del documento d'identità ed estrae i dati"""
        data = {}

        # Pattern migliorati per carte d'identità italiane
        patterns = {
            'Cognome': r"(?:Cognome|COGNOME|Surname)[:\s]*\n?\s*([A-Z\s]+?)(?:\n|Nome|NOME|$)",
            'Nome': r"(?:Nome|NOME|Name)[:\s]*\n?\s*([A-Z][A-Za-z\s]+?)(?:\n|Luogo|Nat|Data|$)",
            'Luogo_Nascita': r"(?:Luogo\s*di\s*nascita|Nat[oa]\s*a|Place\s*of\s*birth)[:\s]*\n?\s*([A-Z][A-Za-z\s\']+?)(?:\s*\(|,|\n|il|$)",
            'Provincia_Nascita': r"(?:Luogo\s*di\s*nascita|Nat[oa]\s*a)[:\s]*[^(\n]*\(([A-Z]{2})\)",
            'Data_Nascita': r"(?:Data\s*di\s*nascita|Nat[oa]\s*il|Date\s*of\s*birth)[:\s]*\n?\s*(\d{1,2}[/\.\-\s]\d{1,2}[/\.\-\s]\d{4})",
            'Sesso': r"(?:Sesso|Sex)[:\s]*\n?\s*([MF])",
            'Statura': r"(?:Statura|Height)[:\s]*\n?\s*(\d+[\.,]?\d*)\s*(?:cm|m)?",
            'Cittadinanza': r"(?:Cittadinanza|Citizenship)[:\s]*\n?\s*([A-Z][A-Za-z]+)",
            'Residenza': r"(?:Residenza|Residence|Indirizzo)[:\s]*\n?\s*([A-Z][A-Za-z0-9\s,\.\']+?)(?:\n\n|\n[A-Z]{2}\d{7}|Rilascia)",
            'Comune_Residenza': r"(?:Comune|Municipality)[:\s]*\n?\s*([A-Z][A-Za-z\s]+?)(?:\s*\(|,|\n|$)",
            'CF_Persona': r"([A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])",
            'Numero_Documento': r"(?:Carta\s*d[\'i]?\s*identit[aà]\s*n|Numero|N\.|Document\s*no)[:\.]?\s*\n?\s*([A-Z]{2}\s*\d{7}[A-Z]?|[A-Z0-9]{6,10})",
            'Data_Rilascio': r"(?:Rilasciat[oa]|Emess[oa]|Data\s*di\s*rilascio|Date\s*of\s*issue)[:\s]*\n?\s*(?:il\s*)?(\d{1,2}[/\.\-\s]\d{1,2}[/\.\-\s]\d{4})",
            'Data_Scadenza': r"(?:Scadenza|Valid[oa]\s*fino\s*al|Date\s*of\s*expiry)[:\s]*\n?\s*(\d{1,2}[/\.\-\s]\d{1,2}[/\.\-\s]\d{4})",
            'Comune_Rilascio': r"(?:Comune\s*di|Rilasciat[oa]\s*da|Issued\s*by)[:\s]*\n?\s*([A-Z][A-Za-z\s]+?)(?:\s*\(|,|\n|$)",
            'Tipo_Documento': r"(CARTA\s*D[\'I]?\s*IDENTIT[AÀ]|PATENTE|PASSAPORTO|IDENTITY\s*CARD)"
        }

        for key, pattern in patterns.items():
            value = self.extract_pattern(text, pattern)
            if value:
                # Pulizia del valore estratto
                cleaned_value = value.strip()
                # Rimuovi spazi multipli
                cleaned_value = re.sub(r'\s+', ' ', cleaned_value)
                # Normalizza date
                if 'Data' in key and cleaned_value:
                    cleaned_value = re.sub(r'[/\.\-\s]+', '/', cleaned_value)
                data[key] = cleaned_value

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

                            st.session_state.extracted_data = data
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

                            st.session_state.extracted_data = data
                            st.session_state.processed_docs += 1

                            if len(data) > 3:  # Se ha estratto più di 3 campi
                                st.success("✅ Dati estratti con successo!")
                                st.balloons()
                            else:
                                st.warning("⚠️ Alcuni dati potrebbero non essere stati estratti. Controlla la qualità dell'immagine.")
        
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
            all_data = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(batch_files):
                status_text.text(f"Elaborazione: {file.name} ({idx+1}/{len(batch_files)})")
                
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
                            data['Tipo_Documento'] = 'Visura Camerale'
                        elif extractor.is_documento_identita(text):
                            data = extractor.parse_documento_identita(text)
                            data['Tipo_Documento'] = 'Documento Identità'
                        else:
                            data = {'Tipo_Documento': 'Non Riconosciuto'}
                        
                        data['Nome_File'] = file.name
                        data['Data_Elaborazione'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        all_data.append(data)
                        
                except Exception as e:
                    st.warning(f"⚠️ Errore con {file.name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(batch_files))
            
            st.session_state.batch_data = all_data
            st.session_state.processed_docs += len(all_data)
            status_text.text("")
            st.success(f"✅ Elaborati {len(all_data)} documenti su {len(batch_files)}")
    
    with tab2:
        st.markdown("### 📊 Dati Estratti")
        
        # Visualizza dati singolo documento
        if 'extracted_data' in st.session_state and st.session_state.extracted_data:
            st.markdown("#### Ultimo Documento Elaborato")
            data = st.session_state.extracted_data
            
            # Card informativa
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 File", data.get('Nome_File', 'N/A'))
            with col2:
                st.metric("📋 Tipo", data.get('Tipo_Documento', 'N/A'))
            with col3:
                st.metric("🕐 Data", data.get('Data_Elaborazione', 'N/A')[:10])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tabella dati
            df_single = pd.DataFrame([data])
            st.dataframe(df_single, use_container_width=True)
            
            # Download singolo
            st.markdown("#### 💾 Download")
            col1, col2 = st.columns(2)
            
            with col1:
                if export_format in ["Excel (.xlsx)", "Entrambi"]:
                    st.markdown(create_download_link(df_single, "dati_estratti", "excel"), unsafe_allow_html=True)
            
            with col2:
                if export_format in ["CSV (.csv)", "Entrambi"]:
                    st.markdown(create_download_link(df_single, "dati_estratti", "csv"), unsafe_allow_html=True)
        
        # Visualizza dati batch
        if 'batch_data' in st.session_state and st.session_state.batch_data:
            st.markdown("---")
            st.markdown("#### Elaborazione Batch")
            
            df_batch = pd.DataFrame(st.session_state.batch_data)
            
            # Statistiche
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Totale", len(df_batch))
            with col2:
                visure = len(df_batch[df_batch['Tipo_Documento'] == 'Visura Camerale'])
                st.metric("📄 Visure", visure)
            with col3:
                doc_id = len(df_batch[df_batch['Tipo_Documento'] == 'Documento Identità'])
                st.metric("🆔 Documenti ID", doc_id)
            with col4:
                non_ric = len(df_batch[df_batch['Tipo_Documento'] == 'Non Riconosciuto'])
                st.metric("❓ Non riconosciuti", non_ric)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tabella
            st.dataframe(df_batch, use_container_width=True)
            
            # Download batch
            st.markdown("#### 💾 Download Batch")
            col1, col2 = st.columns(2)
            
            with col1:
                if export_format in ["Excel (.xlsx)", "Entrambi"]:
                    st.markdown(create_download_link(df_batch, "batch_risultati", "excel"), unsafe_allow_html=True)
            
            with col2:
                if export_format in ["CSV (.csv)", "Entrambi"]:
                    st.markdown(create_download_link(df_batch, "batch_risultati", "csv"), unsafe_allow_html=True)
        
        if 'extracted_data' not in st.session_state and 'batch_data' not in st.session_state:
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
