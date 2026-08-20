import streamlit as str

# Inserisci questo subito dopo set_page_config
str.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, 
    unsafe_allow_html=True
)

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from datetime import datetime
import io

# 1. Configurazione della pagina (Interfaccia Professionale)
st.set_page_config(
    page_title="ADR Safety Check - Logistica Avanzata", 
    page_icon="🚛",
    layout="centered"
)

# 2. Configurazione Credenziali Utenti
config_credenziali = {
    "usernames": {
        "operatore1": { "name": "Operatore (Addetto Carico)", "password": stauth.Hasher.hash("Kadr26") },
        "safety_manager": { "name": "Dott. Bianchi (Consulente ADR)", "password": stauth.Hasher.hash("admin456") }
    }
}

# 3. Inizializzazione del sistema di login
authenticator = stauth.Authenticate(
    credentials=config_credenziali,
    cookie_name="adr_cookie_corporate",
    key="chiave_segreta_molto_lunga_e_sicura_per_il_vostro_saas_adr_2026",
    cookie_expiry_days=30
)

# 4. Schermata di Login (Aggiornata per la massima compatibilità)
authenticator.login(location='main')

# Recuperiamo in modo sicuro i dati dallo stato della sessione di Streamlit
authentication_status = st.session_state.get("authentication_status")
nome_utente = st.session_state.get("name")
username_loggato = st.session_state.get("username")

# 5. Controllo Accesso
if authentication_status == False:
    st.error('❌ Credenziali non valide. Verifica i dati o contatta l\'amministratore IT.')
elif authentication_status == None:
    st.info('🔒 Accesso Riservato\n\nTerminale aziendale di controllo merci pericolose. Inserire le credenziali per sbloccare il piazzale di carico.')
elif authentication_status:
    
    with st.sidebar:
        st.markdown("### 🏢 LOGISTICA SOFTWARE")
        st.markdown(f"👤 **Utente:** {nome_utente}")
        st.markdown(f"🔑 **ID Sessione:** `{username_loggato}`")
        st.markdown("---")
        authenticator.logout('🚪 Disconnetti Sessione', 'sidebar')
        st.markdown("---")
        st.caption("🛡️ **SaaS ADR Compliance Pro v3.1**")
        st.caption("Infrastruttura Cloud Crittografata")

    # --- APPLICATIVO PRINCIPALE CON LOGO E TITOLO ---
    LOGO_URL = "https://placehold.co"
    
    col_logo, col_titolo = st.columns(2)
    with col_logo:
        st.image(LOGO_URL, width=90)
    with col_titolo:
        st.title("ADR Safety Check")
        st.markdown("*Sistema Digitale Unificato di Controllo Spedizioni*")

    st.info("💡 Conformità Normativa: Modulo digitale conforme al Decreto MIT e alla Direttiva Delegata UE 2025/1801 per le Categorie di Rischio I, II, III.")

    # --- SEZIONE 1: DATI GENERALI ---
    st.header("📌 1. Anagrafica e Spedizione")
    col1, col2 = st.columns(2)

    with col1:
        data_controllo = st.date_input("Data del Controllo", datetime.now())
        impresa_caricatrice = st.text_input("Azienda Caricatrice / Mittente", value="La Tua Azienda S.p.A.")
        targa_motrice = st.text_input("Targa Automezzo / Rimorchio")

    with col2:
        operatore_controllo = st.text_input("Addetto alla Verifica (Piazzale)", value=nome_utente)
        vettore_trasportatore = st.text_input("Società di Trasporto / Vettore")
        numero_onu = st.text_input("Numero ONU della Merce (es. UN 1203)")

    classe_adr = st.selectbox("Classe di Pericolo ADR Principale", ["", "1 (Esplosivi)", "2 (Gas)", "3 (Liquidi Infiammabili)", "4.1", "4.2", "4.3", "5.1", "5.2", "6.1", "6.2", "7 (Radioattivi)", "8 (Corrosivi)", "9 (Materie Varie)"])
    # --- SEZIONE 2: RISCHI ---
    st.header("🔎 2. Check-list Categorie di Rischio")
    controlli = {}

    st.markdown("#### 🔴 Categoria di Rischio I (Rischio Alto / Blocco Immediato)")
    controlli['c1_documenti'] = st.radio("Documentazione di trasporto ADR a bordo conforme?", ["SÌ", "NO (Rischio I)"], key="k1", horizontal=True)
    controlli['c1_imballaggi'] = st.radio("Integrità colli, cisterne o imballaggi (assenza di perdite)?", ["SÌ", "NO (Rischio I)"], key="k2", horizontal=True)

    st.markdown("#### 🟡 Categoria di Rischio II (Rischio Medio / Sanabile)")
    controlli['c2_stivaggio'] = st.radio("Fissaggio del carico stivato contro i movimenti strutturali?", ["SÌ", "NO (Rischio II)"], key="k3", horizontal=True)

    st.markdown("#### 🟢 Categoria di Rischio III (Rischio Lieve / Errore Formale)")
    controlli['c3_formalita'] = st.radio("Presenza del codice restrizione gallerie sul DDT?", ["SÌ", "NO (Rischio III)"], key="k4", horizontal=True)

    # --- SEZIONE 3: VALUTAZIONE FINALE ---
    st.header("📊 3. Valutazione ed Esito Ispezione")
    
    if "NO (Rischio I)" in controlli.values():
        rischio_rilevato = "CATEGORIA I (Rischio Alto) - VIOLAZIONE CRITICA DETECTED"
        esito_finale = "NON IDONEO / SOSPESO"
        st.error(f"🚨 **ESITO: {esito_finale}**\n\nIl carico presenta non conformità gravi. Impedire la partenza del veicolo.")
    elif "NO (Rischio II)" in controlli.values():
        rischio_rilevato = "CATEGORIA II (Rischio Medio) - Richiede intervento correttivo"
        esito_finale = "IDONEO CON RISERVA"
        st.warning(f"⚠️ **ESITO: {esito_finale}**\n\nSistemare le anomalie segnalate prima di autorizzare il viaggio.")
    else:
        rischio_rilevato = "Nessuna anomalia riscontrata"
        esito_finale = "IDONEO AL TRASPORTO"
        st.success(f"✅ **ESITO: {esito_finale}**\n\nI controlli stradali preventivi hanno dato esito positivo. Il mezzo può partire.")

    note = st.text_area("Note Operative / Azioni Correttive Applicate sul Piazzale")

    # --- SEZIONE 4: FIRME TOUCH ---
    st.header("✨ 4. Sottoscrizione Elettronica")
    st.caption("Firma direttamente all'interno dei box utilizzando lo schermo touch del dispositivo logistico.")

    col_firma1, col_firma2 = st.columns(2)

    with col_firma1:
        st.markdown("**✍️ Firma dell'Addetto al Carico**")
        canvas_caricatore = st_canvas(
            stroke_width=2, stroke_color="#1a5276", background_color="#FFFFFF",
            height=110, width=280, drawing_mode="freedraw", key="canvas_caricatore_adr"
        )

    with col_firma2:
        st.markdown("**✍️ Firma del Conducente (Vettore)**")
        canvas_autista = st_canvas(
            stroke_width=2, stroke_color="#1a5276", background_color="#FFFFFF",
            height=110, width=280, drawing_mode="freedraw", key="canvas_autista_adr"
        )

    # --- GENERAZIONE PDF ESPANSA ---
    st.header("🖨️ 5. Esporta Documentazione")
    
    if st.button("🔄 Genera e Prepara Report PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Intestazione principale
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 12, "CHECKLIST CARICATORE ADR - VERIFICA PREVENTIVA", ln=True, align="C")
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, f"Generata in data: {data_controllo.strftime('%d/%m/%Y')}", ln=True, align="C")
            pdf.line(10, 32, 200, 32)
            pdf.ln(15)
            
            # Sezione Dati Anagrafici
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "1. ANAGRAFICA E SPEDIZIONE", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(95, 6, f"Azienda Caricatrice: {impresa_caricatrice}", ln=False)
            pdf.cell(95, 6, f"Operatore: {operatore_controllo}", ln=True)
            pdf.cell(95, 6, f"Targa Automezzo: {targa_motrice}", ln=False)
            pdf.cell(95, 6, f"Vettore: {vettore_trasportatore}", ln=True)
            pdf.cell(95, 6, f"Numero ONU: {numero_onu}", ln=False)
            pdf.cell(95, 6, f"Classe ADR: {classe_adr}", ln=True)
            pdf.ln(5)
            
            # Sezione Esito Check-list
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "2. ESITO E VALUTAZIONE RISCHI", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Documentazione conforme: {controlli['c1_documenti']}", ln=True)
            pdf.cell(0, 6, f"Integrita imballaggi: {controlli['c1_imballaggi']}", ln=True)
            pdf.cell(0, 6, f"Stivaggio sicuro: {controlli['c2_stivaggio']}", ln=True)
            pdf.cell(0, 6, f"Codice restrizione gallerie presente: {controlli['c3_formalita']}", ln=True)
            pdf.ln(5)
            
            # Stato Finale
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "3. STATO FINALE DI VALUTAZIONE", ln=True)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 6, f"ESITO: {esito_finale}", ln=True)
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, f"Note di piazzale: {note}", ln=True)
            pdf.ln(20)
            
            # Spazio Firme cartacee / digitali
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(95, 6, "Firma Addetto al Carico:", ln=False)
            pdf.cell(95, 6, "Firma Conducente (Vettore):", ln=True)
            pdf.ln(15)
            pdf.cell(95, 6, "_________________________", ln=False)
            pdf.cell(95, 6, "_________________________", ln=True)

            # CORREZIONE: Gestione sicura del bytearray restituito da fpdf2
            pdf_raw = pdf.output(dest='S')
            pdf_bytes = bytes(pdf_raw) if isinstance(pdf_raw, (bytearray, bytes)) else pdf_raw.encode('latin1')
            
            # Download Button abilitato dopo la generazione automatica
            st.download_button(
                label="⬇️ Scarica File PDF Compilato",
                data=pdf_bytes,
                file_name=f"ADR_Check_{targa_motrice}_{data_controllo.strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            
            st.success("✅ Documento PDF preparato con successo! Clicca sul pulsante sopra per salvarlo.")
            
            # Opzione di Stampa Diretta tramite Browser
            st.markdown("---")
            st.write("📌 **Vuoi stampare la schermata corrente?**")
            st.components.v1.html(
                '<button onclick="window.print()" style="padding: 12px 24px; background-color: #1a5276; color: white; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; width: 100%;">🖨️ Apri Menu di Stampa Browser</button>',
                height=60
            )
            
        except Exception as e:
            st.error(f"Errore durante la generazione del PDF: {e}")
