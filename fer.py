
import streamlit as st
import pandas as pd
import os

# Configuração visual da página
st.set_page_config(page_title="Gestão & Captação Contábil", page_icon="📈", layout="wide")

ARQUIVO_CLIENTES = "clientes_contabilidade.xlsx"
ARQUIVO_LEADS = "potenciais_clientes.xlsx"

# Função para garantir que os arquivos Excel existam
def carregar_dados(arquivo, colunas):
    if not os.path.exists(arquivo):
        df_inicial = pd.DataFrame(columns=colunas)
        df_inicial.to_excel(arquivo, index=False)
    return pd.read_excel(arquivo)

df_clientes = carregar_dados(ARQUIVO_CLIENTES, ["CNPJ/CPF", "Razão Social", "Regime", "Honorário (R$)", "Status"])
df_leads = carregar_dados(ARQUIVO_LEADS, ["Nome", "WhatsApp", "Faturamento Mensal", "Ramo", "Economia Estimada (R$)"])

# Menu Principal de Navegação
st.sidebar.title("🏢 Painel Contábil")
opcao = st.sidebar.radio("Navegação", [
    "🚀 Simulador / Captador de Clientes",
    "📊 Gestão Interna de Clientes",
    "📥 Leads Captados (Oportunidades)"
])

# --- 1. FERRAMENTA DE CAPTAÇÃO DE CLIENTES (PARA ENVIAR AOS POTENCIAIS CLIENTES) ---
if opcao == "🚀 Simulador / Captador de Clientes":
    st.title("🧮 Simulador de Economia de Impostos")
    st.write("Descubra se a sua empresa está pagando mais imposto do que deveria!")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Seu Nome ou Nome da Empresa:")
        whatsapp = st.text_input("Seu WhatsApp para Contato:")
        ramo = st.selectbox("Área de Atuação:", ["Comércio", "Prestação de Serviços", "TI / Programação", "Saúde / Médicos", "Outro"])
        faturamento = st.number_input("Faturamento Médio Mensal (R$):", min_value=1000.0, value=10000.0, step=1000.0)

    with col2:
        st.info \
            ("💡 **Como funciona?** Nós analisamos seu faturamento e calculamos a estimativa de transição para o regime tributário mais econômico.")

        if st.button("🔍 Calcular Minha Economia Agora"):
            if nome and whatsapp:
                # Estimativa visual de economia
                imposto_estimado_atual = faturamento * 0.15
                imposto_otimizado = faturamento * 0.08
                economia_mensal = imposto_estimado_atual - imposto_otimizado
                economia_anual = economia_mensal * 12

                st.success(f"🎉 **{nome}**, estimamos que você pode economizar até **R$ {economia_mensal:.2f}/mês**!")
                st.metric("Economia Anual Estimada", f"R$ {economia_anual:.2f}")

                # Salva o contato no Excel automaticamente
                novo_lead = {
                    "Nome": nome,
                    "WhatsApp": whatsapp,
                    "Faturamento Mensal": faturamento,
                    "Ramo": ramo,
                    "Economia Estimada (R$)": economia_mensal
                }
                df_leads_atualizado = pd.concat([df_leads, pd.DataFrame([novo_lead])], ignore_index=True)
                df_leads_atualizado.to_excel(ARQUIVO_LEADS, index=False)

                st.balloons()
                st.warning \
                    ("📲 Recebemos sua simulação! Nossa equipe entrará em contato via WhatsApp para apresentar o plano de transição.")
            else:
                st.error("Por favor, preencha o Nome e o WhatsApp para ver a simulação.")

# --- 2. GESTÃO INTERNA DE CLIENTES DA SUA ESPOSA ---
elif opcao == "📊 Gestão Interna de Clientes":
    st.title("📋 Carteira de Clientes Ativos")

    col_a, col_b = st.columns(2)
    col_a.metric("Total de Clientes Ativos", len(df_clientes))
    col_b.metric("Faturamento de Honorários", f"R$ {df_clientes['Honorário (R$)'].sum():.2f}")

    st.markdown("---")
    st.dataframe(df_clientes, use_container_width=True)

    with st.expander("➕ Cadastrar Novo Cliente Fixo"):
        with st.form("cad_cliente"):
            doc = st.text_input("CNPJ/CPF")
            rs = st.text_input("Razão Social")
            reg = st.selectbox("Regime", ["MEI", "Simples Nacional", "Lucro Presumido"])
            hon = st.number_input("Honorário (R$)", min_value=0.0, step=50.0)
            if st.form_submit_button("Salvar Cliente"):
                reg_novo = {"CNPJ/CPF": doc, "Razão Social": rs, "Regime": reg, "Honorário (R$)": hon, "Status": "Ativo"}
                pd.concat([df_clientes, pd.DataFrame([reg_novo])], ignore_index=True).to_excel(ARQUIVO_CLIENTES, index=False)
                st.success("Cliente cadastrado com sucesso!")

# --- 3. LISTA DE POTENCIAIS CLIENTES PARA LIGAR ---
elif opcao == "📥 Leads Captados (Oportunidades)":
    st.title("🎯 Pessoas que Usaram o Simulador (Futuros Clientes)")
    st.write("Abaixo estão as pessoas que fizeram a simulação e deixaram o WhatsApp:")
    st.dataframe(df_leads, use_container_width=True)
