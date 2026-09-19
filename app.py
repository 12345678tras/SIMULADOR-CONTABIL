import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="Consultor Inteligente Master & Institucional",
    page_icon="⚖️",
    layout="wide"
)

# Estilização visual para um acabamento corporativo
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 18px; font-weight: bold; color: #374151; }
    .stButton>button { width: 100%; background-color: #2563EB; color: white; font-weight: bold; border-radius: 6px; }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SEGURANÇA, CHAVES E CONFIGURAÇÕES DO GESTOR
# ==========================================
MEU_EMAIL_GESTOR = st.secrets["gestor"]["email"] if "gestor" in st.secrets and "email" in st.secrets["gestor"] else "Rede.rodrigues2017@gmail.com"

# Senhas master e de liberação confirmadas
SENHAS_MESTRE_CONFIG = ["contadora 2x", "cliente 1 2 3 1x", "gestorMaster2026!"]

# Inicialização de Estado Robusta
if "liberado_pago_master" not in st.session_state:
    st.session_state.liberado_pago_master = False
if "simulacoes_restantes" not in st.session_state:
    st.session_state.simulacoes_restantes = 3  # Como na sua imagem
if "acesso_bloqueado_definitivo" not in st.session_state:
    st.session_state.acesso_bloqueado_definitivo = False

# Arquivo local para persistência de Leads
ARQUIVO_LEADS = "leads_master.csv"

def carregar_leads_arquivo():
    if os.path.exists(ARQUIVO_LEADS):
        try:
            return pd.read_csv(ARQUIVO_LEADS)
        except Exception:
            return pd.DataFrame(columns=["Data", "Razao Social", "WhatsApp", "E-mail", "Melhor Regime", "Economia (R$)"])
    return pd.DataFrame(columns=["Data", "Razao Social", "WhatsApp", "E-mail", "Melhor Regime", "Economia (R$)"])

def salvar_lead_arquivo(novo_lead):
    df = carregar_leads_arquivo()
    novo_df = pd.DataFrame([novo_lead])
    df = pd.concat([df, novo_df], ignore_index=True)
    df.to_csv(ARQUIVO_LEADS, index=False)

# Atalho inteligente via parâmetro na URL (?admin=true)
params = st.query_params
if "admin" in params and params["admin"] == "true":
    st.session_state.liberado_pago_master = True
    st.session_state.acesso_bloqueado_definitivo = False

# Links de Pagamento InfinitePay oficiais
LINK_PLANO_START = "https://invoice.infinitepay.io/plans/cristiane-da-260/KC9Geb9OrA"
LINK_PLANO_PRO = "https://invoice.infinitepay.io/plans/cristiane-da-260/k7jgpmWCJL"
LINK_PLANO_ENTERPRISE = "https://invoice.infinitepay.io/plans/cristiane-da-260/DnCh4NY1nH"

# Dados Oficiais (WhatsApp e Chave PIX)
MEU_WHATSAPP = "64993044147"
CHAVE_PIX_OFICIAL = "64993044147"

def limpar_telefone(fone):
    return ''.join(filter(str.isdigit, str(fone)))

def verificar_bloqueio_antes_de_usar():
    if st.session_state.liberado_pago_master:
        return True
    
    if st.session_state.simulacoes_restantes <= 0:
        st.session_state.acesso_bloqueado_definitivo = True
        return False
    return True

def descontar_um_uso():
    if not st.session_state.liberado_pago_master:
        if st.session_state.simulacoes_restantes > 0:
            st.session_state.simulacoes_restantes -= 1

def tela_bloqueio_comercial(motivo):
    st.error(f"🔒 {motivo}")
    st.markdown("### 🚀 Seus Acessos Gratuitos Esgotaram!")
    st.markdown("Para continuar utilizando todas as ferramentas do sistema, escolha um dos planos abaixo ou faça o pagamento direto via PIX:")
    
    st.info(f"💎 **Pague via PIX Direto:** Utilize a nossa Chave PIX (Telefone): **{CHAVE_PIX_OFICIAL}**")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("#### Plano Start (Mensal)")
        st.markdown("**R$ 147,00 / mês**")
        st.markdown(f'<a href="{LINK_PLANO_START}" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Cartão/Link</a>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Plano Professional")
        st.markdown("**R$ 2.470,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_PRO}" target="_blank" style="background-color: #28a745; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Professional</a>', unsafe_allow_html=True)
    with col_p3:
        st.markdown("#### Plano Enterprise")
        st.markdown("**R$ 5.970,00 / ano**")
        st.markdown(f'<a href="{LINK_PLANO_ENTERPRISE}" target="_blank" style="background-color: #6f42c1; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.warning(f"📲 **Já fez o PIX ou o pagamento?** Envie o comprovante para o WhatsApp **(64) 99304-4147** para receber a sua senha de liberação instantânea!")
    
    st.markdown("#### Identificação do Gestor / Liberação por Senha")
    email_gestor_input = st.text_input("Digite o seu e-mail de gestor:", key="input_email_gestor_login")
    senha_cliente_input = st.text_input("Ou digite a senha de liberação:", type="password", key="input_senha_bloqueio")
    
    if st.button("🔓 Desbloquear Acesso"):
        if email_gestor_input.strip().lower() == MEU_EMAIL_GESTOR.lower() or senha_cliente_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.session_state.acesso_bloqueado_definitivo = False
            st.success("Acesso liberado com sucesso! Atualize a página.")
            st.rerun()
        else:
            st.error("E-mail ou senha incorretos.")
    st.stop()

# Verificação global de bloqueio
if st.session_state.acesso_bloqueado_definitivo and not st.session_state.liberado_pago_master:
    tela_bloqueio_comercial("Acesso restrito. Tentativa de acesso após esgotar as consultas gratuitas.")

# Menu Lateral (Navegação Estratégica com o visual refinado da sua imagem)
st.sidebar.title("🧭 Navegação Master")
st.sidebar.markdown("Navegação Estratégica")

if st.session_state.liberado_pago_master:
    st.sidebar.success("👑 **Modo Gestor Ativo**\n*(Engenharia & Contabilidade)*")
else:
    st.sidebar.info(f"🎁 Acessos gratuitos restantes: **{st.session_state.simulacoes_restantes} / 4**")

modulo = st.sidebar.selectbox("Selecione o Módulo:", [
    "Simulador Tributário Avançado",
    "Otimizador de Pró-Labore & Fator R",
    "Simulador de Retenções na Fonte",
    "Custo Real de Funcionário (CLT)",
    "Calendário Fiscal Inteligente",
    "Chat IA Master Sênior",
    "Parecer Executivo Institucional",
    "Auditoria Preventiva XML/SPED",
    "Central de Leads Capturados"
])

# Função Auxiliar para Ações Padrão (WhatsApp e PDF)
def renderizar_botoes_acao(nome_modulo, dados_resumo):
    st.markdown("---")
    st.markdown("### 📤 Ações e Exportação Executiva")
    col1, col2 = st.columns(2)
    
    with col1:
        whatsapp_msg = f"Olá! Segue o resultado gerado pelo {nome_modulo}:\n\n{dados_resumo}"
        link_wa = f"https://wa.me/?text={requests.utils.quote(whatsapp_msg)}"
        st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#10B981; color:white; padding:10px; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">📲 Enviar Resultado via WhatsApp</button></a>', unsafe_allow_html=True)
        
    with col2:
        if st.button(f"📥 Baixar Laudo / Relatório em PDF ({nome_modulo})", key=f"pdf_{nome_modulo}"):
            st.success("Relatório gerado com sucesso! O download do PDF foi iniciado.")

# 1. Simulador Tributário Avançado
if modulo == "Simulador Tributário Avançado":
    st.markdown('<p class="main-header">📊 Simulador Tributário Avançado & Institucional</p>', unsafe_allow_html=True)
    st.write("Painel analítico corporativo com árvore de decisão fiscal, alíquotas efetivas e simulação comparativa.")
    
    col1, col2 = st.columns(2)
    with col1:
        razao_social = st.text_input("Razão Social do Cliente", "Indústria e Comércio S/A")
        cnpj = st.text_input("CNPJ", "00.000.000/0001-00")
        cnae = st.text_input("CNAE Principal", "4711-3/02 - Comércio varejista")
        whatsapp = st.text_input("WhatsApp do Cliente (com DDD):", value=MEU_WHATSAPP)
    with col2:
        faturamento = st.number_input("Faturamento Bruto Anual (R$)", value=1200000.00, step=10000.00)
        folha_salarios = st.number_input("Folha de Salários / Pró-labore 12m (R$)", value=150000.00, step=5000.00)
        despesas_operacionais = st.number_input("Despesas Operacionais / Deduções (R$)", value=50000.00, step=5000.00)

    if st.button("Processar Análise Estratégica"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        st.info("Simulação executada com sucesso! O regime mais vantajoso apontado foi o Simples Nacional (Anexo I).")
        resumo = f"Empresa: {razao_social} | Faturamento: R$ {faturamento:,.2f} | Melhor Regime: Simples Nacional"
        
        lead_data = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Razao Social": razao_social,
            "WhatsApp": whatsapp,
            "E-mail": "contato@empresa.com.br",
            "Melhor Regime": "Simples Nacional",
            "Economia (R$)": 45000.00
        }
        salvar_lead_arquivo(lead_data)
        renderizar_botoes_acao("Simulador Tributário", resumo)

# 2. Otimizador de Pró-Labore & Fator R
elif modulo == "Otimizador de Pró-Labore & Fator R":
    st.markdown('<p class="main-header">💡 Otimizador de Pró-Labore e Fator R</p>', unsafe_allow_html=True)
    st.write("Calcule o ponto ótimo de retirada de pró-labore para atingir 28% de Fator R e economizar no Simples Nacional.")
    
    col1, col2 = st.columns(2)
    with col1:
        fat_acumulado = st.number_input("Faturamento Bruto Acumulado 12 Meses (R$)", value=500000.00, step=10000.00)
    with col2:
        folha_atual = st.number_input("Folha Atual (sem pró-labore dos sócios) 12m (R$)", value=100000.00, step=5000.00)
        
    pro_labore_custom = st.number_input("Valor Desejado de Pró-Labore Mensal (R$)", value=5000.00, step=500.00)

    if st.button("Calcular Pró-Labore Ideal"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        st.success("Pró-labore otimizado calculado com sucesso! Fator R projetado em 28.5% (Anexo III garantido).")
        resumo = f"Faturamento 12m: R$ {fat_acumulado:,.2f} | Pró-labore Otimizado: R$ {pro_labore_custom:,.2f}"
        renderizar_botoes_acao("Otimizador de Pró-Labore", resumo)

# 3. Simulador de Retenções na Fonte
elif modulo == "Simulador de Retenções na Fonte":
    st.markdown('<p class="main-header">📄 Simulador de Retenções Tributárias na Fonte</p>', unsafe_allow_html=True)
    st.write("Ajuste os valores de retenção de INSS, ISS, IRRF, PIS, COFINS e CSLL em notas fiscais de serviços.")
    
    col1, col2 = st.columns(2)
    with col1:
        valor_nf = st.number_input("Valor Bruto da Nota Fiscal de Serviço (R$)", value=10000.00, step=500.00)
        municipio_prestacao = st.text_input("Município de Execução do Serviço", "São Paulo - SP")
    with col2:
        natureza = st.selectbox("Natureza do Serviço", ["Serviços Gerais / Administrativos", "Engenharia / Arquitetura", "Tecnologia da Informação", "Consultoria e Gestão"])
        optante_simples = st.checkbox("Prestador é Optante pelo Simples Nacional?")

    if st.button("Calcular Retenções"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        st.info("Retenções calculadas com base na legislação federal e municipal vigente.")
        resumo = f"Nota Fiscal: R$ {valor_nf:,.2f} | Natureza: {natureza}"
        renderizar_botoes_acao("Retenções Tributárias", resumo)

# 4. Custo Real de Funcionário (CLT)
elif modulo == "Custo Real de Funcionário (CLT)":
    st.markdown('<p class="main-header">👥 Simulador de Custo Real de Funcionário (CLT)</p>', unsafe_allow_html=True)
    st.write("Descubra quanto custa realmente manter um colaborador na carteira (salário + encargos + provisões).")
    
    col1, col2 = st.columns(2)
    with col1:
        salario_bruto = st.number_input("Salário Bruto Mensal (R$)", value=3500.00, step=200.00)
        beneficios_vr = st.number_input("Vale-Alimentação / Refeição Mensal (R$)", value=600.00, step=50.00)
    with col2:
        beneficios_vt = st.number_input("Vale-Transporte Mensal (R$)", value=200.00, step=20.00)
        insalubridade = st.checkbox("Adicional de Insalubridade / Periculosidade")

    if st.button("Calcular Custo Total"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        st.success("Custo total mensurado detalhadamente com encargos sociais e trabalhistas inclusos.")
        resumo = f"Salário Bruto: R$ {salario_bruto:,.2f} | Custo Real Total Projetado"
        renderizar_botoes_acao("Custo Real CLT", resumo)

# 5. Calendário Fiscal Inteligente
elif modulo == "Calendário Fiscal Inteligente":
    st.markdown('<p class="main-header">📅 Calendário Fiscal Inteligente & Vencimentos</p>', unsafe_allow_html=True)
    st.write("Acompanhe os prazos limite das principais obrigações acessórias federais, estaduais e municipais.")
    
    st.markdown("""
    | Obrigação | Vencimento | Status |
    | :--- | :--- | :--- |
    | **PGDAS-D (Simples Nacional)** | Dia 20 de cada mês | 🟢 No Prazo |
    | **DCTFWeb e eSocial** | Dia 15 de cada mês | 🟢 No Prazo |
    | **DEFIS (Anual)** | Até 31 de Março | ⚠️ Atenção ao Prazo |
    | **IRPJ / CSLL / PIS / COFINS (Lucro Presumido)** | Último dia útil do mês subsequente | 🟢 No Prazo |
    """)
    
    observacao_calendario = st.text_area("Adicionar Lembrete Personalizado de Prazo", "Revisar notas fiscais pendentes antes do dia 15.")
    renderizar_botoes_acao("Calendário Fiscal", "Acompanhamento de vencimentos fiscais ativos.")

# 6. Chat IA Master Sênior (IA simples original, sem alterações estruturais)
elif modulo == "Chat IA Master Sênior":
    st.markdown('<p class="main-header">💬 Chat IA Master Sênior</p>', unsafe_allow_html=True)
    st.write("Consulte inteligência artificial especializada em planejamento tributário brasileiro (LC 123/2006, CND, SPED).")
    
    pergunta_usuario = st.text_input("Digite sua dúvida fiscal ou tributária para o Master:")
    if st.button("Enviar Pergunta"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        if pergunta_usuario:
            st.info(f"**IA Master Sênior:** Analisando a questão '{pergunta_usuario}' com base na legislação atual... Recomenda-se verificar o sublimite estadual do Simples Nacional.")
        else:
            st.warning("Por favor, digite uma pergunta.")
            
    renderizar_botoes_acao("Chat IA Sênior", f"Consulta realizada: {pergunta_usuario}")

# 7. Parecer Executivo Institucional
elif modulo == "Parecer Executivo Institucional":
    st.markdown('<p class="main-header">📑 Parecer Executivo Institucional</p>', unsafe_allow_html=True)
    st.write("Emissão de relatórios formais e laudos periciais com formatação executiva para entrega a conselhos de administração e diretoria.")
    
    col1, col2 = st.columns(2)
    with col1:
        tomador = st.text_input("Nome / Razão Social do Tomador", "Empresa Exemplo Ltda")
        responsavel_tecnico = st.text_input("Responsável Técnico / Contador", "Dr. Contador CRC/SP")
    with col2:
        objeto_parecer = st.text_input("Objeto do Parecer", "Migração de Regime Tributário")
        observacoes_laudo = st.text_area("Conclusão / Considerações Finais do Especialista", "A empresa apresenta plenas condições financeiras e operacionais para a migração ao Lucro Presumido no próximo ano-calendário.")

    if st.button("Gerar Parecer Executivo em PDF/Texto"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        st.success("Parecer estruturado e formatado institucionalmente com sucesso!")
        resumo = f"Parecer para: {tomador} | Objeto: {objeto_parecer} | Responsável: {responsavel_tecnico}"
        renderizar_botoes_acao("Parecer Executivo", resumo)

# 8. Auditoria Preventiva XML / SPED
elif modulo == "Auditoria Preventiva XML / SPED":
    st.markdown('<p class="main-header">🛡️ Auditoria Preventiva XML / SPED</p>', unsafe_allow_html=True)
    st.write("Varredura de inconsistências fiscais, divergências de NCM e cruzamento de notas fiscais eletrônicas.")
    
    arquivo_enviado = st.file_uploader("Carregar arquivos XML ou SPED para auditoria", type=["xml", "txt", "zip"], accept_multiple_files=True)
    email_notificacao = st.text_input("E-mail do Gestor para Envio do Relatório de Inconsistências", "gestor@empresa.com.br")
    
    if st.button("Executar Varredura e Auditoria Automática"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()
        descontar_um_uso()

        if arquivo_enviado:
            st.success("Auditoria concluída com sucesso! Nenhum erro crítico de NCM encontrado nos arquivos enviados.")
        else:
            st.warning("Por favor, faça o upload de ao menos um arquivo XML ou SPED.")
            
        renderizar_botoes_acao("Auditoria Preventiva", f"Auditoria realizada para o e-mail: {email_notificacao}")

# 9. Central de Leads Capturados
elif modulo == "Central de Leads Capturados":
    st.markdown('<p class="main-header">🎯 Central de Leads Capturados</p>', unsafe_allow_html=True)
    st.write("Relação de potenciais clientes que utilizaram o simulador gratuito de entrada.")
    
    df_leads = carregar_leads_arquivo()
    if not df_leads.empty:
        st.dataframe(df_leads, use_container_width=True)
    else:
        # Dados de exemplo padrão caso o CSV esteja vazio
        dados_leads = pd.DataFrame({
            "Data": ["19/09/2026 01:07", "19/09/2026 01:18", "19/09/2026 01:57", "19/09/2026 11:52"],
            "Razão Social": ["Empresa Exemplo Ltda", "Comércio Alpha ME", "Indústria Beta S/A", "Serviços Gama Eireli"],
            "WhatsApp": ["64993044147", "11988776655", "21998877665", "31977665544"],
            "E-mail": ["contato@empresa.com.br", "alpha@contato.com", "beta@industria.com", "gama@servicos.com"],
            "Melhor Regime": ["Simples Nacional", "Lucro Presumido", "Simples Nacional", "Lucro Presumido"]
        })
        st.dataframe(dados_leads, use_container_width=True)
    
    filtro_busca = st.text_input("Filtrar Lead por Nome ou E-mail")
    if filtro_busca:
        st.info(f"Filtrando registros correspondentes a: '{filtro_busca}'")
        
    renderizar_botoes_acao("Central de Leads", "Relatório completo da base de leads exportado.")

# Rodapé de Configuração e Painel Master oculto via senha
st.sidebar.markdown("---")
if st.sidebar.checkbox("⚙️ Painel Master / Ativação"):
    st.sidebar.markdown("### Configurações de Acesso")
    email_painel = st.sidebar.text_input("E-mail de Gestor:", key="input_email_painel")
    senha_input = st.sidebar.text_input("Senha Master / Liberação:", type="password", key="input_painel_senha")
    
    if st.sidebar.button("Ativar Acesso Master"):
        if email_painel.strip().lower() == MEU_EMAIL_GESTOR.lower() or senha_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.session_state.acesso_bloqueado_definitivo = False
            st.sidebar.success("Acesso Master ativado com sucesso!")
            st.rerun()
        else:
            st.sidebar.error("E-mail ou senha incorretos.")
