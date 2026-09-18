import datetime
import os
import pandas as pd
import streamlit as st

# Tenta importar o cliente da Groq para a IA, se disponível
try:
  from groq import Groq
except ImportError:
  Groq = None

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Simulador Contábil Profissional com IA",
    page_icon="🤖",
    layout="wide",
)

# ==========================================
# 1. SISTEMA DE AUDITORIA & LOGS
# ==========================================
ARQUIVO_LOG = "sistema_auditoria.log"


def registrar_log(acao, tipo="INFO"):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  mensagem_log = f"[{timestamp}] [{tipo}] {acao}\n"
  try:
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
      f.write(mensagem_log)
  except Exception as e:
    print(f"Erro no log: {e}")


registrar_log("Sistema iniciado com módulos completos e IA.")

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
# 3. INTERFACE VISUAL (SIDEBAR E NAVEGAÇÃO)
# ==========================================
st.sidebar.title("🤖 Painel Contábil & IA")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navegação",
    [
        "Visão Geral",
        "Clientes Ativos",
        "Potenciais Clientes",
        "Simulador Tributário & IA",
        "Assistente Inteligente (Chat)",
        "Auditoria de Sistema",
    ],
)

# ==========================================
# 4. TELAS DO SISTEMA
# ==========================================

if menu == "Visão Geral":
  st.title("🚀 Central de Controle Contábil")
  st.markdown(
      "Ambiente integrado de gestão empresarial, simulação fiscal e suporte"
      " avançado por Inteligência Artificial."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
  with col2:
    st.metric(label="Potenciais Clientes", value=f"{len(df_potenciais)}")
  with col3:
    st.metric(label="Módulo IA", value="Ativo ⚡")
  with col4:
    st.metric(label="Segurança", value="Blindado 🛡️")

  st.markdown("---")
  st.subheader("💡 Como utilizar o sistema")
  st.info(
      "Utilize o menu lateral para navegar entre as carteiras, efetuar"
      " simulações de impostos detalhadas ou conversar diretamente com o"
      " Consultor IA."
  )
  registrar_log("Usuário acessou a Visão Geral.")

elif menu == "Clientes Ativos":
  st.title("📁 Gestão de Clientes Ativos")
  st.markdown("Base de dados corporativa sincronizada.")

  if not df_clientes.empty:
    st.dataframe(df_clientes, use_container_width=True)
  else:
    st.warning(
        f"O arquivo '{ARQUIVO_CLIENTES}' não foi encontrado ou está vazio na"
        " raiz."
    )
  registrar_log("Usuário consultou Clientes Ativos.")

elif menu == "Potenciais Clientes":
  st.title("🎯 Prospecção de Potenciais Clientes")
  st.markdown("Acompanhamento de leads e oportunidades de conversão.")

  if not df_potenciais.empty:
    st.dataframe(df_potenciais, use_container_width=True)
  else:
    st.warning(
        f"O arquivo '{ARQUIVO_POTENCIAIS}' não foi encontrado na raiz."
    )
  registrar_log("Usuário consultou Potenciais Clientes.")

elif menu == "Simulador Tributário & IA":
  st.title("🧮 Simulador de Carga Tributária Avançado")
  st.markdown(
      "Compare o peso dos tributos entre os regimes e obtenha insights da IA."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    faturamento = st.number_input(
        "Faturamento Bruto Mensal (R$)",
        min_value=0.0,
        value=60000.0,
        step=5000.0,
    )
    setor = st.selectbox("Setor de Atuação", ["Comércio", "Serviços", "Indústria"])
  with col_b:
    folha = st.number_input(
        "Folha de Pagamento Mensal (R$)", min_value=0.0, value=15000.0, step=1000.0
    )

  if st.button("Calcular e Gerar Parecer da IA", type="primary"):
    # Cálculos simulados
    if setor == "Comércio":
      simples = faturamento * 0.06
      presumido = faturamento * 0.0593
    elif setor == "Serviços":
      simples = faturamento * 0.15
      presumido = faturamento * 0.1633
    else:
      simples = faturamento * 0.08
      presumido = faturamento * 0.095

    res_df = pd.DataFrame({
        "Regime": ["Simples Nacional", "Lucro Presumido"],
        "Imposto Estimado (R$)": [simples, presumido],
    })
    st.table(res_df)

    st.markdown("### 🤖 Análise Inteligente do Consultor")
    melhor_regime = (
        "Simples Nacional" if simples < presumido else "Lucro Presumido"
    )
    st.success(
        f"Com base nos dados informados, a tendência mais econômica estimada é"
        f" o **{melhor_regime}**."
    )
    registrar_log(
        f"Simulação executada via painel para Faturamento R$ {faturamento}"
    )

elif menu == "Assistente Inteligente (Chat)":
  st.title("🤖 Consultor Contábil Virtual (IA)")
  st.markdown(
      "Tire dúvidas sobre tributos, planejamento fiscal e legislação em"
      " tempo real."
  )

  # Histórico de conversas no chat
  if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
        "role": "assistant",
        "content": (
            "Olá! Sou o seu assistente contábil inteligente. Como posso"
            " ajudar nos seus cálculos ou dúvidas fiscais hoje?"
        ),
    }]

  for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  pergunta = st.chat_input("Digite sua dúvida contábil aqui...")
  if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
      st.markdown(pergunta)

    # Resposta simulada ou integrada via IA
    resposta_ia = (
        f"Analisando a sua questão sobre '{pergunta}': Recomendo avaliar o"
        " impacto do faturamento e da folha de salários (fator R) para garantir"
        " a melhor alíquota no Simples Nacional ou verificar a apuração no"
        " Lucro Presumido."
    )

    with st.chat_message("assistant"):
      st.markdown(resposta_ia)
    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_ia}
    )
    registrar_log("Usuário interagiu com o Chat de IA.")

elif menu == "Auditoria de Sistema":
  st.title("🛡️ Registro de Auditoria & Logs")
  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      linhas = f.readlines()
    st.text_area("Logs Ativos", "".join(reversed(linhas)), height=350)
  else:
    st.info("Nenhum registro de log encontrado.")
  registrar_log("Usuário consultou os logs de auditoria.")
