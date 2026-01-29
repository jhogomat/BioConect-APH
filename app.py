import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Inicialização do Firebase (mesmo padrão anterior)
if not firebase_admin._apps:
    cred = credentials.Certificate("sua-chave-firebase.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- FUNÇÕES DE AUTENTICAÇÃO ---
def logar_usuario(email, senha):
    try:
        # Nota: O Firebase Admin SDK foca em gestão. 
        # Em produção, usa-se a API REST ou o Client SDK para validar a senha.
        # Aqui simulamos a verificação de existência do usuário para o fluxo.
        user = auth.get_user_by_email(email)
        return True, user.display_name
    except:
        return False, None

# --- INTERFACE DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2563/2563319.png", width=100)
    st.header("🔐 BioConnect - Acesso Restrito")
    
    with st.form("login_form"):
        email = st.text_input("E-mail Profissional")
        senha = st.text_input("Senha", type="password")
        botao_login = st.form_submit_button("Entrar no Sistema")
        
        if botao_login:
            sucesso, nome = logar_usuario(email, senha)
            if sucesso:
                st.session_state.logado = True
                st.session_state.usuario_nome = nome
                st.rerun()
            else:
                st.error("Usuário não autorizado ou senha incorreta.")
    
    st.info("Consulte o Administrador de TI para novos cadastros de socorristas.")

# --- CONTEÚDO PROTEGIDO ---
else:
    st.sidebar.success(f"Conectado: {st.session_state.usuario_nome}")
    if st.sidebar.button("Sair/Logout"):
        st.session_state.logado = False
        st.rerun()

    # Inserir aqui o código anterior (Tabs de Ficha APH e Dashboard)
    st.write(f"### Bem-vindo ao Ecossistema de Gestão de Qualidade, {st.session_state.usuario_nome}")
    # ... Restante do código das Fichas e Dashboards ...
