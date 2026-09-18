import datetime
import os
import pandas as pd
import streamlit as st

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Simulador Contábil Profissional",
    page_icon="📊",
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
    print(f"Erro no log espião: {e}")


registrar_log("Sistema iniciado com protocolos de blindagem ativos.")

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
    # Cria um DataFrame padrão caso o arquivo não exista
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
st.sidebar.title("📊 Painel Contábil")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navegação",
    [
        "Visão Geral",
        "Clientes Ativos",
        "Potenciais Clientes",
        "Simulador Tributário",
        "Auditoria de Sistema",
    ],
)

# ==========================================
# 4. TELAS DO SISTEMA
# ==========================================

if menu == "Visão Geral":
  st.title("🚀 Bem-vindo ao Simulador Contábil")
  st.markdown(
      "Gerencie carteiras, faça simulações de tributos e acompanhe métricas"
      " essenciais com alta performance."
  )

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(
        label="Clientes Ativos", value=f"{len(df_clientes)} empresas"
    )
  with col2:
    st.metric(
        label="Potenciais Clientes", value=f"{len(df_potenciais)} leads"
    )
  with col3:
    st.metric(label="Status do Sistema", value="Online & Blindado 🛡️")

  st.markdown("---")
  st.subheader("💡 Instruções Rápidas")
  st.info(
      "Utilize o menu lateral para alternar entre as bases de clientes,"
      " realizar simulações fiscais dinâmicas e visualizar os registros de"
      " auditoria."
  )
  registrar_log("Usuário acessou a Visão Geral.")

elif menu == "Clientes Ativos":
  st.title("📁 Carteira de Clientes Ativos")
  st.markdown(
      "Lista completa de empresas ativas integradas ao sistema contábil."
  )

  if not df_clientes.empty:
    st.dataframe(df_clientes, use_container_width=True)
  else:
    st.warning(
        f"Nenhum dado encontrado no arquivo '{ARQUIVO_CLIENTES}'. Certifique-se"
        " de que a planilha está na raiz."
    )
  registrar_log("Usuário consultou Clientes Ativos.")

elif menu == "Potenciais Clientes":
  st.title("🎯 Gestão de Potenciais Clientes (Leads)")
  st.markdown("Acompanhamento de prospecções e oportunidades de negócio.")

  if not df_potenciais.empty:
    st.dataframe(df_potenciais, use_container_width=True)
  else:
    st.warning(
        f"Nenhum dado encontrado no arquivo '{ARQUIVO_POTENCIAIS}'. Verifique o"
        " diretório."
    )
  registrar_log("Usuário consultou Potenciais Clientes.")

elif menu == "Simulador Tributário":
  st.title("🧮 Simulador de Carga Tributária")
  st.markdown(
      "Simule o impacto fiscal entre diferentes regimes (Simples Nacional,"
      " Lucro Presumido e Lucro Real)."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    faturamento = st.number_input(
        "Faturamento Bruto Mensal (R$)",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
    )
    setor = st.selectbox("Setor de Atuação", ["Comércio", "Serviços", "Indústria"])

  with col_b:
    folha_salarios = st.number_input(
        "Folha de Pagamento Mensal (R$)", min_value=0.0, value=10000.0, step=500.0
    )

  if st.button("Executar Simulação Fiscal", type="primary"):
    # Simulação básica lógica baseada em alíquotas médias estimadas
    if setor == "Comércio":
      imposto_simples = faturamento * 0.06
      imposto_presumido = faturamento * 0.0593
    elif setor == "Serviços":
      imposto_simples = faturamento * 0.15
      imposto_presumido = faturamento * 0.1633
    else:
      imposto_simples = faturamento * 0.08
      imposto_presumido = faturamento * 0.095

    st.success("Simulação concluída com sucesso!")

    res_df = pd.DataFrame({
        "Regime Tributário": ["Simples Nacional", "Lucro Presumido"],
        "Imposto Mensal Estimado (R$)": [imposto_simples, imposto_presumido],
        "Alíquota Efetiva Média": [
            f"{(imposto_simples/faturamento)*100:.2f}%",
            f"{(imposto_presumido/faturamento)*100:.2f}%",
        ],
    })
    st.table(res_df)
    registrar_log(
        f"Simulação executada para Faturamento: R$ {faturamento} | Setor:"
        f" {setor}"
    )

elif menu == "Auditoria de Sistema":
  st.title("🛡️ Log de Auditoria e Segurança")
  st.markdown("Registro em tempo real das atividades executadas no ambiente.")

  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      linhas_log = f.readlines()

    if linhas_log:
      st.text_area(
          "Logs do Sistema", "".join(reversed(linhas_log)), height=350
      )
    else:
      st.info("O arquivo de log está vazio no momento.")
  else:
    st.warning("Nenhum registro de log gerado até o momento.")
  registrar_log("Usuário acessou o painel de Auditoria.")
