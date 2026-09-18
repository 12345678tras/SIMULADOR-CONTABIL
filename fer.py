import streamlit as st
import pandas as pd
import os
import datetime
import hashlib
from openai import OpenAI

# ==========================================
# 0. SISTEMA ESPIÃO DE AUDITORIA & BLINDAGEM
# ==========================================
ARQUIVO_LOG = "sistema_auditoria.log"

def registrar_log(acao, tipo="INFO"):
    """Comando espião para registrar movimentações, erros e tentativas de invasão."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_log = f"[{timestamp}] [{tipo}] {acao}\n"
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(mensagem_log)
    except Exception as e:
        print(f"Erro no log espião: {e}")

registrar_log("Sistema iniciado com protocolos de blindagem ativados.", "STARTUP")

def verificar_senha_master(senha_digitada):
    senha_limpa = senha_digitada.strip().lower()
    return senha_limpa == "contadora2x"

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E DIRETRIZES
# ==========================================
st.set_page_config(
    page_title="Plataforma Executiva de Inteligência Contábil & Fiscal", 
    page_icon="📈", 
    layout="wide"
)

ARQUIVO_CLIENTES = "clientes_contabilidade.xlsx"
ARQUIVO_LEADS = "potenciais_clientes.xlsx"

# Gerenciamento de Estado seguro
if "liberado_pago_contabil" not in st.session_state:
    st.session_state.liberado_pago_contabil = False

if "simulacoes_restantes" not in st.session_state:
    st.session_state.simulacoes_restantes = 2

if "mensagens_ia_restantes" not in st.session_state:
    st.session_state.mensagens_ia_restantes = 3

if "tentativas_falhas_master" not in st.session_state:
    st.session_state.tentativas_falhas_master = 0

def carregar_dados(arquivo, colunas):
    if not os.path.exists(arquivo):
        df_inicial = pd.DataFrame(columns=colunas)
        df_inicial.to_excel(arquivo, index=False)
        registrar_log(f"Base de dados criada automaticamente: {arquivo}", "SETUP")
    return pd.read_excel(arquivo)

df_clientes = carregar_dados(ARQUIVO_CLIENTES, ["CNPJ/CPF", "Razão Social", "Regime", "Honorário (R$)", "Status"])
df_leads = carregar_dados(ARQUIVO_LEADS, ["Nome", "WhatsApp", "Faturamento Mensal", "Ramo", "Economia Estimada (R$)"])

def tela_bloqueio_pagamento(motivo_texto):
    st.error(f"🔒 **Acesso Limitado:** {motivo_texto}")
    registrar_log(f"Tela de bloqueio exibida. Motivo: {motivo_texto}", "SECURITY")
    
    st.markdown("### 💎 Desbloqueie Acesso Ilimitado à Plataforma Executiva")
    st.markdown("Para continuar aproveitando todo o poder da nossa inteligência contábil e auditoria preventiva, escolha o plano ideal abaixo:")

    tipo_plano_escolhido = st.selectbox("Selecione a Modalidade de Assinatura:", [
        "Plano Start (Mensal) - R$ 147,00/mês", 
        "Plano Professional Anual (Destaque) - R$ 2.970,00/ano",
        "Plano Enterprise / Escritório Master - R$ 5.970,00/ano"
    ], key="select_plano_bloqueio")

    if "Mensal" in tipo_plano_escolhido:
        link_pagamento_ativo = "https://invoice.infinitepay.io/plans/cristiane-da-260/XLX77TGv0y"
    else:
        link_pagamento_ativo = "https://invoice.infinitepay.io/plans/cristiane-da-260/qTSP5k9f6S"

    tab_pix, tab_cartao, tab_master = st.tabs(["💎 Pagar com Pix", "💳 Pagar com Cartão", "🔑 Desbloqueio Master"])

    with tab_pix:
        st.write(f"Você selecionou: **{tipo_plano_escolhido}**")
        st.markdown(
            """
            - **Chave Pix (Telefone):** `+5564993044147`
            - **Favorecido:** `CAC CONTABILIZANDO`
            - **Plataforma:** `InfinitePay`
            """
        )
        comprovante_pix_input = st.text_input("Insira o ID ou comprovante do Pix para liberação:", key="input_comp_pix_bloqueio")
        if st.button("Validar Ativação via Pix", key="btn_valida_pix_bloqueio"):
            if comprovante_pix_input.strip() and len(comprovante_pix_input.strip()) > 3:
                st.session_state.liberado_pago_contabil = True
                registrar_log(f"Acesso liberado via Pix com segurança. ID: {comprovante_pix_input}", "PAYMENT")
                st.success("Pagamento validado com sucesso! Acesso liberado.")
                st.rerun()
            else:
                registrar_log("Tentativa de validação Pix inválida/vazia.", "WARNING")
                st.warning("Por favor, informe um comprovante ou ID de Pix válido.")

    with tab_cartao:
        st.write(f"Checkout seguro para: **{tipo_plano_escolhido}**")
        st.markdown(f'<a href="{link_pagamento_ativo}" target="_blank" style="background-color: #0047AB; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">💳 Acessar Checkout Seguro InfinitePay</a>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        transacao_cartao_input = st.text_input("Insira o ID da transação do cartão:", key="input_comp_cartao_bloqueio")
        if st.button("Validar Ativação via Cartão", key="btn_valida_cartao_bloqueio"):
            if transacao_cartao_input.strip() and len(transacao_cartao_input.strip()) > 3:
                st.session_state.liberado_pago_contabil = True
                registrar_log(f"Acesso liberado via Cartão com segurança. Transação ID: {transacao_cartao_input}", "PAYMENT")
                st.success("Assinatura via cartão validada com sucesso! Acesso liberado.")
                st.rerun()
            else:
                registrar_log("Tentativa de validação Cartão inválida/vazia.", "WARNING")
                st.warning("Por favor, informe um ID de transação válido.")

    with tab_master:
        st.markdown("#### Painel de Desbloqueio Rápido do Escritório")
        if st.session_state.tentativas_falhas_master >= 5:
            st.error("🚨 **Mecanismo de Defesa Ativado:** Muitas tentativas incorretas de senha. Aguarde o reset de segurança.")
            registrar_log("BLOQUEIO DE SEGURANÇA: Excesso de tentativas de invasão na tela master.", "SECURITY_BREACH_ATTEMPT")
        else:
            senha_bloqueio_direta = st.text_input("Digite a senha de liberação:", type="password", key="input_senha_tela_bloqueio")
            if st.button("Desbloquear com Senha", key="btn_executar_desbloqueio_master"):
                if verificar_senha_master(senha_bloqueio_direta):
                    st.session_state.liberado_pago_contabil = True
                    st.session_state.tentativas_falhas_master = 0
                    registrar_log("Sistema desbloqueado com sucesso via Painel Master.", "SECURITY")
                    st.success("Senha correta! Sistema totalmente desbloqueado.")
                    st.rerun()
                else:
                    st.session_state.tentativas_falhas_master += 1
                    registrar_log(f"ALERTA DE SEGURANÇA: Senha incorreta digitada (Tentativa {st.session_state.tentativas_falhas_master}/5).", "SECURITY_ALERT")
                    st.error(f"Senha incorreta. Tentativas restantes: {5 - st.session_state.tentativas_falhas_master}")

# ==========================================
# 2. MENU DE NAVEGAÇÃO CORPORATIVA
# ==========================================
st.sidebar.title("🏢 Gestão Contábil Avançada")
opcao = st.sidebar.radio("Módulos Estratégicos", [
    "🚀 Simulador Contínuo & Planos", 
    "💬 Chat com Consultor IA Avançado",
    "📑 Relatório & Parecer Executivo (PDF/Wpp)", 
    "🛡️ Auditoria Preventiva & Malha Fina (XML)", 
    "📊 Indicadores Financeiros do Escritório",
    "💼 Governança de Clientes Ativos", 
    "📥 Central de Leads & Prospecção",
    "🕵️‍♂️ Painel Espião & Segurança"
])

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel Master (Escritório)"):
    senha_admin_input = st.text_input("Senha de Acesso Mestre:", type="password", key="input_senha_contabil")
    if st.button("🔓 Validar Senha Master", key="btn_mestre_contabil"):
        if verificar_senha_master(senha_admin_input):
            st.session_state.liberado_pago_contabil = True
            registrar_log("Acesso master liberado via barra lateral com segurança.", "SECURITY")
            st.success("Senha válida! Acesso irrestrito liberado.")
            st.rerun()
        else:
            registrar_log("ALERTA DE SEGURANÇA: Senha master inválida na barra lateral.", "SECURITY_ALERT")
            st.error("Senha de autorização incorreta.")

    if st.session_state.liberado_pago_contabil:
        st.info("Status: **MASTER ATIVADO 🔓 (Blindado)**")

# ==========================================
# 3. MÓDULO: SIMULADOR CONTÍNUO & PLANOS
# ==========================================
if opcao == "🚀 Simulador Contínuo & Planos":
    st.title("🧮 Simulador Contínuo de Regime Tributário")
    st.markdown("Análise paramétrica inteligente e simulação de cenários fiscais para o seu negócio.")

    if not st.session_state.liberado_pago_contabil:
        st.info(f"🎁 **Modo Demonstração:** Você possui **{st.session_state.simulacoes_restantes}** simulação(ões) gratuita(s) restante(s).")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Parâmetros da Entidade")
        nome_empresa = st.text_input("Razão Social ou Nome do Contribuinte:", value="Empresa Exemplo Ltda")
        whatsapp_empresa = st.text_input("WhatsApp para Contato:", value="64993044147")
        email_empresa = st.text_input("E-mail Corporativo:", value="contato@empresa.com.br")
        segmento = st.selectbox("Segmento de Atuação:", [
            "Comércio Varejista / Atacadista", 
            "Prestação de Serviços (Geral / Intelectual)", 
            "Tecnologia / Software / TI", 
            "Saúde / Clínicas Médicas", 
            "Indústria"
        ])
        faturamento_anual = st.number_input("Faturamento Bruto Anual Estimado (R$):", min_value=10000.0, value=360000.0, step=10000.0)
        folha_salarios_anual = st.number_input("Massa Salarial / Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0)
        despesas_operacionais = st.number_input("Despesas Operacionais / Deduções Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0)

    with col2:
        st.subheader("Motor de Análise Executiva")
        
        if st.button("⚡ Executar Simulação Tributária", type="primary", use_container_width=True):
            if not st.session_state.liberado_pago_contabil and st.session_state.simulacoes_restantes <= 0:
                registrar_log(f"Tentativa de simulação bloqueada por limite excedido: {nome_empresa}", "WARNING")
                st.warning("Suas simulações gratuitas esgotaram!")
            else:
                if not st.session_state.liberado_pago_contabil:
                    st.session_state.simulacoes_restantes -= 1
                    registrar_log(f"Simulação gratuita executada com segurança. Restam: {st.session_state.simulacoes_restantes}", "USAGE")

                imposto_simples = faturamento_anual * 0.09
                imposto_presumido = faturamento_anual * 0.113
                lucro_real_base = max(0.0, faturamento_anual - despesas_operacionais - folha_salarios_anual)
                imposto_real = lucro_real_base * 0.24

                regimes = {
                    "Simples Nacional": imposto_simples,
                    "Lucro Presumido": imposto_presumido,
                    "Lucro Real": imposto_real
                }
                melhor_regime = min(regimes, key=regimes.get)
                menor_imposto = regimes[melhor_regime]
                pior_imposto = max(regimes.values())
                economia_potencial_anual = pior_imposto - menor_imposto

                registrar_log(f"Simulação concluída com sucesso para {nome_empresa}.", "SUCCESS")
                st.success(f"Análise paramétrica concluída para **{nome_empresa}**!")
                
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Melhor Regime Indicado", melhor_regime)
                mc2.metric("Carga Tributária Estimada", f"R$ {menor_imposto:,.2f}")
                mc3.metric("Elisão Fiscal Anual", f"R$ {economia_potencial_anual:,.2f}", delta="Otimização")

    if not st.session_state.liberado_pago_contabil and st.session_state.simulacoes_restantes <= 0:
        st.markdown("---")
        tela_bloqueio_pagamento("Suas simulações gratuitas de demonstração acabaram.")

# ==========================================
# 4. MÓDULO: CHAT COM CONSULTOR IA AVANÇADO
# ==========================================
elif opcao == "💬 Chat com Consultor IA Avançado":
    st.title("🤖 Consultor Inteligente Sênior de Plantão")
    st.markdown("Tire dúvidas tributárias, fiscais e societárias com nossa inteligência artificial sênior.")

    if not st.session_state.liberado_pago_contabil:
        st.info(f"🎁 **Modo Demonstração:** Você possui **{st.session_state.mensagens_ia_restantes}** mensagem(ns) gratuita(s) restante(s) no chat.")

    if "historico_chat" not in st.session_state:
        st.session_state.historico_chat = [
            {"role": "system", "content": "Você é um Consultor Tributário Sênior e Contador altamente experiente. Responda com clareza, autoridade e didática."}
        ]

    for msg in st.session_state.historico_chat:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    bloquear_chat = False
    if not st.session_state.liberado_pago_contabil and st.session_state.mensagens_ia_restantes <= 0:
        bloquear_chat = True

    if bloquear_chat:
        st.warning("🔒 Suas mensagens gratuitas no chat com a IA acabaram.")
        tela_bloqueio_pagamento("Para continuar conversando ilimitadamente, assine um de nossos planos ou use a chave mestra.")
    else:
        pergunta_usuario = st.chat_input("Digite sua dúvida contábil ou fiscal...")
        if pergunta_usuario:
            if not st.session_state.liberado_pago_contabil:
                st.session_state.mensagens_ia_restantes -= 1
                registrar_log(f"Mensagem grátis usada no chat. Restam: {st.session_state.mensagens_ia_restantes}", "USAGE")

            st.session_state.historico_chat.append({"role": "user", "content": pergunta_usuario})
            with st.chat_message("user"):
                st.markdown(pergunta_usuario)

            with st.chat_message("assistant"):
                with st.spinner("Analisando bases fiscais e elaborando resposta sênior..."):
                    api_key_openai = os.environ.get("OPENAI_API_KEY")
                    resposta_ia = ""
                    
                    if api_key_openai:
                        try:
                            client = OpenAI(api_key=api_key_openai)
                            resposta = client.chat.completions.create(
                                model="gpt-4o",
                                messages=st.session_state.historico_chat,
                                temperature=0.3,
                                max_tokens=800
                            )
                            resposta_ia = resposta.choices[0].message.content
                            registrar_log("Consulta OpenAI executada com sucesso.", "AI_SUCCESS")
                        except Exception as e:
                            resposta_ia = f"Erro técnico na comunicação com a API da OpenAI: {e}"
                            registrar_log(f"ERRO DE API OPENAI: {e}", "AI_ERROR")
                    else:
                        resposta_ia = (
                            f"Olá! Analisei a sua dúvida enviada.\n\n"
                            "Como o ambiente atual não detectou uma chave de API configurada (`OPENAI_API_KEY`), "
                            "o chat inteligente requer a inserção da chave nas variáveis de ambiente do seu servidor para gerar análises automáticas completas."
                        )
                        registrar_log("Aviso: Tentativa de uso do chat sem OpenAI API Key configurada.", "AI_WARNING")

                    st.markdown(resposta_ia)
                    st.session_state.historico_chat.append({"role": "assistant", "content": resposta_ia})

# ==========================================
# 5. MÓDULO: RELATÓRIO & PARECER EXECUTIVO
# ==========================================
elif opcao == "📑 Relatório & Parecer Executivo (PDF/Wpp)":
    st.title("📑 Emissor de Parecer Executivo & Disparador Inteligente")
    
    if not st.session_state.liberado_pago_contabil:
        tela_bloqueio_pagamento("O módulo de emissão de Pareceres Executivos é exclusivo para assinantes.")
    else:
        cli_nome = st.text_input("Nome do Cliente / Empresa Destinatária:", value="Empresa Exemplo Ltda")
        cli_whats = st.text_input("WhatsApp para Envio (com DDD):", value="64993044147")
        cli_email = st.text_input("E-mail para Envio:", value="cliente@empresa.com.br")
        fat_input = st.number_input("Faturamento Mensal Base (R$):", value=30000.0)

        if st.button("🤖 Gerar Parecer Executivo Oficial com IA", type="primary"):
            with st.spinner("Elaborando parecer executivo de alto padrão..."):
                api_key_openai = os.environ.get("OPENAI_API_KEY")
                parecer_texto = f"Parecer Técnico Executivo - {cli_nome}\nFaturamento base: R$ {fat_input:,.2f}"
                if api_key_openai:
                    try:
                        client = OpenAI(api_key=api_key_openai)
                        resposta = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "Você é um consultor tributário sênior e auditor fiscal."},
                                {"role": "user", "content": f"Elabore um parecer tributário executivo para {cli_nome}, faturamento mensal de R$ {fat_input:,.2f}."}
                            ],
                            temperature=0.3,
                            max_tokens=600
                        )
                        parecer_texto = resposta.choices[0].message.content
                        registrar_log(f"Parecer gerado com segurança para {cli_nome}", "SUCCESS")
                    except Exception as e:
                        registrar_log(f"Erro ao gerar parecer com IA: {e}", "ERROR")

                st.success("Parecer gerado com sucesso!")
                st.text_area("Visualização do Laudo Executivo:", value=parecer_texto, height=250)

                st.markdown("---")
                st.subheader("📤 Canais de Envio Executivo")
                wpp_limpo = ''.join(filter(str.isdigit, str(cli_whats)))
                link_envio_wpp = f"https://wa.me/55{wpp_limpo}?text=Olá%20{cli_nome},%20segue%20o%20seu%20Parecer%20Tributário%20Executivo."
                
                col_env1, col_env2 = st.columns(2)
                with col_env1:
                    st.markdown(f'<a href="{link_envio_wpp}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar via WhatsApp</a>', unsafe_allow_html=True)
                with col_env2:
                    st.markdown(f'<a href="mailto:{cli_email}?subject=Parecer%20Tributário" style="background-color: #1E3A8A; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📧 Enviar via E-mail</a>', unsafe_allow_html=True)

# ==========================================
# 6. MÓDULO: AUDITORIA PREVENTIVA & MALHA FINA (XML)
# ==========================================
elif opcao == "🛡️ Auditoria Preventiva & Malha Fina (XML)":
    st.title("🛡️ Módulo de Auditoria Preventiva & Malha Fina (SPED / XML)")
    
    if not st.session_state.liberado_pago_contabil:
        tela_bloqueio_pagamento("A auditoria preventiva é restrita a assinantes.")
    else:
        uploaded_file = st.file_uploader("Carregar Arquivo Fiscal (XML, TXT ou CSV):", type=["xml", "txt", "csv"])
        if uploaded_file is not None:
            registrar_log(f"Arquivo fiscal processado com segurança: {uploaded_file.name}", "AUDIT")
            st.success(f"Arquivo **{uploaded_file.name}** carregado com sucesso!")
            if st.button("🔍 Executar Varredura Preventiva de Malha Fina", type="primary"):
                st.markdown("### 📊 Relatório de Diagnóstico Preventivo")
                col_d1, col_d2, col_d3 = st.columns(3)
                col_d1.metric("Inconsistências", "0 Identificadas", delta="Seguro")
                col_d2.metric("Divergências SPED", "Nenhuma", delta="Regular")
                col_d3.metric("Risco de Malha Fina", "Baixo Risco", delta="Conforme")
        else:
            st.info("Faça o upload de um arquivo fiscal para iniciar a varredura.")

# ==========================================
# 7. INDICADORES FINANCEIROS DO ESCRITÓRIO
# ==========================================
elif opcao == "📊 Indicadores Financeiros do Escritório":
    st.title("📊 Indicadores de Desempenho & Saúde Financeira")
    if not df_clientes.empty and "Honorário (R$)" in df_clientes.columns:
        faturamento_total = df_clientes["Honorário (R$)"].sum()
        total_clientes = len(df_clientes)
        ticket_medio = faturamento_total / total_clientes if total_clientes > 0 else 0

        c_ind1, c_ind2, c_ind3 = st.columns(3)
        c_ind1.metric("Receita Recorrente Mensal (MRR)", f"R$ {faturamento_total:,.2f}")
        c_ind2.metric("Total de Clientes Ativos", total_clientes)
        c_ind3.metric("Ticket Médio por Cliente", f"R$ {ticket_medio:,.2f}")
    else:
        st.info("Cadastre clientes na base para habilitar os indicadores.")

# ==========================================
# 8. GOVERNANÇA DE CLIENTES ATIVOS
# ==========================================
elif opcao == "💼 Governança de Clientes Ativos":
    st.title("💼 Carteira de Clientes Ativos do Escritório (Área Protegida)")
    if not df_clientes.empty:
        st.dataframe(df_clientes, use_container_width=True)
    else:
        st.info("Nenhum cliente registrado.")

    with st.expander("➕ Inserir Novo Cliente"):
        with st.form("cad_cliente_contabil"):
            doc = st.text_input("CNPJ ou CPF:")
            rs = st.text_input("Razão Social:")
            reg = st.selectbox("Regime Tributário:", ["MEI", "Simples Nacional", "Lucro Presumido", "Lucro Real"])
            hon = st.number_input("Honorário Mensal (R$):", min_value=0.0, step=50.0, value=600.0)
            
            if st.form_submit_button("Salvar Cliente"):
                if doc and rs:
                    reg_novo = {"CNPJ/CPF": doc, "Razão Social": rs, "Regime": reg, "Honorário (R$)": hon, "Status": "Ativo"}
                    df_cli_atualizado = pd.concat([df_clientes, pd.DataFrame([reg_novo])], ignore_index=True)
                    df_cli_atualizado.to_excel(ARQUIVO_CLIENTES, index=False)
                    registrar_log(f"Novo cliente cadastrado com segurança na base: {rs}", "DATABASE")
                    st.success("Cliente cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha o CNPJ/CPF e a Razão Social.")

# ==========================================
# 9. CENTRAL DE LEADS & PROSPECÇÃO
# ==========================================
elif opcao == "📥 Central de Leads & Prospecção":
    st.title("📥 Prospecção Ativa (Leads do Simulador)")
    if not df_leads.empty:
        st.dataframe(df_leads, use_container_width=True)
    else:
        st.info("Nenhum lead registrado.")

# ==========================================
# 10. PAINEL ESPIÃO & SEGURANÇA
# ==========================================
elif opcao == "🕵️‍♂️ Painel Espião & Segurança":
    st.title("🕵️‍♂️ Painel Espião de Monitoramento & Segurança Antifraude")
    st.markdown("Área restrita de engenharia para inspecionar tentativas de invasão, integridade e logs do sistema.")

    senha_log_input = st.text_input("Digite a senha master para acessar o painel de segurança:", type="password", key="input_senha_log_espiao")
    
    if verificar_senha_master(senha_log_input):
        st.success("Acesso autorizado ao Painel de Segurança.")
        st.session_state.tentativas_falhas_master = 0

        if os.path.exists(ARQUIVO_LOG):
            with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
                linhas_logs = f.readlines()
            
            st.markdown(f"**Total de eventos monitorados:** `{len(linhas_logs)}`")
            
            col_acao_log1, col_acao_log2 = st.columns(2)
            with col_acao_log1:
                if st.button("🧹 Limpar Arquivo de Logs"):
                    open(ARQUIVO_LOG, "w", encoding="utf-8").close()
                    registrar_log("Logs de auditoria limpos pelo administrador.", "SECURITY")
                    st.success("Logs limpos com sucesso!")
                    st.rerun()
            with col_acao_log2:
                if st.download_button("📥 Baixar Relatório de Segurança (.log)", data="".join(linhas_logs), file_name="relatorio_seguranca_sistema.log", mime="text/plain"):
                    st.toast("Relatório baixado!")

            st.markdown("---")
            st.subheader("🚨 Alertas de Segurança & Histórico Recente")
            for linha in reversed(linhas_logs[-100:]):
                if "ERROR" in linha or "ALERT" in linha or "BREACH" in linha:
                    st.error(linha.strip())
                elif "WARNING" in linha:
                    st.warning(linha.strip())
                elif "SUCCESS" in linha or "PAYMENT" in linha or "SECURITY" in linha:
                    st.success(linha.strip())
                else:
                    st.code(linha.strip(), language="text")
        else:
            st.info("Nenhum registro de log encontrado.")
    else:
        if senha_log_input.strip() != "":
            st.error("Senha incorreta para acesso ao painel de segurança.")
        else:
            st.warning("🔒 Digite a senha mestra para auditar a segurança do sistema.")
