import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Assistente Contábil IA - SaaS",
    page_icon="📊",
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

# --- APLICAÇÃO PRINCIPAL (SEM LOGIN) ---
st.sidebar.title("📌 Menu Contábil")
st.sidebar.write("Plataforma SaaS Profissional")

pagina = st.sidebar.radio("Navegação", [
    "Chat com Assistente IA", 
    "Leitura Inteligente (Notas/Recibos)", 
    "Lançamentos e Dashboard"
])

# --- ABA 1: CHAT COM O GEMINI (TOTALMENTE INTOCADA E PERFEITA) ---
if pagina == "Chat com Assistente IA":
    st.title("🤖 Chat com Assistente Contábil (Gemini)")
    st.write("Tire dúvidas sobre balanços, tributos, plano de contas e rotinas fiscais.")

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

# --- ABA 2: LEITURA INTELIGENTE DE DOCUMENTOS (INTOCADA E FUNCIONAL) ---
elif pagina == "Leitura Inteligente (Notas/Recibos)":
    st.title("📄 Leitura de Documentos Fiscais com IA")
    st.write("Envie uma foto de nota fiscal, recibo ou PDF para extrair os dados automaticamente.")

    arquivo_enviado = st.file_uploader("Escolha um arquivo (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])

    if arquivo_enviado is not None:
        st.image(arquivo_enviado, caption="Documento Enviado", use_container_width=True) if "image" in arquivo_enviado.type else st.info("Arquivo PDF carregado com sucesso.")
        
        if st.button("Extrair Dados com IA"):
            with st.spinner("Lendo documento e extraindo informações contábeis..."):
                try:
                    bytes_arquivo = arquivo_enviado.getvalue()
                    
                    prompt_extracao = (
                        "Analise este documento fiscal/recibo e retorne estritamente em formato de texto estruturado "
                        "os seguintes campos: Fornecedor, CNPJ, Valor Total, Data e uma sugestão de Classificação (Ex: Despesa com Material, Aluguel, etc)."
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
                    
                    st.success("Dados extraídos com sucesso!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erro ao processar o documento com a IA: {e}")

# --- ABA 3: SUPABASE E DASHBOARD (MODERNO E PROFISSIONAL) ---
elif pagina == "Lançamentos e Dashboard":
    st.title("📁 Gestão de Lançamentos e Dashboard")
    st.write("Painel executivo para controle de fluxo de caixa, vencimentos e centro de custos.")

    tab1, tab2 = st.tabs(["Cadastrar Lançamento", "Ver Dados e Dashboard"])

    with tab1:
        with st.form("form_lancamento_pro"):
            st.subheader("Novo Registro Financeiro")
            descricao = st.text_input("Descrição do Lançamento (Ex: Pagamento de Fornecedor)")
            
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                valor = st.number_input("Valor (R$)", format="%.2f", min_value=0.0)
            with col_v2:
                tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                status = st.selectbox("Status", ["Pago / Liquidado", "Pendente / Em Aberto"])
            with col_c2:
                centro_custos = st.selectbox("Centro de Custos / Departamento", ["Administrativo", "Operacional", "Comercial", "Financeiro"])
            
            data_vencimento = st.date_input("Data de Vencimento", value=datetime.date.today())
            
            enviar_db = st.form_submit_button("Salvar no Supabase")

            if enviar_db:
                try:
                    dados = {
                        "descricao": descricao, 
                        "valor": float(valor), 
                        "tipo": tipo,
                        "status": status,
                        "centro_custos": centro_custos,
                        "vencimento": str(data_vencimento)
                    }
                    response = supabase.table("lancamentos").insert(dados).execute()
                    st.success("Lançamento salvo com sucesso no Supabase!")
                except Exception as e:
                    st.error(f"Erro ao salvar no banco (certifique-se de que a tabela 'lancamentos' no Supabase possui essas colunas): {e}")

    with tab2:
        if st.button("Carregar Registros e Indicadores"):
            try:
                response = supabase.table("lancamentos").select("*").execute()
                dados = response.data
                if dados:
                    df = pd.DataFrame(dados)
                    
                    st.subheader("📊 Indicadores Chave (KPIs)")
                    if "tipo" in df.columns and "valor" in df.columns:
                        total_receitas = df[df["tipo"] == "Receita"]["valor"].sum()
                        total_despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
                        saldo_liquido = total_receitas - total_despesas
                        
                        kpi1, kpi2, kpi3 = st.columns(3)
                        kpi1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
                        kpi2.metric("Total Despesas", f"R$ {total_despesas:,.2f}")
                        kpi3.metric("Saldo Líquido", f"R$ {saldo_liquido:,.2f}", delta=f"R$ {saldo_liquido:,.2f}")
                        
                        st.markdown("---")
                        st.subheader("Gráfico por Tipo")
                        totais = df.groupby("tipo")["valor"].sum()
                        st.bar_chart(totais)
                    
                    st.subheader("📋 Tabela Completa de Lançamentos")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Baixar Relatório em CSV",
                        data=csv,
                        file_name='relatorio_contabil.csv',
                        mime='text/csv',
                    )
                else:
                    st.info("Nenhum registro encontrado no banco de dados.")
            except Exception as e:
                st.error(f"Erro ao buscar dados: {e}")
