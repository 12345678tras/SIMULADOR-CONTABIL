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
# CONFIGURAÇÕES DO SISTEMA E SENHAS OFICIAIS
# ==========================================
SENHA_CLIENTE = "cliente123x"
SENHA_MESTRE = "contadora2x"
LOG_FILE = "auditoria_consultas.txt"

st.set_page_config(
    page_title="Plataforma de Consultoria Contábil IA",
    page_icon="📊",
    layout="wide",
)

# Inicializar o controle de sessão e tentativas de senha
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
if "tipo_usuario" not in st.session_state:
  st.session_state.tipo_usuario = None
if "tentativas" not in st.session_state:
  st.session_state.tentativas = 0
if "bloqueado" not in st.session_state:
  st.session_state.bloqueado = False


def registrar_log(usuario, tipo, mensagem):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"[{timestamp}] - Usuário: {usuario} ({tipo}) | Pergunta: {mensagem}\n")


# ==========================================
# TELA DE LOGIN / MONETIZAÇÃO COM LIMITE DE 3 TENTATIVAS
# ==========================================
if not st.session_state.autenticado:
  st.markdown("<br><br>", unsafe_allow_html=True)
  col_esq, col_centro, col_dir = st.columns([1, 2, 1])

  with col_centro:
    st.markdown("## 🔐 Acesso à Plataforma Contábil")

    # Verifica se o usuário já estourou o limite de tentativas
    if st.session_state.bloqueado:
      st.error(
          "⚠️ **ACESSO BLOQUEADO POR SEGURANÇA**\n\nVocê excedeu o limite"
          " máximo de 3 tentativas incorretas de acesso. Por motivos de"
          " segurança e conformidade do nosso programa, esta sessão foi"
          " bloqueada. Entre em contato com o suporte do escritório para"
          " reaver suas credenciais."
      )
      st.stop()

    st.write("Digite sua senha de acesso para entrar no assistente profissional.")
    senha_digitada = st.text_input("Senha de Acesso:", type="password")

    tentativas_restantes = 3 - st.session_state.tentativas
    st.caption(
        f"Tentativas restantes antes do bloqueio: {tentativas_restantes}"
    )

    if st.button("Entrar na Plataforma", use_container_width=True):
      if senha_digitada == SENHA_MESTRE:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = "Administrador"
        st.session_state.tentativas = 0
        st.rerun()
      elif senha_digitada == SENHA_CLIENTE:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = "Cliente"
        st.session_state.tentativas = 0
        st.rerun()
      else:
        st.session_state.tentativas += 1
        if st.session_state.tentativas >= 3:
          st.session_state.bloqueado = True
          st.rerun()
        else:
          st.error(
              f"Senha incorreta. Você tem mais {3 - st.session_state.tentativas}"
              " tentativa(s) antes do bloqueio de segurança."
          )

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
  st.session_state.tentativas = 0
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
            "⚠️ **Aviso de Configuração:** A chave de API do Gemini não foi"
            " inserida corretamente no código."
        )
      else:
        try:
          prompt_sistema = (
              "Você é um consultor contábil, tributário e financeiro sênior,"
              " altamente especializado na legislação brasileira (Simples"
              " Nacional, Lucro Presumido, Lucro Real, MEI, obrigações"
              " acessórias, etc.). Forneça respostas profissionais, precisas,"
              " estruturadas em tópicos quando necessário, orientando o"
              " cliente de forma clara, prática e segura dentro da lei."
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
          resposta_final = (
              f"Desculpe, ocorreu um erro técnico ao processar sua"
              f" solicitação com a IA: {str(e)}"
          )

      st.markdown(resposta_final)
      st.session_state.mensagens.append(
          {"role": "assistant", "content": resposta_final}
      )
