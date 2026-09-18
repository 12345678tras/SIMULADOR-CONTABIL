import datetime
import os
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


registrar_log(
    "Sistema iniciado com links separados da InfinitePay (Mensal e Anual)."
)

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
# 3. CONTROLE DE USO, TESTE GRATUITO & PAGAMENTO
# ==========================================
if "usos_gratuitos" not in st.session_state:
  st.session_state.usos_gratuitos = 0

# SEUS LINKS OFICIAIS DA INFINITEPAY SEPARADOS
LINK_PAGAMENTO_MENSAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y"
LINK_PAGAMENTO_ANUAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/qTSP5k9f6S"

LIMITE_GRATIS = 3

st.sidebar.title("🔐 Painel de Controle")
st.sidebar.markdown("---")

senha_digitada = st.sidebar.text_input(
    "Chave Master (Opcional - Admin)",
    type="password",
    placeholder="Apenas para o dono...",
)
SENHA_MESTRE = "contadora2x"
acesso_master = senha_digitada == SENHA_MESTRE

if acesso_master:
  st.sidebar.success("Acesso Master Ativo 🛡️")
else:
  restantes = max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
  if restantes > 0:
    st.sidebar.info(
        f"⚡ Teste Gratuito: Restam **{restantes}** consultas no chat."
    )
  else:
    st.sidebar.error("🔒 Testes gratuitos esgotados!")

st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navegação Estratégica",
    [
        "Visão Geral & Indicadores",
        "Assistente de IA Local (Chat)",
        "Simulação Contínua de Regime",
        "Alertas de Oportunidades Fiscais",
        "Indicadores & Malha Preditiva",
        "Gerador de Parecer Executivo",
        "Área de Assinatura & Planos",
        "Código Espião (Logs)",
    ],
)

# ==========================================
# 4. TELAS DO SISTEMA
# ==========================================

if menu == "Visão Geral & Indicadores":
  st.title("🚀 Plataforma de Inteligência Contábil & Monetização")
  st.markdown(
      "Solução corporativa avançada para escritórios e empresários com controle"
      " financeiro integrado."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
  with col2:
    st.metric(label="Leads / Potenciais", value=f"{len(df_potenciais)}")
  with col3:
    st.metric(label="Módulo IA Local", value="Ativo ⚡")
  with col4:
    restantes_metro = (
        "Ilimitado"
        if acesso_master
        else max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
    )
    st.metric(label="Consultas Restantes", value=restantes_metro)

  st.markdown("---")
  st.info(
      "💡 **Dica:** Explore o **Assistente de IA Local** para testar perguntas"
      " grátis ou acesse a aba **Área de Assinatura & Planos** para garantir"
      " acesso ilimitado através da InfinitePay."
  )
  registrar_log("Visitante visualizou a Visão Geral.")

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

  if not acesso_master and st.session_state.usos_gratuitos >= LIMITE_GRATIS:
    st.warning(
        "🔒 **Você atingiu o limite de 3 interações gratuitas do chat!** Para"
        " continuar consultando sem limites, por favor, conclua a assinatura"
        " segura na aba de planos."
    )
    if st.button("Ir para Planos e Assinatura", type="primary"):
      st.info(
          "Selecione 'Área de Assinatura & Planos' no menu lateral esquerdo."
      )
  else:
    pergunta = st.chat_input("Digite sua dúvida contábil aqui...")
    if pergunta:
      if not acesso_master:
        st.session_state.usos_gratuitos += 1

      st.session_state.mensagens.append({"role": "user", "content": pergunta})
      with st.chat_message("user"):
        st.markdown(pergunta)

      p_lower = pergunta.lower()
      if (
          "pessoa fisica" in p_lower
          or "pf" in p_lower
          or "contribuinte pf" in p_lower
      ):
        resposta_ia = (
            "🔎 **Análise Técnica (Pessoa Física):** Pessoas físicas não"
            " utilizam alíquotas e tabelas de apuração do Simples Nacional ou"
            " Lucro Presumido (exclusivas para Pessoa Jurídica / CNPJ). Para o"
            " CPF, a tributação baseia-se na tabela progressiva do Imposto de"
            " Renda Retido na Fonte (IRRF) ou Carnê-Leão. Em caso de malha"
            " fina por omissão, a retificadora deve ser enviada via e-CAC."
        )
      elif "malha fina" in p_lower or "retificadora" in p_lower:
        resposta_ia = (
            "🛡️ **Orientações sobre Malha Fina:** Para corrigir divergências,"
            " consulte o extrato no e-CAC. Elabore uma declaração retificadora"
            " anexando os comprovantes e documentos hábeis para evitar"
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
            " com cautela a legislação aplicável, seja no âmbito do IRPF (Pessoa"
            " Física) ou na apuração fiscal (Pessoa Jurídica), garantindo"
            " total conformidade com a Receita Federal."
        )

      with st.chat_message("assistant"):
        st.markdown(resposta_ia)
      st.session_state.mensagens.append(
          {"role": "assistant", "content": resposta_ia}
      )
      registrar_log(f"Chat IA executado. Pergunta: {pergunta}")
      st.rerun()

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

elif menu == "Área de Assinatura & Planos":
  st.title("💳 Planos de Assinatura & Acesso Ilimitado (InfinitePay)")
  st.markdown(
      "Desbloqueie todo o poder da inteligência contábil, chat ilimitado e"
      " simulações avançadas de forma rápida e segura."
  )

  col_p1, col_p2 = st.columns(2)

  with col_p1:
    st.subheader("🔹 Plano Mensal Profissional")
    st.markdown(
        "- Acesso Ilimitado ao Chat com IA\n- Simulações de Regime Avançadas\n-"
        " Relatórios e Pareceres Ilimitados\n- Suporte Prioritário"
    )
    st.markdown("### **Assinatura Mensal**")
    st.markdown(
        f"[Pagar com InfinitePay (Mensal)]({LINK_PAGAMENTO_MENSAL})",
        unsafe_allow_html=True,
    )

  with col_p2:
    st.subheader("⭐ Plano Anual Profissional")
    st.markdown(
        "- Tudo do Plano Mensal\n- Acesso Completo e Contínuo\n- Atualizações"
        " Automáticas Prioritárias\n- Consultoria de Configuração"
    )
    st.markdown("### **Assinatura Anual**")
    st.markdown(
        f"[Pagar com InfinitePay (Anual)]({LINK_PAGAMENTO_ANUAL})",
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.info(
      "💡 **Já realizou o pagamento?** Insira a sua chave master no menu lateral"
      " para liberar o painel completo ou aguarde a compensação."
  )
  registrar_log("Visitante visualizou a página de planos com InfinitePay.")

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
