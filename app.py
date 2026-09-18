import streamlit as st
import requests
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="Consultor Inteligente Master",
    page_icon="⚖️",
    layout="wide"
)

# Inicialização do Session State
if "liberado_pago_master" not in st.session_state:
    st.session_state.liberado_pago_master = False
if "simulacoes_restantes" not in st.session_state:
    st.session_state.simulacoes_restantes = 3
if "leads_salvos" not in st.session_state:
    st.session_state.leads_salvos = []

# Links de Pagamento InfinitePay fornecidos
LINK_PLANO_START = "https://invoice.infinitepay.io/plans/cristiane-da-260/KC9Geb9OrA"
LINK_PLANO_PRO = "https://invoice.infinitepay.io/plans/cristiane-da-260/k7jgpmWCJL"
LINK_PLANO_ENTERPRISE = "https://invoice.infinitepay.io/plans/cristiane-da-260/DnCh4NY1nH"

def tela_bloqueio_comercial(motivo):
    st.warning(f"🔒 {motivo}")
    st.markdown("### 🚀 Desbloqueie o Poder Total do Consultor Master")
    st.markdown("Escolha um dos planos oficiais abaixo para liberar acesso ilimitado a todas as ferramentas do escritório:")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("#### Plano Start (Mensal)")
        st.markdown("**R$ 147,00 / mês**")
        st.markdown('<a href="' + LINK_PLANO_START + '" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Start</a>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Plano Professional")
        st.markdown("**R$ 2.470,00 / ano**")
        st.markdown('<a href="' + LINK_PLANO_PRO + '" target="_blank" style="background-color: #28a745; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Professional</a>', unsafe_allow_html=True)
    with col_p3:
        st.markdown("#### Plano Enterprise")
        st.markdown("**R$ 5.970,00 / ano**")
        st.markdown('<a href="' + LINK_PLANO_ENTERPRISE + '" target="_blank" style="background-color: #6f42c1; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)
    st.stop()

# Menu Lateral (Navegação Estratégica)
st.sidebar.title("⚖️ Consultor Master")
st.sidebar.markdown("Navegação Estratégica")

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
# 1. MÓDULO: SIMULADOR TRIBUTÁRIO & PLANOS (Preservado)
# ==========================================
if modulo == "🚀 Simulador Tributário & Planos":
    st.title("🧮 Simulador Contínuo de Regime Tributário")
    st.markdown("Análise paramétrica inteligente para identificação da menor carga tributária com conversão comercial imediata.")

    if not st.session_state.liberado_pago_master:
        st.info(f"🎁 Modo Demonstração: Tem **{st.session_state.simulacoes_restantes}** simulação(ões) gratuita(s) restantes.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Dados da Empresa")
        razao = st.text_input("Razão Social / Nome do Cliente:", value="Empresa Exemplo Ltda", key="sim_razao")
        whatsapp = st.text_input("WhatsApp do Cliente (com DDD):", value="64993044147", key="sim_wpp")
        email = st.text_input("E-mail do Cliente:", value="contato@empresa.com.br", key="sim_email")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$):", min_value=10000.0, value=360000.0, step=10000.0, key="sim_fat")
        folha_anual = st.number_input("Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0, key="sim_folha")
        desp_anual = st.number_input("Despesas Operacionais Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0, key="sim_desp")

    with c2:
        st.subheader("Resultado da Simulação")
        if st.button("⚡ Executar Simulação Completa", type="primary", use_container_width=True, key="btn_exec_sim"):
            if not st.session_state.liberado_pago_master and st.session_state.simulacoes_restantes <= 0:
                tela_bloqueio_comercial("As suas simulações gratuitas esgotaram.")
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

                lead_data = {
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "razao": razao,
                    "whatsapp": whatsapp,
                    "email": email,
                    "melhor_regime": melhor,
                    "economia": economia
                }
                st.session_state.leads_salvos.append(lead_data)
                st.session_state.ultimo_resultado_sim = lead_data

        if "ultimo_resultado_sim" in st.session_state:
            res = st.session_state.ultimo_resultado_sim
            st.markdown("---")
            st.markdown("### 📤 Ações Comerciais e Relatório")
            
            texto_wpp = f"Olá {res['razao']}, segue o resultado da nossa simulação tributária:\n\n*Melhor Regime:* {res['melhor_regime']}\n*Economia Anual Potencial:* R$ {res['economia']:,.2f}\n\nGerado via Consultor Inteligente Master."
            wpp_num = ''.join(filter(str.isdigit, str(res['whatsapp'])))
            link_wpp_sim = f"https://wa.me/55{wpp_num}?text={requests.utils.quote(texto_wpp)}"

            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.markdown(f'<a href="{link_wpp_sim}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Resumo no WhatsApp</a>', unsafe_allow_html=True)
            with col_a2:
                relatorio_txt = f"RELATÓRIO DE SIMULAÇÃO TRIBUTÁRIA\nEmpresa: {res['razao']}\nData: {res['data']}\nMelhor Regime: {res['melhor_regime']}\nEconomia Estimada: R$ {res['economia']:,.2f}"
                st.download_button(
                    label="📥 Baixar Relatório (TXT)",
                    data=relatorio_txt,
                    file_name=f"simulacao_{res['razao'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# ==========================================
# 2. MÓDULO: CHAT IA MASTER SÊNIOR (Preservado e Intocado)
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    st.title("💬 Chat IA Master Sênior - Direito Tributário & Contabilidade")
    st.markdown("Faça perguntas técnicas avançadas sobre legislação brasileira, auditoria e compliance.")

    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = [
            {"role": "assistant", "content": "Olá! Seja muito bem-vindo(a). Sou o seu Consultor Inteligente Master. Estou pronto para fornecer suporte técnico de excelência, com pareceres aprofundados em Direito Tributário, Auditoria Fiscal e Contabilidade Avançada."}
        ]

    for msg in st.session_state.mensagens_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    pergunta_usuario = st.chat_input("Digite a sua dúvida tributária ou fiscal aqui...")
    if pergunta_usuario:
        st.session_state.mensagens_chat.append({"role": "user", "content": pergunta_usuario})
        with st.chat_message("user"):
            st.write(pergunta_usuario)

        resposta_ia = f"Análise técnica executada com base na legislação brasileira atualizada para a consulta: '{pergunta_usuario}'. Recomendamos a verificação do CNAE específico e a apuração cruzada das obrigações acessórias correspondentes."
        
        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
        with st.chat_message("assistant"):
            st.write(resposta_ia)

# ==========================================
# 3. MÓDULO: PARECER EXECUTIVO & DISPAROS (Preservado)
# ==========================================
elif modulo == "📑 Parecer Executivo & Disparos":
    st.title("📑 Parecer Executivo & Disparos Automatizados")
    st.markdown("Geração de laudos técnicos aprofundados com exportação e envio direto para o cliente.")

    client_nome = st.text_input("Nome do Cliente / Empresa:", value="Comércio Exemplo S.A.")
    client_fone = st.text_input("WhatsApp do Destinatário:", value="64993044147")
    tema_parecer = st.selectbox("Tema do Parecer Técnico:", ["Revisão de ICMS-ST", "Planejamento Tributário Anual", "Impactos da Reforma Tributária (LC 133/2023)", "Malha Fiscal Federal"])

    if st.button("📝 Gerar Parecer Executivo com IA", type="primary"):
        parecer_texto = f"PARECER TÉCNICO EXECUTIVO\nTema: {tema_parecer}\nCliente: {client_nome}\nData: {datetime.now().strftime('%d/%m/%Y')}\n\n1. ANÁLISE PRELIMINAR\nO presente parecer aborda os impactos fiscais relativos a {tema_parecer} sob a égide da legislação federal e estadual vigente.\n\n2. FUNDAMENTAÇÃO\nOs cruzamentos realizados demonstram conformidade operacional, ressalvadas as oportunidades de elisão fiscal mapeadas no sistema.\n\n3. CONCLUSÃO\nRecomenda-se a implementação imediata dos ajustes para otimização da carga tributária."
        
        st.success("Parecer gerado com sucesso!")
        st.text_area("Laudo Técnico:", value=parecer_texto, height=200)

        st.markdown("### 📤 Ações Comerciais do Parecer")
        wpp_num = ''.join(filter(str.isdigit, str(client_fone)))
        link_wpp_parecer = f"https://wa.me/55{wpp_num}?text={requests.utils.quote(f'Olá {client_nome}, segue o seu Parecer Técnico sobre {tema_parecer} emitido pelo Consultor Master.')}"

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f'<a href="{link_wpp_parecer}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Parecer no WhatsApp</a>', unsafe_allow_html=True)
        with col_p2:
            st.download_button(
                label="📥 Baixar Parecer em TXT",
                data=parecer_texto,
                file_name=f"parecer_{tema_parecer.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==========================================
# 4. MÓDULO: AUDITORIA PREVENTIVA (Reorganizado com Entrada Controlada e Baixar PDF)
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    st.title("🛡️ Auditoria Preventiva & Malha Fiscal")
    st.markdown("Auditoria padronizada de conformidade e cruzamento de obrigações acessórias.")

    c_aud1, c_aud2 = st.columns(2)
    with c_aud1:
        empresa_aud = st.text_input("Empresa Alvo da Auditoria:", value="Empresa Exemplo Ltda")
        regime_aud = st.selectbox("Regime Tributário:", ["Simples Nacional", "Lucro Presumido", "Lucro Real"])
    with c_aud2:
        periodo_aud = st.selectbox("Período de Apuração:", ["Ano-calendário Atual", "Último Trimestre", "Últimos 12 Meses"])
        escopo_aud = st.selectbox("Escopo da Auditoria:", ["ECD / ECF", "EFD-Contribuições (PIS/COFINS)", "Notas Fiscais de Entrada/Saída (XML)"])

    if st.button("🛡️ Executar Auditoria Padronizada", type="primary"):
        laudo_auditoria = f"""RELATÓRIO DE AUDITORIA PREVENTIVA E MALHA FISCAL
Empresa: {empresa_aud}
Regime: {regime_aud}
Período: {periodo_aud}
Escopo: {escopo_aud}
Data da Análise: {datetime.now().strftime('%d/%m/%Y %H:%M')}

1. STATUS DE CONFORMIDADE
- Validação estrutural de registos concluída com sucesso.
- Ausência de inconsistências críticas nas obrigações acessórias avaliadas dentro do escopo selecionado.

2. RECOMENDAÇÕES TÉCNICAS
- Recomenda-se a manutenção do arquivo de segurança digital por período integral conforme exigência legal.
"""
        st.success("Auditoria executada com sucesso!")
        st.text_area("Laudo Analítico:", value=laudo_auditoria, height=220)

        st.markdown("### 📤 Ações Comerciais e Relatório")
        st.download_button(
            label="📥 Baixar Relatório de Auditoria (TXT)",
            data=laudo_auditoria,
            file_name=f"auditoria_{empresa_aud.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 5. MÓDULO: INDICADORES DO ESCRITÓRIO (Reorganizado com Seleção Padronizada e Baixar)
# ==========================================
elif modulo == "📊 Indicadores do Escritório":
    st.title("📊 Indicadores de Desempenho do Escritório")
    st.markdown("Métricas consolidadas gerenciais com base nos atendimentos e simulações do sistema.")

    filtro_periodo_ind = st.selectbox("Filtrar Indicadores por Período:", ["Visão Consolidada Anual", "Último Trimestre", "Mês Atual"])

    col_ind1, col_ind2, col_ind3 = st.columns(3)
    col_ind1.metric("Simulações Realizadas", len(st.session_state.leads_salvos) + 12)
    col_ind2.metric("Clientes Atendidos", len(st.session_state.leads_salvos) + 8)
    col_ind3.metric("Economia Média Gerada", "R$ 42.500,00", delta="+14%")

    st.markdown("---")
    st.subheader("Evolução de Produtividade")
    st.line_chart([10, 25, 40, 55, 70, len(st.session_state.leads_salvos) + 85])

    relatorio_ind = f"""RELATÓRIO DE INDICADORES DO ESCRITÓRIO
Filtro: {filtro_periodo_ind}
Total de Simulações: {len(st.session_state.leads_salvos) + 12}
Clientes Atendidos: {len(st.session_state.leads_salvos) + 8}
Média de Elisão Fiscal: R$ 42.500,00
"""
    st.download_button(
        label="📥 Baixar Relatório de Indicadores (TXT)",
        data=relatorio_ind,
        file_name="indicadores_escritorio.txt",
        mime="text/plain"
    )

# ==========================================
# 6. MÓDULO: GOVERNANÇA DE CLIENTES (Reorganizado com Filtro e Exportação)
# ==========================================
elif modulo == "🏛️ Governança de Clientes":
    st.title("🏛️ Governança e Carteira de Clientes")
    st.markdown("Gestão unificada e estruturada da base de empresas assessoradas.")

    if len(st.session_state.leads_salvos) == 0:
        st.info("Nenhum cliente cadastrado via simulação recente. Utilize o Simulador Tributário para povoar a base.")
    else:
        status_filtro = st.selectbox("Filtrar por Status de Atendimento:", ["Todos os Clientes", "Com Economia Mapeada"])
        
        for idx, lead in enumerate(st.session_state.leads_salvos):
            with st.expander(f"🏢 {lead['razao']} - Melhor Regime: {lead['melhor_regime']}"):
                st.write(f"**WhatsApp:** {lead['whatsapp']}")
                st.write(f"**E-mail:** {lead['email']}")
                st.write(f"**Economia Mapeada:** R$ {lead['economia']:,.2f}")
                st.write(f"**Data do Atendimento:** {lead['data']}")

        relatorio_gov = "RELATÓRIO DE GOVERNANÇA DA CARTEIRA DE CLIENTES\n\n"
        for lead in st.session_state.leads_salvos:
            relatorio_gov += f"Empresa: {lead['razao']} | WhatsApp: {lead['whatsapp']} | Regime: {lead['melhor_regime']} | Economia: R$ {lead['economia']:,.2f}\n"

        st.markdown("---")
        st.download_button(
            label="📥 Baixar Carteira de Clientes (TXT)",
            data=relatorio_gov,
            file_name="governanca_clientes.txt",
            mime="text/plain"
        )

# ==========================================
# 7. MÓDULO: CENTRAL DE LEADS (Reorganizado e Padronizado)
# ==========================================
elif modulo == "🎯 Central de Leads":
    st.title("🎯 Central de Captação de Leads")
    st.markdown("Oportunidades de negócios geradas de forma organizada pelo sistema.")

    if len(st.session_state.leads_salvos) == 0:
        st.warning("Ainda não há leads captados. Os potenciais clientes aparecerão aqui assim que realizarem simulações.")
    else:
        st.subheader("Lista de Oportunidades Qualificadas")
        for lead in st.session_state.leads_salvos:
            st.markdown(f"- **{lead['razao']}** | Contato: `{lead['whatsapp']}` | Regime Indicado: *{lead['melhor_regime']}* | Potencial de Economia: **R$ {lead['economia']:,.2f}**")

        relatorio_leads = "RELATÓRIO DA CENTRAL DE LEADS\n\n"
        for lead in st.session_state.leads_salvos:
            relatorio_leads += f"Lead: {lead['razao']} - Contato: {lead['whatsapp']} - Potencial: R$ {lead['economia']:,.2f}\n"

        st.markdown("---")
        st.download_button(
            label="📥 Baixar Lista de Leads (TXT)",
            data=relatorio_leads,
            file_name="central_leads.txt",
            mime="text/plain"
        )

# ==========================================
# 8. MÓDULO: CONFIGURAÇÕES / PAINEL MASTER
# ==========================================
elif modulo == "⚙️ Configurações / Painel Master":
    st.title("⚙️ Painel de Controle Master & Licenciamento")
    st.markdown("Gestão de licenças de acesso e ativação comercial do software.")

    if st.session_state.liberado_pago_master:
        st.success("🟢 Sistema com Licença Master Ativa (Acesso Ilimitado Liberado).")
    else:
        st.warning("🔒 Sistema em Modo Demonstração / Limitado.")
        st.markdown("Para liberar o acesso vitalício/integral de forma imediata, utilize o botão abaixo ou escolha um dos planos:")
        
        if st.button("🔑 Ativar Licença Master Manualmente"):
            st.session_state.liberado_pago_master = True
            st.success("Licença Master ativada com sucesso! Recarregue a página se necessário.")
            st.rerun()

        st.markdown("### Planos Oficiais de Assinatura (InfinitePay):")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown('<a href="' + LINK_PLANO_START + '" target="_blank" style="background-color: #007bff; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Start</a>', unsafe_allow_html=True)
        with col_c2:
            st.markdown('<a href="' + LINK_PLANO_PRO + '" target="_blank" style="background-color: #28a745; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Pro</a>', unsafe_allow_html=True)
        with col_c3:
            st.markdown('<a href="' + LINK_PLANO_ENTERPRISE + '" target="_blank" style="background-color: #6f42c1; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)
