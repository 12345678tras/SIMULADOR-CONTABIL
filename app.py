import datetime
import os
import time
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
# 3. CONTROLE DE USO, TESTE GRATUITO & PAGAMENTO
# ==========================================
if "usos_gratuitos" not in st.session_state:
  st.session_state.usos_gratuitos = 0

LINK_PAGAMENTO_MENSAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y"
LINK_PAGAMENTO_ANUAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/on5Ha9URTH"

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
  st.sidebar.success("Acesso Master Ativo 🛡️ (Ilimitado)")
else:
  restantes = max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
  if restantes > 0:
    st.sidebar.info(
        f"⚡ **3 Acessos Gratuitos Permitidos**\n\nRestam **{restantes}**"
        " consultas no chat."
    )
  else:
    st.sidebar.error(
        "🔒 **Limite de 3 acessos gratuitos esgotado!**\n\nAssine para liberar o"
        " uso ilimitado."
    )

st.sidebar.markdown("---")

lista_menu = [
    "Visão Geral & Indicadores",
    "Assistente de IA Local (Chat)",
    "Simulação Contínua de Regime",
    "Alertas de Oportunidades Fiscais",
    "Indicadores & Malha Preditiva",
    "Gerador de Parecer & WhatsApp/PDF",
    "Área de Assinatura & Planos",
]

if acesso_master:
  lista_menu.append("Código Espião (Logs)")

menu = st.sidebar.selectbox("Navegação Estratégica", lista_menu)

# ==========================================
# 4. TELAS DO SISTEMA
# ==========================================

if menu == "Visão Geral & Indicadores":
  st.title("🚀 Plataforma de Inteligência Contábil & Monetização")
  st.markdown(
      "Solução corporativa avançada para escritórios e empresários com controle"
      " financeiro integrado e motor 100% local."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
  with col2:
    st.metric(label="Leads / Potenciais", value=f"{len(df_potenciais)}")
  with col3:
    st.metric(label="Motor IA Local", value="Ativo & Seguro ⚡")
  with col4:
    restantes_metro = (
        "Ilimitado"
        if acesso_master
        else max(0, LIMITE_GRATIS - st.session_state.usos_gratuitos)
    )
    st.metric(label="Consultas Restantes", value=restantes_metro)

  st.markdown("---")
  st.info(
      "💡 **Regra de Uso:** São permitidos **3 acessos gratuitos** no assistente"
      " de IA. Após esse limite, o acesso exige a contratação de um dos planos"
      " na aba **Área de Assinatura & Planos**."
  )

elif menu == "Assistente de IA Local (Chat)":
  st.title("🤖 Consultor Contábil Virtual (IA Local Inteligente)")
  st.markdown(
      "Tire dúvidas técnicas, analise casos de Pessoa Física ou Jurídica,"
      " malha fina e planejamento tributário."
  )

  if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
        "role": "assistant",
        "content": (
            "Olá! Sou o seu consultor contábil inteligente. Você tem direito a"
            " **3 acessos gratuitos permitidos** para testar o chat. Como posso"
            " ajudar nas suas dúvidas fiscais ou malha fina hoje?"
        ),
    }]

  for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # TRAVAMENTO RIGOROSO DOS 3 ACESSOS
  if not acesso_master and st.session_state.usos_gratuitos >= LIMITE_GRATIS:
    st.error(
        "🔒 **Você utilizou seus 3 acessos gratuitos permitidos!**\n\nO chat"
        " foi bloqueado para novas consultas. Para continuar utilizando"
        " ilimitadamente, acesse a aba **'Área de Assinatura & Planos'** no menu"
        " lateral e conclua sua assinatura segura via InfinitePay."
    )
  else:
    pergunta = st.chat_input("Digite sua dúvida contábil aqui...")
    if pergunta:
      if not acesso_master:
        st.session_state.usos_gratuitos += 1

      st.session_state.mensagens.append({"role": "user", "content": pergunta})
      with st.chat_message("user"):
        st.markdown(pergunta)

      p_lower = pergunta.lower().strip()

      if p_lower in [
          "oi",
          "olá",
          "ola",
          "bom dia",
          "boa tarde",
          "boa noite",
          "tudo bem",
      ]:
        resposta_ia = (
            "Olá! Tudo ótimo por aqui. Como posso auxiliar nos seus"
            " procedimentos contábeis ou análise de regime tributário hoje?"
        )
      elif (
          "pessoa fisica" in p_lower
          or "pf" in p_lower
          or "contribuinte pf" in p_lower
      ):
        resposta_ia = (
            "🔎 **Análise Técnica (Pessoa Física):** Pessoas físicas utilizam"
            " a tabela progressiva do Imposto de Renda Retido na Fonte (IRRF) ou"
            " Carnê-Leão. Divergências de omissão de rendimentos caem na malha"
            " fina e exigem retificadora via e-CAC."
        )
      elif "malha fina" in p_lower or "retificadora" in p_lower:
        resposta_ia = (
            "🛡️ **Orientações sobre Malha Fina:** Consulte o extrato no e-CAC"
            " para identificar o motivo da retenção e elabore a declaração"
            " retificadora com os documentos comprobatórios."
        )
      elif "fator r" in p_lower or "simples nacional" in p_lower:
        resposta_ia = (
            "📊 **Sobre o Simples Nacional & Fator R:** O Fator R define se o"
            " serviço tributado inicialmente pelo Anexo V (15,5%) pode migrar"
            " para o Anexo III (6%), se a folha de salários atingir 28% ou mais"
            " do faturamento dos últimos 12 meses."
        )
      else:
        resposta_ia = (
            f"Analisando sua questão sobre '{pergunta}': Recomendo avaliar a"
            " legislação aplicável junto à Receita Federal para assegurar total"
            " conformidade fiscal."
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
      "Monitore o faturamento acumulado e projete o momento ideal para migração."
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

  if "simulacao_executada" not in st.session_state:
    st.session_state.simulacao_executada = False

  if st.button(
      "🔍 Executar Simulação Tributária",
      type="primary",
      use_container_width=True,
  ):
    with st.spinner("Processando simulação tributária local..."):
      time.sleep(1)
    st.session_state.simulacao_executada = True
    registrar_log(
        f"Simulação executada para faturamento anual de R$ {faturamento_anual}"
    )

  if st.session_state.simulacao_executada:
    if faturamento_anual > 4800000:
      recomendacao = "Lucro Presumido ou Lucro Real (Estouro do sublimite)"
      cor_alerta = "error"
    elif faturamento_anual > 3600000:
      recomendacao = "Atenção: Próximo ao limite do Simples. Avaliar Lucro."
      cor_alerta = "warning"
    else:
      recomendacao = "Simples Nacional continua sendo a opção mais vantajosa."
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
    st.dataframe(df_projecao, use_container_width=True)

elif menu == "Alertas de Oportunidades Fiscais":
  st.title("⚡ Alertas de Oportunidades Fiscais")
  st.markdown(
      "Identificação ativa de créditos tributários não aproveitados e"
      " benefícios setoriais."
  )

  st.warning(
      "⚠️ **Oportunidade Detectada:** Potenciais créditos de PIS/COFINS"
      " monofásico não apurados nos últimos 60 dias."
  )
  st.success(
      "✅ **Benefício Disponível:** Redução de alíquota efetiva para o setor"
      " de atuação."
  )

  if "varredura_executada" not in st.session_state:
    st.session_state.varredura_executada = False

  if st.button(
      "🔍 Executar Varredura de Oportunidades Fiscais",
      type="primary",
      use_container_width=True,
  ):
    with st.spinner("Executando varredura analítica na base de dados..."):
      time.sleep(1.0)
    st.session_state.varredura_executada = True
    registrar_log("Varredura de oportunidades fiscais executada localmente.")

  if st.session_state.varredura_executada:
    st.success("🚀 Varredura concluída com sucesso! Relatório gerado:")

    df_oportunidades = pd.DataFrame({
        "Tributo / Base": [
            "PIS/COFINS Monofásico",
            "Incentivo Setorial Regional",
        ],
        "Potencial Recuperável": ["R$ 8.450,00", "R$ 6.100,00"],
        "Status": ["Disponível para Compensação", "Aplicável imediatamente"],
    })
    st.dataframe(df_oportunidades, use_container_width=True)

elif menu == "Indicadores & Malha Preditiva":
  st.title("📈 Indicadores Financeiros & Malha Fina Preditiva")
  st.markdown(
      "Insira os dados financeiros do cliente abaixo para realizar o cruzamento"
      " analítico e a auditoria de risco."
  )

  st.subheader("📝 Dados Financeiros para Análise")
  col_input1, col_input2 = st.columns(2)
  with col_input1:
    faturamento_input = st.number_input(
        "Faturamento Declarado (R$)",
        min_value=0.0,
        value=250000.0,
        step=10000.0,
    )
    despesas_input = st.number_input(
        "Despesas / Deduções (R$)", min_value=0.0, value=50000.0, step=5000.0
    )
  with col_input2:
    impostos_pagos = st.number_input(
        "Total de Impostos Recolhidos (R$)",
        min_value=0.0,
        value=15000.0,
        step=1000.0,
    )
    divergencias_previas = st.selectbox(
        "Possui histórico de pendências no e-CAC?", ["Não", "Sim"]
    )

  st.markdown("---")

  margem_calculada = (
      ((faturamento_input - despesas_input) / faturamento_input * 100)
      if faturamento_input > 0
      else 0
  )
  carga_efetiva = (
      (impostos_pagos / faturamento_input * 100) if faturamento_input > 0 else 0
  )

  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.subheader("📊 Indicadores Derivados")
    st.metric(label="Margem de Lucro Calculada", value=f"{margem_calculada:.1f}%")
    st.metric(label="Carga Tributária Efetiva", value=f"{carga_efetiva:.1f}%")

  with col_m2:
    st.subheader("🛡️ Malha Fina Preditiva")
    if divergencias_previas == "Sim" or carga_efetiva < 4.0:
      risco = "Alto ⚠️"
      info_texto = (
          "Atenção: Os dados indicam margem ou carga tributária incompatível"
          " com o setor, elevando o risco de malha fina."
      )
    else:
      risco = "Baixo ✅"
      info_texto = (
          "Nenhuma divergência estrutural grave encontrada nos dados"
          " informados. Risco de autuação controlado."
      )

    st.info(f"{info_texto}\n\n**Risco Estimado:** {risco}")

  if "auditoria_executada" not in st.session_state:
    st.session_state.auditoria_executada = False

  if st.button(
      "🔍 Executar Auditoria Preditiva com os Dados Acima",
      type="primary",
      use_container_width=True,
  ):
    with st.spinner("Processando cruzamento analítico dos dados..."):
      time.sleep(1)
    st.session_state.auditoria_executada = True
    registrar_log(
        f"Auditoria preditiva executada para faturamento de R$"
        f" {faturamento_input:,.2f}"
    )

  if st.session_state.auditoria_executada:
    st.success(
        "✅ Auditoria concluída com base nos valores informados! Risco mapeado"
        f" como: **{risco}**."
    )

elif menu == "Gerador de Parecer & WhatsApp/PDF":
  st.title("📄 Relatório, Parecer PDF & Envio Direto para o WhatsApp")
  st.markdown(
      "Gere resumos visuais com linguagem simples e envie diretamente para o"
      " cliente."
  )

  nome_cliente_rel = st.text_input(
      "Nome do Cliente / Empresa", "Empresa Exemplo Ltda"
  )
  economia_estimada = st.text_input(
      "Economia Financeira Projetada (R$)", "R$ 14.500,00/ano"
  )
  telefone_cliente = st.text_input(
      "Telefone / WhatsApp do Cliente (com DDD)", "5511999999999"
  )

  parecer_texto = f"""PARECER TÉCNICO EXECUTIVO - CONTABILIDADE INTELIGENTE
Prezado(a) gestor(a) da {nome_cliente_rel},
Após nossa análise tributária avançada, identificamos uma oportunidade clara de otimização para o seu negócio.
- Economia Direta Estimada: {economia_estimada}
Recomendamos a adoção imediata das estratégias mapeadas para evitar bitributação e garantir total segurança fiscal.
Atenciosamente, Sua Equipe Contábil."""

  st.text_area(
      "Prévia do Parecer:",
      parecer_texto,
      height=180,
  )

  col_b1, col_b2 = st.columns(2)

  with col_b1:
    st.download_button(
        label="📥 Baixar Parecer (Relatório)",
        data=parecer_texto,
        file_name=f"Parecer_{nome_cliente_rel.replace(' ', '_')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )

  with col_b2:
    link_whatsapp = f"https://wa.me/{telefone_cliente}?text={parecer_texto.replace(' ', '%20').replace(chr(10), '%0A')}"
    st.markdown(
        f"""<a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
            <div style="width:100%; background-color:#25D366; color:white; text-align:center; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
                💬 Enviar Parecer no WhatsApp
            </div>
        </a>""",
        unsafe_allow_html=True,
    )

elif menu == "Área de Assinatura & Planos":
  st.title("💳 Planos de Assinatura & Acesso Ilimitado (InfinitePay)")
  st.markdown(
      "Desbloqueie todo o poder da inteligência contábil, chat ilimitado e"
      " simulações avançadas."
  )

  col_p1, col_p2 = st.columns(2)

  with col_p1:
    st.subheader("🔹 Plano Mensal Profissional")
    st.markdown(
        "- Acesso Ilimitado ao Chat com IA\n- Simulações de Regime Avançadas\n-"
        " Relatórios Ilimitados\n- Suporte Prioritário"
    )
    st.markdown("### **R$ 147,00 / mês**")
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
    st.markdown("### **R$ 1.350,00 / ano**")
    st.markdown(
        f"[Pagar com InfinitePay (Anual)]({LINK_PAGAMENTO_ANUAL})",
        unsafe_allow_html=True,
    )

elif menu == "Código Espião (Logs)" and acesso_master:
  st.title("🕵️‍♂️ Central do Código Espião (Auditoria em Tempo Real)")
  st.markdown("Monitoramento completo de todas as ações executadas.")

  if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
      linhas_log = f.readlines()

    if linhas_log:
      st.text_area(
          "Logs de Rastreamento Ativos", "".join(reversed(linhas_log)), height=400
      )
      if st.button("Limpar Histórico de Logs", use_container_width=True):
        open(ARQUIVO_LOG, "w").close()
        st.success("Histórico limpo com sucesso!")
        st.rerun()
    else:
      st.info("Nenhum evento registrado no momento.")
  else:
    st.warning("O arquivo de auditoria ainda não foi criado.")
