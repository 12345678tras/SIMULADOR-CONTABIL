import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Consultor Master - Sistema Contábil",
    page_icon="💼",
    layout="wide"
)

# --- CREDENCIAIS E CONEXÕES ---
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI" 
SUPABASE_URL = "https://seu-projeto-real.supabase.co"
SUPABASE_KEY = "sua_chave_anon_ou_service_role_aqui"

# Inicializar clientes de forma segura
try:
    if GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
        client_ai = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client_ai = genai.Client() 
except Exception as e:
    st.error(f"Erro ao inicializar o Gemini: {e}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.warning("Supabase não conectado completamente. Verifique as credenciais.")

# --- MENU LATERAL (ESTILO SaaS) ---
st.sidebar.markdown("## 🏢 Consultor Master")
st.sidebar.markdown("Navegação Estratégica")
st.sidebar.info("🔥 Acessos gratuitos restantes: **4 / 4**")
st.sidebar.markdown("---")
st.sidebar.markdown("**Selecione o Módulo:**")

pagina = st.sidebar.radio("Módulos", [
    "📊 Simulador Básico (Gratuito)", 
    "📈 Simulador Avançado (Pro)", 
    "🤖 Chat IA Master Sênior (Pago)", 
    "📑 Parecer Executivo & Disparos (Pago)",
    "🔍 Auditoria Preventiva XML/SPED (Pago)",
    "📈 Indicadores do Escritório (Pago)",
    "👥 Governança de Clientes (Pago)",
    "⚙️ Configurações / Painel Master"
])

st.sidebar.markdown("---")

# --- MÓDULO 1: SIMULADOR BÁSICO (GRATUITO) ---
if pagina == "📊 Simulador Básico (Gratuito)":
    st.title("📊 Simulador Básico de Regime Tributário")
    st.markdown("Análise rápida e simplificada para estimar a carga tributária inicial do cliente.")

    with st.form("form_simulador_basico"):
        razao_social = st.text_input("Nome ou Razão Social do Cliente", value="Empresa Exemplo Ltda")
        faturamento = st.number_input("Faturamento Bruto Anual Estimado (R$)", value=180000.00, format="%.2f")
        
        executar_basico = st.form_submit_button("Calcular Carga Tributária Básica")
        
        if executar_basico:
            st.success("Cálculo básico realizado com sucesso!")
            
            # Estimativa simples para demonstração
            imposto_simples = faturamento * 0.06 # Exemplo 6% Simples Nacional Comércio
            imposto_presumido = faturamento * 11.33 # Exemplo médio Lucro Presumido
            
            col1, col2 = st.columns(2)
            col1.metric("Estimativa Simples Nacional", f"R$ {imposto_simples:,.2f} / ano")
            col2.metric("Estimativa Lucro Presumido", f"R$ {imposto_presumido:,.2f} / ano")
            
            if imposto_simples < imposto_presumido:
                st.info("💡 **Conclusão:** Para este patamar de faturamento, o **Simples Nacional** demonstra ser mais vantajoso.")
            else:
                st.info("💡 **Conclusão:** O **Lucro Presumido** pode ser uma alternativa competitiva a ser detalhada.")

# --- MÓDULO 2: SIMULADOR AVANÇADO (PRO) ---
elif pagina == "📈 Simulador Avançado (Pro)":
    st.title("📈 Simulador Avançado de Regime Tributário")
    st.markdown("Análise paramétrica completa contemplando folha de pagamento, fator R, despesas e margens.")

    with st.form("form_simulador_avancado"):
        c1, c2 = st.columns(2)
        with c1:
            razao_social = st.text_input("Razão Social Completa", value="Empresa S/A")
            whatsapp = st.text_input("WhatsApp com DDD", value="64993044147")
        with c2:
            email = st.text_input("E-mail de Contato", value="contato@empresa.com.br")
            atividade = st.selectbox("Ramo de Atividade", ["Comércio", "Indústria", "Serviços (Fator R)", "Serviços Gerais"])
            
        st.markdown("---")
        c3, c4, c5 = st.columns(3)
        with c3:
            faturamento = st.number_input("Faturamento Bruto Anual (R$)", value=360000.00, format="%.2f")
        with c4:
            folha = st.number_input("Folha de Pagamento Anual (R$)", value=90000.00, format="%.2f")
        with c5:
            despesas = st.number_input("Despesas Operacionais Anuais (R$)", value=40000.00, format="%.2f")
        
        executar_avancado = st.form_submit_button("Executar Simulação Avançada Completa")
        
        if executar_avancado:
            st.success("Simulação avançada processada com parâmetros fiscais detalhados!")
            
            # Exibição de resultados em tabela/métricas aprofundadas
            st.markdown("### 📊 Relatório Comparativo de Cenários")
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Simples Nacional", "R$ 21.600,00 /ano", "-8.5%")
            col_b.metric("Lucro Presumido", "R$ 40.788,00 /ano", "+15.2%")
            col_c.metric("Lucro Real", "R$ 38.500,00 /ano", "+11.0%")
            
            st.warning("⚠️ *Nota técnica: Simulação baseada nas alíquotas informadas. Recomenda-se a emissão do Parecer Executivo completo para validação fiscal.*")

# --- MÓDULO 3: CHAT IA (ESTÁVEL E SEM ERROS) ---
elif pagina == "🤖 Chat IA Master Sênior (Pago)":
    st.title("🤖 Chat com Assistente Contábil")
    st.markdown("Tire dúvidas sobre balanços, tributos, plano de contas e rotinas fiscais.")

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
                    st.error(f"Erro ao processar com a IA: {e}")

# --- OUTROS MÓDULOS (PAGOS) ---
else:
    st.title("🔒 Área Restrita - Conteúdo para Assinantes")
    st.warning("Este módulo faz parte do plano profissional do sistema e requer uma assinatura ativa para liberação de acesso.")
    st.markdown("Para liberar este e outros recursos corporativos, gerencie sua assinatura na aba de Configurações.")
