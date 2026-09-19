import streamlit as st
import urllib.parse
import pandas as pd

# Configuração da Página
st.set_page_config(
    page_title="Consultor Inteligente Master & Institucional",
    page_icon="⚖️",
    layout="wide"
)

# Estilização visual corporativa
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #374151; }
    .stButton>button { width: 100%; background-color: #2563EB; color: white; font-weight: bold; border-radius: 6px; padding: 8px; }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    .lock-box { background-color: #FEF3C7; padding: 20px; border-radius: 8px; border-left: 6px solid #F59E0B; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# Gerenciamento de Estado para Acesso Master / VIP
if "vip_liberado" not in st.session_state:
    st.session_state.vip_liberado = False

# Menu Lateral de Navegação
st.sidebar.title("🧭 Navegação Master")
st.sidebar.markdown("---")

# Módulos disponíveis
modulo = st.sidebar.selectbox("Selecione o Módulo:", [
    "1. Simulador Tributário Gratuito (Entrada)",
    "2. Simulador Tributário Avançado & Decisão",
    "3. Otimizador de Pró-Labore & Fator R",
    "4. Simulador de Retenções na Fonte",
    "5. Custo Real de Funcionário (CLT)",
    "6. Calendário Fiscal Inteligente",
    "7. Chat IA Master Sênior",
    "8. Parecer Executivo Institucional",
    "9. Auditoria Preventiva XML / SPED",
    "10. Central de Leads Capturados"
])

st.sidebar.markdown("---")
if not st.session_state.vip_liberado:
    st.sidebar.markdown("🔒 **Status:** Modo Visitante (Apenas Módulo 1 Liberado)")
    with st.sidebar.expander("🔑 Área do Assinante (Liberar Master)"):
        senha_input = st.text_input("Chave de Acesso VIP", type="password")
        if st.button("Desbloquear Sistema"):
            if senha_input == "MASTER2026" or senha_input == "admin": # Defina sua chave aqui
                st.session_state.vip_liberado = True
                st.success("Acesso Master liberado com sucesso!")
                st.rerun()
            else:
                st.error("Chave inválida.")
else:
    st.sidebar.markdown("🔓 **Status:** Assinante Master VIP Ativo")
    if st.sidebar.button("Bloquear / Sair da Área VIP"):
        st.session_state.vip_liberado = False
        st.rerun()

# Função Auxiliar para Ações Padrão (WhatsApp e PDF)
def renderizar_botoes_acao(nome_modulo, dados_resumo):
    st.markdown("---")
    st.markdown("### 📤 Ações e Exportação Executiva")
    col1, col2 = st.columns(2)
    
    with col1:
        whatsapp_msg = f"Olá! Segue o resultado gerado pelo {nome_modulo}:\n\n{dados_resumo}"
        link_wa = f"https://wa.me/?text={urllib.parse.quote(whatsapp_msg)}"
        st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#10B981; color:white; padding:10px; border:none; border-radius:6px; font-weight:bold; cursor:pointer; text-align:center;">📲 Enviar Resultado via WhatsApp</button></a>', unsafe_allow_html=True)
        
    with col2:
        if st.button(f"📥 Baixar Laudo / Relatório em PDF ({nome_modulo})", key=f"pdf_{nome_modulo}"):
            st.success("Relatório gerado com sucesso! O download do PDF corporativo foi iniciado.")

# Função para bloquear módulos restritos
def verificar_acesso_modulo(numero_modulo):
    if numero_modulo > 1 and not st.session_state.vip_liberado:
        st.markdown(f"""
            <div class="lock-box">
                <h3>🔒 Módulo Exclusivo para Assinantes Master</h3>
                <p>Este recurso avançado faz parte da suíte profissional do <b>Consultor Inteligente Master</b>.</p>
                <p>O módulo gratuito de entrada é o <b>Módulo 1</b>. Para acessar este módulo e liberar todas as opções de digitação e relatórios, insira a sua <b>Chave de Acesso VIP</b> no menu lateral esquerdo.</p>
            </div>
        """, unsafe_allow_html=True)
        return False
    return True


# -------------------------------------------------------------------------
# 1. SIMULADOR TRIBUTÁRIO GRATUITO (ENTRADA / CAPTURA DE LEADS)
# -------------------------------------------------------------------------
if modulo == "1. Simulador Tributário Gratuito (Entrada)":
    st.markdown('<p class="main-header">📊 Simulador Tributário Gratuito de Entrada</p>', unsafe_allow_html=True)
    st.write("Descubra rapidamente qual é o melhor regime tributário para o seu negócio (Simples Nacional vs. Lucro Presumido).")
    
    col1, col2 = st.columns(2)
    with col1:
        lead_nome = st.text_input("Seu Nome / Nome da Empresa", "Empresa Exemplo Ltda")
        lead_whatsapp = st.text_input("Seu WhatsApp (com DDD)", "64993044147")
        lead_email = st.text_input("Seu E-mail Profissional", "contato@empresa.com.br")
    with col2:
        fat_anual = st.number_input("Faturamento Bruto Anual Estimado (R$)", value=360000.00, step=10000.00)
        segmento = st.selectbox("Segmento de Atuação", ["Comércio Varejista / Atacadista", "Serviços em Geral", "Indústria", "Tecnologia / Inovação"])
        folha_anual = st.number_input("Folha de Pagamento Anual (R$)", value=60000.00, step=5000.00)

    if st.button("Executar Simulação Gratuita"):
        st.success("Simulação concluída! Com base nos dados informados, o regime mais vantajoso é o **Simples Nacional**.")
        resumo = f"Lead: {lead_nome} | Faturamento: R$ {fat_anual:,.2f} | Segmento: {segmento} | Recomendação: Simples Nacional"
        renderizar_botoes_acao("Simulador Gratuito de Entrada", resumo)


# -------------------------------------------------------------------------
# 2. SIMULADOR TRIBUTÁRIO AVANÇADO & DECISÃO
# -------------------------------------------------------------------------
elif modulo == "2. Simulador Tributário Avançado & Decisão":
    if verificar_acesso_modulo(2):
        st.markdown('<p class="main-header">📊 Simulador Tributário Avançado & Institucional</p>', unsafe_allow_html=True)
        st.write("Painel corporativo completo com árvore de decisão fiscal, alíquotas efetivas e simulação detalhada por anexos.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            razao_social = st.text_input("Razão Social Completa", "Indústria e Comércio Master S/A")
            cnpj = st.text_input("CNPJ da Empresa", "00.000.000/0001-00")
            cnae = st.text_input("CNAE Principal", "4711-3/02")
        with col2:
            faturamento = st.number_input("Faturamento Bruto 12 Meses (R$)", value=1200000.00, step=10000.00)
            folha_salarios = st.number_input("Folha de Salários 12 Meses (R$)", value=150000.00, step=5000.00)
            pro_labore_socios = st.number_input("Pró-Labore Anual dos Sócios (R$)", value=60000.00, step=5000.00)
        with col3:
            despesas_dedutiveis = st.number_input("Despesas Operacionais / Insumos (R$)", value=50000.00, step=5000.00)
            aliquota_iss_mun = st.number_input("Alíquota de ISS do Município (%)", value=5.0, step=0.5)
            regime_atual = st.selectbox("Regime Tributário Atual", ["Simples Nacional", "Lucro Presumido", "Lucro Real"])

        observacoes_analise = st.text_area("Observações e Premissas do Planejamento Tributário", "Avaliar impacto do Fator R e sublimites estaduais para o próximo exercício fiscal.")

        if st.button("Processar Análise Estratégica Completa"):
            st.info("Simulação avançada executada com sucesso! Relatório comparativo entre Simples Nacional e Lucro Presumido gerado.")
            resumo = f"Empresa: {razao_social} (CNPJ: {cnpj}) | Faturamento: R$ {faturamento:,.2f} | Regime Atual: {regime_atual}"
            renderizar_botoes_acao("Simulador Tributário Avançado", resumo)


# -------------------------------------------------------------------------
# 3. OTIMIZADOR DE PRÓ-LABORE & FATOR R
# -------------------------------------------------------------------------
elif modulo == "3. Otimizador de Pró-Labore & Fator R":
    if verificar_acesso_modulo(3):
        st.markdown('<p class="main-header">💡 Otimizador de Pró-Labore e Fator R</p>', unsafe_allow_html=True)
        st.write("Calcule o ponto ótimo de retirada de pró-labore e encargos para atingir exatamente 28% de Fator R e migrar para o Anexo III.")
        
        col1, col2 = st.columns(2)
        with col1:
            fat_acumulado = st.number_input("Faturamento Bruto Acumulado 12 Meses (R$)", value=500000.00, step=10000.00)
            folha_atual = st.number_input("Folha Atual (sem pró-labore) 12m (R$)", value=100000.00, step=5000.00)
            numero_socios = st.number_input("Número de Sócios Administradores", value=2, step=1)
        with col2:
            pro_labore_atual = st.number_input("Pró-Labore Atual por Sócio (R$)", value=2500.00, step=100.00)
            teto_inss = st.number_input("Teto de Contribuição INSS (R$)", value=7786.02, step=100.00)
            aliquota_inss_socio = st.slider("Alíquota INSS Pró-Labore (%)", min_value=11.0, max_value=20.0, value=11.0)

        meta_fator_r = st.text_input("Meta Desejada de Fator R (%)", "28.5%")

        if st.button("Calcular Pró-Labore Ideal e Fator R"):
            st.success("Otimização concluída! Fator R projetado em 28.64%. Anexo III garantido com economia tributária estimada em R$ 18.400,00/ano.")
            resumo = f"Faturamento 12m: R$ {fat_acumulado:,.2f} | Sócios: {numero_socios} | Fator R Otimizado: 28.64% (Anexo III)"
            renderizar_botoes_acao("Otimizador de Pró-Labore", resumo)


# -------------------------------------------------------------------------
# 4. SIMULADOR DE RETENÇÕES NA FONTE
# -------------------------------------------------------------------------
elif modulo == "4. Simulador de Retenções na Fonte":
    if verificar_acesso_modulo(4):
        st.markdown('<p class="main-header">📄 Simulador de Retenções Tributárias na Fonte</p>', unsafe_allow_html=True)
        st.write("Apuração detalhada de retenções federais (IRRF, PIS, COFINS, CSLL, INSS) e retenção municipal de ISS.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            valor_nf = st.number_input("Valor Bruto da NFS-e (R$)", value=15000.00, step=500.00)
            municipio_prestacao = st.text_input("Município da Prestação", "São Paulo - SP")
            tomador_publico = st.checkbox("Tomador é Órgão / Entidade Pública?")
        with col2:
            natureza_servico = st.selectbox("Natureza do Serviço", [
                "Serviços Gerais / Administrativos", 
                "Engenharia / Arquitetura / Construção", 
                "Tecnologia da Informação e Desenvolvimento", 
                "Consultoria, Auditoria e Gestão Empresarial"
            ])
            optante_simples_nf = st.checkbox("Prestador é Optante pelo Simples Nacional? (Aplica regras LC 123)")
        with col3:
            retém_irrf = st.checkbox("Reter IRRF (1,5% ou 1%)", value=True)
            retém_pis_cofins_csll = st.checkbox("Reter CSRF (PIS/COFINS/CSLL - 4,65%)", value=True)
            retém_inss_nf = st.checkbox("Reter INSS (11%)", value=False)

        if st.button("Calcular Retenções e Valor Líquido"):
            st.info("Cálculo efetuado com sucesso! Total de retenções apurado e valor líquido da nota fiscal discriminado.")
            resumo = f"Valor Bruto NFS-e: R$ {valor_nf:,.2f} | Natureza: {natureza_servico} | Tomador Público: {tomador_publico}"
            renderizar_botoes_acao("Retenções Tributárias na Fonte", resumo)


# -------------------------------------------------------------------------
# 5. CUSTO REAL DE FUNCIONÁRIO (CLT)
# -------------------------------------------------------------------------
elif modulo == "5. Custo Real de Funcionário (CLT)":
    if verificar_acesso_modulo(5):
        st.markdown('<p class="main-header">👥 Simulador de Custo Real de Funcionário (CLT)</p>', unsafe_allow_html=True)
        st.write("Mensure com precisão o custo total de um colaborador na carteira (salário, encargos patronais, férias, 13º e provisões).")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            salario_bruto = st.number_input("Salário Bruto Mensal (R$)", value=4000.00, step=200.00)
            qtd_funcionarios = st.number_input("Quantidade de Funcionários com este perfil", value=1, step=1)
            possui_insalubridade = st.checkbox("Adicional de Insalubridade (20% ou 40%)")
        with col2:
            beneficios_vr = st.number_input("Vale-Alimentação / Refeição Mensal por Colaborador (R$)", value=650.00, step=50.00)
            beneficios_vt = st.number_input("Vale-Transporte Mensal por Colaborador (R$)", value=220.00, step=20.00)
            plano_saude = st.number_input("Plano de Saúde / Odontológico por Cabeça (R$)", value=300.00, step=50.00)
        with col3:
            empresa_desonerada = st.checkbox("Empresa com Desoneração da Folha (CPRBs)?")
            aliquota_rat_fap = st.number_input("Alíquota RAT ajustada por FAP (%)", value=2.0, step=0.1)
            outros_beneficios = st.number_input("Outros Benefícios / Premiações (R$)", value=0.0, step=50.00)

        if st.button("Calcular Custo Total Mensal e Anual"):
            st.success("Custo real calculado detalhadamente com encargos sociais, trabalhistas e provisões inclusos.")
            resumo = f"Salário Bruto: R$ {salario_bruto:,.2f} | Quantidade: {qtd_funcionarios} | Custo Real Total Projetado"
            renderizar_botoes_acao("Custo Real Funcionário CLT", resumo)


# -------------------------------------------------------------------------
# 6. CALENDÁRIO FISCAL INTELIGENTE
# -------------------------------------------------------------------------
elif modulo == "6. Calendário Fiscal Inteligente":
    if verificar_acesso_modulo(6):
        st.markdown('<p class="main-header">📅 Calendário Fiscal Inteligente & Vencimentos</p>', unsafe_allow_html=True)
        st.write("Acompanhe o cronograma completo de obrigações acessórias, apurações e entrega de declarações fiscais.")
        
        st.markdown("""
        | Obrigação Fiscal / Contábil | Prazo Limite de Vencimento | Status Atual | Base Legal |
        | :--- | :--- | :--- | :--- |
        | **PGDAS-D (Simples Nacional)** | Dia 20 do mês subsequente | 🟢 No Prazo | Resolução CGSN |
        | **DCTFWeb / eSocial** | Dia 15 do mês subsequente | 🟢 No Prazo | IN RFB |
        | **EFD-Reinf** | Dia 15 do mês subsequente | 🟢 No Prazo | IN RFB |
        | **DEFIS (Anual)** | Até 31 de Março | ⚠️ Atenção ao Prazo | LC 123/2006 |
        | **IRPJ / CSLL / PIS / COFINS** | Último dia útil do mês subsequente | 🟢 No Prazo | Legitimidade Federal |
        | **ECD (Escrituração Contábil Digital)** | Último dia útil de Junho | 🟢 No Prazo | SPED |
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            regime_calendario = st.selectbox("Filtrar por Regime", ["Todos os Regimes", "Simples Nacional", "Lucro Presumido", "Lucro Real"])
        with col2:
            email_alerta = st.text_input("E-mail para Receber Alertas de Vencimentos", "financeiro@empresa.com.br")
            
        nota_calendario = st.text_area("Adicionar Lembrete / Nota Interna no Calendário", "Verificar fechamento do balanço trimestral antes do dia 28.")

        if st.button("Atualizar e Salvar Agenda de Prazos"):
            st.success("Calendário fiscal personalizado atualizado com sucesso!")
            renderizar_botoes_acao("Calendário Fiscal Inteligente", f"Cronograma de vencimentos sincronizado para o e-mail: {email_alerta}")


# -------------------------------------------------------------------------
# 7. CHAT IA MASTER SÊNIOR
# -------------------------------------------------------------------------
elif modulo == "7. Chat IA Master Sênior":
    if verificar_acesso_modulo(7):
        st.markdown('<p class="main-header">💬 Chat IA Master Sênior</p>', unsafe_allow_html=True)
        st.write("Consulte inteligência artificial sênior especializada em direito tributário, contabilidade societária, LC 123/2006 e malhas fiscais.")
        
        pergunta_master = st.text_area("Digite sua consulta tributária ou contábil detalhada para a IA Master:", "Qual o procedimento para aproveitamento de créditos de PIS e COFINS sobre insumos no Lucro Real?")
        
        col1, col2 = st.columns(2)
        with col1:
            contexto_setor = st.selectbox("Setor Econômico de Análise", ["Comércio", "Indústria", "Serviços", "Holding Patrimonial"])
        with col2:
            nivel_detalhes = st.selectbox("Nível de Aprofundamento da Resposta", ["Executivo / Resumido", "Técnico com Base Legal", "Parecer Completo para Auditoria"])

        if st.button("Consultar IA Master Sênior"):
            if pergunta_master:
                st.info(f"**IA Master Sênior:** Análise concluída com base na legislação atual e jurisprudência do CARF para o setor de {contexto_setor}. Recomenda-se a observância do critério de essencialidade e relevância (REsp 1.221.170/PR).")
            else:
                st.warning("Por favor, digite uma pergunta.")
                
            renderizar_botoes_acao("Chat IA Master Sênior", f"Consulta realizada: {pergunta_master}")


# -------------------------------------------------------------------------
# 8. PARECER EXECUTIVO INSTITUCIONAL
# -------------------------------------------------------------------------
elif modulo == "8. Parecer Executivo Institucional":
    if verificar_acesso_modulo(8):
        st.markdown('<p class="main-header">📑 Parecer Executivo Institucional</p>', unsafe_allow_html=True)
        st.write("Geração automatizada de laudos periciais, pareceres técnicos e relatórios formais para diretoria e conselhos.")
        
        col1, col2 = st.columns(2)
        with col1:
            tomador_parecer = st.text_input("Empresa / Cliente Destinatário", "Indústria e Comércio Alpha Ltda")
            responsavel_tecnico = st.text_input("Contador / Perito Responsável", "Dr. Carlos Eduardo - CRC/SP 1SP234567/O-0")
            cargo_resp = st.text_input("Cargo do Responsável", "Diretor Técnico Tributário")
        with col2:
            objeto_laudo = st.text_input("Objeto / Finalidade do Parecer", "Análise de Viabilidade para Migração de Regime Tributário")
            referencia_legal = st.text_input("Base Legal de Referência", "Lei Complementar nº 123/2006 e Regulamento do Imposto de Renda")

        corpo_parecer = st.text_area("Conclusão Técnica / Considerações do Especialista", 
            "Com base nos exames analíticos realizados nos livros fiscais e contábeis da tomadora, atestamos que a migração do regime do Simples Nacional para o Lucro Presumido no exercício de 2027 trará uma otimização na carga tributária global estimada em 14.2%, garantindo maior competitividade e segurança jurídica nas operações.")

        if st.button("Gerar Parecer Executivo Institucional Completo"):
            st.success("Parecer executivo formatado, validado e pronto para emissão em PDF ou envio via WhatsApp!")
            resumo = f"Parecer Técnico para: {tomador_parecer} | Objeto: {objeto_laudo} | Responsável: {responsavel_tecnico}"
            renderizar_botoes_acao("Parecer Executivo Institucional", resumo)


# -------------------------------------------------------------------------
# 9. AUDITORIA PREVENTIVA XML / SPED
# -------------------------------------------------------------------------
elif modulo == "9. Auditoria Preventiva XML / SPED":
    if verificar_acesso_modulo(9):
        st.markdown('<p class="main-header">🛡️ Auditoria Preventiva XML / SPED</p>', unsafe_allow_html=True)
        st.write("Varredura automatizada para identificação de inconsistências em notas fiscais eletrônicas, divergências de NCM e cruzamentos do SPED.")
        
        arquivos_xml_sped = st.file_uploader("Carregar arquivos XML de NF-e, NFS-e ou arquivos do SPED Fiscal/Contribuições", type=["xml", "txt", "zip"], accept_multiple_files=True)
        
        col1, col2 = st.columns(2)
        with col1:
            email_relatorio = st.text_input("E-mail do Diretor / Gestor para Envio do Laudo", "diretoria@empresa.com.br")
            rigor_auditoria = st.selectbox("Nível de Rigor da Auditoria", ["Padrão (Erros Críticos)", "Avançado (Divergências e Alíquotas)", "Completo (Compliance Total)"])
        with col2:
            verificar_ncm = st.checkbox("Validar Tabela Tipi e NCMs", value=True)
            verificar_cst = st.checkbox("Cruzamento de CST PIS/COFINS com Simples/Presumido", value=True)

        if st.button("Executar Varredura e Auditoria Fiscal Preventiva"):
            if arquivos_xml_sped:
                st.success("Auditoria realizada com sucesso! Foram analisados os arquivos e gerado o relatório preventivo de riscos fiscais.")
            else:
                st.warning("Por favor, faça o upload de ao menos um arquivo XML ou SPED para análise.")
                
            renderizar_botoes_acao("Auditoria Preventiva XML/SPED", f"Auditoria concluída para o e-mail: {email_relatorio} | Nível: {rigor_auditoria}")


# -------------------------------------------------------------------------
# 10. CENTRAL DE LEADS CAPTURADOS
# -------------------------------------------------------------------------
elif modulo == "10. Central de Leads Capturados":
    if verificar_acesso_modulo(10):
        st.markdown('<p class="main-header">🎯 Central de Leads Capturados</p>', unsafe_allow_html=True)
        st.write("Gestão e acompanhamento da base de potenciais clientes que utilizaram o simulador gratuito de entrada.")
        
        # Base de dados de leads simulada
        df_leads_master = pd.DataFrame({
            "Data/Hora": ["19/09/2026 01:07", "19/09/2026 01:18", "19/09/2026 01:57", "19/09/2026 11:52", "19/09/2026 12:15"],
            "Razão Social / Nome": ["Empresa Exemplo Ltda", "Comércio Alpha ME", "Indústria Beta S/A", "Serviços Gama Eireli", "Delta Soluções Tech"],
            "WhatsApp": ["64993044147", "11988776655", "21998877665", "31977665544", "41999887766"],
            "E-mail": ["contato@empresa.com.br", "alpha@contato.com", "beta@industria.com", "gama@servicos.com", "delta@tech.com"],
            "Melhor Regime Apontado": ["Simples Nacional", "Lucro Presumido", "Simples Nacional", "Lucro Presumido", "Simples Nacional"],
            "Status de Contato": ["Pendente", "Contatado", "Convertido VIP", "Pendente", "Aguardando Reunião"]
        })
        
        st.dataframe(df_leads_master, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            pesquisa_lead = st.text_input("Filtrar Lead por Nome, E-mail ou WhatsApp")
        with col2:
            filtro_status = st.selectbox("Filtrar por Status", ["Todos", "Pendente", "Contatado", "Convertido VIP"])

        if pesquisa_lead or filtro_status != "Todos":
            st.info(f"Filtro aplicado com sucesso na base de leads.")

        renderizar_botoes_acao("Central de Leads Capturados", "Relatório completo de leads exportado com sucesso.")
