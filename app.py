import datetime
import os
import google.generativeai as genai
import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA CHAVE DE API DO GEMINI
# ==========================================
# Cole aqui a chave que você gerou no Google AI Studio:
GEMINI_API_KEY = "SUA_CHAVE_AQUI"

if GEMINI_API_KEY and GEMINI_API_KEY != "SUA_CHAVE_AQUI":
  genai.configure(api_key=GEMINI_API_KEY)
  generation_config = {"temperature": 0.3}
  ai_model = genai.GenerativeModel(
      model_name="gemini-2.5-flash", generation_config=generation_config
  )
else:
  ai_model = None

# ==========================================
# CONFIGURAÇÕES DO SISTEMA E SENHAS
# ==========================================
SENHA_CLIENTE = "cliente123x"
SENHA_MESTRE = "admin999"
LOG_FILE = "auditoria_consultas.txt"

st.set_page_config(
    page_title="Plataforma de Consultoria Contábil IA",
    page_icon="📊",
    layout="wide",
)

if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
if "tipo_usuario" not in st.session_state:
  st.session_state.tipo_usuario = None


def registrar_log(usuario, tipo, mensagem):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"[{timestamp}] - Usuário: {usuario} ({tipo}) | Pergunta: {mensagem}\n")


# ==========================================
# TELA DE LOGIN / MONETIZAÇÃO (CORRIGIDA)
# ==========================================
if not st.session_state.autenticado:
  st.markdown("<br><br>", unsafe_allow_html=True)

  # Usando um layout centralizado e limpo para o login
  col_esq, col_centro, col_dir = st.columns([1, 2, 1])

  with col_centro:
    st.markdown("## 🔐 Acesso à Plataforma Contábil")
    st.write("Digite sua senha de acesso para entrar no assistente profissional.")

    senha_digitada = st.text_input("Senha de Acesso:", type="password")

    if st.button("Entrar na Plataforma", use_container_width=True):
      if senha_digitada == SENHA_MESTRE:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = "Administrador"
        st.rerun()
      elif senha_digitada == SENHA_CLIENTE:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = "Cliente"
        st.rerun()
      else:
        st.error("Senha incorreta. Verifique seus dados de acesso.")

    st.markdown("---")
    st.info(
        "💡 **Não tem acesso ou plano ativo?** Entre em contato com o"
        " escritório para adquirir sua assinatura mensal ou anual."
    )

  st.stop()

# ==========================================
# INTERFACE PRINCIPAL DO SISTEMA (APÓS LOGIN)
# ==========================================
st.sidebar.title("Painel de Controle")
st.sidebar.write(f"Logado como: **{st.session_state.tipo_usuario}**")

if st.sidebar.button("Sair / Encerrar Sessão"):
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None
  st.rerun()

if st.session_state.tipo_usuario == "Administrador":
  st.sidebar.markdown("---")
  st.sidebar.subheader("Área do Admin")
  if os.path.exists(LOG_FILE):
    if st.sidebar.button("Baixar Log de Auditoria"):
      with open(LOG_FILE, "r", encoding="utf-8") as f:
        st.sidebar.download_button(
            "Baixar Arquivo .txt", f.read(), file_name="auditoria.txt"
        )

st.title("💼 Assistente Contábil e Tributário Inteligente")
st.markdown(
    "Tire dúvidas sobre legislação fiscal, abertura de empresas, obrigações"
    " acessórias e planejamento tributário com suporte de IA em tempo real."
)

if "mensagens" not in st.session_state:
  st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
  with st.chat_message(mensagem["role"]):
    st.markdown(mensagem["content"])

pergunta = st.chat_input(
    "Digite sua dúvida contábil ou fiscal (ex: Como funciona o limite do MEI?"
    " )"
)

if pergunta:
  st.session_state.mensagens.append({"role": "user", "content": pergunta})
  with st.chat_message("user"):
    st.markdown(pergunta)

  registrar_log(st.session_state.tipo_usuario, "Consulta IA", pergunta)

  with st.chat_message("assistant"):
    with st.spinner("Analisando legislação e elaborando resposta..."):
      if not ai_model or GEMINI_API_KEY == "SUA_CHAVE_AQUI":
        resposta_final = (
            "⚠️ **Aviso:** A chave de API do Gemini não foi configurada."
        )
      else:
        try:
          prompt_sistema = (
              "Você é um consultor contábil, tributário e financeiro sênior,"
              " altamente especializado na legislação brasileira. Forneça"
              " respostas profissionais, precisas e estruturadas."
          )
          chat_contexto = [
              {
                  "role": "user" if m["role"] == "user" else "model",
                  "parts": [m["content"]],
              }
              for m in st.session_state.mensagens[:-1]
          ]
          chat = ai_model.start_chat(history=chat_contexto)
          full_prompt = f"{prompt_sistema}\n\nDúvida do cliente: {pergunta}"
          response = chat.send_message(full_prompt)
          resposta_final = response.text
        except Exception as e:
          resposta_final = f"Erro técnico ao processar com a IA: {str(e)}"

      st.markdown(resposta_final)
      st.session_state.mensagens.append(
          {"role": "assistant", "content": resposta_final}
      )
