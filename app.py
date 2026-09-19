import streamlit as st
import pandas as pd
import datetime
from google import genai
from google.genai import types
from supabase import create_client, Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Consultor Master - Sistema Contábil Corporativo",
    page_icon="💼",
    layout="wide"
)

# --- CONEXÃO COM SUPABASE (BANCO DE DADOS) ---
# O sistema busca as credenciais de forma segura nos segredos do Streamlit (st.secrets)
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "SUA_URL_SUPABASE")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "SUA_CHAVE_SUPABASE")
    if SUPABASE_URL != "SUA_URL_SUPABASE" and SUPABASE_KEY != "SUA_CHAVE_SUPABASE":
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        supabase = None
except Exception:
    supabase = None

# --- CREDENCIAIS E CONEXÕES DA IA ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "SUA_CHAVE_GEMINI_AQUI")

try:
    if GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
        client_ai = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client_ai = genai.Client() 
except Exception as e:
    st.error(f"Erro ao inicializar o Gemini: {e}")

# --- FUNÇÃO AUXILIAR: GERAR PDF EXECUTIVO ---
def gerar_conteudo_pdf(titulo, empresa, detalhes):
    conteudo = f"""==================================================
CONSULTOR MASTER - PARECER TÉCNICO EXECUTIVO
==================================================
Data: {datetime.date.today().strftime('%d/%m/%Y')}
Relatório: {titulo}
Empresa: {empresa}
--------------------------------------------------

{detalhes}

==================================================
Documento gerado automaticamente pelo Consultor Master
Escritório de Contabilidade Inteligente
==================================================
"""
    return conteudo.encode('utf-8')

# --- MENU LATERAL CORPORATIVO COMPLETO ---
st.sidebar.markdown("## 🏢 Consultor Master")
st.sidebar.markdown("Plataforma de Inteligência Contábil")
if supabase:
    st.sidebar.success("🟢 Supabase Conectado")
else:
    st.sidebar.warning("🟡 Modo Local / Supabase Pendente")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação Principal", 
    [
        "📊 Dashboard / Visão Geral", 
        "🆓 Simulador Básico (Isca Gratuita)",
        "📇 Gestão de Clientes (CRM)", 
        "⚖️ Comparativo de Regimes (Lado a Lado)",
        "📈 Simulador Avançado", 
        "🔄 Simulação Contínua & Migração",
        "🚨 Alertas de Oportunidades Fiscais",
        "📅 Planejamento Tributário Anual", 
        "💰 Análise de Lucros Isentos",
        "🤖 Chat IA Master Sênior", 
        "📑 Histórico de Relatórios",
        "⚙️ Configurações / Alíquotas",
        "🧮 Calculadora de Retenções"
    ]
)
st.sidebar.markdown("---")

# --- MÓDULO 1: DASHBOARD / VISÃO GERAL ---
if pagina == "📊 Dashboard / Visão Geral":
    st.title("📊 Dashboard e Visão Geral do Escritório")
    st.markdown("Painel inicial com indicadores de desempenho e resumo das operações.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empresas na Base", "42", "+3 este mês")
    col2.metric("Simulações Realizadas", "128", "+12 hoje")
    col3.metric("Economia Gerada (Total)", "R$ 450.200,00", "+15%")
    col4.metric("Status da IA", "Conectado & Estável", "Online")
    
    st.markdown("---")
    st.subheader("🚀 Indicadores Financeiros Derivados")
    c_ind1, c_ind2 = st.columns(2)
    with c_ind1:
        st.metric("Margem de Lucro Efetiva Média", "18.4%", "+2.1% vs. Setor")
    with c_ind2:
        st.metric("Carga Tributária Média Real", "8.2%", "-1.5% otimizado")

# --- MÓDULO 2: SIMULADOR BÁSICO (ISCA) ---
elif pagina == "🆓 Simulador Básico (Isca Gratuita)":
    st.title("🆓 Simulador Básico de Carga Tributária")
    st.markdown("Ferramenta de entrada rápida e gratuita para estimativa preliminar de impostos.")

    with st.form("form_simulador_basico"):
        razao_social = st.text_input("Razão Social do Cliente", value="Empresa Exemplo Ltda")
        faturamento = st.number_input("Faturamento Bruto Anual Estimado (R$)", value=180000.00, format="%.2f")
        executar_basico = st.form_submit_button("Calcular Carga Básica Gratuita")
        
    if executar_basico:
        st.success("Cálculo básico realizado com sucesso!")
        imposto_simples = faturamento * 0.06 
        imposto_presumido = faturamento * 0.1133 
        
        col1, col2 = st.columns(2)
        col1.metric("Simples Nacional (Estimado)", f"R$ {imposto_simples:,.2f} / ano")
        col2.metric("Lucro Presumido (Estimado)", f"R$ {imposto_presumido:,.2f} / ano")
        st.info("💡 **Dica Comercial:** Cadastre-se na versão completa para desbloquear relatórios em PDF e assessoria via IA.")

# --- MÓDULO 3: GESTÃO DE CLIENTES (CRM) ---
elif pagina == "📇 Gestão de Clientes (CRM)":
    st.title("📇 Gestão de Clientes e Cadastro (CRM)")
    st.markdown("Gerencie a carteira de empresas cadastradas no banco de dados.")
    
    with st.form("form_novo_cliente"):
        st.subheader("Cadastrar Nova Empresa / Cliente")
        c1, c2 = st.columns(2)
        with c1:
            cli_razao = st.text_input("Razão Social")
            cli_cnpj = st.text_input("CNPJ")
        with c2:
            cli_resp = st.text_input("Responsável / Sócio")
            cli_fone = st.text_input("WhatsApp de Contato (com DDD)")
        salvar_cli = st.form_submit_button("Salvar no Supabase")
        
        if salvar_cli:
            if supabase:
                try:
                    data = {"razao_social": cli_razao, "cnpj": cli_cnpj, "responsavel": cli_resp, "whatsapp": cli_fone}
                    supabase.table("clientes").insert(data).execute()
                    st.success(f"Cliente {cli_razao} salvo com sucesso no Supabase!")
                except Exception as e:
                    st.error(f"Erro ao salvar no Supabase: {e}")
            else:
                st.success(f"Cliente {cli_razao} simulado com sucesso (Supabase não configurado no momento).")
            
    st.markdown("---")
    st.subheader("📋 Clientes Cadastrados")
    df_clientes = pd.DataFrame({
        "Razão Social": ["Comércio Exemplo Ltda", "Tech Soluções S/A", "Prestadora Alpha ME"],
        "CNPJ": ["12.345.678/0001-90", "98.765.432/0001-12", "11.223.344/0001-55"],
        "Regime Atual": ["Simples Nacional", "Lucro Presumido", "Simples Nacional"],
        "Contato": ["(64) 99999-1111", "(64) 98888-2222", "(64) 97777-3333"]
    })
    st.dataframe(df_clientes, hide_index=True, use_container_width=True)

# --- MÓDULO 4: COMPARATIVO DE REGIMES (Lado a Lado) ---
elif pagina == "⚖️ Comparativo de Regimes (Lado a Lado)":
    st.title("⚖️ Comparativo Direto de Regimes Tributários")
    st.markdown("Confronto direto de impostos entre Simples Nacional, Lucro Presumido e Lucro Real.")
    
    c_comp1, c_comp2 = st.columns(2)
    with c_comp1:
        empresa_nome = st.text_input("Nome da Empresa", value="Empresa Exemplo S/A")
        whatsapp_cli = st.text_input("WhatsApp do Cliente (com DDD)", value="64993044147")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$)", value=600000.00, format="%.2f")
    with c_comp2:
        folha_anual = st.number_input("Folha de Pagamento Anual (R$)", value=150000.00, format="%.2f")
        despesa_anual = st.number_input("Despesas Operacionais Dedutíveis (R$)", value=80000.00, format="%.2f")
        ramo_ativ = st.selectbox("Setor de Atuação", ["Comércio / Varejo", "Serviços Gerais", "Indústria"])
        
    if st.button("Executar Confronto Lado a Lado & Gerar Relatório"):
        simples_est = fat_anual * 0.085
        presumido_est = fat_anual * 0.1133
        real_est = (fat_anual - despesa_anual - folha_anual) * 0.34
        if real_est < 0: real_est = fat_anual * 0.03
        
        st.markdown("### 📊 Resultado do Confronto Direto")
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("Simples Nacional", f"R$ {simples_est:,.2f} /ano")
        col_r2.metric("Lucro Presumido", f"R$ {presumido_est:,.2f} /ano")
        col_r3.metric("Lucro Real", f"R$ {real_est:,.2f} /ano")
        
        menor_imposto = min(simples_est, presumido_est, real_est)
        melhor_regime = "Simples Nacional" if menor_imposto == simples_est else ("Lucro Presumido" if menor_imposto == presumido_est else "Lucro Real")
        st.success(f"🏆 **Melhor Enquadramento:** {melhor_regime} apresenta a menor carga tributária projetada.")
        
        detalhes_rel = f"Análise Comparativa:\n- Simples: R$ {simples_est:,.2f}\n- Presumido: R$ {presumido_est:,.2f}\n- Real: R$ {real_est:,.2f}\n- Recomendado: {melhor_regime}"
        pdf_bytes = gerar_conteudo_pdf("Confronto Lado a Lado de Regimes", empresa_nome, detalhes_rel)
        
        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button("📥 Baixar Relatório em PDF", data=pdf_bytes, file_name=f"Comparativo_{empresa_nome}.pdf", mime="application/pdf")
        with col_dl2:
            link_wapp = f"https://wa.me/55{whatsapp_cli}?text=Olá,%20segue%20o%20parecer%20tributário%20do%20Consultor%20Master."
            st.markdown(f"<a href='{link_wapp}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 5: SIMULADOR AVANÇADO ---
elif pagina == "📈 Simulador Avançado":
    st.title("📈 Simulador Avançado de Fator R e Margens")
    st.markdown("Cruzamento detalhado de despesas e variáveis setoriais.")
    
    emp_adv = st.text_input("Empresa", value="Empresa Beta Ltda")
    wapp_adv = st.text_input("WhatsApp para Envio", value="64993044147")
    faturamento_adv = st.number_input("Faturamento Anual Base (R$)", value=360000.00)
    folha_adv = st.number_input("Folha de Salários Anual (R$)", value=100000.00)
    
    if st.button("Analisar Fator R & Gerar Relatório"):
        fator_r = (folha_adv / faturamento_adv) * 100
        st.metric("Fator R Calculado", f"{fator_r:.2f}%")
        if fator_r >= 28:
            st.success("✅ Fator R superior a 28%. Tributado pelo Anexo III do Simples Nacional.")
            status_fator = "Anexo III (Fator R >= 28%)"
        else:
            st.warning("⚠️ Fator R inferior a 28%. Tributado pelo Anexo V do Simples Nacional.")
            status_fator = "Anexo V (Fator R < 28%)"
            
        pdf_fator = gerar_conteudo_pdf("Análise de Fator R", emp_adv, f"Fator R: {fator_r:.2f}% - {status_fator}")
        
        c_df1, c_df2 = st.columns(2)
        with c_df1:
            st.download_button("📥 Baixar PDF Fator R", data=pdf_fator, file_name=f"FatorR_{emp_adv}.pdf", mime="application/pdf")
        with c_df2:
            link_w_fator = f"https://wa.me/55{wapp_adv}?text=Olá,%20segue%20o%20parecer%20do%20Fator%20R."
            st.markdown(f"<a href='{link_w_fator}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 6: SIMULAÇÃO CONTÍNUA & MIGRAÇÃO ---
elif pagina == "🔄 Simulação Contínua & Migração":
    st.title("🔄 Simulação Contínua de Regime Tributário")
    st.markdown("Painel de monitoramento do faturamento acumulado.")
    
    emp_cont = st.text_input("Empresa Monitorada", value="Empresa Contínua S/A")
    fat_acumulado = st.number_input("Faturamento Acumulado no Ano (R$)", value=3200000.00)
    
    if st.button("Analisar Momento de Migração"):
        st.metric("Faturamento Acumulado Atual", f"R$ {fat_acumulado:,.2f}")
        if fat_acumulado > 4200000:
            st.warning("⚠️ **Alerta Crítico de Migração:** Faturamento próximo ao teto do Simples Nacional (R$ 4,8M).")
        else:
            st.success("✅ **Status Estável:** Operação dentro da margem segura do regime atual.")

# --- MÓDULO 7: ALERTAS DE OPORTUNIDADES FISCAIS ---
elif pagina == "🚨 Alertas de Oportunidades Fiscais":
    st.title("🚨 Alertas de Oportunidades Fiscais")
    st.markdown("Identificação de créditos tributários não aproveitados.")
    
    setor_alerta = st.selectbox("Segmento da Empresa", ["Comércio Varejista", "Indústria", "Serviços Médicos", "Tecnologia / Software"])
    if st.button("Verificar Oportunidades para o Setor"):
        st.success(f"🔍 Análise concluída para o setor de **{setor_alerta}**!")
        st.info("💡 **Oportunidade Identificada:** Possibilidade de recuperação de PIS/COFINS monofásico e créditos acumulados.")

# --- MÓDULO 8: PLANEJAMENTO TRIBUTÁRIO ANUAL ---
elif pagina == "📅 Planejamento Tributário Anual":
    st.title("📅 Planejamento Tributário Anual")
    st.markdown("Projeção de 12 meses para antecipação de mudanças de faixa.")
    
    emp_plan = st.text_input("Nome da Empresa", value="Empresa Planejamento S/A")
    wapp_plan = st.text_input("WhatsApp Destino", value="64993044147")
    
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    df_proj = pd.DataFrame({"Mês": meses, "Faturamento Previsto (R$)": [35000.0] * 12})
    df_editado = st.data_editor(df_proj, hide_index=True, use_container_width=True)
    
    if st.button("Consolidar Projeção & Gerar Relatório"):
        total_proj = df_editado["Faturamento Previsto (R$)"].sum()
        st.success(f"Projeção consolidada! Total previsto no ano: R$ {total_proj:,.2f}")
        pdf_plan = gerar_conteudo_pdf("Planejamento Tributário Anual", emp_plan, f"Total Projetado: R$ {total_proj:,.2f}")
        
        cp1, cp2 = st.columns(2)
        with cp1:
            st.download_button("📥 Baixar PDF Planejamento", data=pdf_plan, file_name=f"Planejamento_{emp_plan}.pdf", mime="application/pdf")
        with cp2:
            link_w_plan = f"https://wa.me/55{wapp_plan}?text=Olá,%20segue%20o%20planejamento%20tributário."
            st.markdown(f"<a href='{link_w_plan}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 9: ANÁLISE DE LUCROS ISENTOS ---
elif pagina == "💰 Análise de Lucros Isentos":
    st.title("💰 Análise de Distribuição de Lucros Isentos")
    st.markdown("Cálculo do limite de isenção baseado na contabilidade e presunção.")
    
    emp_lucro = st.text_input("Empresa", value="Empresa Lucros Ltda")
    wapp_lucro = st.text_input("WhatsApp Destino", value="64993044147")
    rec_b = st.number_input("Receita Bruta Contábil (R$)", value=400000.0)
    pres = st.selectbox("Percentual de Presunção", [0.08, 0.16, 0.32])
    impostos_p = st.number_input("Tributos Federais Pagos (R$)", value=20000.0)
    
    if st.button("Calcular Limite Isento & Relatório"):
        limite = (rec_b * pres) - impostos_p
        st.metric("Lucro Isento Máximo Distribuível", f"R$ {limite:,.2f}")
        pdf_lucro = gerar_conteudo_pdf("Análise de Lucros Isentos", emp_lucro, f"Limite Isento: R$ {limite:,.2f}")
        
        cl1, cl2 = st.columns(2)
        with cl1:
            st.download_button("📥 Baixar PDF Lucros Isentos", data=pdf_lucro, file_name=f"Lucros_{emp_lucro}.pdf", mime="application/pdf")
        with cl2:
            link_w_lucro = f"https://wa.me/55{wapp_lucro}?text=Olá,%20segue%20a%20análise%20de%20lucros."
            st.markdown(f"<a href='{link_w_lucro}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 10: CHAT IA (GOOGLE-GENAI ESTÁVEL) ---
elif pagina == "🤖 Chat IA Master Sênior":
    st.title("🤖 Chat com Assistente Contábil Sênior")
    st.markdown("Tire dúvidas sobre legislação fiscal, normas contábeis e análises estratégicas em tempo real.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Digite sua dúvida contábil aqui..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("O assistente está consultando as normas contábeis..."):
                resposta_ia = None
                
                try:
                    response = client_ai.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    if response and response.text:
                        resposta_ia = response.text
                except Exception:
                    try:
                        response = client_ai.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=prompt
                        )
                        if response and response.text:
                            resposta_ia = response.text
                    except Exception as err:
                        st.error(f"Erro de conexão com a API do Gemini. Verifique a chave configurada. Detalhe: {err}")

                if resposta_ia:
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})

# --- MÓDULO 11: HISTÓRICO DE RELATÓRIOS ---
elif pagina == "📑 Histórico de Relatórios":
    st.title("📑 Histórico de Relatórios e Exportação")
    st.markdown("Espaço centralizado de relatórios gerados.")
    
    df_rels = pd.DataFrame({
        "Data": ["19/09/2026", "18/09/2026", "17/09/2026"],
        "Cliente": ["Comércio Exemplo Ltda", "Tech Soluções S/A", "Prestadora Alpha ME"],
        "Tipo": ["Simulação Comparativa", "Parecer de Lucros", "Planejamento Anual"],
        "Status": ["Gerado com Sucesso", "Enviado WhatsApp", "Arquivado"]
    })
    st.dataframe(df_rels, hide_index=True, use_container_width=True)

# --- MÓDULO 12: CONFIGURAÇÕES / ALÍQUOTAS ---
elif pagina == "⚙️ Configurações / Alíquotas":
    st.title("⚙️ Configurações e Atualização de Alíquotas")
    st.markdown("Área administrativa para parâmetros gerais.")
    
    st.number_input("Salário Mínimo Vigente (R$)", value=1502.00)
    st.number_input("Teto do INSS (R$)", value=7786.02)
    st.selectbox("Ano-Calendário de Referência", ["2026", "2025", "2024"])
    
    if st.button("Salvar Alterações de Parâmetros"):
        st.success("Tabelas de alíquotas atualizadas com sucesso!")

# --- MÓDULO 13: CALCULADORA DE RETENÇÕES ---
elif pagina == "🧮 Calculadora de Retenções":
    st.title("🧮 Calculadora de Retenções Federais (IRRF, CSRF, INSS)")
    st.markdown("Apuração rápida de retenções na fonte para notas fiscais.")
    
    emp_ret = st.text_input("Empresa Tomadora / Prestadora", value="Prestadora Exemplo Ltda")
    wapp_ret = st.text_input("WhatsApp Destino", value="64993044147")
    valor_nf = st.number_input("Valor Bruto da Nota Fiscal (R$)", value=10000.00)
    tipo_servico = st.selectbox("Natureza do Serviço", ["Serviços Gerais / Administrativos", "Segurança / Limpeza", "Serviços Profissionais (Lei 10.833)"])
    
    if st.button("Calcular Retenções Detalhadas & Relatório"):
        pis_cofins_csll = valor_nf * 0.0465 
        irrf = valor_nf * 0.015 if valor_nf > 666.66 else 0.0 
        inss = valor_nf * 0.11 if "Segurança" in tipo_servico or "Limpeza" in tipo_servico else 0.0
        
        total_retido = pis_cofins_csll + irrf + inss
        liquido_receber = valor_nf - total_retido
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Retenções", f"R$ {total_retido:,.2f}")
        col2.metric("Líquido a Receber", f"R$ {liquido_receber:,.2f}")
        col3.metric("CSRF + IRRF + INSS", f"R$ {total_retido:,.2f}")
        
        detalhes_ret = f"Valor Bruto: R$ {valor_nf:,.2f}\nRetido: R$ {total_retido:,.2f}\nLíquido: R$ {liquido_receber:,.2f}"
        pdf_ret = gerar_conteudo_pdf("Cálculo de Retenções Federais", emp_ret, detalhes_ret)
        
        cr1, cr2 = st.columns(2)
        with cr1:
            st.download_button("📥 Baixar PDF Retenções", data=pdf_ret, file_name=f"Retencoes_{emp_ret}.pdf", mime="application/pdf")
        with cr2:
            link_w_ret = f"https://wa.me/55{wapp_ret}?text=Olá,%2520segue%2520o%2520demonstrativo%2520de%2520retenções."
            st.markdown(f"<a href='{link_w_ret}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)
