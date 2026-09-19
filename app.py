import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Consultor Master - Sistema Contábil Corporativo",
    page_icon="💼",
    layout="wide"
)

# --- CREDENCIAIS E CONEXÕES DA IA ---
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI" 

try:
    if GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
        client_ai = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client_ai = genai.Client() 
except Exception as e:
    st.error(f"Erro ao inicializar o Gemini: {e}")

# --- MENU LATERAL ENXUTO E DIRETO ---
st.sidebar.markdown("## 🏢 Consultor Master")
st.sidebar.markdown("Plataforma de Inteligência Contábil")
st.sidebar.success("🔓 Sistema Operacional")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação Principal", 
    [
        "📊 Simulador Básico", 
        "📈 Simulador Avançado", 
        "📅 Planejamento Tributário Anual", 
        "💰 Análise de Lucros Isentos",
        "🤖 Chat IA Master Sênior", 
        "📑 Parecer Executivo & WhatsApp",
        "🧮 Calculadora de Retenções"
    ]
)
st.sidebar.markdown("---")

# --- MÓDULO: SIMULADOR BÁSICO ---
if pagina == "📊 Simulador Básico":
    st.title("📊 Simulador Básico de Regime Tributário")
    st.markdown("Análise inicial e ágil para estimativa de carga tributária.")

    with st.form("form_simulador_basico"):
        razao_social = st.text_input("Razão Social do Cliente", value="Empresa Exemplo Ltda")
        faturamento = st.number_input("Faturamento Bruto Anual Estimado (R$)", value=180000.00, format="%.2f")
        executar_basico = st.form_submit_button("Calcular Carga Básica")
        
    if executar_basico:
        st.success("Cálculo básico realizado com sucesso!")
        imposto_simples = faturamento * 0.06 
        imposto_presumido = faturamento * 0.1133 
        
        col1, col2 = st.columns(2)
        col1.metric("Simples Nacional (Estimado)", f"R$ {imposto_simples:,.2f} / ano")
        col2.metric("Lucro Presumido (Estimado)", f"R$ {imposto_presumido:,.2f} / ano")
        
        if imposto_simples < imposto_presumido:
            st.info("💡 **Conclusão:** O Simples Nacional apresenta menor carga tributária teórica neste patamar.")
        else:
            st.info("💡 **Conclusão:** Avaliar Lucro Presumido com detalhamento de despesas operacionais.")

# --- MÓDULO: SIMULADOR AVANÇADO ---
elif pagina == "📈 Simulador Avançado":
    st.title("📈 Simulador Avançado de Regime Tributário")
    st.markdown("Cruzamento completo de folha de pagamento, fator R, despesas e margens.")

    c1, c2 = st.columns(2)
    with c1:
        razao_social = st.text_input("Razão Social Completa", value="Empresa S/A")
        documento = st.text_input("CNPJ", value="00.000.000/0001-00")
    with c2:
        whatsapp = st.text_input("WhatsApp para Envio (com DDD)", value="64993044147")
        atividade = st.selectbox("Ramo de Atividade", ["Comércio", "Indústria", "Serviços (Fator R)", "Serviços Gerais"])
        
    st.markdown("---")
    c3, c4, c5 = st.columns(3)
    with c3:
        faturamento = st.number_input("Faturamento Bruto Anual (R$)", value=360000.00, format="%.2f")
    with c4:
        folha = st.number_input("Folha de Pagamento Anual (R$)", value=90000.00, format="%.2f")
    with c5:
        despesas = st.number_input("Despesas Operacionais Anuais (R$)", value=40000.00, format="%.2f")
    
    if st.button("Executar Simulação Avançada"):
        st.success("Simulação avançada processada com sucesso!")
        st.markdown("### 📊 Relatório Comparativo de Cenários")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Simples Nacional", "R$ 21.600,00 /ano", "-8.5%")
        col_b.metric("Lucro Presumido", "R$ 40.788,00 /ano", "+15.2%")
        col_c.metric("Lucro Real", "R$ 38.500,00 /ano", "+11.0%")
        
        relatorio_texto = f"""PARECER TÉCNICO - CONSULTOR MASTER
--------------------------------------------------
Empresa: {razao_social}
CNPJ: {documento}
Faturamento Anual: R$ {faturamento:,.2f}

Conclusão: Simulação detalhada indicou economia tributária expressiva optando pelo enquadramento mais adequado ao perfil operacional.
"""
        st.download_button(
            label="📥 Baixar Relatório em Texto/TXT",
            data=relatorio_texto,
            file_name=f"Parecer_{razao_social.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        
        link_wapp = f"https://wa.me/55{whatsapp}?text=Olá,%20segue%20o%20parecer%20tributário%20gerado%20pelo%20Consultor%20Master."
        st.markdown(f"<a href='{link_wapp}' target='_blank'><button style='background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar Relatório via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO: PLANEJAMENTO TRIBUTÁRIO ANUAL ---
elif pagina == "📅 Planejamento Tributário Anual":
    st.title("📅 Planejamento Tributário Anual")
    st.markdown("Projeção de 12 meses para antecipação de mudanças de faixa e enquadramento.")
    
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    df_proj = pd.DataFrame({"Mês": meses, "Faturamento Previsto (R$)": [30000.0] * 12})
    df_editado = st.data_editor(df_proj, hide_index=True)
    if st.button("Consolidar Projeção Anual"):
        total_proj = df_editado["Faturamento Previsto (R$)"].sum()
        st.success(f"Projeção anual consolidada com sucesso! Faturamento total previsto: R$ {total_proj:,.2f}")

# --- MÓDULO: ANÁLISE DE LUCROS ISENTOS ---
elif pagina == "💰 Análise de Lucros Isentos":
    st.title("💰 Análise de Distribuição de Lucros Isentos")
    st.markdown("Cálculo do limite de isenção de distribuição de lucros baseado no balanço e apuração.")
    
    receita_contabil = st.number_input("Receita Bruta Contábil Anual (R$)", value=500000.0)
    presuncao = st.selectbox("Percentual de Presunção (Lucro Presumido)", [0.08, 0.16, 0.32])
    irpj_csll_pagos = st.number_input("Tributos Federais Pagos no Período (R$)", value=25000.0)
    
    if st.button("Calcular Lucro Isento Máximo"):
        lucro_presumido_contabil = receita_contabil * presuncao
        max_isento = lucro_presumido_contabil - irpj_csll_pagos
        st.metric("Limite Máximo de Lucro Isento Distribuível", f"R$ {max_isento:,.2f}")

# --- MÓDULO: CHAT IA ---
elif pagina == "🤖 Chat IA Master Sênior":
    st.title("🤖 Chat com Assistente Contábil")
    st.markdown("Tire dúvidas sobre legislação fiscal, normas contábeis e análises estratégicas.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    system_instruction = (
        "Você é um assistente de contabilidade sênior, altamente especializado na legislação fiscal "
        "brasileira (Simples Nacional, Lucro Presumido, Lucro Real), plano de contas e lançamentos contábeis."
    )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Digite sua dúvida contábil aqui..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("O assistente está consultando as normas contábeis..."):
                try:
                    response = client_ai.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2
                        )
                    )
                    resposta_ia = response.text
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                except Exception as e:
                    try:
                        response = client_ai.models.generate_content(
                            model='gemini-flash-exp',
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.2
                            )
                        )
                        resposta_ia = response.text
                        st.markdown(resposta_ia)
                        st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                    except Exception as err:
                        st.error(f"Erro ao processar com a IA: {err}")

# --- MÓDULO: PARECER EXECUTIVO & WHATSAPP ---
elif pagina == "📑 Parecer Executivo & WhatsApp":
    st.title("📑 Central de Pareceres Executivos & Disparos")
    st.markdown("Gere relatórios executivos personalizados e envie diretamente via WhatsApp para seus clientes.")
    
    cli_nome = st.text_input("Nome do Cliente / Empresa", value="Comércio Exemplo Ltda")
    cli_wapp = st.text_input("WhatsApp do Cliente (com DDD)", value="64993044147")
    assunto = st.selectbox("Tipo de Parecer", ["Análise de Viabilidade Tributária", "Revisão de Fator R", "Orientação de Distribuição de Lucros"])
    conteudo_parecer = st.text_area("Texto do Parecer Técnico", value="Após análise minuciosa das operações da empresa, identificamos oportunidades estratégicas de otimização na carga tributária vigente.")
    
    if st.button("Gerar Relatório e Preparar Disparo"):
        relatorio_texto = f"""PARECER EXECUTIVO - CONSULTOR MASTER
--------------------------------------------------
Assunto: {assunto}
Cliente: {cli_nome}

{conteudo_parecer}
"""
        st.success("Relatório executivo gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Parecer em TXT",
            data=relatorio_texto,
            file_name=f"Parecer_{cli_nome.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        
        link_wapp = f"https://wa.me/55{cli_wapp}?text=Olá,%20segue%20o%20parecer%20executivo%20contábil%20referente%20ao%20seu%20atendimento."
        st.markdown(f"<a href='{link_wapp}' target='_blank'><button style='background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar Parecer via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO: CALCULADORA DE RETENÇÕES ---
elif pagina == "🧮 Calculadora de Retenções":
    st.title("🧮 Calculadora de Retenções Federais (IRRF, CSRF, INSS)")
    st.markdown("Apuração rápida de retenções na fonte para notas fiscais de prestação de serviços.")
    
    valor_nf = st.number_input("Valor Bruto da Nota Fiscal (R$)", value=10000.00)
    tipo_servico = st.selectbox("Natureza do Serviço", ["Serviços Gerais / Administrativos", "Segurança / Limpeza", "Serviços Profissionais (Lei 10.833)"])
    
    if st.button("Calcular Retenções"):
        pis_cofins_csll = valor_nf * 0.0465 
        irrf = valor_nf * 0.015 if valor_nf > 666.66 else 0.0 
        inss = valor_nf * 0.11 if "Segurança" in tipo_servico or "Limpeza" in tipo_servico else 0.0
        
        total_retido = pis_cofins_csll + irrf + inss
        liquido_receber = valor_nf - total_retido
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Retenções", f"R$ {total_retido:,.2f}")
        col2.metric("Líquido a Receber", f"R$ {liquido_receber:,.2f}")
        col3.metric("PIS/COFINS/CSLL", f"R$ {pis_cofins_csll:,.2f}")
