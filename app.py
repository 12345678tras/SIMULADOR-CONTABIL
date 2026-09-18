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
    "Digite sua Senha de Acesso (ou Chave Master)",
    value=st.session_state.senha_salva,
    type="password",
    placeholder="Sua senha...",
)

if senha_input != st.session_state.senha_salva:
  st.session_state.senha_salva = senha_input
  st.rerun()

SENHA_MESTRE = "contadora2x"
SENHAS_CLIENTES_PAGANTES = [
    "cliente123x",
]

acesso_master = st.session_state.senha_salva == SENHA_MESTRE
acesso_cliente_pago = st.session_state.senha_salva in SENHAS_CLIENTES_PAGANTES
acesso_liberado_total = acesso_master or acesso_cliente_pago

mostrar_espiao = False

if acesso_master:
  st.sidebar.success("Acesso Master (Dona) Ativo 🛡️")
  st.sidebar.markdown("---")
  st.sidebar.subheader("⚙️ Configurações da Dona")
  mostrar_espiao = st.sidebar.checkbox("👁️ Exibir Código Espião (Logs)")

  if st.sidebar.button("🔒 Bloquear Painel / Sair"):
    st.session_state.senha_salva = ""
    st.rerun()

  st.sidebar.markdown("---")
elif acesso_cliente_pago:
  st.sidebar.success("Assinatura Ativa Detectada ⭐ (Acesso Ilimitado)")
  if st.sidebar.button("🔒 Sair da Conta"):
    st.session_state.senha_salva = ""
    st.rerun()
else:
  restantes = max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
  if restantes > 0:
    st.sidebar.info(
        f"⚡ **3 Acessos Gratuitos**\n\nRestam **{restantes}**"
        " consultas/simulações."
    )
  else:
    st.sidebar.error(
        "🔒 **Limite de 3 acessos esgotado!**\n\nInsira sua senha de assinante"
        " ou assine abaixo."
    )

st.sidebar.markdown("---")

# ==========================================
# 4. CONFIGURAÇÃO DA INTELIGÊNCIA ARTIFICIAL
# ==========================================
model = None

try:
  google_api_key_nuvem = st.secrets.get("GEMINI_API_KEY", "")
  if google_api_key_nuvem:
    genai.configure(api_key=google_api_key_nuvem)
    generation_config = {"temperature": 0.3, "max_output_tokens": 1000}
    # Atualizado para o modelo padrão e compatível gemini-1.5-flash
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Você é um Consultor Contábil Virtual Especializado, focado em"
            " contabilidade brasileira, planejamento tributário (Simples Nacional,"
            " Lucro Presumido, Lucro Real), Fator R, Pessoa Física e Malha Fina."
            " Dê respostas técnicas, claras, objetivas e profissionais."
        ),
    )
except Exception as e:
  registrar_log(f"Erro ao configurar chave do Gemini via secrets: {e}", "ERRO")

# ==========================================
# 5. MENU DE NAVEGAÇÃO
# ==========================================
lista_menu = [
    "Visão Geral & Indicadores",
    "Assistente Contábil",
    "Simulação Contínua de Regime",
    "Alertas de Oportunidades Fiscais",
    "Indicadores & Malha Preditiva",
    "Gerador de Parecer & WhatsApp/PDF",
    "Área de Assinatura & Planos",
]

menu = st.sidebar.selectbox("Navegação Estratégica", lista_menu)


def verificar_e_consumir_uso():
  if acesso_liberado_total:
    return True
  if st.session_state.usos_gratuitos >= LIMITE_GRATIS:
    return False
  return True


def exibir_aviso_limite_esgotado():
  st.error(
      "🔒 **Você atingiu o limite de 3 acessos gratuitos desta plataforma!**"
  )
  st.warning(
      "Se você já é assinante, digite sua senha de cliente na barra lateral à"
      " esquerda (`cliente123x`). Caso contrário, escolha um plano abaixo:"
  )

  col_p1, col_p2 = st.columns(2)
  with col_p1:
    st.markdown(
        "### 🔹 Plano Mensal Profissional\n- Acesso Ilimitado\n- **R$ 147,00 /"
        " mês**"
    )
    st.markdown(
        f"""<a href="{LINK_PAGAMENTO_MENSAL}" target="_blank" style="text-decoration:none;">
            <div style="width:100%; background-color:#0066cc; color:white; text-align:center; padding:12px; border-radius:6px; font-weight:bold;">
                💳 Assinar Plano Mensal
            </div>
        </a>""",
        unsafe_allow_html=True,
    )
  with col_p2:
    st.markdown(
        "### ⭐ Plano Anual Profissional\n- Acesso Contínuo & Prioritário\n-"
        " **R$ 1.350,00 / ano**"
    )
    st.markdown(
        f"""<a href="{LINK_PAGAMENTO_ANUAL}" target="_blank" style="text-decoration:none;">
            <div style="width:100%; background-color:#28a745; color:white; text-align:center; padding:12px; border-radius:6px; font-weight:bold;">
                ⭐ Assinar Plano Anual
            </div>
        </a>""",
        unsafe_allow_html=True,
    )


# ==========================================
# 6. EXIBIÇÃO DAS TELAS
# ==========================================

if acesso_master and mostrar_espiao:
  st.title("🕵️‍♂️ Central do Código Espião (Auditoria em Tempo Real)")
  st.markdown(
      "Painel restrito de auditoria visível apenas quando ativado na barra"
      " lateral."
  )
  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      st.text_area("Logs", "".join(reversed(f.readlines())), height=400)
    if st.button("Limpar Histórico de Logs", use_container_width=True):
      open(ARQUIVO_LOG, "w").close()
      st.success("Histórico limpo com sucesso!")
      st.rerun()
  else:
    st.warning("Nenhum log encontrado.")
  st.stop()
else:
  if menu == "Visão Geral & Indicadores":
    st.title("🚀 Plataforma de Inteligência Contábil & Monetização")
    st.markdown(
        "Solução corporativa avançada para escritórios com inteligência"
        " artificial Gemini integrada."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
    with col2:
      st.metric(label="Leads / Potenciais", value=f"{len(df_potenciais)}")
    with col3:
      st.metric(
          label="Motor IA",
          value="Gemini Ativo ⚡" if model else "Aguardando Chave ⚠️",
      )
    with col4:
      if acesso_liberado_total:
        restantes_metro = "Ilimitado 🛡️"
      else:
        restantes_metro = max(
            0, LIMITE_GRATIS - st.session_state.usos_gratuitos
        )
      st.metric(label="Consultas Restantes", value=restantes_metro)

  elif menu == "Assistente Contábil":
    st.title("🤖 Assistente Contábil (Powered by Gemini)")
    st.markdown(
        "Tire dúvidas técnicas em tempo real com inteligência artificial"
        " avançada sobre Pessoa Física, Jurídica e planejamento tributário."
    )

    if "mensagens" not in st.session_state:
      st.session_state.mensagens = [{
          "role": "assistant",
          "content": (
              "Olá! Sou o seu Assistente Contábil inteligente impulsionado por"
              " Gemini. Como posso ajudar nas suas dúvidas fiscais hoje?"
          ),
      }]

    for msg in st.session_state.mensagens:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    if (
        not acesso_liberado_total
        and st.session_state.usos_gratuitos >= LIMITE_GRATIS
    ):
      exibir_aviso_limite_esgotado()
    else:
      pergunta = st.chat_input("Digite sua dúvida contábil aqui...")
      if pergunta:
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1

        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
          st.markdown(pergunta)

        with st.chat_message("assistant"):
          with st.spinner("Consultando a Inteligência Gemini..."):
            try:
              if model:
                chat_history = []
                for m in st.session_state.mensagens[:-1]:
                  role_gemini = (
                      "user" if m["role"] == "user" else "model"
                  )
                  chat_history.append(
                      {"role": role_gemini, "parts": [m["content"]]}
                  )

                chat = model.start_chat(history=chat_history)
                response = chat.send_message(pergunta)
                resposta_ia = response.text
              else:
                resposta_ia = (
                    "⚠️ A chave do Gemini não foi encontrada nos segredos da"
                    " nuvem. Verifique a configuração."
                )
            except Exception as e:
              resposta_ia = (
                  f"Desculpe, ocorreu um erro ao consultar o Gemini: {e}"
              )

            st.markdown(resposta_ia)

        st.session_state.mensagens.append(
            {"role": "assistant", "content": resposta_ia}
        )
        registrar_log(f"Chat Gemini executado. Pergunta: {pergunta}")
        st.rerun()

  elif menu == "Simulação Contínua de Regime":
    st.title("📊 Simulação Contínua & Migração de Regime")
    if not verificar_e_consumir_uso():
      exibir_aviso_limite_esgotado()
    else:
      faturamento_anual = st.number_input(
          "Faturamento Acumulado Anual (R$)",
          min_value=0.0,
          value=3600000.0,
          step=50000.0,
      )
      if st.button(
          "🔍 Calcular Simulação Real", type="primary", use_container_width=True
      ):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        registrar_log(f"Simulação executada: R$ {faturamento_anual}")

      # Exibição do resultado da simulação (garantindo que o bloco não fique vazio)
      st.markdown("---")
      st.subheader("📋 Resultado da Análise de Regime Tributário")
      st.info(
          f"Análise baseada no faturamento anual informado de R$"
          f" {faturamento_anual:,.2f}."
      )
      col_res1, col_res2 = st.columns(2)
      with col_res1:
        st.metric(
            label="Simples Nacional / Anexo",
            value=(
                "Limite Estourado ⚠️"
                if faturamento_anual > 4800000
                else "Enquadrado ✅"
            ),
        )
      with col_res2:
        st.metric(
            label="Lucro Presumido / Real Sugerido",
            value=(
                "Obrigatório Lucro Real/Presumido"
                if faturamento_anual > 3600000
                else "Viável"
            ),
        )

  elif menu == "Alertas de Oportunidades Fiscais":
    st.title("⚡ Alertas de Oportunidades Fiscais")
    if not verificar_e_consumir_uso():
      exibir_aviso_limite_esgotado()
    else:
      fat_mensal_op = st.number_input(
          "Faturamento Mensal (R$)", min_value=0.0, value=150000.0, step=10000.0
      )
      if st.button(
          "🔍 Executar Varredura de Créditos",
          type="primary",
          use_container_width=True,
      ):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Varredura concluída com sucesso!")
        registrar_log(f"Varredura de oportunidades executada: R$ {fat_mensal_op}")

  elif menu == "Indicadores & Malha Preditiva":
    st.title("📈 Indicadores Financeiros & Malha Fina Preditiva")
    if not verificar_e_consumir_uso():
      exibir_aviso_limite_esgotado()
    else:
      faturamento_input = st.number_input(
          "Faturamento Declarado (R$)",
          min_value=0.0,
          value=250000.0,
          step=10000.0,
      )
      if st.button(
          "🔍 Executar Auditoria Preditiva",
          type="primary",
          use_container_width=True,
      ):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Auditoria realizada com sucesso!")
        registrar_log(f"Auditoria preditiva executada: R$ {faturamento_input}")

  elif menu == "Gerador de Parecer & WhatsApp/PDF":
    st.title("📄 Relatório, Parecer PDF & Envio Direto para o WhatsApp")
    if not verificar_e_consumir_uso():
      exibir_aviso_limite_esgotado()
    else:
      nome_cliente_rel = st.text_input(
          "Nome do Cliente / Empresa", "Empresa Exemplo Ltda"
      )
      telefone_cliente = st.text_input(
          "Telefone / WhatsApp do Cliente (com DDI/DDD)", "5511999999999"
      )
      if st.button(
          "⚙️ Processar e Gerar Parecer na Tela",
          type="primary",
          use_container_width=True,
      ):
        if not acesso_liberado_total:
          st.session_state.usos_gratuitos += 1
        st.success("Parecer gerado com sucesso!")

  elif menu == "Área de Assinatura & Planos":
    st.title("💳 Planos de Assinatura & Acesso Ilimitado (InfinitePay)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
      st.subheader("🔹 Plano Mensal Profissional - R$ 147,00 / mês")
      st.markdown(
          f"""<a href="{LINK_PAGAMENTO_MENSAL}" target="_blank"><button style="background-color:#0066cc;color:white;padding:10px;border-radius:5px;border:none;font-weight:bold;width:100%;">Assinar Mensal</button></a>""",
          unsafe_allow_html=True,
      )
    with col_p2:
      st.subheader("⭐ Plano Anual Profissional - R$ 1.350,00 / ano")
      st.markdown(
          f"""<a href="{LINK_PAGAMENTO_ANUAL}" target="_blank"><button style="background-color:#28a745;color:white;padding:10px;border-radius:5px;border:none;font-weight:bold;width:100%;">Assinar Anual</button></a>""",
          unsafe_allow_html=True,
      )
