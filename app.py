import datetime
import os
import pandas as pd
import streamlit as st

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Simulador Contábil Inteligente & IA Local",
    page_icon="🛡️",
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


registrar_log("Sistema iniciado com IA Local Avançada e rastreamento espião.")

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
# 3. PAINEL LATERAL & CHAVE DE ACESSO (SEGURANÇA)
# ==========================================
st.sidebar.title("🔐 Painel de Controle")
st.sidebar.markdown("---")

senha_digitada = st.sidebar.text_input(
    "Chave de Acesso Master", type="password", placeholder="Digite sua senha..."
)
SENHA_MESTRE = "contadora2x"

acesso_liberado = senha_digitada == SENHA_MESTRE

if acesso_liberado:
  st.sidebar.success("Acesso Master Liberado 🛡️")
  registrar_log("Acesso master autenticado com sucesso.")
else:
  if senha_digitada:
    st.sidebar.error("Chave incorreta!")
    registrar_log("Tentativa de acesso com chave incorreta.", "ALERTA")
  else:
    st.sidebar.warning("Insira a chave de acesso para liberar os módulos.")

st.sidebar.markdown("---")

if acesso_liberado:
  menu = st.sidebar.selectbox(
      "Navegação Estratégica",
      [
          "Visão Geral & Indicadores",
          "Assistente de IA Local (Chat)",
          "Simulação Contínua de Regime",
          "Alertas de Oportunidades Fiscais",
          "Indicadores & Malha Preditiva",
          "Gerador de Parecer Executivo",
          "Código Espião (Logs)",
      ],
  )
else:
  menu = "Visão Geral & Indicadores"

# ==========================================
# 4. TELAS DO SISTEMA
# ==========================================

if menu == "Visão Geral & Indicadores":
  st.title("🚀 Plataforma de Inteligência Contábil & IA Local")
  st.markdown(
      "Solução corporativa avançada com inteligência fiscal integrada e pronta"
      " para uso imediato."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
  with col2:
    st.metric(label="Leads / Potenciais", value=f"{len(df_potenciais)}")
  with col3:
    st.metric(label="Módulo IA Local", value="Ativo ⚡")
  with col4:
    st.metric(
        label="Nível de Segurança",
        value="Blindado" if acesso_liberado else "Restrito",
    )

  st.markdown("---")
  st.info(
      "💡 **Dica:** Insira a sua **Chave de Acesso Master** (`contadora2x`) na"
      " barra lateral para desbloquear o Chat Inteligente e os demais"
      " simuladores."
  )
  registrar_log("Usuário visualizou a Visão Geral.")

elif menu == "Assistente de IA Local (Chat)":
  st.title("🤖 Consultor Contábil Virtual (IA Local Inteligente)")
  st.markdown(
      "Tire dúvidas técnicas, analise casos de Pessoa Física ou Jurídica,"
      " malha fina e planejamento tributário instantaneamente."
  )

  if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
        "role": "assistant",
        "content": (
            "Olá! Sou o seu consultor contábil inteligente local. Como posso"
            " ajudar nas suas dúvidas fiscais, malha fina ou distinção entre"
            " PJ e PF hoje?"
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

    # Motor de Inteligência Local Especializado em Contabilidade
    p_lower = pergunta.lower()
    if (
        "pessoa fisica" in p_lower
        or "pf" in p_lower
        or "contribuinte pf" in p_lower
    ):
      resposta_ia = (
          "🔎 **Análise Técnica (Pessoa Física):** Pessoas físicas não utilizam"
          " alíquotas e tabelas de apuração do Simples Nacional ou Lucro"
          " Presumido (que são exclusivas para Pessoa Jurídica / CNPJ). Para o"
          " CPF, a tributação baseia-se na tabela progressiva do Imposto de"
          " Renda Retido na Fonte (IRRF) ou Carnê-Leão. Caso tenha caído em"
          " malha fina por omissão de rendimentos, a declaração retificadora"
          " deve ser enviada diretamente pelo e-CAC."
      )
    elif "malha fina" in p_lower or "retificadora" in p_lower:
      resposta_ia = (
          "🛡️ **Orientações sobre Malha Fina:** Para corrigir divergências e"
          " sair da malha fina, é necessário verificar o extrato do e-CAC."
          " Caso haja erro em valores declarados, elabore uma declaração"
          " retificadora anexando os comprovantes e documentos hábeis (informes"
          " de rendimentos, recibos médicos, notas fiscais) para evitar"
          " autuações futuras."
      )
    elif "fator r" in p_lower or "simples nacional" in p_lower:
      resposta_ia = (
          "📊 **Sobre o Simples Nacional & Fator R:** O Fator R determina se"
          " uma empresa do Anexo V (serviços com alíquota inicial de 15,5%)"
          " pode ser tributada pelo Anexo III (alíquota inicial de 6%), desde"
          " que a folha de salários represente 28% ou mais do faturamento"
          " bruto dos últimos 12 meses."
      )
    else:
      resposta_ia = (
          f"Analisando a sua questão sobre '{pergunta}': Recomendo avaliar"
          " com cautela a legislação aplicável, seja no âmbito do IRPF (se"
          " contribuinte Pessoa Física) ou na apuração fiscal da empresa (se"
          " Pessoa Jurídica), garantindo a conformidade com as normas da"
          " Receita Federal e evitando riscos de autuação."
      )

    with st.chat_message("assistant"):
      st.markdown(resposta_ia)
    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_ia}
    )
    registrar_log(
        f"Interação com Chat IA Local realizada. Pergunta: {pergunta}"
    )

elif menu == "Simulação Contínua de Regime":
  st.title("📊 Simulação Contínua & Migração de Regime")
  st.markdown(
      "Monitore o faturamento acumulado e projete o momento ideal para migração"
      " (Simples Nacional vs. Lucro Presumido vs. Lucro Real)."
  )

  faturamento_anual = st.number_input(
      "Faturamento Acumulado Anual Estimado (R$)",
      min_value=0.0,
      value=3600000.0,
      step=50000.0,
  )
  setor_empresa = st.selectbox(
      "Segmento da Empresa", ["Comércio", "Serviço (Fator R)", "Indústria"]
  )

  if st.button("Analisar Viabilidade de Migração", type="primary"):
    if faturamento_anual > 4800000:
      recomendacao = "Lucro Presumido ou Lucro Real (Estouro do sublimite do Simples Nacional)"
      cor_alerta = "error"
    elif faturamento_anual > 3600000:
      recomendacao = (
          "Atenção Redobrada: Próximo ao limite do Simples. Avaliar Lucro"
          " Presumido."
      )
      cor_alerta = "warning"
    else:
      recomendacao = (
          "Simples Nacional continua sendo a opção mais vantajosa pela carga"
          " tributária efetiva."
      )
      cor_alerta = "success"

    getattr(st, cor_alerta)(f"**Diagnóstico de Migração:** {recomendacao}")

    df_projecao = pd.DataFrame({
        "Indicador": [
            "Faturamento Anual",
            "Teto do Simples",
            "Margem de Segurança",
        ],
        "Valor": [
            f"R$ {faturamento_anual:,.2f}",
            "R$ 4.800.000,00",
            f"R$ {max(0, 4800000 - faturamento_anual):,.2f}",
        ],
    })
    st.table(df_projecao)
    registrar_log(
        f"Simulação de migração executada para faturamento anual de R$"
        f" {faturamento_anual}"
    )

elif menu == "Alertas de Oportunidades Fiscais":
  st.title("⚡ Alertas Automáticos de Oportunidades Fiscais")
  st.markdown(
      "Identificação ativa de créditos tributários não aproveitados e"
      " benefícios setoriais."
  )

  st.warning(
      "⚠️ **Oportunidade Detectada:** Foram identificados potenciais créditos de"
      " PIS/COFINS monofásico não apurados nos últimos 60 dias para o CNPJ"
      " simulado."
  )
  st.success(
      "✅ **Benefício Fiscal Disponível:** Redução de alíquota efetiva aplicável"
      " para o setor de atuação via incentivos regionais."
  )

  if st.button("Executar Varredura de Oportunidades"):
    st.info(
        "Varredura concluída! Relatório de créditos gerado para apresentação"
        " comercial."
    )
    registrar_log("Varredura de oportunidades fiscais executada.")

elif menu == "Indicadores & Malha Preditiva":
  st.title("📈 Indicadores Financeiros & Malha Fina Preditiva")
  st.markdown(
      "Validação prévia de arquivos fiscais e métricas de desempenho"
      " empresarial."
  )

  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.subheader("📊 Indicadores Derivados")
    st.metric(label="Margem de Lucro Média Estimada", value="18.5%")
    st.metric(label="Carga Tributária Efetiva Média", value="8.2%")
  with col_m2:
    st.subheader("🛡️ Malha Fina Preditiva")
    st.info(
        "Nenhuma divergência encontrada entre os arquivos XMLs e o SPED"
        " simulado. Risco de autuação: **Baixo**."
    )
  registrar_log("Usuário consultou indicadores e malha preditiva.")

elif menu == "Gerador de Parecer Executivo":
  st.title("📄 Relatório / Parecer Automático em PDF Executivo")
  st.markdown(
      "Gere resumos visuais com linguagem simples, prontos para enviar no"
      " WhatsApp ou E-mail do cliente."
  )

  nome_cliente_rel = st.text_input(
      "Nome do Cliente / Empresa", "Empresa Exemplo Ltda"
  )
  economia_estimada = st.text_input(
      "Economia Financeira Projetada (R$)", "R$ 14.500,00/ano"
  )

  parecer_texto = f"""
    *PARECER TÉCNICO EXECUTIVO - CONTABILIDADE INTELIGENTE*
    Prezado(a) gestor(a) da {nome_cliente_rel},
    Após nossa análise tributária avançada, identificamos uma oportunidade clara de otimização para o seu negócio.
    💰 *Economia Direta Estimada:* {economia_estimada}
    Recomendamos a adoção imediata das estratégias mapeadas para evitar bitributação e garantir total segurança fiscal.
    Atenciosamente, Sua Equipe Contábil.
    """

  st.text_area(
      "Texto pronto para envio (Copie e cole no WhatsApp):",
      parecer_texto,
      height=200,
  )
  registrar_log(
      f"Parecer executivo gerado para o cliente: {nome_cliente_rel}"
  )

elif menu == "Código Espião (Logs)":
  st.title("🕵️‍♂️ Central do Código Espião (Auditoria em Tempo Real)")
  st.markdown(
      "Monitoramento completo de todas as ações executadas pelos usuários no"
      " sistema."
  )

  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      linhas_log = f.readlines()

    if linhas_log:
      st.text_area(
          "Logs de Rastreamento Ativos", "".join(reversed(linhas_log)), height=400
      )
      if st.button("Limpar Histórico de Logs"):
        open(ARQUIVO_LOG, "w").close()
        st.success("Histórico limpo com sucesso!")
        st.rerun()
    else:
      st.info("Nenhum evento registrado no momento.")
  else:
    st.warning("O arquivo de auditoria ainda não foi criado.")
  registrar_log("Usuário acessou o painel do Código Espião.")
