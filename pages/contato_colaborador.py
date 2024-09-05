import streamlit as st
from app import get_contato_colaborador, render_login

if "credentials" not in st.session_state:
    st.session_state.credentials = {}


render_login()
st.title('Contato Colaborador')
domain = st.text_input('Domínio')
download_col1, download_col2 = st.columns(2)

if domain:
    if not st.session_state.credentials:
        st.warning("Efetue o login")
    else:        
        if download_col1.button('Coletar JSON'):
            json_data = get_contato_colaborador(domain)     
            if json_data:     
                download_col2.download_button(
                    label="Baixar JSON",
                    data=json_data,
                    file_name=f"contato_colaborador - ({domain.split('.')[0]}).json",
                    mime="application/json"
                )
            else:
                warning = st.warning('Não foi possível executar a ação')
