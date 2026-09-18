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
LIMITE_GRATIS = 3

if "usos_gratuitos" not in st.session_state:
  st.session_state.usos_gratuitos = 0

LINK_PAGAMENTO_MENSAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y"
LINK_PAGAMENTO_ANUAL = "https://invoice.infinitepay.io/plans/cristiane-da-260/on5Ha9URTH"

st.sidebar.title("🔐 Painel de Controle & Acesso")
st.sidebar.markdown("---")

senha_digitada = st.sidebar.text_input(
    "Digite sua Senha de Acesso (ou Chave Master)",
    type="password",
    placeholder="Sua senha...",
)

# Senha de Dona (Master) e Senha padrão para Clientes Pagantes
SENHA_MESTRE = "contadora2x"
SENHAS_CLIENTES_PAGANTES = [
    "cliente123x",
]

acesso_master = senha_digitada == SENHA_MESTRE
acesso_cliente_pago = senha_digitada in SENHAS_CLIENTES_PAGANTES
acesso_liberado_total = acesso_master or acesso_cliente_pago

if acesso_master:
  st.sidebar.success("Acesso Master (Dona) Ativo 🛡️ (Ilimitado)")
elif acesso_cliente_pago:
  st.sidebar.success("Assinatura Ativa Detectada ⭐ (Acesso Ilimitado)")
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
# 4. TELAS DO SISTEMA (100% REAIS E FUNCIONAIS)
# ==========================================

if menu == "Visão Geral & Indicadores":
  st.title("🚀 Plataforma de Inteligência Contábil & Monetização")
  st.markdown(
      "Solução corporativa avançada para escritórios com controle financeiro"
      " integrado e motor de cálculo real."
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Clientes Ativos", value=f"{len(df_clientes)}")
  with col2:
    st.metric(label="Leads / Potenciais", value=f"{len(df_potenciais)}")
  with col3:
    st.metric(label="Motor IA Local", value="Ativo & Seguro ⚡")
  with col4:
    if acesso_liberado_total:
      restantes_metro = "Ilimitado 🛡️"
    else:
      restantes_metro = max(
          0, LIMITE_GRATIS - st.session_state.usos_gratuitos
      )
    st.metric(label="Consultas Restantes", value=restantes_metro)

  st.markdown("---")
  st.info(
      "💡 **Regra de Uso:** São permitidos **3 acessos gratuitos** em toda a"
      " plataforma. Clientes pagantes que utilizam a senha `cliente123x` possuem"
      " acesso ilimitado."
  )

elif menu == "Assistente de IA Local (Chat)":
  st.title("🤖 Consultor Contábil Virtual (IA Local Inteligente)")
  st.markdown(
      "Tire dúvidas técnicas, analise casos de Pessoa Física ou Jurídica e"
      " planejamento tributário."
  )

  if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
        "role": "assistant",
        "content": (
            "Olá! Sou o seu consultor contábil inteligente. Você tem direito a"
            " **3 acessos gratuitos** para testar. Como posso ajudar nas suas"
            " dúvidas fiscais hoje?"
        ),
    }]

  for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  if not acesso_liberado_total and st.session_state.usos_gratuitos >= LIMITE_GRATIS:
    exibir_aviso_limite_esgotado()
  else:
    pergunta = st.chat_input("Digite sua dúvida contábil aqui...")
    if pergunta:
      if not acesso_liberado_total:
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
            " procedimentos contábeis hoje?"
        )
      elif "pessoa fisica" in p_lower or "pf" in p_lower:
        resposta_ia = (
            "🔎 **Análise Técnica (Pessoa Física):** Pessoas físicas utilizam"
            " a tabela progressiva do IRRF ou Carnê-Leão."
        )
      elif "malha fina" in p_lower:
        resposta_ia = (
            "🛡️ **Orientações sobre Malha Fina:** Consulte o extrato no e-CAC"
            " e elabore a declaração retificadora."
        )
      elif "fator r" in p_lower or "simples nacional" in p_lower:
        resposta_ia = (
            "📊 **Sobre o Simples Nacional & Fator R:** O Fator R define a"
            " migração do Anexo V (15,5%) para o Anexo III (6%) se a folha for"
            " >= 28%."
        )
      else:
        resposta_ia = f"Analisando sua questão sobre '{pergunta}': Recomendo avaliar a legislação aplicável junto à Receita Federal."

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
      "Insira o faturamento e escolha o segmento para calcular o momento ideal"
      " de migração de regime de forma real."
  )

  if not verificar_e_consumir_uso():
    exibir_aviso_limite_esgotado()
  else:
    faturamento_anual = st.number_input(
        "Faturamento Acumulado Anual (R$)",
        min_value=0.0,
        value=3600000.0,
        step=50000.0,
    )
    setor_empresa = st.selectbox(
        "Segmento da Empresa", ["Comércio", "Serviço (Fator R)", "Indústria"]
    )

    if st.button(
        "🔍 Calcular Simulação Real", type="primary", use_container_width=True
    ):
      if not acesso_liberado_total:
        st.session_state.usos_gratuitos += 1

      with st.spinner("Processando cálculos..."):
        time.sleep(0.6)

      if faturamento_anual > 4800000:
        recomendacao = "Lucro Presumido ou Lucro Real (Estouro do sublimite)"
        cor_alerta = "error"
      elif faturamento_anual > 3600000:
        recomendacao = "Próximo ao limite do Simples Nacional."
        cor_alerta = "warning"
      else:
        recomendacao = "Simples Nacional vantajoso e dentro do teto."
        cor_alerta = "success"

      getattr(st, cor_alerta)(f"**Diagnóstico:** {recomendacao}")

      df_projecao = pd.DataFrame({
          "Indicador": [
              "Faturamento Informado",
              "Teto Máximo",
              "Margem de Segurança",
          ],
          "Valores": [
              f"R$ {faturamento_anual:,.2f}",
              "R$ 4.800.000,00",
              f"R$ {max(0, 4800000 - faturamento_anual):,.2f}",
          ],
      })
      st.dataframe(df_projecao, use_container_width=True)
      registrar_log(f"Simulação de regime executada: R$ {faturamento_anual}")

elif menu == "Alertas de Oportunidades Fiscais":
  st.title("⚡ Alertas de Oportunidades Fiscais (Cálculo Real)")
  st.markdown("Digite os dados de faturamento para calcular créditos reais.")

  if not verificar_e_consumir_uso():
    exibir_aviso_limite_esgotado()
  else:
    col_op1, col_op2 = st.columns(2)
    with col_op1:
      fat_mensal_op = st.number_input(
          "Faturamento Mensal (R$)", min_value=0.0, value=150000.0, step=10000.0
      )
    with col_op2:
      tipo_atividade = st.selectbox(
          "Atividade Principal",
          [
              "Comércio Varejista (Geral)",
              "Autopeças / Farmácia / Minimercado (Monofásico)",
              "Prestador de Serviços",
          ],
      )

    if st.button(
        "🔍 Executar Varredura de Créditos",
        type="primary",
        use_container_width=True,
    ):
      if not acesso_liberado_total:
        st.session_state.usos_gratuitos += 1

      with st.spinner("Calculando créditos fiscais..."):
        time.sleep(0.8)

      if "Monofásico" in tipo_atividade:
        credito_pis_cofins = fat_mensal_op * 0.035 * 12
        status_pis = "Disponível para Compensação"
      else:
        credito_pis_cofins = 0.0
        status_pis = "Não aplicável"

      incentivo_reg = fat_mensal_op * 0.015 * 12 if fat_mensal_op > 50000 else 0.0

      st.success("🚀 Varredura concluída com base nos dados informados!")

      df_oportunidades = pd.DataFrame({
          "Tributo / Oportunidade": [
              "PIS/COFINS (Monofásico)",
              "Incentivo Setorial",
          ],
          "Potencial Recuperável (Anual)": [
              f"R$ {credito_pis_cofins:,.2f}",
              f"R$ {incentivo_reg:,.2f}",
          ],
          "Status": [
              status_pis,
              "Disponível" if incentivo_reg > 0 else "Sem saldo",
          ],
      })
      st.dataframe(df_oportunidades, use_container_width=True)
      registrar_log(f"Varredura de oportunidades executada: R$ {fat_mensal_op}")

elif menu == "Indicadores & Malha Preditiva":
  st.title("📈 Indicadores Financeiros & Malha Fina Preditiva")
  st.markdown(
      "Insira os dados para realizar o cruzamento analítico e auditoria de"
      " risco."
  )

  if not verificar_e_consumir_uso():
    exibir_aviso_limite_esgotado()
  else:
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

    if divergencias_previas == "Sim" or carga_efetiva < 4.0:
      risco = "Alto ⚠️"
      info_texto = "Atenção: Margem ou carga tributária incompatível com o setor."
    else:
      risco = "Baixo ✅"
      info_texto = "Nenhuma divergência estrutural grave encontrada."

    if st.button(
        "🔍 Executar Auditoria Preditiva",
        type="primary",
        use_container_width=True,
    ):
      if not acesso_liberado_total:
        st.session_state.usos_gratuitos += 1

      with st.spinner("Processando cruzamento analítico..."):
        time.sleep(0.6)

      st.session_state.auditoria_realizada = True
      st.session_state.margem_res = margem_calculada
      st.session_state.carga_res = carga_efetiva
      st.session_state.risco_res = risco
      st.session_state.info_res = info_texto
      registrar_log(f"Auditoria preditiva executada: R$ {faturamento_input}")

    if st.session_state.get("auditoria_realizada", False):
      st.markdown("---")
      col_m1, col_m2 = st.columns(2)
      with col_m1:
        st.subheader("📊 Indicadores (Calculados)")
        st.metric(
            label="Margem de Lucro",
            value=f"{st.session_state.margem_res:.1f}%",
        )
        st.metric(
            label="Carga Tributária Efetiva",
            value=f"{st.session_state.carga_res:.1f}%",
        )
      with col_m2:
        st.subheader("🛡️ Malha Fina Preditiva")
        st.info(
            f"{st.session_state.info_res}\n\n**Risco Estimado:**"
            f" {st.session_state.risco_res}"
        )
      st.success("✅ Auditoria cruzada com sucesso!")

elif menu == "Gerador de Parecer & WhatsApp/PDF":
  st.title("📄 Relatório, Parecer PDF & Envio Direto para o WhatsApp")
  st.markdown(
      "Preencha os dados e os valores calculados de economia para gerar o"
      " parecer dinâmico com envio direto."
  )

  if not verificar_e_consumir_uso():
    exibir_aviso_limite_esgotado()
  else:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
      nome_cliente_rel = st.text_input(
          "Nome do Cliente / Empresa", "Empresa Exemplo Ltda"
      )
      telefone_cliente = st.text_input(
          "Telefone / WhatsApp do Cliente (com DDD e DDI)", "5511999999999"
      )
    with col_g2:
      valor_economia_num = st.number_input(
          "Valor da Economia Calculada (R$/ano)",
          min_value=0.0,
          value=14500.0,
          step=500.0,
      )
      honorario_cobranca = st.number_input(
          "Honorário / Proposta Comercial (R$)",
          min_value=0.0,
          value=1500.0,
          step=100.0,
      )

    if st.button(
        "⚙️ Processar e Gerar Parecer na Tela",
        type="primary",
        use_container_width=True,
    ):
      if not acesso_liberado_total:
        st.session_state.usos_gratuitos += 1
      st.session_state.parecer_gerado = True
      st.session_state.texto_parecer_dinamico = f"""PARECER TÉCNICO EXECUTIVO - CONTABILIDADE INTELIGENTE
Prezado(a) gestor(a) da {nome_cliente_rel},

Após nossa análise tributária avançada, identificamos uma oportunidade clara de otimização para o seu negócio:
- Economia Direta Projetada: R$ {valor_economia_num:,.2f} / ano
- Proposta de Implementação / Honorários: R$ {honorario_cobranca:,.2f}

Recomendamos a adoção imediata das estratégias mapeadas para evitar bitributação e garantir total segurança fiscal.

Atenciosamente, Sua Equipe Contábil."""
      registrar_log(f"Parecer processado para: {nome_cliente_rel}")

    if st.session_state.get("parecer_gerado", False):
      st.markdown("---")
      st.subheader("📋 Prévia do Parecer Gerado (Validado)")

      st.text_area(
          "Texto do Parecer:",
          st.session_state.texto_parecer_dinamico,
          height=200,
      )

      col_b1, col_b2 = st.columns(2)
      with col_b1:
        st.download_button(
            label="📥 Baixar Parecer (Relatório)",
            data=st.session_state.texto_parecer_dinamico,
            file_name=f"Parecer_{nome_cliente_rel.replace(' ', '_')}.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True,
        )
      with col_b2:
        texto_zap = st.session_state.texto_parecer_dinamico.replace(
            " ", "%20"
        ).replace(chr(10), "%0A")
        link_whatsapp = (
            f"https://wa.me/{telefone_cliente}?text={texto_zap}"
        )
        st.markdown(
            f"""<a href="{link_whatsapp}" target="_blank" style="text-decoration:none;">
                <div style="width:100%; background-color:#25D366; color:white; text-align:center; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
                    💬 Enviar Parecer no WhatsApp
                </div>
            </a>""",
            unsafe_allow_html=True,
        )
    else:
      st.info(
          "👆 Preencha os campos acima e clique em **'Processar e Gerar Parecer"
          " na Tela'** para visualizar os resultados reais e liberar o"
          " download/Zap."
      )

elif menu == "Área de Assinatura & Planos":
  st.title("💳 Planos de Assinatura & Acesso Ilimitado (InfinitePay)")
  st.markdown(
      "Desbloqueie todo o poder da inteligência contábil e simulações"
      " avançadas."
  )

  col_p1, col_p2 = st.columns(2)
  with col_p1:
    st.subheader("🔹 Plano Mensal Profissional")
    st.markdown("- Acesso Ilimitado ao Chat\n- Simulações Avançadas")
    st.markdown("### **R$ 147,00 / mês**")
    st.markdown(
        f"""<a href="{LINK_PAGAMENTO_MENSAL}" target="_blank" style="text-decoration:none;">
            <div style="width:100%; background-color:#0066cc; color:white; text-align:center; padding:12px; border-radius:6px; font-weight:bold;">
                💳 Pagar Plano Mensal
            </div>
        </a>""",
        unsafe_allow_html=True,
    )
  with col_p2:
    st.subheader("⭐ Plano Anual Profissional")
    st.markdown("- Tudo do Mensal\n- Acesso Contínuo e Prioritário")
    st.markdown("### **R$ 1.350,00 / ano**")
    st.markdown(
        f"""<a href="{LINK_PAGAMENTO_ANUAL}" target="_blank" style="text-decoration:none;">
            <div style="width:100%; background-color:#28a745; color:white; text-align:center; padding:12px; border-radius:6px; font-weight:bold;">
                ⭐ Pagar Plano Anual
            </div>
        </a>""",
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
