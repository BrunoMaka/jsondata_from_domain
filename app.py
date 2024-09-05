import streamlit as st
import requests
import json

st.title('Coletar dados de empresas a partir de domínios')

if "credentials" not in st.session_state:
    st.session_state.credentials = {}

def login(username, password):
    url_login = "https://gtmsi.cortex-intelligence.com/service/integration-authorization-service.login"
    data = {
        'login': username,
        'password': password   
    }
    response_login = requests.post(url_login, json=data)  
    if response_login.status_code == 200:
        user_id = response_login.json().get('userId')
        token = response_login.json().get('key')
        return user_id, token
    else:
        st.sidebar.warning(response_login.json().get('error', 'Solicitação inválida'))
        return None, None

def render_login():
    username = st.sidebar.text_input('Usuario')
    password = st.sidebar.text_input('Senha')    
    if username and password:
        if st.sidebar.button('Gerar credenciais'):
            user_id, token = login(username, password)
            if user_id and token:
                st.session_state.credentials['user_id'] = user_id
                st.session_state.credentials['token'] = token
                st.sidebar.success('Credenciais geradas. Não é necessário gerar novamente, somente se solicitado')   


def convert_to_json(tsv_data):
    lines = tsv_data.strip().split('\n')
    fields = [field.strip('"') for field in lines[0].split('\t')]
    data = []
    for line in lines[1:]:
        values = [value.strip('"') for value in line.split('\t')]
        record = dict(zip(fields, values))
        data.append(record)
    return json.dumps(data, indent=4)

def get_empresa_linkedin_data(domain):  
    url = "https://gtmsi.cortex-intelligence.com/service/integration-cube-service.download"
    params = {
        "cube": '{"name": "[SIDATA] Empresa Linkedin"}',
        "charset": "UTF-8",
        "filters": f'[{{"name":"dominio","value":"{domain}","exactMatch":true}}]'
    }
    headers = {
        "Content-Type": "text/csv;charset=UTF-8",
        "x-authorization-user-id": st.session_state.credentials['user_id'],
        "x-authorization-token": st.session_state.credentials['token']
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:      
            tsv_data = response.text        
        except:
            tsv_data = None
        if tsv_data:
            return convert_to_json(tsv_data)
        else:
            return None
    else:
        st.warning('Efetue o login novamente')


def get_contato_colaborador(domain):  
    url = "https://gtmsi.cortex-intelligence.com/service/integration-cube-service.download"
    params = {
        "cube": '{"name": "[SIDATA] Contato Colaborador"}',
        "charset": "UTF-8",
        "filters": f'[{{"name":"dominio","value":"{domain}","exactMatch":true}}, {{"name":"Buying Committee","value":"Sim","exactMatch":true}}]'
    }
    headers = {
        "Content-Type": "text/csv;charset=UTF-8",
        "x-authorization-user-id": st.session_state.credentials['user_id'],
        "x-authorization-token": st.session_state.credentials['token']
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:      
            tsv_data = response.text        
        except:
            tsv_data = None
        if tsv_data:
            return convert_to_json(tsv_data)
        else:
            return None
    else:
        st.warning('Efetue o login novamente')


def get_evolucao_buying_committee(domain):  
    url = "https://gtmsi.cortex-intelligence.com/service/integration-cube-service.download"
    params = {
        "cube": '{"name": "[GTM-LINKEDIN] Evolução Buying Committee"}',
        "charset": "UTF-8",
        "filters": f'[{{"name":"dominio","value":"{domain}","exactMatch":true}}]'
    }
    headers = {
        "Content-Type": "text/csv;charset=UTF-8",
        "x-authorization-user-id": st.session_state.credentials['user_id'],
        "x-authorization-token": st.session_state.credentials['token']
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:      
            tsv_data = response.text        
        except:
            tsv_data = None
        if tsv_data:
            return convert_to_json(tsv_data)
        else:
            return None
    else:
        st.warning('Efetue o login novamente')




