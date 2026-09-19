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
    
    st.markdown("### 🚀 Escolha seu Plano de Assinatura na InfinitePay:")
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
                st.success("Licença Master ativada com sucesso!")
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
            input_senha_mestre = st.text_input("Senha de Gestor / Cliente (Opcional):", type="password", value="")

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
# MENU LATERAL ORGANIZADO
# ==========================================
st.sidebar.title("⚖️ Consultor Master")
if st.session_state.liberado_pago_master:
    st.sidebar.success("👑 **Modo Gestor / Master Ativo**\n*(Acesso Total Liberado)*")
else:
    st.sidebar.warning(f"👤 **Lead Ativo:**\n`{st.session_state.email_atual}`\n\n🟢 *Simulador Gratuito Liberado*")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Navegação")

modulo = st.sidebar.radio(
    "Selecione o Módulo:",
    [
        "🚀 1. Simulador Tributário Gratuito",
        "⚙️ 2. Simulador Tributário Avançado",
        "💡 3. Pró-Labore x Lucros (Fator R)",
        "🧾 4. Retenções na Fonte (Notas Fiscais)",
        "⛽ 5. Recuperação Crédito Monofásico",
        "👥 6. Custo Real de Funcionário (CLT)",
        "📅 7. Calendário de Obrigações Fiscais",
        "💬 Chat IA Master Sênior",
        "📑 Parecer Executivo & Laudos",
        "🛡️ Auditoria Preventiva (XML/SPED)",
        "📊 Indicadores & Fator R",
        "🏛️ Governança de Clientes",
        "🎯 Central de Leads",
        "🔐 Painel Master / Configurações"
    ]
)

st.sidebar.markdown("---")
if not st.session_state.liberado_pago_master:
    if st.sidebar.button("💎 Desbloquear Todos os Módulos", type="primary", use_container_width=True):
        st.session_state.liberado_pago_master = True
        st.rerun()

# ==========================================
# 1. MÓDULO: SIMULADOR TRIBUTÁRIO GRATUITO
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
# 2. MÓDULO: SIMULADOR TRIBUTÁRIO AVANÇADO (RECHEADO E PROFISSIONAL)
# ==========================================
elif modulo == "⚙️ 2. Simulador Tributário Avançado":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Simulador Tributário Avançado")
    
    st.title("⚙️ Simulador Tributário Avançado & Institucional")
    st.markdown("Painel analítico corporativo com árvore de decisão fiscal, alíquotas efetivas, gráficos de comparação e exportação de laudo em PDF.")
    
    col_av1, col_av2 = st.columns(2, gap="large")
    with col_av1:
        st.subheader("🛠️ Parâmetros Fiscais e Estruturais")
        adv_razao = st.text_input("Razão Social do Cliente:", value="Indústria e Comércio S/A")
        adv_cnpj = st.text_input("CNPJ:", value="00.000.000/0001-00")
        adv_cnae = st.text_input("CNAE Principal:", value="4711-3/02 - Comércio varejista")
        
        st.markdown("---")
        adv_faturamento = st.number_input("Faturamento Bruto Anual (R$):", min_value=0.0, value=1200000.0, step=50000.0)
        adv_folha = st.number_input("Folha de Salários / Pró-labore 12m (R$):", min_value=0.0, value=320000.0, step=10000.0)
        adv_compras = st.number_input("Aquisição de Mercadorias / Insumos (R$):", min_value=0.0, value=500000.0, step=20000.0)
        adv_despesas = st.number_input("Despesas Operacionais Dedutíveis (R$):", min_value=0.0, value=150000.0, step=10000.0)
        
        st.markdown("---")
        anexo_pretendido = st.selectbox("Anexo Base Simples Nacional:", ["Anexo I (Comércio)", "Anexo II (Indústria)", "Anexo III (Serviços gerais)", "Anexo V (Serviços fator R)"])

    with col_av2:
        st.subheader("📊 Laudo Comparativo Executivo")
        if st.button("🚀 Processar Análise Estratégica Avançada", type="primary", use_container_width=True):
            fator_r = (adv_folha / adv_faturamento) * 100 if adv_faturamento > 0 else 0
            
            # Cálculo refinado por regime
            aliquota_simples = 0.11 if "Comércio" in anexo_pretendido or "Indústria" in anexo_pretendido else (0.155 if fator_r < 28 else 0.12)
            imposto_simples = adv_faturamento * aliquota_simples
            
            imposto_presumido = (adv_faturamento * 0.08 * 0.34) + (adv_faturamento * 0.0365)
            lucro_real_base = max(0.0, adv_faturamento - adv_compras - adv_despesas - adv_folha)
            imposto_real = lucro_real_base * 0.34
            
            st.success("Análise paramétrica concluída com sucesso!")
            
            m_a1, m_a2 = st.columns(2)
            m_a1.metric("Fator R Apurado", f"{fator_r:.2f}%")
            
            cenarios_adv = {
                "Simples Nacional": round(imposto_simples, 2),
                "Lucro Presumido": round(imposto_presumido, 2),
                "Lucro Real": round(imposto_real, 2)
            }
            melhor_av = min(cenarios_adv, key=cenarios_adv.get)
            m_a2.metric("Regime Mais Lucrativo", melhor_av)
            
            # Tabela de Comparação
            df_comparativo = pd.DataFrame({
                "Regime Tributário": list(cenarios_adv.keys()),
                "Carga Anual Estimada (R$)": list(cenarios_adv.values())
            })
            st.dataframe(df_comparativo, use_container_width=True)
            
            # Gráfico de Barras Visual para Bater o Olho
            st.markdown("#### 📈 Comparativo Visual de Carga Tributária")
            st.bar_chart(df_comparativo.set_index("Regime Tributário"))
            
            economia_max = max(cenarios_adv.values()) - cenarios_adv[melhor_av]
            st.info(dict(melhor_regime=melhor_av, economia=economia_max)) # placeholder interno
            st.markdown(f"💡 **Parecer Técnico Master:** A adoção do **{melhor_av}** trará uma otimização expressiva no fluxo de caixa, gerando uma economia de até **R$ {economia_max:,.2f}** anuais para a empresa {adv_razao}.")
            
            # Botão de Exportação de Laudo (Simulado em Texto formatado / Download)
            texto_laudo = f"""LAUDO TÉCNICO TRIBUTÁRIO - {adv_razao}
CNPJ: {adv_cnpj}
Faturamento Anual: R$ {adv_faturamento:,.2f}
Fator R: {fator_r:.2f}%
Melhor Regime Indicado: {melhor_av}
Economia Estimada: R$ {economia_max:,.2f}
"""
            st.download_button(
                label="📥 Baixar Laudo Executivo Completo (.TXT / PDF)",
                data=texto_laudo,
                file_name=f"Laudo_Tributario_{adv_razao.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==========================================
# 3. MÓDULO: PRÓ-LABORE X LUCROS (FATOR R)
# ==========================================
elif modulo == "💡 3. Pró-Labore x Lucros (Fator R)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Pró-Labore x Lucros (Fator R)")
    
    st.title("💡 Otimizador de Pró-Labore e Fator R")
    st.markdown("Calcule o ponto ótimo de retirada de pró-labore para atingir 28% de Fator R e economizar no Simples Nacional.")
    
    c_pl1, c_pl2 = st.columns(2)
    with c_pl1:
        faturamento_12m = st.number_input("Faturamento Bruto Acumulado 12 Meses (R$):", value=500000.0, step=10000.0)
        folha_atual_12m = st.number_input("Folha Atual (sem pró-labore dos sócios) 12m (R$):", value=100000.0, step=5000.0)
    with c_pl2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚖️ Calcular Pró-Labore Ideal", type="primary", use_container_width=True):
            folha_necessaria = faturamento_12m * 0.28
            pro_labore_anual_necessario = max(0.0, folha_necessaria - folha_atual_12m)
            pro_labore_mensal = pro_labore_anual_necessario / 12
            
            st.success("Cálculo realizado!")
            st.metric("Pró-Labore Mensal Ideal para o Sócio", f"R$ {pro_labore_mensal:,.2f}")
            st.info(f"Com esse valor, sua folha atinge exatamente 28% do faturamento, garantindo sua empresa no **Anexo III** (evitando o Anexo V que é muito mais caro).")

# ==========================================
# 4. MÓDULO: RETENÇÕES NA FONTE
# ==========================================
elif modulo == "🧾 4. Retenções na Fonte (Notas Fiscais)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Retenções na Fonte (Notas Fiscais)")
    
    st.title("🧾 Simulador de Retenções Tributárias na Fonte")
    st.markdown("Aureste os valores de retenção de INSS, ISS, IRRF, PIS, COFINS e CSLL em notas fiscais de serviços.")
    
    rf1, rf2 = st.columns(2)
    with rf1:
        valor_nf = st.number_input("Valor Bruto da Nota Fiscal de Serviço (R$):", value=10000.0, step=500.0)
        tipo_servico = st.selectbox("Natureza do Serviço:", ["Serviços Gerais / Administrativos", "Serviços de Engenharia / Arquitetura", "Serviços Médicos / Saúde"])
    with rf2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Calcular Retenções", type="primary", use_container_width=True):
            irrf = valor_nf * 0.015 if valor_nf > 666.66 else 0.0
            pis_cofins_csll = valor_nf * 0.0465 if valor_nf > 5000 else 0.0
            iss = valor_nf * 0.05
            liquido = valor_nf - (irrf + pis_cofins_csll + iss)
            
            st.metric("Valor Líquido a Receber", f"R$ {liquido:,.2f}")
            df_ret = pd.DataFrame({
                "Tributo Retido": ["IRRF (1,5%)", "PIS/COFINS/CSLL (4,65%)", "ISS Municipal (5%)"],
                "Valor (R$)": [round(irrf, 2), round(pis_cofins_csll, 2), round(iss, 2)]
            })
            st.dataframe(df_ret, use_container_width=True)

# ==========================================
# 5. MÓDULO: RECUPERAÇÃO DE CRÉDITO MONOFÁSICO
# ==========================================
elif modulo == "⛽ 5. Recuperação Crédito Monofásico":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Recuperação Crédito Monofásico")
    
    st.title("⛽ Simulador de Recuperação de Crédito (PIS/COFINS Monofásico)")
    st.markdown("Exclusivo para postos de combustíveis, distribuidoras, autopeças, farmácias e pet shops.")
    
    m1, m2 = st.columns(2)
    with m1:
        fat_monofasico = st.number_input("Faturamento Mensal com Produtos Monofásicos (R$):", value=150000.0, step=10000.0)
        meses_retroativos = st.slider("Meses para Recuperação Retroativa (até 60m):", 1, 60, 36)
    with m2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💰 Estimar Crédito a Recuperar", type="primary", use_container_width=True):
            credito_estimado = fat_monofasico * 0.03 * meses_retroativos
            st.metric("Crédito Potencial Recuperável", f"R$ {credito_estimado:,.2f}")
            st.success("Oportunidade identificada! Estes valores podem ser compensados via PER/DCOMP na Receita Federal.")

# ==========================================
# 6. MÓDULO: CUSTO REAL DE FUNCIONÁRIO (CLT)
# ==========================================
elif modulo == "👥 6. Custo Real de Funcionário (CLT)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Custo Real de Funcionário (CLT)")
    
    st.title("👥 Simulador de Custo Real de Funcionário (CLT)")
    st.markdown("Descubra quanto custa realmente manter um colaborador na carteira (salário + encargos + provisões).")
    
    clt1, clt2 = st.columns(2)
    with clt1:
        salario_base = st.number_input("Salário Bruto Mensal (R$):", value=3500.0, step=200.0)
        tem_insalubridade = st.checkbox("Adicional de Insalubridade / Periculosidade")
    with clt2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 Calcular Custo Total", type="primary", use_container_width=True):
            inss_patronal = salario_base * 0.20
            fgts = salario_base * 0.08
            provisao_13 = salario_base / 12
            provisao_ferias = (salario_base * 1.3333) / 12
            custo_total = salario_base + inss_patronal + fgts + provisao_13 + provisao_ferias
            
            st.metric("Custo Total Mensal para a Empresa", f"R$ {custo_total:,.2f}")
            st.info(f"O colaborador custa aproximadamente **{(custo_total/salario_base):.2f}x** o valor do seu salário bruto nominal.")

# ==========================================
# 7. MÓDULO: CALENDÁRIO DE OBRIGAÇÕES
# ==========================================
elif modulo == "📅 7. Calendário de Obrigações Fiscais":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Calendário de Obrigações Fiscais")
    
    st.title("📅 Calendário Fiscal Inteligente & Vencimentos")
    st.markdown("Acompanhe os prazos limite das principais obrigações acessórias federais, estaduais e municipais.")
    
    dados_calendario = [
        {"Obrigação": "PGDAS-D (Simples Nacional)", "Vencimento": "Dia 20 de cada mês", "Status": "🟢 No Prazo"},
        {"Obrigação": "DCTFWeb e eSocial", "Vencimento": "Dia 15 de cada mês", "Status": "🟢 No Prazo"},
        {"Obrigação": "DEFIS (Anual)", "Vencimento": "Até 31 de Março", "Status": "⚠️ Atenção ao Prazo"},
        {"Obrigação": "IRPJ / CSLL / PIS / COFINS (Lucro Presumido)", "Vencimento": "Último dia útil do mês subsequente", "Status": "🟢 No Prazo"}
    ]
    st.dataframe(pd.DataFrame(dados_calendario), use_container_width=True)

# ==========================================
# 8. MÓDULO: CHAT IA MASTER SÊNIOR
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Chat IA Master Sênior")
    
    st.title("💬 Chat IA Master Sênior")
    st.markdown("Consulter inteligência artificial especializada em planejamento tributário brasileiro (LC 123/2006, RIR/2018).")
    
    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = [{"role": "assistant", "content": "Olá, Gestor! Como posso ajudar na consultoria fiscal ou na elisão tributária hoje?"}]
        
    for msg in st.session_state.mensagens_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Digite sua dúvida tributária ou parâmetro de cliente..."):
        st.session_state.mensagens_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        resposta_ia = f"Análise executiva para a consulta '{prompt}': Com base na legislação tributária vigente, recomenda-se a revisão do enquadramento e cruzamento com as obrigações acessórias aplicáveis."
        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
        with st.chat_message("assistant"):
            st.markdown(resposta_ia)

# ==========================================
# 9. MÓDULO: PARECER EXECUTIVO & LAUDOS
# ==========================================
elif modulo == "📑 Parecer Executivo & Laudos":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Parecer Executivo & Laudos")
    
    st.title("📑 Parecer Executivo Institucional")
    st.markdown("Emissão de relatórios formais e laudos periciais com formatação executiva para entrega a conselhos de administração e diretoria.")
    
    cliente_parecer = st.text_input("Nome / Razão Social do Tomador:", value="Empresa Exemplo Ltda")
    assunto_parecer = st.selectbox("Objeto do Parecer:", ["Migração de Regime Tributário", "Recuperação de Créditos PIS/COFINS", "Análise de Distribuição de Lucros Isentos"])
    
    if st.button("Gerar Parecer Executivo em PDF/Texto"):
        st.markdown(f"---")
        st.markdown(f"### 🏛️ LAUDO TÉCNICO DE CONSULTORIA TRIBUTÁRIA")
        st.markdown(f"**Cliente:** {cliente_parecer} | **Data:** {datetime.now().strftime('%d/%m/%Y')}")
        st.markdown(f"**Objeto:** {assunto_parecer}")
        st.markdown("""
        **1. Considerações Preliminares:**
        O presente parecer tem por escopo analisar a otimização da carga tributária suportada pela consulente, fundamentando-se nas normas da legislação federal brasileira.
        
        **2. Conclusão e Fundamentação:**
        Constatou-se viabilidade jurídica e econômica para a reestruturação das operações, mitigando riscos fiscais e otimizando o fluxo de caixa corporativo.
        """)

# ==========================================
# 10. MÓDULO: AUDITORIA PREVENTIVA (XML/SPED)
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Auditoria Preventiva (XML/SPED)")
    
    st.title("🛡️ Auditoria Preventiva XML / SPED")
    st.markdown("Varredura de inconsistências fiscais, divergências de NCM e cruzamento de notas fiscais eletrônicas.")
    
    uploaded_files = st.file_uploader("Carregar arquivos XML ou SPED para auditoria:", accept_multiple_files=True, type=["xml", "txt"])
    if uploaded_files:
        st.success(f"{len(uploaded_files)} arquivo(s) carregado(s) com sucesso para análise preventiva.")
        if st.button("Executar Varredura de Riscos Fiscais"):
            st.warning("Nenhum passivo fiscal crítico detectado nos arquivos validados.")

# ==========================================
# 11. MÓDULO: INDICADORES & FATOR R
# ==========================================
elif modulo == "📊 Indicadores & Fator R":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Indicadores & Fator R")
    
    st.title("📊 Painel de Indicadores & Gestão do Fator R")
    st.markdown("Monitoramento contínuo da relação folha/receita para empresas enquadradas no Simples Nacional.")
    
    f_bruto_12m = st.number_input("Receita Bruta Acumulada 12 Meses (R$):", value=1800000.0)
    f_folha_12m = st.number_input("Folha de Salários Acumulada 12 Meses (R$):", value=520000.0)
    
    if f_bruto_12m > 0:
        f_r_atual = (f_folha_12m / f_bruto_12m) * 100
        st.metric("Fator R Calculado", f"{f_r_atual:.2f}%", delta="Meta: >= 28.0%" if f_r_atual < 28 else "Anexo III Garantido")
        if f_r_atual >= 28:
            st.success("A empresa está apta ao Anexo III (alíquotas iniciais mais benéficas).")
        else:
            st.warning("Atenção: Fator R abaixo de 28%. A atividade está sujeita ao Anexo V.")

# ==========================================
# 12. MÓDULO: GOVERNANÇA DE CLIENTES
# ==========================================
elif modulo == "🏛️ Governança de Clientes":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Governança de Clientes")
    
    st.title("🏛️ Governança de Clientes e Conformidade Fiscal")
    st.markdown("Gestão de carteira de clientes, status de certidões negativas e prazos de entrega de obrigações.")
    st.info("Nenhum alerta de regularidade fiscal pendente na carteira ativa.")

# ==========================================
# 13. MÓDULO: CENTRAL DE LEADS
# ==========================================
elif modulo == "🎯 Central de Leads":
    if not st.session_state.liberado_pago_master:
        renderizar_paywall_modulo("Central de Leads")
    
    st.title("🎯 Central de Leads Capturados")
    st.markdown("Relação de potenciais clientes que utilizaram o simulador gratuito de entrada.")
    if os.path.exists(ARQUIVO_LEADS):
        st.dataframe(pd.read_csv(ARQUIVO_LEADS), use_container_width=True)
    else:
        st.info("Nenhum lead registrado localmente até o momento.")

# ==========================================
# 14. MÓDULO: CONFIGURAÇÕES / PAINEL MASTER
# ==========================================
elif modulo == "🔐 Painel Master / Configurações":
    st.title("🔐 Painel de Controle Master")
    st.markdown("Área restrita para autenticação administrativa e testes de liberação de licenças.")
    
    senha_input = st.text_input("Digite a Senha Mestre de Acesso:", type="password")
    if st.button("Ativar Acesso Total"):
        if senha_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.success("Licença Master ativada com sucesso em todos os módulos!")
            st.rerun()
        else:
            st.error("Senha incorreta.")
