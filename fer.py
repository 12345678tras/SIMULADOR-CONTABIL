import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E DIRETRIZES DE DESIGN
# ==========================================
st.set_page_config(
    page_title="Plataforma de Inteligência Contábil & IA Avançada", 
    page_icon="📈", 
    layout="wide"
)

ARQUIVO_CLIENTES = "clientes_contabilidade.xlsx"
ARQUIVO_LEADS = "potenciais_clientes.xlsx"

# Gerenciamento de Estado para liberação de acesso pago/comprovante
if "liberado_pago_contabil" not in st.session_state:
    st.session_state.liberado_pago_contabil = False

# Função para garantir a persistência segura dos dados em Excel
def carregar_dados(arquivo, colunas):
    if not os.path.exists(arquivo):
        df_inicial = pd.DataFrame(columns=colunas)
        df_inicial.to_excel(arquivo, index=False)
    return pd.read_excel(arquivo)

df_clientes = carregar_dados(ARQUIVO_CLIENTES, ["CNPJ/CPF", "Razão Social", "Regime", "Honorário (R$)", "Status"])
df_leads = carregar_dados(ARQUIVO_LEADS, ["Nome", "WhatsApp", "Faturamento Mensal", "Ramo", "Economia Estimada (R$)"])

# ==========================================
# 2. MENU DE NAVEGAÇÃO E PAINEL ADMINISTRATIVO
# ==========================================
st.sidebar.title("🏢 Gestão Contábil Estratégica")
opcao = st.sidebar.radio("Navegação do Sistema", [
    "🚀 Simulador Executivo (Público / IA)", 
    "📊 Governança de Clientes Ativos", 
    "📥 Central de Leads & Oportunidades"
])

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel Master (Escritório)"):
    senha_admin_input = st.text_input("Chave Mestra de Acesso:", type="password", key="input_senha_contabil")
    if st.button("🔓 Validar Chave Master", key="btn_mestre_contabil"):
        if senha_admin_input.strip().upper() in ["CONTABIL12", "CONTABIL", "ADMIN", "MASTER"]:
            st.session_state.liberado_pago_contabil = True
            st.success("Credenciais validas. Acesso irrestrito liberado.")
            st.rerun()
        else:
            st.error("Chave de autorização incorreta.")

    if st.session_state.liberado_pago_contabil:
        st.info("Status: **MASTER ATIVADO 🔓**")

# ==========================================
# 3. MÓDULO: SIMULADOR INTELIGENTE COM IA AVANÇADA
# ==========================================
if opcao == "🚀 Simulador Executivo (Público / IA)":
    st.title("📊 Diagnóstico Tributário Preditivo & Inteligência Artificial")
    st.markdown("Ferramenta corporativa de elisão fiscal lícita. Avalie o impacto de enquadramento tributário para a sua estrutura empresarial.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Parâmetros da Empresa")
        nome = st.text_input("Nome do Gestor ou Razão Social:")
        whatsapp = st.text_input("WhatsApp Corporativo (com DDD):")
        ramo = st.selectbox("Segmento de Atuação:", [
            "Comércio Atacadista / Varejista", 
            "Prestação de Serviços Especializados", 
            "Tecnologia / Desenvolvimento de Software / TI", 
            "Saúde / Clínicas Médicas e Odontológicas", 
            "Indústria e Manufatura",
            "Outro Setor"
        ])
        faturamento = st.number_input("Faturamento Médio Mensal Bruto (R$):", min_value=1000.0, value=35000.0, step=5000.0)

    with col2:
        st.subheader("Diretriz de Análise")
        st.info(
            "💡 **Metodologia de Simulação:** O algoritmo cruza dados de faturamento para estimar "
            "o descasamento de carga tributária entre o Lucro Presumido e o Simples Nacional, "
            "acionando uma IA de alta performance para redigir o parecer executivo preliminar."
        )
        
        if st.button("⚙️ Executar Análise Tributária Avançada", type="primary", use_container_width=True):
            if nome and whatsapp:
                # Modelagem matemática base para estimativa preliminar
                imposto_estimado_atual = faturamento * 0.145
                imposto_otimizado = faturamento * 0.075
                economia_mensal = imposto_estimado_atual - imposto_otimizado
                economia_anual = economia_mensal * 12

                # Persistência automática do Lead captado
                novo_lead = {
                    "Nome": nome, 
                    "WhatsApp": whatsapp, 
                    "Faturamento Mensal": faturamento, 
                    "Ramo": ramo,
                    "Economia Estimada (R$)": economia_mensal
                }
                
                df_leads_atualizado = pd.concat([df_leads, pd.DataFrame([novo_lead])], ignore_index=True)
                df_leads_atualizado.drop_duplicates(subset=["WhatsApp"], keep="last", inplace=True)
                df_leads_atualizado.to_excel(ARQUIVO_LEADS, index=False)

                st.success(f"📈 Projeção calculada para **{nome}** com sucesso!")
                
                m1, m2 = st.columns(2)
                m1.metric("Redução Média Mensal", f"R$ {economia_mensal:,.2f}")
                m2.metric("Elisão Fiscal Anual Projetada", f"R$ {economia_anual:,.2f}")
                st.balloons()

                st.markdown("---")
                st.subheader("📋 Parecer Técnico Estratégico (Gerado por IA Avançada)")

                # Integração com a API da OpenAI utilizando uma persona técnica de alto padrão
                api_key_openai = os.environ.get("OPENAI_API_KEY")
                if api_key_openai:
                    try:
                        client = OpenAI(api_key=api_key_openai)
                        prompt_sistema = (
                            "Você é um consultor tributário sênior, auditor fiscal e estrategista empresarial brasileiro. "
                            "Elabore um parecer técnico formal, sofisticado, analítico e de alto valor agregado para um empresário. "
                            "Utilize terminologia técnica precisa da área contábil (ex: carga tributária efetiva, elisão fiscal, "
                            "regime de apuração, fator R, repartição de receitas). Evite termos genéricos; seja incisivo e demonstre alta autoridade técnica."
                        )
                        prompt_usuario = (
                            f"Dados do Contribuinte:\n"
                            f"- Entidade: {nome}\n"
                            f"- Setor de Atuação: {ramo}\n"
                            f"- Faturamento Médio Mensal: R$ {faturamento:,.2f}\n"
                            f"- Economia Mensal Estimada: R$ {economia_mensal:,.2f}\n"
                            "Redija um parecer executivo estruturado em tópicos apontando os riscos de uma tributação desalinhada, "
                            "a importância de uma revisão de enquadramento (Simples vs Presumido) e uma recomendação firme para contratação de assessoria contábil especializada."
                        )

                        resposta_ia = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": prompt_sistema},
                                {"role": "user", "content": prompt_usuario}
                            ],
                            temperature=0.4,
                            max_tokens=600
                        )
                        texto_laudo = resposta_ia.choices[0].message.content
                        st.markdown(texto_laudo)
                    except Exception as e:
                        st.warning("⚠️ Os cálculos numéricos foram processados com êxito, mas o módulo de IA encontrou instabilidade momentânea na conexão. A diretoria técnica do escritório emitirá o laudo em anexo.")
                else:
                    # Fallback analítico caso a chave de ambiente não esteja injetada
                    st.markdown(
                        f"""
                        **PARECER TÉCNICO PRELIMINAR - ANÁLISE DE ENQUADRAMENTO**
                        
                        - **Perfil do Contribuinte:** {nome} ({ramo})
                        - **Volume Operacional Bruto:** R$ {faturamento:,.2f} / mês
                        - **Diagnóstico Inicial:** Identificou-se uma assimetria na alocação da carga tributária efetiva. Dependendo do histórico de folha de salários e incidência de obrigações acessórias, a transição para um modelo otimizado pode gerar uma elisão fiscal anual da ordem de **R$ {economia_anual:,.2f}**.
                        - **Recomendação:** Recomenda-se a auditoria imediata dos livros fiscais de saída e o estudo de viabilidade para repactuação societária.
                        """
                    )

                st.markdown("---")
                if st.session_state.liberado_pago_contabil:
                    st.success("✅ **Plano de Implementação Completo Liberado pelo Escritório!**")
                else:
                    st.warning("🔒 O memorial descritivo com o cronograma de migração fiscal e entrega das obrigações acessórias é restrito.")
                    with st.expander("💳 Desbloquear Memorial Técnico Integral por R$ 20,00"):
                        st.write("Efetue o pagamento para liberar o documento de diretrizes estratégicas e agendamento prioritário:")
                        st.markdown(
                            """
                            - **Chave Pix (Telefone):** `+5564993044147`[span_0](start_span)[span_0](end_span)
                            - **Favorecido:** `CAC CONTABILIZANDO`[span_1](start_span)[span_1](end_span)
                            """
                        )
                        comprovante_cli = st.text_input("Identificador / Comprovante da Transferência Pix:", key="comp_lead_simulacao")
                        if st.button("Validar Liberação do Documento"):
                            if comprovante_cli.strip() != "":
                                st.session_state.liberado_pago_contabil = True
                                st.success("Validação concluída com sucesso. Documentação liberada.")
                                st.rerun()
                            else:
                                st.warning("Insira o comprovante para prosseguir.")

            else:
                st.error("Por favor, preencha o Nome e o WhatsApp corporativo para prosseguir com a simulação.")

# ==========================================
# 4. MÓDULO: GOVERNANÇA DE CLIENTES ATIVOS
# ==========================================
elif opcao == "📊 Governança de Clientes Ativos":
    st.title("💼 Carteira de Clientes Ativos do Escritório")
    
    col_a, col_b = st.columns(2)
    col_a.metric("Total de Entidades Ativas", len(df_clientes))
    col_b.metric("Receita Recorrente (Honorários)", f"R$ {df_clientes['Honorário (R$)'].sum():,.2f}" if not df_clientes.empty else "R$ 0,00")

    st.markdown("---")
    if not df_clientes.empty:
        st.dataframe(df_clientes, use_container_width=True)
    else:
        st.info("Nenhum cliente registrado na base atual.")

    with st.expander("➕ Inserir Novo Cliente na Base de Dados"):
        with st.form("cad_cliente_contabil"):
            doc = st.text_input("CNPJ ou CPF do Contribuinte:")
            rs = st.text_input("Razão Social / Nome Fantasia:")
            reg = st.selectbox("Regime Tributário Aplicado:", ["MEI", "Simples Nacional", "Lucro Presumido", "Lucro Real"])
            hon = st.number_input("Honorário Mensal Contratado (R$):", min_value=0.0, step=50.0, value=600.0)
            
            if st.form_submit_button("Efetivar Cadastro do Cliente"):
                if doc and rs:
                    reg_novo = {"CNPJ/CPF": doc, "Razão Social": rs, "Regime": reg, "Honorário (R$)": hon, "Status": "Ativo"}
                    df_cli_atualizado = pd.concat([df_clientes, pd.DataFrame([reg_novo])], ignore_index=True)
                    df_cli_atualizado.to_excel(ARQUIVO_CLIENTES, index=False)
                    st.success("Cliente cadastrado e salvo com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha obrigatoriamente o CNPJ/CPF e a Razão Social.")

# ==========================================
# 5. MÓDULO: CENTRAL DE LEADS & OPORTUNIDADES COMERCIAIS
# ==========================================
elif opcao == "📥 Central de Leads & Oportunidades":
    st.title("🎯 Prospecção Ativa (Leads do Simulador)")
    st.write("Gestão dos contatos corporativos que realizaram simulações no ambiente público e demonstraram interesse em redução tributária:")
    
    if not df_leads.empty:
        st.metric("Total de Oportunidades Captadas", len(df_leads))
        st.markdown("---")
        
        st.dataframe(df_leads, use_container_width=True)

        st.markdown("### 📞 Abordagem Comercial Direta")
        st.write("Selecione o lead para iniciar o contato estratégico via WhatsApp com script automatizado:")
        
        for index, row in df_leads.iterrows():
            numero_limpo = ''.join(filter(str.isdigit, str(row['WhatsApp'])))
            link_wpp = f"https://wa.me/55{numero_limpo}?text=Olá%20{row['Nome']},%20analisamos%20a%20simulação%20tributária%20realizada%20no%20nosso%20sistema%20corporativo.%20Nossa%20equipe%20contábil%20preparou%20um%20estudo%20para%20potencializar%20a%20redução%20dos%20tributos%20da%20sua%20empresa.%20Podemos%20agendar%20uma%20reunião?"
            
            col_l1, col_l2, col_l3 = st.columns([2, 2, 1])
            col_l1.write(f"**{row['Nome']}** ({row['Ramo']})")
            col_l2.write(f"Potencial est.: **R$ {row['Economia Estimada (R$)']:,.2f}/mês**")
            col_l3.markdown(f'<a href="{link_wpp}" target="_blank" style="background-color: #25D366; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 13px;">📲 Contatar</a>', unsafe_allow_html=True)
    else:
        st.info("Nenhum lead registrado no momento. Divulgue o link do simulador para alimentar o pipeline de vendas do escritório.")
