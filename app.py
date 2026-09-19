import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client, Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Assistente Contábil IA",
    page_icon="📊",
    layout="wide"
)

# --- CREDENCIAIS E CONEXÕES ---
# (Substitua pelos seus dados reais ou mantenha integrado com suas variáveis)
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI" # Ou puxe de st.secrets se preferir
SUPABASE_URL = "https://seu-projeto-real.supabase.co"
SUPABASE_KEY = "sua_chave_anon_ou_service_role_aqui"

# Senhas e gestor definidos no seu projeto
GESTOR_EMAIL = "Rede.rodrigues2017@gmail.com"
SENHAS_VALIDAS = ["cliente 1 2 3x", "contadora 2x", "doctorMactor20261""]

# Inicializar clientes de forma segura
try:
    if GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
        client_ai = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client_ai = genai.Client() # Tenta pegar do ambiente
except Exception as e:
    st.error(f"Erro ao inicializar o Gemini: {e}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.warning("Supabase não conectado completamente. Verifique as credenciais.")

# --- CONTROLE DE ACESSO (LOGIN) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acesso ao Sistema Contábil")
    st.write("Insira suas credenciais para acessar o assistente de IA.")
    
    with st.form("form_login"):
        input_email = st.text_input("E-mail")
        input_senha = st.text_input("Senha de Acesso", type="password")
        submit_login = st.form_submit_button("Entrar")
        
        if submit_login:
            if input_email == GESTOR_EMAIL and input_senha in SENHAS_VALIDAS:
                st.session_state.autenticado = True
                st.session_state.usuario = input_email
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos. Tente novamente.")
    st.stop()

# --- APLICAÇÃO PRINCIPAL (PÓS-LOGIN) ---
st.sidebar.title("📌 Menu Contábil")
st.sidebar.write(f"Logado como: **{st.session_state.usuario}**")

pagina = st.sidebar.radio("Navegação", ["Chat com Assistente IA", "Lançamentos e Supabase"])

if st.sidebar.button("Sair / Logout"):
    st.session_state.autenticado = False
    st.rerun()

# --- ABA 1: CHAT COM O GEMINI ---
if pagina == "Chat com Assistente IA":
    st.title("🤖 Chat com Assistente Contábil (Gemini)")
    st.write("Tire dúvidas sobre balanços, tributos, plano de contas e rotinas fiscais.")

    # Inicializar histórico do chat no Streamlit
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Configuração do comportamento da IA
    system_instruction = (
        "Você é um assistente de contabilidade sênior, altamente especializado na legislação fiscal "
        "brasileira (Simples Nacional, Lucro Presumido, Lucro Real), plano de contas, lançamentos contábeis "
        "e balancetes. Seja direto, técnico, educado e preciso nas respostas."
    )

    # Exibir histórico de mensagens na tela
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário pelo chat do Streamlit
    if prompt := st.chat_input("Digite sua dúvida contábil aqui..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("O assistente está consultando as normas contábeis..."):
                try:
                    # Cria a sessão de chat usando a API moderna do google-genai
                    chat_session = client_ai.chats.create(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2
                        )
                    )
                    
                    # Reconstruir o histórico recente para o modelo ter contexto
                    for past_msg in st.session_state.chat_history[:-1]:
                        # Apenas alimentando o fluxo se necessário, ou enviando direto a última
                        pass

                    response = chat_session.send_message(prompt)
                    resposta_ia = response.text
                    
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                except Exception as e:
                    erro_msg = f"Ocorreu um erro ao processar sua solicitação com a IA: {e}"
                    st.error(erro_msg)

# --- ABA 2: INTEGRAÇÃO SUPABASE ---
elif pagina == "Lançamentos e Supabase":
    st.title("📁 Integração com Supabase")
    st.write("Painel para visualizar e enviar dados diretamente para o seu banco de dados.")

    tab1, tab2 = st.tabs(["Cadastrar Lançamento", "Ver Dados Salvos"])

    with tab1:
        with st.form("form_lancamento"):
            descricao = st.text_input("Descrição do Lançamento (Ex: Pagamento de Aluguel)")
            valor = st.number_input("Valor (R$)", min_format_decimal=2, format="%.2f")
            tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
            enviar_db = st.form_submit_button("Salvar no Supabase")

            if enviar_db:
                try:
                    # Exemplo de inserção na tabela 'lancamentos' do Supabase
                    # Certifique-se de criar a tabela 'lancamentos' no seu painel do Supabase com essas colunas
                    dados = {"descricao": descricao, "valor": valor, "tipo": tipo}
                    response = supabase.table("lancamentos").insert(dados).execute()
                    st.success("Lançamento salvo com sucesso no Supabase!")
                except Exception as e:
                    st.error(f"Erro ao salvar no banco (verifique se a tabela 'lancamentos' existe no Supabase): {e}")

    with tab2:
        if st.button("Carregar Registros do Banco"):
            try:
                response = supabase.table("lancamentos").select("*").execute()
                dados = response.data
                if dados:
                    st.dataframe(dados)
                else:
                    st.info("Nenhum registro encontrado no banco de dados.")
            except Exception as e:
                st.error(f"Erro ao buscar dados: {e}")
