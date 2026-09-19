import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Plataforma Contábil Profissional",
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

# --- MENU LATERAL MODERNO ---
st.sidebar.markdown("## 🏢 Sistema Contábil SaaS")
st.sidebar.markdown("---")
pagina = st.sidebar.radio("Módulos do Sistema", [
    "🤖 Assistente IA (Gemini)", 
    "📄 Leitura Inteligente de Notas", 
    "📊 Dashboard & Lançamentos"
])
st.sidebar.markdown("---")
st.sidebar.info("Modo de Operação: Comercial / Testes")

# --- ABA 1: CHAT COM O GEMINI (INTOCADA) ---
if pagina == "🤖 Assistente IA (Gemini)":
    st.title("🤖 Chat com Assistente Contábil")
    st.markdown("Tire dúvidas sobre balanços, tributos, plano de contas e rotinas fiscais com inteligência artificial avançada.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    system_instruction = (
        "Você é um assistente de contabilidade sênior, altamente especializado na legislação fiscal "
        "brasileira (Simples Nacional, Lucro Presumido, Lucro Real), plano de contas, lançamentos contábeis "
        "e balancetes. Seja direto, técnico, educado e preciso nas respostas."
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
                    chat_session = client_ai.chats.create(
                        model="gemini-3.6-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2
                        )
                    )
                    
                    response = chat_session.send_message(prompt)
                    resposta_ia = response.text
                    
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar sua solicitação com a IA: {e}")

# --- ABA 2: LEITURA INTELIGENTE DE DOCUMENTOS (INTOCADA) ---
elif pagina == "📄 Leitura Inteligente de Notas":
    st.title("📄 Leitura de Documentos Fiscais com IA")
    st.markdown("Envie uma foto de nota fiscal, recibo ou PDF para extração automática de dados.")

    arquivo_enviado = st.file_uploader("Selecione o arquivo (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])

    if arquivo_enviado is not None:
        if "image" in arquivo_enviado.type:
            st.image(arquivo_enviado, caption="Documento Enviado", use_container_width=True)
        else:
            st.info("Arquivo PDF carregado com sucesso.")
        
        if st.button("Executar Extração com IA"):
            with st.spinner("Analisando documento fiscal..."):
                try:
                    bytes_arquivo = arquivo_enviado.getvalue()
                    
                    prompt_extracao = (
                        "Analise este documento fiscal/recibo e retorne estritamente em formato de texto estruturado "
                        "os seguintes campos: Fornecedor, CNPJ, Valor Total, Data e uma sugestão de Classificação contábil."
                    )
                    
                    response = client_ai.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=bytes_arquivo,
                                mime_type=arquivo_enviado.type
                            ),
                            prompt_extracao
                        ]
                    )
                    
                    st.success("Extração concluída!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erro ao processar o documento: {e}")

# --- ABA 3: DASHBOARD E LANÇAMENTOS (NOVA ESTRUTURA PROFISSIONAL) ---
elif pagina == "📊 Dashboard & Lançamentos":
    st.title("📊 Painel Executivo e Gestão Financeira")
    st.markdown("Controle completo de fluxo de caixa, centros de custos e relatórios gerenciais.")

    tab_dash, tab_cad = st.tabs(["📈 Visão Geral & Relatórios", "➕ Novo Lançamento"])

    with tab_cad:
        st.markdown("### Registrar Nova Movimentação")
        with st.form("form_lancamento_moderno", clear_on_submit=True):
            descricao = st.text_input("Descrição / Histórico do Lançamento")
            
            c1, c2 = st.columns(2)
            with c1:
                valor = st.number_input("Valor (R$)", format="%.2f", min_value=0.0)
            with c2:
                tipo = st.selectbox("Tipo de Movimento", ["Receita", "Despesa"])
            
            c3, c4 = st.columns(2)
            with c3:
                status = st.selectbox("Status Financeiro", ["Pago / Liquidado", "Pendente / Em Aberto"])
            with c4:
                centro_custos = st.selectbox("Centro de Custos", ["Administrativo", "Operacional", "Comercial", "Tributário"])
            
            data_vencimento = st.date_input("Data de Vencimento / Ocorrência", value=datetime.date.today())
            
            salvar = st.form_submit_button("Salvar no Banco de Dados")

            if salvar:
                try:
                    dados = {
                        "descricao": descricao, 
                        "valor": float(valor), 
                        "tipo": tipo,
                        "status": status,
                        "centro_custos": centro_custos,
                        "vencimento": str(data_vencimento)
                    }
                    supabase.table("lancamentos").insert(dados).execute()
                    st.success("Lançamento registrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao salvar no Supabase: {e}")

    with tab_dash:
        if st.button("Atualizar Dados e Métricas"):
            try:
                response = supabase.table("lancamentos").select("*").execute()
                dados = response.data
                if dados:
                    df = pd.DataFrame(dados)
                    
                    # Cartões de Métricas (KPIs modernos)
                    if "tipo" in df.columns and "valor" in df.columns:
                        total_rec = df[df["tipo"] == "Receita"]["valor"].sum()
                        total_desp = df[df["tipo"] == "Despesa"]["valor"].sum()
                        lucro = total_rec - total_desp
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Receitas Totais", f"R$ {total_rec:,.2f}")
                        col2.metric("Despesas Totais", f"R$ {total_desp:,.2f}")
                        col3.metric("Resultado Líquido", f"R$ {lucro:,.2f}")
                        
                        st.markdown("---")
                        st.markdown("### Distribuição Gráfica")
                        totais = df.groupby("tipo")["valor"].sum()
                        st.bar_chart(totais)
                    
                    st.markdown("### Extrato de Lançamentos")
                    st.dataframe(df, use_container_width=True)
                    
                    # Botão de Exportação profissional
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Exportar Dados (CSV)",
                        data=csv_data,
                        file_name='extrato_contabil.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("Nenhum lançamento encontrado cadastrado no banco.")
            except Exception as e:
                st.error(f"Erro ao carregar dados do Supabase: {e}")
