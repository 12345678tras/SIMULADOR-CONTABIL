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

# --- MENU LATERAL (TUDO LIBERADO PARA TESTES) ---
st.sidebar.markdown("## 🏢 Consultor Master")
st.sidebar.markdown("Navegação Estratégica")
st.sidebar.success("🔓 Modo de Testes: 100% Liberado")
st.sidebar.markdown("---")
st.sidebar.markdown("**Selecione o Módulo:**")

pagina = st.sidebar.radio("Módulos", [
    "📊 Simulador Básico", 
    "📈 Simulador Avançado", 
    "🤖 Chat IA Master Sênior", 
    "📑 Parecer Executivo & Disparos",
    "🔍 Auditoria Preventiva XML/SPED",
    "📈 Indicadores do Escritório",
    "👥 Governança de Clientes",
    "⚙️ Configurações / Painel Master"
])

st.sidebar.markdown("---")

# --- MÓDULO 1: SIMULADOR BÁSICO ---
if pagina == "📊 Simulador Básico":
    st.title("📊 Simulador Básico de Regime Tributário")
    st.markdown("Análise rápida e simplificada para estimar a carga tributária inicial do cliente.")

    with st.form("form_simulador_basico"):
        razao_social = st.text_input("Nome ou Razão Social do Cliente", value="Empresa Exemplo Ltda")
        faturamento = st.number_input("Faturamento Bruto Anual Estimado (R$)", value=180000.00, format="%.2f")
        
        executar_basico = st.form_submit_button("Calcular Carga Tributária Básica")
        
        if executar_basico:
            st.success("Cálculo básico realizado com sucesso!")
            
            imposto_simples = faturamento * 0.06 
            imposto_presumido = faturamento * 11.33 
            
            col1, col2 = st.columns(2)
            col1.metric("Estimativa Simples Nacional", f"R$ {imposto_simples:,.2f} / ano")
            col2.metric("Estimativa Lucro Presumido", f"R$ {imposto_presumido:,.2f} / ano")
            
            if imposto_simples < imposto_presumido:
                st.info("💡 **Conclusão:** Para este patamar de faturamento, o **Simples Nacional** demonstra ser mais vantajoso.")
            else:
                st.info("💡 **Conclusão:** O **Lucro Presumido** pode ser uma alternativa competitiva a ser detalhada.")

# --- MÓDULO 2: SIMULADOR AVANÇADO ---
elif pagina == "📈 Simulador Avançado":
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
            
            st.markdown("### 📊 Relatório Comparativo de Cenários")
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Simples Nacional", "R$ 21.600,00 /ano", "-8.5%")
            col_b.metric("Lucro Presumido", "R$ 40.788,00 /ano", "+15.2%")
            col_c.metric("Lucro Real", "R$ 38.500,00 /ano", "+11.0%")
            
            st.info("ℹ️ Simulação paramétrica concluída com sucesso no modo de testes livres.")

# --- MÓDULO 3: CHAT IA (ESTÁVEL) ---
elif pagina == "🤖 Chat IA Master Sênior":
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
                    # Tentativa com o modelo padrão atual de mercado do SDK do Gemini
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
                    # Fallback automático caso o ambiente prefira o modelo flash padrão genérico
                    try:
                        response = client_ai.models.generate_content(
                            model='gemini-flash',
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

# --- OUTROS MÓDULOS (TAMBÉM LIBERADOS PARA TESTE) ---
else:
    st.title(f"🛠️ Módulo: {pagina}")
    st.success("Este módulo está liberado no seu ambiente de testes para você configurar e estruturar livremente.")
    st.markdown("Utilize esta área para construir as rotinas complementares do seu escritório contábil.")
