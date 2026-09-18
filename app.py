import datetime
import os
import google.generativeai as genai
import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA CHAVE DE API DO GEMINI
# ==========================================
# Cole aqui a chave que você acabou de gerar no Google AI Studio:
GEMINI_API_KEY = "SUA_CHAVE_AQUI"

if GEMINI_API_KEY and GEMINI_API_KEY != "SUA_CHAVE_AQUI":
  genai.configure(api_key=GEMINI_API_KEY)
  # Usando o modelo rápido e inteligente do Gemini
  generation_config = {"temperature": 0.3}  # Respostas mais objetivas e técnicas
  ai_model = genai.GenerativeModel(
      model_name="gemini-2.5-flash", generation_config=generation_config
  )
else:
  ai_model = None

# ==========================================
# CONFIGURAÇÕES DO SISTEMA E SENHAS
# ==========================================
SENHA_CLIENTE = "cliente123x"
SENHA_MESTRE = "admin999"  # Altere para sua senha mestre se desejar
LOG_FILE = "auditoria_consultas.txt"

st.set_page_config(
    page_title="Plataforma de Consultoria Contábil IA",
    page_icon="📊",
    layout="wide",
)

# Inicializar o controle de sessão
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
if "tipo_usuario" not in st.session_state:
  st.session_state.tipo_usuario = None


# Função para registrar logs de auditoria
def registrar_log(usuario, tipo, mensagem):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"[{timestamp}] - Usuário: {usuario} ({tipo}) | Pergunta: {mensagem}\n")


# ==========================================
# TELA DE LOGIN / MONETIZAÇÃO
# ==========================================
if not st.session_state.autenticado:
  st.title("🔐 Acesso à Plataforma de Inteligência Contábil")
  st.markdown(
      "Por favor, insira sua senha de acesso para utilizar o assistente"
      " profissional."
  )

  senha_digitada = st.text_input("Senha de Acesso:", type="password")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Entrar"):
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

  with col2:
    st.info(
        "💡 **Não tem acesso?** Entre em contato com o escritório para adquirir"
        " seu plano mensal ou anual."
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

# Área do Administrador (se for admin)
if st.session_state.tipo_usuario == "Administrador":
  st.sidebar.markdown("---")
  st.sidebar.subheader("Área do Admin")
  if os.path.exists(LOG_FILE):
    if st.sidebar.button("Baixar Log de Auditoria"):
      with open(LOG_FILE, "r", encoding="utf-8") as f:
        st.sidebar.download_button(
            "Baixar Arquivo .txt", f.read(), file_name="auditoria.txt"
        )

# Título da Aplicação
st.title("💼 Assistente Contábil e Tributário Inteligente")
st.markdown(
    "Tire dúvidas sobre legislação fiscal, abertura de empresas, obrigações"
    " acessórias e planejamento tributário com suporte de IA em tempo real."
)

# Inicializar histórico de chat na tela
if "mensagens" not in st.session_state:
  st.session_state.mensagens = []

# Exibir histórico de conversas
for mensagem in st.session_state.mensagens:
  with st.chat_message(mensagem["role"]):
    st.markdown(mensagem["content"])

# Entrada do usuário (pergunta)
pergunta = st.chat_input(
    "Digite sua dúvida contábil ou fiscal (ex: Como funciona o limite do MEI?"
    " )"
)

if pergunta:
  # Adicionar mensagem do usuário ao histórico
  st.session_state.mensagens.append({"role": "user", "content": pergunta})
  with st.chat_message("user"):
    st.markdown(pergunta)

  # Registrar auditoria
  registrar_log(
      st.session_state.tipo_usuario,
      "Consulta IA",
      pergunta,
  )

  # Resposta da IA
  with st.chat_message("assistant"):
    with st.spinner("Analisando legislação e elaborando resposta..."):
      if not ai_model or GEMINI_API_KEY == "SUA_CHAVE_AQUI":
        resposta_final = (
            "⚠️ **Aviso de Configuração:** A chave de API do Gemini ainda não"
            " foi configurada corretamente no código. Por favor, insira sua"
            " chave válida para ativar as respostas inteligentes."
        )
      else:
        try:
          # Prompt de Sistema customizado para garantir respostas contábeis de alto nível
          prompt_sistema = (
              "Você é um consultor contábil, tributário e financeiro sênior,"
              " altamente especializado na legislação brasileira (Simples"
              " Nacional, Lucro Presumido, Lucro Real, MEI, obrigações"
              " acessórias, etc.). Forneça respostas profissionais, precisas,"
              " estruturadas em tópicos quando necessário, orientando o"
              " cliente de forma clara, prática e segura dentro da lei."
          )

          # Histórico recente para contexto da conversa
          chat_contexto = [
              {
                  "role": "user" if m["role"] == "user" else "model",
                  "parts": [m["content"]],
              }
              for m in st.session_state.mensagens[:-1]
          ]

          # Criar chat com histórico e instrução de sistema
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
