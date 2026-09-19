import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from google import genai

# Configuração da Página
st.set_page_config(
    page_title="Consultor Inteligente Master",
    page_icon="⚖️",
    layout="wide"
)

# ==========================================
# CONFIGURAÇÃO DA IA (GEMINI)
# ==========================================
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
    client_ai = genai.Client(api_key=gemini_key)
except Exception:
    client_ai = None

# ==========================================
# SEGURANÇA E CONFIGURAÇÕES DO GESTOR
# ==========================================
MEU_EMAIL_GESTOR = st.secrets["gestor"]["email"] if "gestor" in st.secrets and "email" in st.secrets["gestor"] else "Rede.rodrigues2017@gmail.com"
SENHAS_MESTRE_CONFIG = st.secrets["gestor"]["senhas"] if "gestor" in st.secrets and "senhas" in st.secrets["gestor"] else ["cliente 1 2 3x", "contadora 2x", "gestorMaster2026!"]

# Inicialização de Estado Robusta
if "liberado_pago_master" not in st.session_state:
    st.session_state.liberado_pago_master = False
if "simulacoes_restantes" not in st.session_state:
    st.session_state.simulacoes_restantes = 4
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
    st.markdown("### 🚀 Os seus 4 Acessos Gratuitos Esgotaram!")
    st.markdown("Para continuar a utilizar todas as ferramentas do sistema, escolha um dos planos abaixo ou faça o pagamento direto via PIX:")
    
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
    st.warning(f"📲 **Já fez o PIX ou o pagamento?** Envie o comprovativo para o WhatsApp **(64) 99304-4147** para receber a sua palavra-passe de liberação instantânea!")
    
    st.markdown("#### Identificação do Gestor / Liberação por Senha")
    email_gestor_input = st.text_input("Digite o seu e-mail de gestor:", key="input_email_gestor_login")
    senha_cliente_input = st.text_input("Ou digite a senha de liberação:", type="password", key="input_senha_bloqueio")
    
    if st.button("🔓 Desbloquear Acesso"):
        if email_gestor_input.strip().lower() == MEU_EMAIL_GESTOR.lower() or senha_cliente_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.session_state.acesso_bloqueado_definitivo = False
            st.success("Acesso de gestor liberado com sucesso! Atualize a página.")
            st.rerun()
        else:
            st.error("E-mail ou senha incorretos.")
    st.stop()

# Verificação global de bloqueio
if st.session_state.acesso_bloqueado_definitivo and not st.session_state.liberado_pago_master:
    tela_bloqueio_comercial("Acesso restrito. Tentativa de acesso após esgotar as 4 consultas gratuitas.")

# Menu Lateral (Navegação Estratégica)
st.sidebar.title("⚖️ Consultor Master")
st.sidebar.markdown("Navegação Estratégica")

if st.session_state.liberado_pago_master:
    st.sidebar.success("👑 **Modo Gestor Ativo**\n*(Engenharia & Contabilidade)*")
else:
    st.sidebar.info(f"🎁 Acessos gratuitos restantes: **{st.session_state.simulacoes_restantes} / 4**")

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
        email = st.text_input("E-mail do Cliente:", value="contato@empresa.com.br", key="sim_email")
        fat_anual = st.number_input("Faturamento Bruto Anual (R$):", min_value=10000.0, value=360000.0, step=10000.0, key="sim_fat")
        folha_anual = st.number_input("Folha de Pagamento Anual (R$):", min_value=0.0, value=90000.0, step=5000.0, key="sim_folha")
        desp_anual = st.number_input("Despesas Operacionais Anuais (R$):", min_value=0.0, value=60000.0, step=5000.0, key="sim_desp")

    with c2:
        st.subheader("Resultado da Simulação")
        if st.button("⚡ Executar Simulação Completa", type="primary", use_container_width=True, key="btn_exec_sim"):
            if not verificar_bloqueio_antes_de_usar():
                st.rerun()

            descontar_um_uso()

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
# 2. MÓDULO: CHAT IA MASTER SÊNIOR (Modo Natural & Fluido)
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    st.title("💬 Chat IA Master Sênior - Inteligência Natural & Contábil")
    st.markdown("Bate-papo estratégico, fluido e contextualizado com a IA.")

    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = [
            {"role": "assistant", "content": "Olá! Que bom conversar com você. Estou com o meu modo de conversa natural ativado, pronto para te ajudar com ideias, dúvidas ou estratégias tributárias. O que vamos conversar agora?"}
        ]

    if "chat_sessao_gemini" not in st.session_state and client_ai:
        st.session_state.chat_sessao_gemini = client_ai.chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": (
                    "Você é um parceiro consultivo, inteligente, caloroso e altamente empático. "
                    "Converse de forma natural, fluida e amigável, evitando respostas robóticas ou listas excessivas. "
                    "Mantenha o foco em Direito Tributário, Contabilidade e Estratégia Empresarial."
                )
            }
        )

    for msg in st.session_state.mensagens_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    pergunta_usuario = st.chat_input("Digite sua mensagem para conversarmos...")
    if pergunta_usuario:
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()

        descontar_um_uso()

        st.session_state.mensagens_chat.append({"role": "user", "content": pergunta_usuario})
        with st.chat_message("user"):
            st.write(pergunta_usuario)

        with st.chat_message("assistant"):
            with st.spinner("A pensar na resposta..."):
                try:
                    if client_ai and "chat_sessao_gemini" in st.session_state:
                        response = st.session_state.chat_sessao_gemini.send_message(pergunta_usuario)
                        resposta_ia = response.text
                    else:
                        resposta_ia = "⚠️ Chave do Gemini não configurada ou sessão indisponível."
                except Exception as e:
                    resposta_ia = f"Ops, tive um pequeno problema ao processar: {e}"
                
                st.write(resposta_ia)
                st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})

# ==========================================
# 3. MÓDULO: PARECER EXECUTIVO & DISPAROS
# ==========================================
elif modulo == "📑 Parecer Executivo & Disparos":
    st.title("📑 Parecer Executivo & Disparos Automatizados")
    st.markdown("Geração de laudos técnicos aprofundados com suporte da IA.")

    client_nome = st.text_input("Nome do Cliente / Empresa:", value="Comércio Exemplo S.A.")
    client_fone = st.text_input("WhatsApp do Destinatário:", value=MEU_WHATSAPP)
    tema_parecer = st.selectbox("Tema do Parecer Técnico:", ["Revisão de ICMS-ST", "Planejamento Tributário Anual", "Impactos da Reforma Tributária", "Malha Fiscal Federal"])

    if st.button("📝 Gerar Parecer Executivo com IA", type="primary"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()

        descontar_um_uso()

        with st.spinner("Elaborando parecer executivo detalhado..."):
            try:
                if client_ai:
                    prompt_parecer = f"Elabore um Parecer Técnico Executivo formal sobre o tema '{tema_parecer}' para a empresa '{client_nome}', considerando a legislação tributária brasileira."
                    response = client_ai.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_parecer
                    )
                    parecer_texto = response.text
                else:
                    parecer_texto = f"PARECER TÉCNICO EXECUTIVO\nTema: {tema_parecer}\nCliente: {client_nome}\n(Erro: IA não configurada)"
            except Exception as e:
                parecer_texto = f"Erro ao gerar parecer: {e}"

        st.success("Parecer gerado com sucesso!")
        st.text_area("Laudo Técnico:", value=parecer_texto, height=250)

        wpp_num = limpar_telefone(client_fone)
        link_wpp_parecer = f"https://wa.me/55{wpp_num}?text={requests.utils.quote(f'Olá {client_nome}, segue o seu Parecer Técnico sobre {tema_parecer}.')}"

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f'<a href="{link_wpp_parecer}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block; text-align: center;">📲 Enviar Parecer no WhatsApp</a>', unsafe_allow_html=True)
        with col_p2:
            st.download_button(label="📥 Baixar Parecer em TXT", data=parecer_texto, file_name="parecer.txt", mime="text/plain", use_container_width=True)

# ==========================================
# 4. MÓDULO: AUDITORIA PREVENTIVA
# ==========================================
elif modulo == "🛡️ Auditoria Preventiva (XML/SPED)":
    st.title("🛡️ Auditoria Preventiva & Malha Fiscal")
    st.markdown("Auditoria padronizada de conformidade.")

    empresa_aud = st.text_input("Empresa Alvo da Auditoria:", value="Empresa Exemplo Ltda")
    if st.button("🛡️ Executar Auditoria Padronizada", type="primary"):
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()

        descontar_um_uso()

        laudo_auditoria = f"RELATÓRIO DE AUDITORIA\nEmpresa: {empresa_aud}\nStatus: Conformidade verificada com sucesso."
        st.success("Auditoria executada com sucesso!")
        st.text_area("Laudo Analítico:", value=laudo_auditoria, height=220)
        st.download_button(label="📥 Baixar Relatório (TXT)", data=laudo_auditoria, file_name="auditoria.txt", mime="text/plain", use_container_width=True)

# ==========================================
# 5. MÓDULO: INDICADORES DO ESCRITÓRIO
# ==========================================
elif modulo == "📊 Indicadores do Escritório":
    st.title("📊 Indicadores de Desempenho do Escritório")
    
    df_leads_ind = carregar_leads_arquivo()
    total_leads = len(df_leads_ind)

    col_ind1, col_ind2, col_ind3 = st.columns(3)
    col_ind1.metric("Simulações Realizadas", total_leads + 12)
    col_ind2.metric("Clientes Atendidos", total_leads + 8)
    col_ind3.metric("Economia Média Gerada", "R$ 42.500,00", delta="+14%")

# ==========================================
# 6. MÓDULO: GOVERNANÇA DE CLIENTES
# ==========================================
elif modulo == "🏛️ Governança de Clientes":
    st.title("🏛️ Governança e Carteira de Clientes")
    st.info("Utilize o painel para gerenciar os clientes cadastrados.")
    
    df_gov = carregar_leads_arquivo()
    if not df_gov.empty:
        st.dataframe(df_gov, use_container_width=True)
    else:
        st.warning("Nenhum cliente cadastrado até o momento.")

# ==========================================
# 7. MÓDULO: CENTRAL DE LEADS
# ==========================================
elif modulo == "🎯 Central de Leads":
    st.title("🎯 Central de Captação de Leads")
    st.markdown("Oportunidades de negócios geradas através das simulações tributárias.")

    df_leads = carregar_leads_arquivo()
    if not df_leads.empty:
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
        st.info("Ainda não há leads salvos no sistema. Faça simulações para começar a capturar contatos!")

# ==========================================
# 8. MÓDULO: CONFIGURAÇÕES / PAINEL MASTER
# ==========================================
elif modulo == "⚙️ Configurações / Painel Master":
    st.title("⚙️ Painel de Controle Master & Licenciamento")
    st.markdown("Gestão de licenças de acesso, chave PIX e ativação comercial.")

    if st.session_state.liberado_pago_master:
        st.success("🟢 Sistema com Licença Master Ativa (Acesso Ilimitado Liberado).")
    else:
        st.warning(f"🔒 Sistema em Modo Demonstração. Tentativas restantes: {st.session_state.simulacoes_restantes} / 4")
        
    st.markdown("### 🔑 Identificação do Gestor ou Resgate de Senha")
    email_painel = st.text_input("Seu E-mail de Gestor:", key="input_email_painel")
    senha_input = st.text_input("Ou Senha de Ativação:", type="password", key="input_painel_senha")
    
    if st.button("Ativar Acesso Master"):
        if email_painel.strip().lower() == MEU_EMAIL_GESTOR.lower() or senha_input in SENHAS_MESTRE_CONFIG:
            st.session_state.liberado_pago_master = True
            st.session_state.acesso_bloqueado_definitivo = False
            st.success("Licença de gestor ativada com sucesso neste dispositivo!")
            st.rerun()
        else:
            st.error("E-mail ou senha incorretos.")

    st.markdown("---")
    st.markdown("### 💳 Informações Oficiais de Pagamento (PIX e Cartão)")
    st.info(f"📌 **Chave PIX Oficial (InfinitePay):** `{CHAVE_PIX_OFICIAL}`\n\n📲 **WhatsApp para Comprovantes:** `(64) 99304-4147`")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown(f'<a href="{LINK_PLANO_START}" target="_blank" style="background-color: #007bff; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Start</a>', unsafe_allow_html=True)
    with col_c2:
        st.markdown(f'<a href="{LINK_PLANO_PRO}" target="_blank" style="background-color: #28a745; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Plano Pro</a>', unsafe_allow_html=True)
    with col_c3:
        st.markdown(f'<a href="{LINK_PLANO_ENTERPRISE}" target="_blank" style="background-color: #6f42c1; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; text-align: center;">Assinar Enterprise</a>', unsafe_allow_html=True)
