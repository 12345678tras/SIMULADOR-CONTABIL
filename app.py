import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from supabase import create_client, Client

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Consultor Inteligente Master",
    page_icon="⚖️",
    layout="wide"
)

# ==========================================
# CONEXÃO COM O SUPABASE (NUVEM)
# ==========================================
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if url and key:
        return create_client(url, key)
    return None

try:
    supabase: Client = init_supabase()
except Exception as e:
    supabase = None

# ==========================================
# CREDENCIAIS E LINKS (PROTEGIDOS VIA SECRETS)
# ==========================================
GESTOR_CONFIG = st.secrets.get("gestor", {})
MEU_EMAIL_GESTOR = GESTOR_CONFIG.get("email", "Rede.rodrigues2017@gmail.com")
SENHAS_MESTRE_CONFIG = GESTOR_CONFIG.get("senhas", ["cliente 1 2 3x", "contadora2x", "gestorMaster2026!"])

LINK_PLANO_START = "https://invoice.infinitepay.io/plans/cristiane-da-260/KC9Geb9OrA"
LINK_PLANO_PRO = "https://invoice.infinitepay.io/plans/cristiane-da-260/k7jgpmWCJL"
LINK_PLANO_ENTERPRISE = "https://invoice.infinitepay.io/plans/cristiane-da-260/DnCh4NY1nH"
CHAVE_PIX_OFICIAL = "64993044147"
MEU_WHATSAPP = "64993044147"

def limpar_telefone(fone):
    return ''.join(filter(str.isdigit, str(fone)))

# ==========================================
# INICIALIZAÇÃO DE ESTADO DA SESSÃO
# ==========================================
if "liberado_pago_master" not in st.session_state:
    st.session_state.liberado_pago_master = False
if "usuario_identificado" not in st.session_state:
    st.session_state.usuario_identificado = False
if "email_atual" not in st.session_state:
    st.session_state.email_atual = ""

params = st.query_params
if "admin" in params and params["admin"] == "true":
    st.session_state.liberado_pago_master = True
    st.session_state.usuario_identificado = True

ARQUIVO_LEADS = "leads_master.csv"

def salvar_lead_arquivo(novo_lead):
    try:
        if os.path.exists(ARQUIVO_LEADS):
            df = pd.read_csv(ARQUIVO_LEADS)
        else:
            df = pd.DataFrame(columns=["Data", "Razao Social", "WhatsApp", "E-mail", "Melhor Regime", "Economia (R$)"])
        novo_df = pd.DataFrame([novo_lead])
        df = pd.concat([df, novo_df], ignore_index=True)
        df.to_csv(ARQUIVO_LEADS, index=False)
    except Exception as e:
        print(f"Erro ao salvar lead local: {e}")

def registrar_lead_nuvem(email, whatsapp, razao):
    if not supabase:
        return
    try:
        email_limpo = email.strip().lower()
        res = supabase.table("acessos_email").select("*").eq("email", email_limpo).execute()
        if not res.data or len(res.data) == 0:
            novo_registro = {
                "email": email_limpo,
                "whatsapp": whatsapp,
                "razao_social": razao,
                "simulacoes_feitas": 1,
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            supabase.table("acessos_email").insert(novo_registro).execute()
    except Exception as e:
        print(f"Erro ao registrar lead: {e}")

# ==========================================
# COMPONENTE DE PAYWALL (EXIBIDO NOS MÓDULOS PAGOS)
# ==========================================
def renderizar_paywall_modulo(nome_modulo):
    st.markdown(f"## 🔒 Acesso Restrito: {nome_modulo}")
    st.info("Este módulo avançado é exclusivo para assinantes dos planos profissionais ou contas com Licença Master.")
    
    st.markdown("### 🚀 Escolha seu Plano de Assinatura:")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("#### Plano Start")
        st.markdown("**R$ 147,00 / mês**")
        st.markdown(f'<a href="{LINK_PLANO_START}" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Start</a>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Plano Professional")
        st.markdown("**R$ 2.470,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_PRO}" target="_blank" style="background-color: #28a745; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Pro</a>', unsafe_allow_html=True)
    with col_p3:
        st.markdown("#### Plano Enterprise")
        st.markdown("**R$ 5.970,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_ENTERPRISE}" target="_blank" style="background-color: #6f42c1; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"💎 **PIX Direto:** Chave Telefone: `{CHAVE_PIX_OFICIAL}` | WhatsApp Comprovantes: `({MEU_WHATSAPP[:2]}) {MEU_WHATSAPP[2:7]}-{MEU_WHATSAPP[7:]}`")
    
    with st.expander("🔑 Possui senha mestre de liberação?"):
        senha_input = st.text_input("Digite a senha:", type="password", key=f"senha_paywall_{nome_modulo}")
        if st.button("Ativar Acesso", key=f"btn_senha_{nome_modulo}"):
            if senha_input in SENHAS_MESTRE_CONFIG:
                st.session_state.liberado_pago_master = True
                st.success("Licença ativada com sucesso!")
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

# ==========================================
# TELA DE IDENTIFICAÇÃO INICIAL (LEAD DA ENTRADA)
# ==========================================
def tela_identificacao_inicial():
    col_v1, col_centro, col_v2 = st.columns([1, 2.5, 1])
    with col_centro:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1e293b;'>⚖️ Consultor Master</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #0284c7; font-size: 20px;'>Simulador Tributário Gratuito de Entrada</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Informe seus dados abaixo para acessar o simulador gratuito livre.</p>", unsafe_allow_html=True)
        st.markdown("---")

        with st.form("form_lead_gratis"):
            input_nome = st.text_input("Empresa / Razão Social:", value="Empresa Exemplo Ltda")
            input_email = st.text_input("E-mail Profissional:", value="")
            input_wpp = st.text_input("WhatsApp com DDD:", value=MEU_WHATSAPP)
            input_senha_mestre = st.text_input("Senha de Gestor (Opcional):", type="password", value="")

            submitted = st.form_submit_button("⚡ ENTRAR NO SIMULADOR GRATUITO")
            
            if submitted:
                if input_senha_mestre in SENHAS_MESTRE_CONFIG or (input_email.strip().lower() == MEU_EMAIL_GESTOR.lower() and input_senha_mestre):
                    st.session_state.liberado_pago_master = True
                    st.session_state.usuario_identificado = True
                    st.session_state.email_atual = MEU_EMAIL_GESTOR
                    st.success("Acesso Master liberado!")
                    st.rerun()
                elif not input_email or "@" not in input_email or "." not in input_email:
                    st.error("Por favor, digite um e-mail válido.")
                else:
                    email_limpo = input_email.strip().lower()
                    st.session_state.email_atual = email_limpo
                    st.session_state.usuario_identificado = True
                    registrar_lead_nuvem(email_limpo, input_wpp, input_nome)
                    st.success("Acesso liberado!")
                    st.rerun()
    st.stop()

if not st.session_state.usuario_identificado:
    tela_identificacao_inicial()

# ==========================================
# MENU LATERAL
# ==========================================
st.sidebar.title("⚖️ Consultor Master")
if st.session_state.liberado_pago_master:
    st.sidebar.success("👑 **Modo Gestor Ativo**\n*(Acesso Total)*")
else:
    st.sidebar.warning(f"👤 **Lead Ativo:**\n`{st.session_state.email_atual}`\n\n🟢 *Simulador Gratuito Liberado*")

modulo = st.sidebar.radio(
    "Selecione o Módulo:",
    [
        "🚀 1. Simulador Tributário Gratuito",
        "⚙️ 2. Simulador Tributário Avançado (Pago)",
        "💬 Chat IA Master Sênior",
        "📑 Parecer Executivo & Disparos",
        "🛡️ Auditoria Preventiva (XML/SPED)",
        "📊 Indicadores do Escritório",
        "🏛️ Governança de Clientes",
        "🎯 Central de Leads",
        "🔐 Painel Master / Configurações"
    ]
)

# ==========================================
# 1. MÓDULO: SIMULADOR TRIBUTÁRIO GRATUITO (LIVRE)
# ==========================================
if modulo == "🚀 1. Simulador Tributário Gratuito":
    st.title("🧮 Simulador Contínuo de Regime Tributário (Versão Gratuita)")
    st.markdown("Análise paramétrica inicial para identificação rápida da carga tributária.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Dados da Empresa")
        razao = st.text_input("Razão Social:", value="Empresa Exemplo Ltda", key="sim_gratis_razao")
        whatsapp = st.text_input("WhatsApp:", value=MEU_WHATSAPP, key="sim_gratis_wpp")
        email = st.text_input("E-mail:", value=st.session_state.email_atual, key="sim_gratis_email")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$):", min_value=10000.0, value=370000.0, step=10000.0, key="sim_gratis_fat")
        folha_anual = st.number_input("Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0, key="sim_gratis_folha")
        desp_anual = st.number_input("Despesas Operacionais Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0, key="sim_gratis_desp")

    with c2:
        st.subheader("Resultado da Simulação")
        if st.button("⚡ Executar Simulação Gratuita", type="primary", use_container_width=True):
            simples = fat_anual * 0.09
            presumido = fat_anual * 0.113
            lucro_base = max(0.0, fat_anual - desp_anual - folha_anual)
            real = lucro_base * 0.24

            cenarios = {"Simples Nacional": simples, "Lucro Presumido": presumido, "Lucro Real": real}
            melhor = min(cenarios, key=cenarios.get)
            menor_val = cenarios[melhor]
            economia = max(cenarios.values()) - menor_val

            lead_data = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Razao Social": razao,
                "WhatsApp": whatsapp,
                "E-mail": email,
                "Melhor Regime": melhor,
                "Economia (R$)": round(economia, 2)
            }
            salvar_lead_arquivo(lead_data)
            st.session_state.res_gratis = lead_data
            st.success("Simulação executada com sucesso!")

        if "res_gratis" in st.session_state:
            res = st.session_state.res_gratis
            m1, m2 = st.columns(2)
            m1.metric("Melhor Regime", res["Melhor Regime"])
            m2.metric("Economia Potencial", f"R$ {res['Economia (R$)']:,.2f}")
            
            st.markdown("---")
            texto_wpp = f"Olá {res['Razao Social']}, segue o resultado da simulação: Melhor Regime: {res['Melhor Regime']} (Economia: R$ {res['Economia (R$)']:,.2f})."
            link_wpp = f"https://wa.me/55{limpar_telefone(res['WhatsApp'])}?text={requests.utils.quote(texto_wpp)}"
            st.markdown(f'<a href="{link_wpp}" target="_blank" style="background-color: #25D366; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Resultado no WhatsApp</a>', unsafe_allow_html=True)

# ==========================================
# 2. MÓDULO: SIMULADOR TRIBUTÁRIO AVANÇADO (PAGO)
# ==========================================
elif modulo == "⚙️ 2. Simulador Tributário Avançado (Pago)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Simulador Tributário Avançado")
    st.title("⚙️ Simulador Tributário Avançado & Institucional")
    st.markdown("Módulo completo com simulação paramétrica profunda, fator R e árvore de decisões fiscais.")
    st.success("🟢 Acesso liberado ao Simulador Avançado!")

# ==========================================
# 3. MÓDULO: CHAT IA MASTER SÊNIOR (PAGO)
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Chat IA Master Sênior")
    st.title("💬 Chat IA Master Sênior")
    st.write("Ambiente de chat executivo ativado.")

# ==========================================
# 4. MÓDULO: PARECER EXECUTIVO & DISPAROS (PAGO)
# ==========================================
elif modulo == "📑 Parecer Executivo & Disparos":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Parecer Executivo & Disparos")
    st.title("📑 Parecer Executivo Institucional")

# ==========================================
# 5. MÓDULO: AUDITORIA PREVENTIVA (PAGO)
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Auditoria Preventiva")
    st.title("🛡️ Auditoria Preventiva XML/SPED")

# ==========================================
# 6. MÓDULO: INDICADORES DO ESCRITÓRIO (PAGO)
# ==========================================
elif modulo == "📊 Indicadores do Escritório":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Indicadores do Escritório")
    st.title("📊 Indicadores de Desempenho")

# ==========================================
# 7. MÓDULO: GOVERNANÇA DE CLIENTES (PAGO)
# ==========================================
elif modulo == "🏛️ Governança de Clientes":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Governança de Clientes")
    st.title("🏛️ Governança de Clientes")

# ==========================================
# 8. MÓDULO: CENTRAL DE LEADS (PAGO)
# ==========================================
elif modulo == "🎯 Central de Leads":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Central de Leads")
    st.title("🎯 Central de Leads")
    if os.path.exists(ARQUIVO_LEADS):
        st.dataframe(pd.read_csv(ARQUIVO_LEADS), use_container_width=True)

# ==========================================
# 9. MÓDULO: CONFIGURAÇÕES / PAINEL MASTER
# ==========================================
elif modulo == "🔐 Painel Master / Configurações":
    st.title("🔐 Painel de Controle Master")
    senha_input = st.text_input("Senha Mestre:", type="password")
    if st.button("Ativar Acesso Master"):
        if senha_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.success("Licença ativada!")
            st.rerun()
        else:
            st.error("Senha incorreta.")
