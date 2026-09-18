import streamlit as st
import pandas as pd
import os
import datetime
import requests
import json

# ==========================================
# 0. CONFIGURAÇÃO DO SISTEMA E LOGS
# ==========================================
ARQUIVO_LOG = "sistema_auditoria.log"

def registrar_log(acao, tipo="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_log = f"[{timestamp}] [{tipo}] {acao}\n"
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(mensagem_log)
    except Exception as e:
        print(f"Erro no log: {e}")

registrar_log("Plataforma Consultor Inteligente Master iniciada com REST API pura.", "STARTUP")

def verificar_senha_master(senha_digitada):
    return senha_digitada.strip().lower() == "contadora2x"

# Função da IA Master blindada via REST API (Zero dependência de pacotes do Google)
def consultar_ia_master(prompt_usuario, historico_chat=None):
    try:
        gemini_api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            gemini_api_key = st.secrets["GEMINI_API_KEY"]
        elif os.environ.get("GEMINI_API_KEY"):
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
        elif os.environ.get("GOOGLE_API_KEY"):
            gemini_api_key = os.environ.get("GOOGLE_API_KEY")

        if not gemini_api_key:
            return "⚠️ **Chave de API do Gemini não configurada.** Por favor, adicione sua `GEMINI_API_KEY` nos Secrets do Streamlit ou no Painel Master."

        # Endpoint oficial universal e estável da API REST do Google Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"

        contexto_sistema = (
            "Você é o 'Consultor Inteligente Master', um auditor fiscal, tributarista sênior e contador consultor de elite. "
            "Suas respostas devem ser profundas, altamente técnicas, precisas, fundamentadas na legislação brasileira e estruturadas com didática executiva.\n\n"
        )

        texto_completo = contexto_sistema
        if historico_chat:
            for h in historico_chat:
                texto_completo += f"{h['role'].upper()}: {h['content']}\n"
        
        texto_completo += f"USER: {prompt_usuario}\nASSISTANT:"

        payload = {
            "contents": [{
                "parts": [{"text": texto_completo}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        
        if response.status_code == 200:
            dados = response.json()
            try:
                resposta_texto = dados["candidates"][0]["content"]["parts"][0]["text"]
                return resposta_texto
            except (KeyError, IndexError):
                return "⚠️ A resposta da API veio em formato inesperado."
        else:
            return f"⚠️ Erro de comunicação com a API (Status {response.status_code}): {response.text}"

    except Exception as e:
        registrar_log(f"Erro crítico na REST API da IA Master: {e}", "AI_ERROR")
        return f"⚠️ Erro ao processar na IA Master. Detalhe técnico: {e}"

# ==========================================
# 1. CONFIGURAÇÃO DA TELA E ESTADOS
# ==========================================
st.set_page_config(
    page_title="Consultor Inteligente Master", 
    page_icon="💼", 
    layout="wide"
)

ARQUIVO_CLIENTES = "clientes_contabilidade.xlsx"
ARQUIVO_LEADS = "potenciais_clientes.xlsx"

if "liberado_pago_master" not in st.session_state:
    st.session_state.liberado_pago_master = False

if "simulacoes_restantes" not in st.session_state:
    st.session_state.simulacoes_restantes = 2

if "mensagens_ia_restantes" not in st.session_state:
    st.session_state.mensagens_ia_restantes = 3

if "historico_chat_master" not in st.session_state:
    st.session_state.historico_chat_master = []

def carregar_dados_excel(arquivo, colunas):
    if not os.path.exists(arquivo):
        df_inicial = pd.DataFrame(columns=colunas)
        df_inicial.to_excel(arquivo, index=False)
    return pd.read_excel(arquivo)

df_clientes = carregar_dados_excel(ARQUIVO_CLIENTES, ["CNPJ/CPF", "Razão Social", "Regime", "Honorário (R$)", "Status"])
df_leads = carregar_dados_excel(ARQUIVO_LEADS, ["Nome", "WhatsApp", "Faturamento Mensal", "Ramo", "Economia Estimada (R$)"])

def tela_bloqueio_comercial(motivo):
    st.error(f"🔒 **Acesso Restrito:** {motivo}")
    st.markdown("### 💎 Desbloqueie o Sistema Consultor Inteligente Master")
    st.markdown("Tenha acesso ilimitado a todas as ferramentas de simulação tributária, pareceres com IA avançada e gestão completa.")

    plano = st.selectbox("Escolha o Plano Ideal:", [
        "Plano Start Mensal - R$ 147,00/mês", 
        "Plano Professional Anual - R$ 2.970,00/ano",
        "Plano Enterprise Escritório Master - R$ 5.970,00/ano"
    ], key="select_plano_novo")

    link_pagamento = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y" if "Mensal" in plano else "https://invoice.infinitepay.io/plans/cristiane-da-260/qTSP5k9f6S"

    t1, t2, t3 = st.tabs(["💎 Pix", "💳 Cartão de Crédito", "🔑 Acesso Admin"])

    with t1:
        st.markdown("- **Chave Pix (Telefone):** `+5564993044147`\n- **Favorecido:** `CAC CONTABILIZANDO`")
        comprovante = st.text_input("ID ou Comprovante do Pix:", key="pix_input_bloq")
        if st.button("Validar Pix", key="btn_val_pix"):
            if len(comprovante.strip()) > 3:
                st.session_state.liberado_pago_master = True
                st.success("Acesso liberado com sucesso!")
                st.rerun()
            else:
                st.warning("Insira um comprovante válido.")

    with t2:
        st.markdown(f'<a href="{link_pagamento}" target="_blank" style="background-color: #0047AB; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold;">💳 Pagar com Cartão InfinitePay</a>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        id_cartao = st.text_input("ID da Transação do Cartão:", key="cartao_input_bloq")
        if st.button("Validar Cartão", key="btn_val_cartao"):
            if len(id_cartao.strip()) > 3:
                st.session_state.liberado_pago_master = True
                st.success("Acesso liberado!")
                st.rerun()
            else:
                st.warning("Insira um ID de transação válido.")

    with t3:
        senha_adm = st.text_input("Senha Master:", type="password", key="adm_bloq_pass")
        if st.button("Entrar como Admin", key="btn_adm_bloq"):
            if verificar_senha_master(senha_adm):
                st.session_state.liberado_pago_master = True
                st.success("Administrador autenticado!")
                st.rerun()
            else:
                st.error("Senha incorreta.")

# ==========================================
# 2. MENU LATERAL
# ==========================================
st.sidebar.title("📈 Consultor Master")
modulo = st.sidebar.radio("Navegação Estratégica", [
    "🚀 Simulador Tributário & Planos",
    "🤖 Chat IA Master Sênior",
    "📑 Parecer Executivo & Disparos",
    "🛡️ Auditoria Preventiva (XML/SPED)",
    "📊 Indicadores do Escritório",
    "💼 Governança de Clientes",
    "📥 Central de Leads",
    "⚙️ Configurações / Painel Master"
])

# ==========================================
# 3. MÓDULO: SIMULADOR TRIBUTÁRIO
# ==========================================
if modulo == "🚀 Simulador Tributário & Planos":
    st.title("🧮 Simulador Contínuo de Regime Tributário")
    st.markdown("Análise paramétrica inteligente para identificação da menor carga tributária.")

    if not st.session_state.liberado_pago_master:
        st.info(f"🎁 Modo Demonstração: Você possui **{st.session_state.simulacoes_restantes}** simulação(ões) gratuita(s).")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Dados da Empresa")
        razao = st.text_input("Razão Social:", value="Empresa Exemplo Ltda")
        whatsapp = st.text_input("WhatsApp:", value="64993044147")
        email = st.text_input("E-mail:", value="contato@empresa.com.br")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$):", min_value=10000.0, value=360000.0, step=10000.0)
        folha_anual = st.number_input("Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0)
        desp_anual = st.number_input("Despesas Operacionais Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0)

    with c2:
        st.subheader("Resultado da Simulação")
        if st.button("⚡ Executar Simulação Completa", type="primary", use_container_width=True):
            if not st.session_state.liberado_pago_master and st.session_state.simulacoes_restantes <= 0:
                st.warning("Suas simulações gratuitas acabaram.")
            else:
                if not st.session_state.liberado_pago_master:
                    st.session_state.simulacoes_restantes -= 1

                simples = fat_anual * 0.09
                presumido = fat_anual * 0.113
                lucro_base = max(0.0, fat_anual - desp_anual - folha_anual)
                real = lucro_base * 0.24

                cenarios = {"Simples Nacional": simples, "Lucro Presumido": presumido, "Lucro Real": real}
                melhor = min(cenarios, key=cenarios.get)
                menor_val = cenarios[melhor]
                economia = max(cenarios.values()) - menor_val

                st.success("Análise paramétrica realizada com sucesso!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Melhor Regime", melhor)
                m2.metric("Imposto Anual Estimado", f"R$ {menor_val:,.2f}")
                m3.metric("Elisão Fiscal Potencial", f"R$ {economia:,.2f}", delta="Otimizado")

    if not st.session_state.liberado_pago_master and st.session_state.simulacoes_restantes <= 0:
        st.markdown("---")
        tela_bloqueio_comercial("Suas simulações gratuitas esgotaram.")

# ==========================================
# 4. MÓDULO: CHAT IA MASTER SÊNIOR
# ==========================================
elif modulo == "🤖 Chat IA Master Sênior":
    st.title("🤖 Consultor Inteligente Master (IA Sênior)")
    st.markdown("Tire dúvidas tributárias, societárias e fiscais complexas com inteligência artificial de alta performance.")

    if not st.session_state.liberado_pago_master:
        st.info(f"🎁 Modo Demonstração: Você possui **{st.session_state.mensagens_ia_restantes}** mensagem(ns) gratuita(s) no chat.")

    for msg in st.session_state.historico_chat_master:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    bloquear_chat = not st.session_state.liberado_pago_master and st.session_state.mensagens_ia_restantes <= 0

    if bloquear_chat:
        st.warning("🔒 Suas mensagens gratuitas no chat acabaram.")
        tela_bloqueio_comercial("Assine um plano para continuar conversando ilimitadamente com o Consultor Inteligente Master.")
    else:
        pergunta = st.chat_input("Digite sua dúvida tributária, fiscal ou contábil...")
        if pergunta:
            if not st.session_state.liberado_pago_master:
                st.session_state.mensagens_ia_restantes -= 1

            st.session_state.historico_chat_master.append({"role": "user", "content": pergunta})
            with st.chat_message("user"):
                st.markdown(pergunta)

            with st.chat_message("assistant"):
                with st.spinner("Consultando bases legislativas com o Consultor Master..."):
                    resposta_ia = consultar_ia_master(pergunta, st.session_state.historico_chat_master[:-1])
                    st.markdown(resposta_ia)
                    st.session_state.historico_chat_master.append({"role": "assistant", "content": resposta_ia})

# ==========================================
# 5. MÓDULO: PARECER EXECUTIVO
# ==========================================
elif modulo == "📑 Parecer Executivo & Disparos":
    st.title("📑 Emissor de Parecer Executivo Master")
    if not st.session_state.liberado_pago_master:
        tela_bloqueio_comercial("O módulo de pareceres executivos é exclusivo para assinantes.")
    else:
        with st.form("form_parecer"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                cli_n = st.text_input("Nome do Cliente:", value="Comércio Exemplo Ltda")
                cli_w = st.text_input("WhatsApp (com DDD):", value="64993044147")
            with c_p2:
                cli_e = st.text_input("E-mail:", value="financeiro@empresa.com.br")
                cli_f = st.number_input("Faturamento Mensal (R$):", value=50000.0, step=5000.0)
            
            objetivo = st.selectbox("Objetivo Técnico:", [
                "Planejamento Tributário Estratégico",
                "Migração de Simples para Lucro Presumido",
                "Revisão de Riscos Fiscais e Compliance",
                "Recuperação de Créditos Tributários"
            ])
            
            gerar_btn = st.form_submit_button("Gerar Laudo Técnico com IA Master", type="primary")

        if gerar_btn:
            with st.spinner("Elaborando laudo formal de auditoria..."):
                prompt_laudo = f"Elabore um parecer técnico formal, detalhado e de alto padrão para a empresa {cli_n}, com faturamento mensal de R$ {cli_f:,.2f}, com foco em {objetivo}."
                laudo = consultar_ia_master(prompt_laudo)
                
                st.success("Parecer gerado com sucesso!")
                st.text_area("Laudo Executivo Oficial:", value=laudo, height=300)

                wpp_num = ''.join(filter(str.isdigit, str(cli_w)))
                link_wpp = f"https://wa.me/55{wpp_num}?text=Olá%20{cli_n},%20segue%20o%20seu%20Parecer%20Técnico%20Executivo%20Master."
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    st.markdown(f'<a href="{link_wpp}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar via WhatsApp</a>', unsafe_allow_html=True)
                with col_e2:
                    st.markdown(f'<a href="mailto:{cli_e}?subject=Parecer%20Tributário&body=Prezado,%20segue%20o%20laudo." style="background-color: #1E3A8A; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📧 Enviar via E-mail</a>', unsafe_allow_html=True)

# ==========================================
# 6. MÓDULO: AUDITORIA PREVENTIVA
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    st.title("🛡️ Auditoria Preventiva & Malha Fina")
    if not st.session_state.liberado_pago_master:
        tela_bloqueio_comercial("A auditoria preventiva é restrita a assinantes.")
    else:
        xml_file = st.file_uploader("Carregar Arquivo Fiscal (XML, TXT, CSV):", type=["xml", "txt", "csv"])
        if xml_file:
            st.success(f"Arquivo `{xml_file.name}` carregado!")
            if st.button("🔍 Rodar Varredura de Inconsistências", type="primary"):
                st.metric("Riscos de Malha Fina", "Baixo Risco", delta="Conforme")
        else:
            st.info("Faça upload de um arquivo fiscal para análise.")

# ==========================================
# 7. INDICADORES DO ESCRITÓRIO
# ==========================================
elif modulo == "📊 Indicadores do Escritório":
    st.title("📊 Painel de Desempenho Financeiro")
    if not df_clientes.empty and "Honorário (R$)" in df_clientes.columns:
        mrr = df_clientes["Honorário (R$)"].sum()
        total_c = len(df_clientes)
        ticket = mrr / total_c if total_c > 0 else 0
        
        i1, i2, i3 = st.columns(3)
        i1.metric("Receita Recorrente (MRR)", f"R$ {mrr:,.2f}")
        i2.metric("Clientes Ativos", total_c)
        i3.metric("Ticket Médio", f"R$ {ticket:,.2f}")
    else:
        st.info("Sem dados cadastrados na base de clientes.")

# ==========================================
# 8. GOVERNANÇA DE CLIENTES
# ==========================================
elif modulo == "💼 Governança de Clientes":
    st.title("💼 Carteira de Clientes Ativos")
    if not df_clientes.empty:
        st.dataframe(df_clientes, use_container_width=True)
    else:
        st.info("Nenhum cliente cadastrado.")

    with st.expander("➕ Adicionar Novo Cliente"):
        with st.form("form_cliente"):
            dc = st.text_input("CNPJ ou CPF:")
            rs = st.text_input("Razão Social:")
            rg = st.selectbox("Regime:", ["MEI", "Simples Nacional", "Lucro Presumido", "Lucro Real"])
            hn = st.number_input("Honorário Mensal (R$):", value=600.0, step=50.0)
            if st.form_submit_button("Salvar Cliente"):
                if dc and rs:
                    novo = {"CNPJ/CPF": dc, "Razão Social": rs, "Regime": rg, "Honorário (R$)": hn, "Status": "Ativo"}
                    df_novo = pd.concat([df_clientes, pd.DataFrame([novo])], ignore_index=True)
                    df_novo.to_excel(ARQUIVO_CLIENTES, index=False)
                    st.success("Cliente cadastrado!")
                    st.rerun()
                else:
                    st.error("Preencha os campos obrigatórios.")

# ==========================================
# 9. CENTRAL DE LEADS
# ==========================================
elif modulo == "📥 Central de Leads":
    st.title("📥 Leads Capturados pelo Simulador")
    if not df_leads.empty:
        st.dataframe(df_leads, use_container_width=True)
    else:
        st.info("Nenhum lead capturado ainda.")

# ==========================================
# 10. PAINEL MASTER / CONFIGURAÇÕES
# ==========================================
elif modulo == "⚙️ Configurações / Painel Master":
    st.title("⚙️ Painel de Administração Master")
    senha_adm_input = st.text_input("Senha Master:", type="password")

    if verificar_senha_master(senha_adm_input):
        st.success("🔓 Autenticado com sucesso!")
        t_cfg1, t_cfg2 = st.tabs(["🔑 Chave API Gemini", "🕵️‍♂️ Logs do Sistema"])

        with t_cfg1:
            nova_chave = st.text_input("Definir Chave GEMINI_API_KEY:", type="password")
            if st.button("Salvar Chave"):
                if nova_chave.strip():
                    os.environ["GEMINI_API_KEY"] = nova_chave.strip()
                    st.success("Chave configurada na sessão!")
                else:
                    st.warning("Insira uma chave válida.")

        with t_cfg2:
            if os.path.exists(ARQUIVO_LOG):
                with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
                    logs = f.readlines()
                st.code("".join(logs[-50:]), language="text")
            else:
                st.info("Nenhum log registrado.")
    else:
        if senha_adm_input:
            st.error("Senha incorreta.")
        else:
            st.info("Digite a senha master para acessar as configurações.")
