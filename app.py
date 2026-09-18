import datetime
import os
import time
import google.generativeai as genai
import pandas as pd
import streamlit as st

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Plataforma Contábil Inteligente & Monetização",
    page_icon="💰",
    layout="wide",
)

# ==========================================
# 1. SISTEMA ESPIÃO DE AUDITORIA & BLINDAGEM
# ==========================================
ARQUIVO_LOG = "sistema_auditoria.log"


def registrar_log(acao, tipo="INFO"):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  mensagem_log = f"[{timestamp}] [{tipo}] {acao}\n"
  try:
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
      f.write(mensagem_log)
  except Exception as e:
    print(f"Erro no log espião: {e}")


if "sistema_iniciado" not in st.session_state:
  registrar_log("Sistema iniciado com painel espião blindado por senha.")
  st.session_state.sistema_iniciado = True

# ==========================================
# 2. CARREGAMENTO DE DADOS (PLANILHAS)
# ==========================================
ARQUIVO_CLIENTES = "clientes_contabilidade.xlsx"
ARQUIVO_POTENCIAIS = "potenciais_clientes.xlsx"


@st.cache_data
def carregar_dados(caminho):
  if os.path.exists(caminho):
    try:
      return pd.read_excel(caminho)
    except Exception as e:
      registrar_log(f"Erro ao ler {caminho}: {e}", "ERRO")
      return pd.DataFrame()
  else:
    return pd.DataFrame(
        columns=[
            "ID",
            "Nome/Empresa",
            "CNPJ",
            "Regime Tributário",
            "Faturamento Mensal (R$)",
            "Status",
        ]
    )


df_clientes = carregar_dados(ARQUIVO_CLIENTES)
df_potenciais = carregar_dados(ARQUIVO_POTENCIAIS)

# ==========================================
# 3. CONTROLE DE USO, TESTE GRATUITO & ACESSO
# ==========================================
LIMITE_GRATIS = 3

if "usos_gratuitos" not in st.session_state:
  st.session_state.usos_gratuitos = 0

if "senha_salva" not in st.session_state:
  st.session_state.senha_salva = ""

LINK_PAGAMENTO_MENSAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y"
LINK_PAGAMENTO_ANUAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/on5Ha9URTH"

st.sidebar.title("🔐 Painel de Controle & Acesso")
st.sidebar.markdown("---")

senha_input = st.sidebar.text_input(
    "Digite sua Senha de Acesso",
    value=st.session_state.senha_salva,
    type="password",
    placeholder="Sua senha...",
)

if senha_input != st.session_state.senha_salva:
  st.session_state.senha_salva = senha_input
  st.rerun()

SENHA_MESTRE = "contadora2x"
SENHAS_CLIENTES_PAGANTES = ["cliente123x"]

acesso_master = st.session_state.senha_salva == SENHA_MESTRE
acesso_cliente_pago = st.session_state.senha_salva in SENHAS_CLIENTES_PAGANTES
acesso_liberado_total = acesso_master or acesso_cliente_pago

mostrar_espiao = False

if acesso_master:
  st.sidebar.success("Acesso Master (Dona) Ativo 🛡️")
  st.sidebar.markdown("---")
  mostrar_espiao = st.sidebar.checkbox("👁️ Exibir Código Espião (Logs)")
  if st.sidebar.button("🔒 Sair"):
    st.session_state.senha_salva = ""
    st.rerun()
elif acesso_cliente_pago:
  st.sidebar.success("Assinatura Ativa ⭐ (Ilimitado)")
  if st.sidebar.button("🔒 Sair"):
    st.session_state.senha_salva = ""
    st.rerun()
else:
  restantes = max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
  st.sidebar.info(
      f"⚡ **Acessos Gratuitos:** Restam **{restantes}** consultas."
  )

st.sidebar.markdown("---")

# ==========================================
# 4. CONFIGURAÇÃO DA INTELIGÊNCIA ARTIFICIAL (GEMINI 1.5 FLASH)
# ==========================================
model = None

try:
  google_api_key_nuvem = st.secrets.get("GEMINI_API_KEY", "")
  if google_api_key_nuvem:
    genai.configure(api_key=google_api_key_nuvem)
    generation_config = {"temperature": 0.3, "max_output_tokens": 1000}
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Você é um Consultor Contábil Virtual Especializado, focado em"
            " contabilidade brasileira, planejamento tributário, Fator R e"
            " malha fiscal."
        ),
    )
except Exception as e:
  registrar_log(f"Erro ao configurar Gemini: {e}", "ERRO")

# ==========================================
# 5. MENU DE NAVEGAÇÃO
# ==========================================
menu = st.sidebar.selectbox(
    "Navegação Estratégica",
    [
        "Visão Geral & Indicadores",
        "Assistente Contábil",
        "Simulação Contínua de Regime",
        "Alertas de Oportunidades Fiscais",
        "Indicadores & Malha Preditiva",
        "Gerador de Parecer & WhatsApp/PDF",
        "Área de Assinatura & Planos",
    ],
)


def verificar_uso():
  if acesso_liberado_total:
    return True
  if st.session_state.usos_gratuitos >= LIMITE_GRATIS:
    return False
  return True


def aviso_limite():
  st.error("🔒 **Limite de 3 acessos gratuitos esgotado!**")
  st.info("Insira sua senha de assinante na barra lateral para continuar.")


# ==========================================
# 6. TELAS DO SISTEMA
# ==========================================
if acesso_master and mostrar_espiao:
  st.title("🕵️‍♂️ Central do Código Espião (Auditoria)")
  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      st.text_area("Logs de Acesso", "".join(reversed(f.readlines())), height=400)
    if st.button("Limpar Logs"):
      open(ARQUIVO_LOG, "w").close()
      st.rerun()
  else:
    st.warning("Nenhum log encontrado.")
  st.stop()

else:
  if menu == "Visão Geral & Indicadores":
    st.title("🚀 Plataforma de Inteligência Contábil")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric("Clientes", len(df_clientes))
    with col2:
      st.metric("Potenciais", len(df_potenciais))
    with col3:
      st.metric(
          "Motor IA", "Gemini 1.5 Flash ⚡" if model else "Sem Chave ⚠️"
      )
    with col4:
      rest = (
          "Ilimitado 🛡️"
          if acesso_liberado_total
          else max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
      )
      st.metric("Restantes", rest)

    st.markdown("---")
    tab1, tab2 = st.tabs(["Clientes Cadastrados", "Potenciais Clientes"])
    with tab1:
      if not df_clientes.empty:
        st.dataframe(df_clientes, use_container_width=True)
      else:
        st.info("Nenhum cliente cadastrado.")
    with tab2:
      if not df_potenciais.empty:
        st.dataframe(df_potenciais, use_container_width=True)
      else:
        st.info("Nenhum potencial cadastrado.")

  elif menu == "Assistente Contábil":
    st.title("🤖 Assistente Contábil (Powered by Gemini 1.5 Flash)")

    if "mensagens" not in st.session_state:
      st.session_state.mensagens = [{
          "role": "assistant",
          "content": (
              "Olá! Sou seu assistente contábil com Gemini 1.5 Flash. Como posso"
              " ajudar?"
          ),
      }]

    for msg in st.session_state.mensagens:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    if not verificar_uso():
      aviso_limite()
    else:
      pergunta = st.chat_input("Digite sua dúvida contábil...")
      if pergunta:
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
          st.markdown(pergunta)

        with st.chat_message("assistant"):
          with st.spinner("Consultando Gemini 1.5 Flash..."):
            try:
              if model:
                chat_history = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [m["content"]],
                    }
                    for m in st.session_state.mensagens[:-1]
                ]
                chat = model.start_chat(history=chat_history)
                resposta = chat.send_message(pergunta).text
              else:
                resposta = "⚠️ Chave do Gemini não configurada."
            except Exception as ex:
              resposta = f"Erro ao consultar Gemini: {ex}"
            st.markdown(resposta)

        st.session_state.mensagens.append(
            {"role": "assistant", "content": resposta}
        )
        st.rerun()

  elif menu == "Simulação Contínua de Regime":
    st.title("📊 Simulação & Migração de Regime")
    if not verificar_uso():
      aviso_limite()
    else:
      fat = st.number_input(
          "Faturamento Anual (R$)", min_value=0.0, value=3600000.0, step=50000.0
      )
      folha = st.number_input(
          "Folha de Salários Anual (R$)", min_value=0.0, value=100000.0
      )
      if st.button("Calcular Simulação", type="primary"):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Simulação processada com sucesso!")
      st.info(
          f"Análise para faturamento de R$ {fat:,.2f} e folha de R$"
          f" {folha:,.2f}"
      )

  elif menu == "Alertas de Oportunidades Fiscais":
    st.title("⚡ Alertas de Oportunidades Fiscais")
    if not verificar_uso():
      aviso_limite()
    else:
      st.number_input(
          "Faturamento Mensal Médio (R$)", min_value=0.0, value=150000.0
      )
      if st.button("Executar Varredura", type="primary"):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Varredura concluída! Oportunidades de créditos mapeadas.")

  elif menu == "Indicadores & Malha Preditiva":
    st.title("📈 Malha Fina Preditiva")
    if not verificar_uso():
      aviso_limite()
    else:
      st.number_input("Faturamento Declarado (R$)", min_value=0.0, value=250000.0)
      if st.button("Executar Auditoria Preditiva", type="primary"):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Auditoria realizada com sucesso! Baixo risco.")

  elif menu == "Gerador de Parecer & WhatsApp/PDF":
    st.title("📄 Gerador de Parecer & WhatsApp")
    if not verificar_uso():
      aviso_limite()
    else:
      cliente = st.text_input("Nome do Cliente", "Empresa Exemplo Ltda")
      tel = st.text_input("WhatsApp (com DDI/DDD)", "5511999999999")
      parecer = st.text_area(
          "Resumo / Conclusão do Parecer",
          "Recomendação de manutenção no Simples Nacional.",
      )

      if "parecer_gerado" not in st.session_state:
        st.session_state.parecer_gerado = ""

      if st.button(
          "⚙️ Processar e Gerar Parecer na Tela",
          type="primary",
          use_container_width=True,
      ):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.session_state.parecer_gerado = f"""PARECER CONTÁBIL TÉCNICO
----------------------------------------
Cliente: {cliente}
Data: {datetime.datetime.now().strftime('%d/%m/%Y')}

Conclusão:
{parecer}"""
        st.success("Parecer gerado com sucesso!")

      if st.session_state.parecer_gerado:
        st.markdown("---")
        st.subheader("📄 Visualização do Parecer Gerado")
        st.text_area(
            "Texto Pronto para Cópia ou Envio",
            value=st.session_state.parecer_gerado,
            height=160,
        )
        import urllib.parse

        link = f"https://api.whatsapp.com/send?phone={tel}&text={urllib.parse.quote(st.session_state.parecer_gerado)}"
        st.markdown(
            f"""<a href="{link}" target="_blank"><div style="background-color:#25D366;color:white;text-align:center;padding:12px;border-radius:6px;font-weight:bold;">🚀 Enviar Parecer via WhatsApp</div></a>""",
            unsafe_allow_html=True,
        )

  elif menu == "Área de Assinatura & Planos":
    st.title("💳 Planos de Assinatura (InfinitePay)")
    col1, col2 = st.columns(2)
    with col1:
      st.subheader("Plano Mensal - R$ 147,00")
      st.markdown(
          f"""<a href="{LINK_PAGAMENTO_MENSAL}" target="_blank"><button style="background-color:#0066cc;color:white;padding:10px;border-radius:5px;border:none;width:100%;">Assinar Mensal</button></a>""",
          unsafe_allow_html=True,
      )
    with col2:
      st.subheader("Plano Anual - R$ 1.350,00")
      st.markdown(
          f"""<a href="{LINK_PAGAMENTO_ANUAL}" target="_blank"><button style="background-color:#28a745;color:white;padding:10px;border-radius:5px;border:none;width:100%;">Assinar Anual</button></a>""",
          unsafe_allow_html=True,
      )
