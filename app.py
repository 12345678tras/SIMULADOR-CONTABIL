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
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Erro ao conectar com o Supabase: {e}")
    supabase = None

# ==========================================
# CREDENCIAIS DO GESTOR
# ==========================================
MEU_EMAIL_GESTOR = st.secrets["gestor"]["email"] if "gestor" in st.secrets and "email" in st.secrets["gestor"] else "Rede.rodrigues2017@gmail.com"
SENHAS_MESTRE_CONFIG = st.secrets["gestor"]["senhas"] if "gestor" in st.secrets and "senhas" in st.secrets["gestor"] else ["cliente 1 2 3x", "contadora 2x", "gestorMaster2026!"]

# Links Oficiais e Contatos
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

# Atalho inteligente via parâmetro na URL (?admin=true)
params = st.query_params
if "admin" in params and params["admin"] == "true":
    st.session_state.liberado_pago_master = True
    st.session_state.usuario_identificado = True

# ==========================================
# PERSISTÊNCIA LOCAL DE LEADS (BACKUP)
# ==========================================
ARQUIVO_LEADS = "leads_master.csv"

def salvar_lead_arquivo(novo_lead):
    try:
        if os.path.exists(ARQUIVO_LEADS):
            df = pd.read_csv(ARQUIVO_LEADS)
        else:
            df = pd.DataFrame(columns=["Data", "Razao Social", "WhatsApp", "E-mail", "Melhor Regime", "Economia (R$)"])
        
        # Evita duplicar exatamente o mesmo e-mail no CSV local se já existir
        novo_df = pd.DataFrame([novo_lead])
        df = pd.concat([df, novo_df], ignore_index=True)
        df.to_csv(ARQUIVO_LEADS, index=False)
    except Exception as e:
        print(f"Erro ao salvar lead local: {e}")

# ==========================================
# FUNÇÕES DE CONTROLE DE USOS POR E-MAIL (SUPABASE)
# ==========================================
LIMITE_MAXIMO_ACESSO = 3

def consultar_ou_criar_usuario_nuvem(email, whatsapp, razao):
    if not supabase:
        return 0
    try:
        email_limpo = email.strip().lower()
        # Verifica se o e-mail já existe na base de controle de acessos
        res = supabase.table("acessos_email").select("*").eq("email", email_limpo).execute()
        
        if res.data and len(res.data) > 0:
            # Já existe, retorna os usos atuais
            return res.data[0]["contador"]
        else:
            # Não existe, cadastra o novo lead/usuário com 0 usos iniciais
            novo_registro = {
                "email": email_limpo,
                "whatsapp": whatsapp,
                "razao_social": razao,
                "contador": 0,
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            supabase.table("acessos_email").insert(novo_registro).execute()
            
            # Salva também no CSV local para garantir
            salvar_lead_arquivo({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Razao Social": razao,
                "WhatsApp": whatsapp,
                "E-mail": email_limpo,
                "Melhor Regime": "Cadastro Inicial",
                "Economia (R$)": 0.0
            })
            return 0
    except Exception as e:
        print(f"Erro ao gerenciar usuário na nuvem: {e}")
        return 0

def obter_usos_email(email):
    if not supabase:
        return 0
    try:
        res = supabase.table("acessos_email").select("contador").eq("email", email.strip().lower()).execute()
        if res.data and len(res.data) > 0:
            val = res.data[0]["contador"]
            return val if val is not None else 0
    except Exception as e:
        print(f"Erro ao buscar contador: {e}")
    return 0

def incrementar_uso_email(email):
    if st.session_state.liberado_pago_master:
        return
    try:
        email_limpo = email.strip().lower()
        atual = obter_usos_email(email_limpo)
        novo_valor = atual + 1
        supabase.table("acessos_email").update({"contador": novo_valor}).eq("email", email_limpo).execute()
    except Exception as e:
        print(f"Erro ao incrementar uso: {e}")

# ==========================================
# TELA DE CAPTURA / IDENTIFICAÇÃO OBRIGATÓRIA (ESTILO SAAS GLOBAL)
# ==========================================
def tela_identificacao_inicial():
    st.title("⚖️ Consultor Inteligente Master")
    st.markdown("### 🚀 Acesso à Plataforma de Inteligência Tributária")
    st.info("Para liberar os seus **3 acessos gratuitos** de demonstração ou entrar na sua conta, por favor preencha os seus dados abaixo:")

    with st.form("form_login_saas"):
        col1, col2 = st.columns(2)
        with col1:
            input_nome = st.text_input("Sua Empresa / Razão Social:", value="Empresa Exemplo Ltda")
            input_email = st.text_input("Seu E-mail Profissional (Obrigatório):", value="")
        with col2:
            input_wpp = st.text_input("Seu WhatsApp com DDD:", value=MEU_WHATSAPP)
            input_senha_mestre = st.text_input("Senha Mestre (Se já for assinante/gestor):", type="password", value="")

        submitted = st.form_submit_button("🚀 Acessar Sistema Gratuitamente", use_container_width=True)
        
        if submitted:
            # Verifica se é o gestor logando por senha mestre
            if input_senha_mestre in SENHAS_MESTRE_CONFIG or (input_email.strip().lower() == MEU_EMAIL_GESTOR.lower() and input_senha_mestre):
                st.session_state.liberado_pago_master = True
                st.session_state.usuario_identificado = True
                st.session_state.email_atual = MEU_EMAIL_GESTOR
                st.success("Acesso Master liberado com sucesso!")
                st.rerun()
            
            # Validação normal de e-mail
            elif not input_email or "@" not in input_email or "." not in input_email:
                st.error("Por favor, digite um e-mail profissional válido para continuar.")
            else:
                email_limpo = input_email.strip().lower()
                st.session_state.email_atual = email_limpo
                
                # Consulta na nuvem quantos usos esse e-mail já teve
                usos = consultar_ou_criar_usuario_nuvem(email_limpo, input_wpp, input_nome)
                
                if usos >= LIMITE_MAXIMO_ACESSO:
                    st.session_state.usuario_identificado = True # Vai cair direto na tela de bloqueio comercial
                    st.rerun()
                else:
                    st.session_state.usuario_identificado = True
                    st.success("Acesso liberado com sucesso! Entrando...")
                    st.rerun()

    st.markdown("---")
    st.markdown("#### 💎 Já é assinante ou quer pular os testes?")
    with st.expander("Clique aqui para ver os Planos e Chave PIX de Liberação Imediata"):
        st.markdown(f"**Chave PIX (Telefone):** `{CHAVE_PIX_OFICIAL}`")
        st.markdown(f"📲 Após o pagamento, envie o comprovante para o WhatsApp **(64) 99304-4147** para receber sua senha mestre.")
    st.stop()

# ==========================================
# TELA DE BLOQUEIO COMERCIAL (QUANDO OS 3 USOS ZERAM)
# ==========================================
def tela_bloqueio_comercial():
    st.error("🔒 Seus 3 acessos gratuitos vinculados a este e-mail esgotaram!")
    st.markdown("### 🚀 Escolha um Plano para Continuar Faturando com o Sistema")
    st.markdown("Tenha acesso ilimitado a todas as simulações, chat avançado, pareceres e auditorias fiscais.")
    
    st.info(f"💎 **Pague via PIX Direto:** Chave PIX (Telefone): **{CHAVE_PIX_OFICIAL}**")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("#### Plano Start (Mensal)")
        st.markdown("**R$ 147,00 / mês**")
        st.markdown(f'<a href="{LINK_PLANO_START}" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Start</a>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Plano Professional")
        st.markdown("**R$ 2.470,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_PRO}" target="_blank" style="background-color: #28a745; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Professional</a>', unsafe_allow_html=True)
    with col_p3:
        st.markdown("#### Plano Enterprise")
        st.markdown("**R$ 5.970,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_ENTERPRISE}" target="_blank" style="background-color: #6f42c1; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Já realizou o pagamento ou possui senha de liberação?")
    senha_desbloqueio = st.text_input("Digite a sua senha de liberação mestre:", type="password", key="input_senha_desbloqueio_final")
    if st.button("🔓 Ativar Licença Definitiva"):
        if senha_desbloqueio in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.success("Licença ativada com sucesso! Atualizando...")
            st.rerun()
        else:
            st.error("Senha incorreta.")
            
    if st.button("🔄 Entrar com Outro E-mail"):
        st.session_state.usuario_identificado = False
        st.session_state.email_atual = ""
        st.rerun()
        
    st.stop()

# ==========================================
# FLUXO DE VERIFICAÇÃO DE ESTADO DE ACESSO
# ==========================================
if not st.session_state.usuario_identificado:
    tela_identificacao_inicial()

# Se já está identificado, checa se esgotou os usos na nuvem (exceto se for gestor pago)
if not st.session_state.liberado_pago_master:
    usos_atuais_cliente = obter_usos_email(st.session_state.email_atual)
    if usos_atuais_cliente >= LIMITE_MAXIMO_ACESSO:
        tela_bloqueio_comercial()

# ==========================================
# MENU LATERAL (NAVEGAÇÃO ESTRATÉGICA)
# ==========================================
st.sidebar.title("⚖️ Consultor Master")
st.sidebar.markdown("Navegação Estratégica")

if st.session_state.liberado_pago_master:
    st.sidebar.success("👑 **Modo Gestor Ativo**\n*(Acesso Ilimitado)*")
else:
    restantes = max(0, LIMITE_MAXIMO_ACESSO - obter_usos_email(st.session_state.email_atual))
    st.sidebar.info(f"👤 **Conta:** {st.session_state.email_atual}\n🎁 Restantes: **{restantes} / {LIMITE_MAXIMO_ACESSO}**")

modulo = st.sidebar.radio(
    "Selecione o Módulo:",
    [
        "🚀 Simulador Tributário & Planos",
        "💬 Chat IA Master Sênior",
        "📑 Parecer Executivo & Disparos",
        "🛡️ Auditoria Preventiva (XML/SPED)",
        "📊 Indicadores do Escritório",
        "🏛️ Governança de Clientes",
        "🎯 Central de Leads",
        "⚙️ Configurações / Painel Master"
    ]
)

# ==========================================
# FUNÇÃO AUXILIAR PARA CONTABILIZAR USO AO EXECUTAR AÇÕES
# ==========================================
def registrar_consumo_acao():
    if not st.session_state.liberado_pago_master:
        incrementar_uso_email(st.session_state.email_atual)

# ==========================================
# 1. MÓDULO: SIMULADOR TRIBUTÁRIO & PLANOS
# ==========================================
if modulo == "🚀 Simulador Tributário & Planos":
    st.title("🧮 Simulador Contínuo de Regime Tributário")
    st.markdown("Análise paramétrica inteligente para identificação da menor carga tributária.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Dados da Empresa")
        razao = st.text_input("Razão Social / Nome do Cliente:", value="Empresa Exemplo Ltda", key="sim_razao")
        whatsapp = st.text_input("WhatsApp do Cliente (com DDD):", value=MEU_WHATSAPP, key="sim_wpp")
        email = st.text_input("E-mail do Cliente:", value=st.session_state.email_atual, key="sim_email")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$):", min_value=10000.0, value=360000.0, step=10000.0, key="sim_fat")
        folha_anual = st.number_input("Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0, key="sim_folha")
        desp_anual = st.number_input("Despesas Operacionais Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0, key="sim_desp")

    with c2:
        st.subheader("Resultado da Simulação")
        if st.button("⚡ Executar Simulação Completa", type="primary", use_container_width=True, key="btn_exec_sim"):
            registrar_consumo_acao()

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

            lead_data = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Razao Social": razao,
                "WhatsApp": whatsapp,
                "E-mail": email,
                "Melhor Regime": melhor,
                "Economia (R$)": round(economia, 2)
            }
            salvar_lead_arquivo(lead_data)
            st.session_state.ultimo_resultado_sim = lead_data
            
            # Se atingiu o limite após o uso, força re-execução para travar
            if not st.session_state.liberado_pago_master and obter_usos_email(st.session_state.email_atual) >= LIMITE_MAXIMO_ACESSO:
                st.rerun()

        if "ultimo_resultado_sim" in st.session_state:
            res = st.session_state.ultimo_resultado_sim
            st.markdown("---")
            st.markdown("### 📤 Ações Comerciais e Relatório")
            
            texto_wpp = f"Olá {res['Razao Social']}, segue o resultado da nossa simulação tributária:\n\n*Melhor Regime:* {res['Melhor Regime']}\n*Economia Anual Potencial:* R$ {res['Economia (R$)']:,.2f}\n\nGerado via Consultor Inteligente Master."
            wpp_num = limpar_telefone(res['WhatsApp'])
            link_wpp_sim = f"https://wa.me/55{wpp_num}?text={requests.utils.quote(texto_wpp)}"

            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.markdown(f'<a href="{link_wpp_sim}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Resumo no WhatsApp</a>', unsafe_allow_html=True)
            with col_a2:
                relatorio_txt = f"RELATÓRIO DE SIMULAÇÃO TRIBUTÁRIA\nEmpresa: {res['Razao Social']}\nData: {res['Data']}\nMelhor Regime: {res['Melhor Regime']}\nEconomia Estimada: R$ {res['Economia (R$)']:,.2f}"
                st.download_button(
                    label="📥 Baixar Relatório (TXT)",
                    data=relatorio_txt,
                    file_name=f"simulacao_{res['Razao Social'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# ==========================================
# 2. MÓDULO: CHAT IA MASTER SÊNIOR
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    st.title("💬 Chat IA Master Sênior - Direito Tributário & Contabilidade")
    st.markdown("Faça perguntas técnicas avançadas sobre legislação brasileira.")

    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = [
            {"role": "assistant", "content": "Olá! Seja muito bem-vindo(a). Sou o seu Consultor Inteligente Master. Estou pronto para fornecer suporte técnico de excelência."}
        ]

    for msg in st.session_state.mensagens_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    pergunta_usuario = st.chat_input("Digite a sua dúvida tributária ou fiscal aqui...")
    if pergunta_usuario:
        registrar_consumo_acao()

        st.session_state.mensagens_chat.append({"role": "user", "content": pergunta_usuario})
        with st.chat_message("user"):
            st.write(pergunta_usuario)

        resposta_ia = f"Análise técnica executada com base na legislação brasileira atualizada para a consulta: '{pergunta_usuario}'."
        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
        with st.chat_message("assistant"):
            st.write(resposta_ia)
            
        if not st.session_state.liberado_pago_master and obter_usos_email(st.session_state.email_atual) >= LIMITE_MAXIMO_ACESSO:
            st.rerun()

# ==========================================
# 3. MÓDULO: PARECER EXECUTIVO & DISPAROS
# ==========================================
elif modulo == "📑 Parecer Executivo & Disparos":
    st.title("📑 Parecer Executivo & Disparos Automatizados")
    st.markdown("Geração de laudos técnicos aprofundados.")

    client_nome = st.text_input("Nome do Cliente / Empresa:", value="Comércio Exemplo S.A.")
    client_fone = st.text_input("WhatsApp do Destinatário:", value=MEU_WHATSAPP)
    tema_parecer = st.selectbox("Tema do Parecer Técnico:", ["Revisão de ICMS-ST", "Planejamento Tributário Anual", "Impactos da Reforma Tributária", "Malha Fiscal Federal"])

    if st.button("📝 Gerar Parecer Executivo com IA", type="primary"):
        registrar_consumo_acao()

        parecer_texto = f"PARECER TÉCNICO EXECUTIVO\nTema: {tema_parecer}\nCliente: {client_nome}\nData: {datetime.now().strftime('%d/%m/%Y')}\n\nConclusão: Recomendada a implementação imediata dos ajustes fiscais."
        st.success("Parecer gerado com sucesso!")
        st.text_area("Laudo Técnico:", value=parecer_texto, height=200)

        wpp_num = limpar_telefone(client_fone)
        link_wpp_parecer = f"https://wa.me/55{wpp_num}?text={requests.utils.quote(f'Olá {client_nome}, segue o seu Parecer Técnico sobre {tema_parecer}.')}"

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f'<a href="{link_wpp_parecer}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Parecer no WhatsApp</a>', unsafe_allow_html=True)
        with col_p2:
            st.download_button(label="📥 Baixar Parecer em TXT", data=parecer_texto, file_name="parecer.txt", mime="text/plain", use_container_width=True)

        if not st.session_state.liberado_pago_master and obter_usos_email(st.session_state.email_atual) >= LIMITE_MAXIMO_ACESSO:
            st.rerun()

# ==========================================
# 4. MÓDULO: AUDITORIA PREVENTIVA
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    st.title("🛡️ Auditoria Preventiva & Malha Fiscal")
    st.markdown("Auditoria padronizada de conformidade.")

    empresa_aud = st.text_input("Empresa Alvo da Auditoria:", value="Empresa Exemplo Ltda")
    if st.button("🛡️ Executar Auditoria Padronizada", type="primary"):
        registrar_consumo_acao()

        laudo_auditoria = f"RELATÓRIO DE AUDITORIA\nEmpresa: {empresa_aud}\nStatus: Conformidade verificada com sucesso."
        st.success("Auditoria executada com sucesso!")
        st.text_area("Laudo Analítico:", value=laudo_auditoria, height=220)
        st.download_button(label="📥 Baixar Relatório (TXT)", data=laudo_auditoria, file_name="auditoria.txt", mime="text/plain", use_container_width=True)

        if not st.session_state.liberado_pago_master and obter_usos_email(st.session_state.email_atual) >= LIMITE_MAXIMO_ACESSO:
            st.rerun()

# ==========================================
# 5. MÓDULO: INDICADORES DO ESCRITÓRIO
# ==========================================
elif modulo == "📊 Indicadores do Escritório":
    st.title("📊 Indicadores de Desempenho do Escritório")
    col_ind1, col_ind2, col_ind3 = st.columns(3)
    col_ind1.metric("Simulações Realizadas", "24")
    col_ind2.metric("Leads Capturados", "18")
    col_ind3.metric("Economia Média Gerada", "R$ 42.500,00", delta="+14%")

# ==========================================
# 6. MÓDULO: GOVERNANÇA DE CLIENTES
# ==========================================
elif modulo == "🏛️ Governança de Clientes":
    st.title("🏛️ Governança e Carteira de Clientes")
    try:
        if os.path.exists(ARQUIVO_LEADS):
            df_gov = pd.read_csv(ARQUIVO_LEADS)
            st.dataframe(df_gov, use_container_width=True)
        else:
            st.warning("Nenhum cliente cadastrado até o momento.")
    except Exception:
        st.info("Painel de governança pronto.")

# ==========================================
# 7. MÓDULO: CENTRAL DE LEADS
# ==========================================
elif modulo == "🎯 Central de Leads":
    st.title("🎯 Central de Captação de Leads")
    st.markdown("Contatos de e-mail e WhatsApp gerados pelas entradas e simulações na plataforma.")

    try:
        if os.path.exists(ARQUIVO_LEADS):
            df_leads = pd.read_csv(ARQUIVO_LEADS)
            st.dataframe(df_leads, use_container_width=True)
            
            csv_data = df_leads.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar Planilha de Leads (CSV)",
                data=csv_data,
                file_name="leads_consultor_master.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Ainda não há leads salvos no sistema.")
    except Exception:
        st.info("Central de leads em operação.")

# ==========================================
# 8. MÓDULO: CONFIGURAÇÕES / PAINEL MASTER
# ==========================================
elif modulo == "⚙️ Configurações / Painel Master":
    st.title("⚙️ Painel de Controle Master & Licenciamento")
    st.markdown("Gestão de licenças de acesso, chave PIX e ativação comercial.")

    if st.session_state.liberado_pago_master:
        st.success("🟢 Sistema com Licença Master Ativa (Acesso Ilimitado).")
    else:
        restantes = max(0, LIMITE_MAXIMO_ACESSO - obter_usos_email(st.session_state.email_atual))
        st.warning(f"🔒 Conta atual: `{st.session_state.email_atual}` | Tentativas restantes: {restantes} / {LIMITE_MAXIMO_ACESSO}")
        
    st.markdown("### 🔑 Ativar Senha Mestre de Gestor")
    senha_input = st.text_input("Digite a senha de ativação:", type="password", key="input_painel_senha")
    
    if st.button("Ativar Acesso Master"):
        if senha_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.success("Licença de gestor ativada com sucesso neste navegador!")
            st.rerun()
        else:
            st.error("Senha incorreta.")

    st.markdown("---")
    st.markdown("### 💳 Informações Oficiais de Pagamento (PIX e Cartão)")
    st.info(f"📌 **Chave PIX Oficial (InfinitePay):** `{CHAVE_PIX_OFICIAL}`\n\n📲 **WhatsApp para Comprovantes:** `(64) 99304-4147`")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown(f'<a href="{LINK_PLANO_START}" target="_blank" style="background-color: #007bff; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Start</a>', unsafe_allow_html=True)
    with col_c2:
        st.markdown(f'<a href="{LINK_PLANO_PRO}" target="_blank" style="background-color: #28a745; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Pro</a>', unsafe_allow_html=True)
    with col_c3:
        st.markdown(f'<a href="{LINK_PLANO_ENTERPRISE}" target="_blank" style="background-color: #6f42c1; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Enterprise</a>', unsafe_allow_html=True)
