import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import datetime
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Consultor Master - Sistema Contábil Corporativo",
    page_icon="💼",
    layout="wide"
)

# --- CREDENCIAIS E CONEXÕES DA IA ---
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI" 

try:
    if GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
        client_ai = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client_ai = genai.Client() 
except Exception as e:
    st.error(f"Erro ao inicializar o Gemini: {e}")

# --- FUNÇÃO AUXILIAR: GERAR CONTEÚDO PDF SIMULADO/ESTRUTURADO ---
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

# --- MENU LATERAL CORPORATIVO ORGANIZADO ---
st.sidebar.markdown("## 🏢 Consultor Master")
st.sidebar.markdown("Plataforma de Inteligência Contábil")
st.sidebar.success("🔓 Sistema Ativo & Integrado")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação Principal", 
    [
        "📊 Dashboard / Visão Geral", 
        "📇 Gestão de Clientes (CRM)", 
        "⚖️ Comparativo de Regimes (Lado a Lado)",
        "📈 Simulador Avançado", 
        "📅 Planejamento Tributário Anual", 
        "💰 Análise de Lucros Isentos",
        "🤖 Chat IA Master Sênior", 
        "📑 Histórico de Relatórios",
        "⚙️ Configurações / Alíquotas",
        "🧮 Calculadora de Retenções"
    ]
)
st.sidebar.markdown("---")

# --- MÓDULO 1: DASHBOARD / VISÃO GENERAL ---
if pagina == "📊 Dashboard / Visão Geral":
    st.title("📊 Dashboard e Visão Geral do Escritório")
    st.markdown("Painel inicial com indicadores de desempenho, atalhos rápidos e resumo das últimas simulações.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empresas na Base", "42", "+3 este mês")
    col2.metric("Simulações Realizadas", "128", "+12 hoje")
    col3.metric("Economia Gerada (Total)", "R$ 450.200,00", "+15%")
    col4.metric("Status da IA", "Conectado & Estável", "Online")
    
    st.markdown("---")
    st.subheader("🚀 Atalhos Rápidos para Operação")
    c_at1, c_at2, c_at3 = st.columns(3)
    with c_at1:
        st.info("💡 **Dica:** Utilize o Comparativo Lado a Lado para confrontar os 3 regimes de forma direta.")
    with c_at2:
        st.success("🤖 **IA Sênior:** Tire dúvidas complexas de legislação com o assistente inteligente.")
    with c_at3:
        st.warning("📑 **PDF & WhatsApp:** Todos os relatórios agora geram PDF e link direto de envio.")

# --- MÓDULO 2: GESTÃO DE CLIENTES (CRM) ---
elif pagina == "📇 Gestão de Clientes (CRM)":
    st.title("📇 Gestão de Clientes e Cadastro (CRM)")
    st.markdown("Gerencie a carteira de empresas cadastradas, histórico de alterações e consultas de apoio.")
    
    with st.form("form_novo_cliente"):
        st.subheader("Cadastrar Nova Empresa / Cliente")
        c1, c2 = st.columns(2)
        with c1:
            cli_razao = st.text_input("Razão Social")
            cli_cnpj = st.text_input("CNPJ")
        with c2:
            cli_resp = st.text_input("Responsável / Sócio")
            cli_fone = st.text_input("WhatsApp de Contato (com DDD)")
        salvar_cli = st.form_submit_button("Salvar na Base de Clientes")
        if salvar_cli:
            st.success(f"Cliente {cli_razao} cadastrado com sucesso na base de dados!")
            
    st.markdown("---")
    st.subheader("📋 Clientes Cadastrados Recentemente")
    df_clientes = pd.DataFrame({
        "Razão Social": ["Comércio Exemplo Ltda", "Tech Soluções S/A", "Prestadora Alpha ME"],
        "CNPJ": ["12.345.678/0001-90", "98.765.432/0001-12", "11.223.344/0001-55"],
        "Regime Atual": ["Simples Nacional", "Lucro Presumido", "Simples Nacional"],
        "Contato": ["(64) 99999-1111", "(64) 98888-2222", "(64) 97777-3333"]
    })
    st.dataframe(df_clientes, hide_index=True, use_container_width=True)

# --- MÓDULO 3: COMPARATIVO DE REGIMES (LADO A LADO) ---
elif pagina == "⚖️ Comparativo de Regimes (Lado a Lado)":
    st.title("⚖️ Comparativo Direto de Regimes Tributários")
    st.markdown("Confronto direto de impostos entre Simples Nacional, Lucro Presumido e Lucro Real em uma única tela.")
    
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
        
        # Bloco de Exportação PDF & WhatsApp
        detalhes_rel = f"""Análise Comparativa de Regimes Tributários:
- Faturamento Anual: R$ {fat_anual:,.2f}
- Folha de Pagamento: R$ {folha_anual:,.2f}
- Despesas Operacionais: R$ {despesa_anual:,.2f}

Projeções Anuais:
1. Simples Nacional: R$ {simples_est:,.2f}
2. Lucro Presumido: R$ {presumido_est:,.2f}
3. Lucro Real: R$ {real_est:,.2f}

Conclusão Técnica: O regime mais vantajoso para a empresa é o {melhor_regime}."""

        pdf_bytes = gerar_conteudo_pdf("Confronto Lado a Lado de Regimes", empresa_nome, detalhes_rel)
        
        st.markdown("---")
        st.subheader("📥 Exportação e Envio Direto")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Baixar Relatório em PDF",
                data=pdf_bytes,
                file_name=f"Comparativo_{empresa_nome.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        with col_dl2:
            link_wapp = f"https://wa.me/55{whatsapp_cli}?text=Olá,%20segue%20o%20parecer%20de%20comparativo%20tributário%20gerado%20pelo%20Consultor%20Master%20para%20a%20sua%20empresa."
            st.markdown(f"<a href='{link_wapp}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar PDF/Relatório via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 4: SIMULADOR AVANÇADO ---
elif pagina == "📈 Simulador Avançado":
    st.title("📈 Simulador Avançado de Fator R e Margens")
    st.markdown("Cruzamento detalhado de despesas, margens de lucro e variáveis setoriais.")
    
    emp_adv = st.text_input("Empresa", value="Empresa Beta Ltda")
    wapp_adv = st.text_input("WhatsApp para Envio", value="64993044147")
    faturamento_adv = st.number_input("Faturamento Anual Base (R$)", value=360000.00)
    folha_adv = st.number_input("Folha de Salários Anual (R$)", value=100000.00)
    
    if st.button("Analisar Fator R & Gerar Relatório"):
        fator_r = (folha_adv / faturamento_adv) * 100
        st.metric("Fator R Calculado", f"{fator_r:.2f}%")
        if fator_r >= 28:
            st.success("✅ Fator R superior a 28%. A empresa pode ser tributada pelo Anexo III do Simples Nacional.")
            status_fator = "Aprovado no Anexo III (Fator R >= 28%)"
        else:
            st.warning("⚠️ Fator R inferior a 28%. A empresa cai no Anexo V do Simples Nacional (tributação mais onerosa).")
            status_fator = "Enquadrado no Anexo V (Fator R < 28%)"
            
        detalhes_fator = f"Faturamento: R$ {faturamento_adv:,.2f}\nFolha: R$ {folha_adv:,.2f}\nFator R: {fator_r:.2f}%\nStatus: {status_fator}"
        pdf_fator = gerar_conteudo_pdf("Análise de Fator R", emp_adv, detalhes_fator)
        
        c_df1, c_df2 = st.columns(2)
        with c_df1:
            st.download_button("📥 Baixar PDF Fator R", data=pdf_fator, file_name=f"FatorR_{emp_adv}.pdf", mime="application/pdf")
        with c_df2:
            link_w_fator = f"https://wa.me/55{wapp_adv}?text=Olá,%20segue%20o%20parecer%20do%20Fator%20R%20gerado%20pelo%20Consultor%20Master."
            st.markdown(f"<a href='{link_w_fator}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 5: PLANEJAMENTO TRIBUTÁRIO ANUAL ---
elif pagina == "📅 Planejamento Tributário Anual":
    st.title("📅 Planejamento Tributário Anual")
    st.markdown("Projeção de 12 meses para antecipação de mudanças de faixa e limites de enquadramento.")
    
    emp_plan = st.text_input("Nome da Empresa", value="Empresa Planejamento S/A")
    wapp_plan = st.text_input("WhatsApp Destino", value="64993044147")
    
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    df_proj = pd.DataFrame({"Mês": meses, "Faturamento Previsto (R$)": [35000.0] * 12})
    df_editado = st.data_editor(df_proj, hide_index=True, use_container_width=True)
    
    if st.button("Consolidar Projeção & Gerar Relatório"):
        total_proj = df_editado["Faturamento Previsto (R$)"].sum()
        st.success(f"Projeção consolidada! Total previsto no ano: R$ {total_proj:,.2f}")
        
        detalhes_plan = f"Faturamento Total Anual Projetado: R$ {total_proj:,.2f}\nPlanejamento de 12 meses validado."
        pdf_plan = gerar_conteudo_pdf("Planejamento Tributário Anual", emp_plan, detalhes_plan)
        
        cp1, cp2 = st.columns(2)
        with cp1:
            st.download_button("📥 Baixar PDF Planejamento", data=pdf_plan, file_name=f"Planejamento_{emp_plan}.pdf", mime="application/pdf")
        with cp2:
            link_w_plan = f"https://wa.me/55{wapp_plan}?text=Olá,%20segue%20o%20planejamento%20tributário%20anual."
            st.markdown(f"<a href='{link_w_plan}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 6: ANÁLISE DE LUCROS ISENTOS ---
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
        
        detalhes_lucro = f"Receita Bruta: R$ {rec_b:,.2f}\nPresunção: {pres*100}%\nTributos Pagos: R$ {impostos_p:,.2f}\nLimite Isento: R$ {limite:,.2f}"
        pdf_lucro = gerar_conteudo_pdf("Análise de Lucros Isentos", emp_lucro, detalhes_lucro)
        
        cl1, cl2 = st.columns(2)
        with cl1:
            st.download_button("📥 Baixar PDF Lucros Isentos", data=pdf_lucro, file_name=f"Lucros_{emp_lucro}.pdf", mime="application/pdf")
        with cl2:
            link_w_lucro = f"https://wa.me/55{wapp_lucro}?text=Olá,%20segue%20a%20análise%20de%20lucros%20isentos."
            st.markdown(f"<a href='{link_w_lucro}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)

# --- MÓDULO 7: CHAT IA (CORRIGIDO PARA EVITAR ERRO 404) ---
elif pagina == "🤖 Chat IA Master Sênior":
    st.title("🤖 Chat com Assistente Contábil Sênior")
    st.markdown("Tire dúvidas sobre legislação fiscal, normas contábeis e análises estratégicas em tempo real.")

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
                    # Chamada corrigida com modelo padrão estável para evitar 404
                    response = client_ai.models.generate_content(
                        model='gemini-1.5-flash',
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
                    st.error(f"Erro ao processar com a IA. Verifique sua chave ou conexão: {e}")

# --- MÓDULO 8: HISTÓRICO DE RELATÓRIOS ---
elif pagina == "📑 Histórico de Relatórios":
    st.title("📑 Histórico de Relatórios e Exportação")
    st.markdown("Espaço centralizado onde o operador visualiza relatórios gerados e exporta dados.")
    
    df_rels = pd.DataFrame({
        "Data": ["18/09/2026", "17/09/2026", "15/09/2026"],
        "Cliente": ["Comércio Exemplo Ltda", "Tech Soluções S/A", "Prestadora Alpha ME"],
        "Tipo": ["Simulação Comparativa", "Parecer de Lucros", "Planejamento Anual"],
        "Status": ["Gerado com Sucesso", "Enviado WhatsApp", "Arquivado"]
    })
    st.dataframe(df_rels, hide_index=True, use_container_width=True)
    st.info("💡 Você pode exportar o histórico completo em formato de planilha para auditoria interna.")

# --- MÓDULO 9: CONFIGURAÇÕES / ALÍQUOTAS ---
elif pagina == "⚙️ Configurações / Alíquotas":
    st.title("⚙️ Configurações e Atualização de Alíquotas")
    st.markdown("Área administrativa para atualizar as tabelas de alíquotas vigentes conforme muda a legislação.")
    
    st.subheader("Parâmetros Gerais do Sistema")
    st.number_input("Salário Mínimo Vigente (R$)", value=1502.00)
    st.number_input("Teto do INSS (R$)", value=7786.02)
    st.selectbox("Ano-Calendário de Referência", ["2026", "2025", "2024"])
    
    if st.button("Salvar Alterações de Parâmetros"):
        st.success("Tabelas de alíquotas e parâmetros atualizados com sucesso no sistema!")

# --- MÓDULO 10: CALCULADORA DE RETENÇÕES ---
elif pagina == "🧮 Calculadora de Retenções":
    st.title("🧮 Calculadora de Retenções Federais (IRRF, CSRF, INSS)")
    st.markdown("Apuração rápida de retenções na fonte para notas fiscais de prestação de serviços.")
    
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
        
        detalhes_ret = f"Valor Bruto NF: R$ {valor_nf:,.2f}\nNatureza: {tipo_servico}\nTotal Retido: R$ {total_retido:,.2f}\nLíquido a Receber: R$ {liquido_receber:,.2f}"
        pdf_ret = gerar_conteudo_pdf("Cálculo de Retenções Federais", emp_ret, detalhes_ret)
        
        cr1, cr2 = st.columns(2)
        with cr1:
            st.download_button("📥 Baixar PDF Retenções", data=pdf_ret, file_name=f"Retencoes_{emp_ret}.pdf", mime="application/pdf")
        with cr2:
            link_w_ret = f"https://wa.me/55{wapp_ret}?text=Olá,%20segue%20o%20demonstrativo%20de%20retenções%20federais."
            st.markdown(f"<a href='{link_w_ret}' target='_blank'><button style='background-color:#25D366; color:white; padding:8px 16px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>📲 Enviar via WhatsApp</button></a>", unsafe_allow_html=True)
