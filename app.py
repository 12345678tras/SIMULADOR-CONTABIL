import streamlit as st
import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma de Engenharia e IA",
    page_icon="🏗️",
    layout="wide",
)

# ==========================================
# 2. CONTROLE DE TEMA (MODO ESCURO / CLARO)
# ==========================================
modo_escuro = st.sidebar.toggle("🌙 Ativar Modo Escuro", value=False)

if modo_escuro:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .main-header { font-size: 28px; font-weight: bold; color: #60A5FA; }
        .sub-header { font-size: 16px; color: #9CA3AF; }
        .box-pagamento { background-color: #1F2937; padding: 25px; border-radius: 12px; border: 3px solid #3B82F6; margin-bottom: 20px; }
        .btn-pagar { background-color: #059669; color: white !important; padding: 14px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: block; text-align: center; margin-top: 10px; }
        .pix-box-baixo { background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #10B981; text-align: center; margin-top: 15px; }
        </style>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFFFFF; color: #111827; }
        .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
        .sub-header { font-size: 16px; color: #4B5563; }
        .box-pagamento { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border: 3px solid #2563EB; margin-bottom: 20px; }
        .btn-pagar { background-color: #059669; color: white !important; padding: 14px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: block; text-align: center; margin-top: 10px; }
        .pix-box-baixo { background-color: #ECFDF5; padding: 15px; border-radius: 8px; border: 1px solid #10B981; text-align: center; margin-top: 15px; }
        </style>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# 3. GERENCIAMENTO DE ESTADO (SESSION STATE)
# ==========================================
if "liberado_pago" not in st.session_state:
    st.session_state.liberado_pago = False

if "uso_modulos" not in st.session_state:
    st.session_state.uso_modulos = {}

if "historico_comprovantes" not in st.session_state:
    st.session_state.historico_comprovantes = []

# Controle rigoroso de 4 acessos gratuitos na IA
if "contador_ia_gratis" not in st.session_state:
    st.session_state.contador_ia_gratis = 0

if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = [
        {
            "role": "assistant",
            "content": (
                "Fala, meu irmão! Sou o engenheiro virtual da Construtech Tubarão. "
                "Você tem **4 consultas gratuitas** para testar. "
                "Pode mandar sua dúvida do seu jeito, que eu te ajudo na obra!"
            ),
        }
    ]

# ==========================================
# 4. MENU LATERAL E PAINEL ADMINISTRADOR
# ==========================================
st.sidebar.title("Navegação de Módulos")
lista_modulos = [
    "📊 Visão Geral e BDI",
    "🧱 Alvenaria Completa (Blocos, Cimento e Areia)",
    "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)",
    "🏗️ Concreto, Traços e Volume Estrutural",
    "⚙️ Projeto de Aço, Custo e Auditoria de Armadura",
    "🏗️ Estrutural, Vigas, Bitolas e Aços",
    "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)",
    "🎨 Revestimento, Acabamento e Pintura",
    "🏠 Cobertura e Telhado",
    "⚡ Elétrica Básica Residencial",
    "📅 Cronograma Físico-Financeiro (Curva S)",
    "📝 Gerador de Contrato de Empreitada",
    "💼 Faturamento e CNPJ",
    "🤖 Assistente IA (Engenheiro Virtual Inteligente)",
]

modulo = st.sidebar.selectbox("Selecione a Ferramenta:", lista_modulos)

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel do Administrador"):
    senha_admin_input = st.text_input("Digite sua chave de liberação:", type="password", key="input_senha_adm")
    if st.button("🔓 Ativar Acesso Mestre"):
        senha_tratada = senha_admin_input.strip().upper()
        if senha_tratada in ["CONSTRUTECH12", "CONSTRUTECH", "CONTRUTECH12", "CONTRUTECH"]:
            st.session_state.liberado_pago = True
            st.success("Acesso Administrador liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave incorreta!")

    if st.session_state.liberado_pago:
        st.info("Status atual: **MODO MASTER LIBERADO 🔓**")

if st.sidebar.button("🔄 Resetar Sessão (Simular Novo Cliente)"):
    st.session_state.uso_modulos = {}
    st.session_state.contador_ia_gratis = 0
    st.session_state.liberado_pago = False
    st.rerun()

# ==========================================
# 5. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown('<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Plataforma Profissional com Inteligência de Canteiro e Engenharia</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ==========================================
# FUNÇÃO DE BLOQUEIO DE MÓDULOS APÓS AMOSTRA
# ==========================================
def executar_com_controle_amostra(nome_modulo, funcao_conteudo):
    if nome_modulo not in st.session_state.uso_modulos:
        st.session_state.uso_modulos[nome_modulo] = "livre"

    status_atual = st.session_state.uso_modulos[nome_modulo]

    if status_atual == "bloqueado" and not st.session_state.liberado_pago:
        st.markdown(f'<p class="main-header">🔒 Amostra Grátis Utilizada: {nome_modulo}</p>', unsafe_allow_html=True)
        st.info("💡 Você já utilizou sua consulta gratuita neste módulo. Para continuar acessando, realize o pagamento de **R$ 20,00** para **CAC CONTABILIZANDO**[span_0](start_span)[span_0](end_span) ou insira sua chave de acesso mestre ao lado.")

        st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
        col_pag1, col_pag2 = st.columns(2, gap="large")

        with col_pag1:
            st.markdown("### 1️⃣ Forma de Pagamento (Pix / Cartão)")
            st.markdown(
                '<a href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00" target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div class="pix-box-baixo">
                    <p style="margin: 0 0 5px 0; font-size: 14px; font-weight: bold;">Ou pague via Pix Direto:</p>
                    <p style="margin: 0; font-size: 13px;">Chave Pix (Telefone):</p>
                    <code style="font-size: 16px; background: rgba(0,0,0,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold;">+5564993044147</code>[span_1](start_span)[span_1](end_span)
                    <p style="margin: 5px 0 0 0; font-size: 12px;">Favorecido: <b>CAC CONTABILIZANDO</b></p>[span_2](start_span)[span_2](end_span)
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_pag2:
            st.markdown("### 2️⃣ Liberar com Comprovante")
            comprovante_texto = st.text_area(
                "Comprovante de Pagamento:", 
                key=f"comp_{nome_modulo}", 
                placeholder="Cole o ID do Pix ou dados da transferência...",
                height=120
            )
            
            if st.button("✨ Validar e Liberar Acesso", key=f"btn_gerar_{nome_modulo}", type="primary", use_container_width=True):
                if comprovante_texto.strip() != "":
                    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    st.session_state.historico_comprovantes.append({
                        "modulo": nome_modulo,
                        "comprovante": comprovante_texto.strip(),
                        "data": data_atual
                    })
                    st.session_state.liberado_pago = True
                    st.success("Acesso liberado com sucesso!")
                    st.rerun()
                else:
                    st.warning("⚠️ Insira o comprovante de pagamento.")

        st.markdown('</div>', unsafe_allow_html=True)
        return

    funcao_conteudo()

# ==========================================
# 6. MÓDULOS DO SISTEMA
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    def conteudo():
        st.subheader("Painel de Controle e Viabilidade Comercial")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nome do Projeto / Cliente:", value="Obra Residencial Exemplo", key="bdi_cli")
            custo_base = st.number_input("Custo Direto Total Estimado (R$):", min_value=0.0, value=50000.0, step=1000.0, key="bdi_custo")
        with col2:
            bdi_taxa = st.slider("Taxa de BDI Aplicada (%):", 0.0, 50.0, 25.0, key="bdi_taxa")

        if st.button("Calcular Viabilidade e Venda", type="primary", key="btn_bdi"):
            preco_venda = custo_base * (1 + bdi_taxa / 100)
            lucro_estimado = preco_venda - custo_base
            st.success("Viabilidade calculada com sucesso!")
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Preço Final de Venda", f"R$ {preco_venda:,.2f}")
            col_m2.metric("Lucro Bruto Estimado", f"R$ {lucro_estimado:,.2f}")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🧱 Alvenaria Completa (Blocos, Cimento e Areia)":
    def conteudo():
        st.subheader("🧱 Dimensionamento e Soma de Insumos de Alvenaria")
        col1, col2 = st.columns(2)
        with col1:
            area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0, step=1.0, key="alv_area")
            tipo_material = st.selectbox(
                "Escolha a Variedade do Bloco / Tijolo:", 
                [
                    "Bloco Cerâmico 9x19x19 cm (Vedação)", 
                    "Bloco Cerâmico 14x19x19 cm (Estrutural/Vedação)", 
                    "Bloco de Concreto 14x19x39 cm", 
                    "Tijolo Baiano 8 furos (9x19x19 cm)", 
                    "Tijolo Maciço / Comum"
                ],
                key="alv_tipo"
            )
            preco_unidade = st.number_input("Preço Unitário do Bloco/Tijolo (R$):", value=1.20, step=0.10, key="alv_pr_bloco")
        with col2:
            preco_cimento = st.number_input("Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00, key="alv_pr_cim")
            preco_m3_areia = st.number_input("Preço do m³ de Areia Média (R$):", value=120.00, step=10.00, key="alv_pr_areia")

        if st.button("Calcular Soma Total da Alvenaria", type="primary", key="btn_calc_alv"):
            if "9x19x19" in tipo_material or "Baiano" in tipo_material:
                qtd_blocos_m2 = 25
                vol_arg = 0.018
            elif "14x19x19" in tipo_material:
                qtd_blocos_m2 = 25
                vol_arg = 0.025
            elif "Concreto 14x19x39" in tipo_material:
                qtd_blocos_m2 = 12.5
                vol_arg = 0.020
            else:
                qtd_blocos_m2 = 90
                vol_arg = 0.040

            total_blocos = area_paredes * qtd_blocos_m2 * 1.05
            total_arg = area_paredes * vol_arg * 1.05
            sacos_c = total_arg * 7.5
            m3_a = total_arg * 1.05

            custo_bl = total_blocos * preco_unidade
            custo_ci = sacos_c * preco_cimento
            custo_ar = m3_a * preco_m3_areia
            custo_tot = custo_bl + custo_ci + custo_ar

            st.success("Soma de alvenaria concluída com sucesso!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Blocos/Tijolos Totais", f"{int(total_blocos)} un")
            c2.metric("Sacos de Cimento", f"{sacos_c:.1f} sc")
            c3.metric("Areia Média", f"{m3_a:.2f} m³")
            st.info(f"💰 **Soma do Custo Total da Alvenaria:** `R$ {custo_tot:,.2f}`")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    def conteudo():
        st.subheader("🏠 Dimensionamento, Variedade e Ferro da Laje")
        col1, col2 = st.columns(2)
        with col1:
            area_laje = st.number_input("Área Total da Laje (m²):", min_value=1.0, value=50.0, step=1.0, key="laje_area")
            tipo_enchimento = st.selectbox(
                "Variedade de Enchimento da Laje:",
                ["Lajota Cerâmica Tradicional", "Bloco de Isopor (EPS - Alta Densidade)", "Lajota Concreto / Paulistinha"],
                key="laje_enchimento"
            )
        with col2:
            st.selectbox(
                "Altura da Laje (Vigota + Capa):",
                ["H8 (11 cm total)", "H12 (16 cm total)", "H16 (20 cm total)", "H20 (25 cm total)"],
                key="laje_altura"
            )

        if st.button("Calcular Materiais e Ferro da Laje", type="primary", key="btn_calc_laje"):
            ml_vigotas = area_laje * 1.35
            qtd_blocos = area_laje * 8.3 if "Cerâmica" in tipo_enchimento else area_laje * 2.5
            vol_concreto_m3 = area_laje * 0.070 * 1.07

            st.success("Soma de materiais da laje realizada!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} m")
            c2.metric("Blocos / Lajotas", f"{int(qtd_blocos)} un")
            c3.metric("Concreto (Capa)", f"{vol_concreto_m3:.2f} m³")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    def conteudo():
        st.subheader("🏗️ Dimensão, Espessura e Soma de Sacos de Cimento (Traço)")
        col1, col2 = st.columns(2)
        with col1:
            area_concreto = st.number_input("Metragem da Área / Piso (m²):", min_value=1.0, value=50.0, key="conc_area")
            espessura_cm = st.number_input("Espessura da Camada/Laje (cm):", min_value=1.0, value=7.0, key="conc_esp")
        with col2:
            st.selectbox(
                "Variedade do Traço de Concreto:",
                ["Traço 1:2:3 (Fck 25 MPa)", "Traço 1:2.5:3.5 (Fck 20 MPa)", "Traço 1:3:5 (Contrapiso)"],
                key="conc_traco"
            )

        if st.button("Calcular Volume e Quantidade de Sacos", type="primary", key="btn_calc_conc"):
            volume_real = (area_concreto * (espessura_cm / 100.0)) * 1.07 
            sc_cif = volume_real * 7.5
            areia_m3 = volume_real * 0.55
            brita_m3 = volume_real * 0.75

            st.success("Cálculo de concreto finalizado!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Volume Total com Perda", f"{volume_real:.2f} m³")
            c2.metric("Sacos de Cimento", f"{sc_cif:.1f} sacos")
            c3.metric("Areia / Brita", f"{areia_m3:.2f} m³ / {brita_m3:.2f} m³")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
    def conteudo():
        st.subheader("⚙️ Projeto Geral de Aço e Auditoria")
        area_obra = st.number_input("Área Construída Total (m²):", min_value=10.0, value=120.0, key="aco_geral_area")
        preco_aco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, key="aco_geral_pr")
        if st.button("Gerar Auditoria de Aço", type="primary", key="btn_calc_aco_geral"):
            peso_tot = area_obra * 14.0 
            custo_tot_aco = peso_tot * preco_aco_kg
            st.success("Auditoria gerada!")
            c1, c2 = st.columns(2)
            c1.metric("Peso Estimado de Aço", f"{peso_tot:.1f} kg")
            c2.metric("Custo Total do Aço", f"R$ {custo_tot_aco:,.2f}")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    def conteudo():
        st.subheader("🏗️ Dimensionamento de Vigas, Colunas e Bitolas de Ferro")
        col1, col2 = st.columns(2)
        with col1:
            vao_viga = st.number_input("Vão Livre da Viga ou Coluna (metros):", min_value=1.0, value=4.0, key="viga_vao")
            qtd_pecas = st.number_input("Quantidade de Vigas/Colunas iguais:", min_value=1, value=4, key="viga_qtd")
        with col2:
            tipo_bitola_principal = st.selectbox(
                "Bitola do Ferro Principal:",
                ["Ferro 3/8'' (10.0 mm)", "Ferro 5/16'' (8.0 mm)", "Ferro 1/2'' (12.5 mm)"],
                key="viga_bitola"
            )

        if st.button("Calcular Quantidade de Ferro das Vigas", type="primary", key="btn_calc_vigas"):
            kg_por_viga = vao_viga * 8.5 * qtd_pecas
            estribos_un = int((vao_viga / 0.12) * qtd_pecas)
            
            st.success("Dimensionamento de vigas concluído!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Ferro Principal", tipo_bitola_principal)
            c2.metric("Peso Total", f"{kg_por_viga:.1f} kg")
            c3.metric("Estribos", f"{estribos_un} un")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    def conteudo():
        st.subheader("🚰 Quantitativo de Canos, Conexões e Fossa para Banheiro e Cozinha")
        col1, col2 = st.columns(2)
        with col1:
            qtd_banheiros = st.number_input("Número de Banheiros Completos:", min_value=1, value=1, step=1, key="hid_banh")
            qtd_cozinhas = st.number_input("Número de Cozinhas:", min_value=1, value=1, step=1, key="hid_coz")
        with col2:
            distancia_fossa = st.number_input("Distância até a Fossa (metros):", min_value=2.0, value=10.0, step=1.0, key="hid_dist")

        if st.button("Calcular Soma de Peças Hidráulicas", type="primary", key="btn_calc_hid"):
            cano_esgoto_100 = (qtd_banheiros * 6.0) + distancia_fossa
            cano_agua_25 = (qtd_banheiros * 8.0) + (qtd_cozinhas * 6.0)

            st.success("Soma hidráulica gerada com sucesso!")
            st.write(f"- Tubo Esgoto 100mm: **{cano_esgoto_100:.1f} metros**")
            st.write(f"- Tubo Água Fria 25mm: **{cano_agua_25:.1f} metros**")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🎨 Revestimento, Acabamento e Pintura":
    def conteudo():
        st.subheader("🎨 Cálculo de Reboco, Pintura e Pisos/Porcelanatos")
        col1, col2 = st.columns(2)
        with col1:
            area_rev = st.number_input("Área de Paredes para Reboco/Pintura (m²):", min_value=1.0, value=100.0, key="rev_parede")
            demãos_tinta = st.slider("Número de Demãos de Tinta:", 1, 4, 2, key="rev_demaos")
        with col2:
            area_piso = st.number_input("Área de Piso para Revestimento (m²):", min_value=1.0, value=60.0, key="rev_piso")
            taxa_perda_piso = st.slider("Taxa de Perda de Recorte de Piso (%):", 5, 20, 10, key="rev_perda")

        if st.button("Calcular Revestimento e Acabamento", type="primary", key="btn_calc_rev"):
            sacos_arg_reboco = (area_rev * 0.025) * 18
            litros_tinta = (area_rev * demãos_tinta) / 10
            piso_com_perda = area_piso * (1 + taxa_perda_piso / 100.0)

            st.success("Cálculo de acabamento concluído!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Argamassa Reboco", f"{sacos_arg_reboco:.1f} sc (20kg)")
            c2.metric("Tinta Estimada", f"{litros_tinta:.1f} litros")
            c3.metric("Piso c/ Recorte", f"{piso_com_perda:.1f} m²")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏠 Cobertura e Telhado":
    def conteudo():
        st.subheader("🏠 Quantitativo de Telhas, Caibros e Ripas")
        col1, col2 = st.columns(2)
        with col1:
            proj_chao = st.number_input("Área de Projeção em Planta do Telhado (m²):", min_value=1.0, value=80.0, key="telh_proj")
            tipo_telha = st.selectbox("Modelo de Telha:", ["Telha Colonial / Cerâmica", "Telha de Fibrocimento", "Telha Metálica / Sanduíche"], key="telh_tipo")
        with col2:
            inclinacao = st.slider("Inclinação Estimada (%):", 10, 45, 30, key="telh_inc")

        if st.button("Calcular Estrutura do Telhado", type="primary", key="btn_calc_telh"):
            area_real = proj_chao * (1 + (inclinacao / 100.0) * 0.3)
            if "Colonial" in tipo_telha:
                qtd_telhas = area_real * 16
            elif "Fibrocimento" in tipo_telha:
                qtd_telhas = area_real * 0.55
            else:
                qtd_telhas = area_real * 1.1

            ml_caibros = area_real * 3.5
            ml_ripas = area_real * 7.0

            st.success("Dimensionamento de telhado finalizado!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Área Real do Telhado", f"{area_real:.1f} m²")
            c2.metric("Quantidade de Telhas", f"{int(qtd_telhas)} un")
            c3.metric("Madeiramento (Caibros/Ripas)", f"{ml_caibros:.0f}m / {ml_ripas:.0f}m")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "⚡ Elétrica Básica Residencial":
    def conteudo():
        st.subheader("⚡ Estimativa de Eletrodutos, Caixas e Fios")
        col1, col2 = st.columns(2)
        with col1:
            area_casa = st.number_input("Área Construída para Elétrica (m²):", min_value=10.0, value=90.0, key="el_area")
            qtd_comodos = st.number_input("Número de Cômodos / Quartos / Salas:", min_value=1, value=6, key="el_com")
        with col2:
            st.write("Parâmetros automáticos baseados na NBR 5410 para residências.")

        if st.button("Calcular Insumos Elétricos", type="primary", key="btn_calc_eletrica"):
            m_conduite = area_casa * 2.2
            caixas_4x2 = qtd_comodos * 5
            caixas_4x4 = qtd_comodos * 1

            st.success("Orçamento elétrico calculado com sucesso!")
            c1, c2 = st.columns(2)
            c1.metric("Eletrodutos Corrugados", f"{m_conduite:.1f} metros")
            c2.metric("Caixas 4x2 / 4x4", f"{caixas_4x2} / {caixas_4x4} un")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "📅 Cronograma Físico-Financeiro (Curva S)":
    def conteudo():
        st.subheader("📅 Distribuição de Custos por Etapas da Obra")
        custo_total_obra = st.number_input("Custo Total Estimado da Obra (R$):", value=150000.0, key="curva_val")
        
        if st.button("Gerar Cronograma de Gastos", type="primary", key="btn_calc_curvas"):
            fase_fundacao = custo_total_obra * 0.15
            fase_estrutura = custo_total_obra * 0.25
            fase_alvenaria = custo_total_obra * 0.15
            fase_cobertura = custo_total_obra * 0.10
            fase_instalacoes = custo_total_obra * 0.15
            fase_acabamento = custo_total_obra * 0.20

            st.success("Curva S e Cronograma gerados!")
            st.write(f"- **1. Fundação:** R$ {fase_fundacao:,.2f} (15%)")
            st.write(f"- **2. Estrutura:** R$ {fase_estrutura:,.2f} (25%)")
            st.write(f"- **3. Alvenaria:** R$ {fase_alvenaria:,.2f} (15%)")
            st.write(f"- **4. Cobertura:** R$ {fase_cobertura:,.2f} (10%)")
            st.write(f"- **5. Instalações:** R$ {fase_instalacoes:,.2f} (15%)")
            st.write(f"- **6. Acabamentos:** R$ {fase_acabamento:,.2f} (20%)")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "📝 Gerador de Contrato de Empreitada":
    def conteudo():
        st.subheader("📝 Emissor de Minuta de Contrato de Prestação de Serviços")
        col1, col2 = st.columns(2)
        with col1:
            contratante = st.text_input("Nome do Contratante (Cliente):", value="João da Silva", key="ct_cli")
            st.text_input("Nome do Engenheiro / Construtor:", value="Futuro Engenheiro", key="ct_eng")
        with col2:
            valor_contrato = st.number_input("Valor Total do Contrato (R$):", value=80000.0, key="ct_val")
            prazo_meses = st.number_input("Prazo de Execução (meses):", min_value=1, value=6, key="ct_mes")

        if st.button("Gerar Contrato Completo", type="primary", key="btn_calc_contrato"):
            st.success("Contrato gerado com sucesso!")
            minuta_texto = f"""CONTRATO PARTICULAR DE PRESTAÇÃO DE SERVIÇOS
CONSTRUTECH TUBARÃO
CONTRATANTE: {contratante}
VALOR: R$ {valor_contrato:,.2f}
PRAZO: {prazo_meses} meses
"""
            st.text_area("Visualização do Contrato:", value=minuta_texto, height=200)
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "💼 Faturamento e CNPJ":
    def conteudo():
        st.subheader("Orçamento Comercial e Proposta de Serviços")
        valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0, key="fat_val")
        if st.button("Emitir Proposta", type="primary", key="btn_calc_fat"):
            st.success(f"Proposta emitida no valor de R$ {valor_bruto:,.2f}!")
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

# ==========================================
# 7. ASSISTENTE IA COM RECONHECIMENTO AMPLO DE GÍRIAS DE OBRA
# ==========================================
elif modulo == "🤖 Assistente IA (Engenheiro Virtual Inteligente)":
    def conteudo_ia():
        st.subheader("🤖 Engenheiro Virtual Inteligente - Construtech Tubarão")
        
        consultas_restantes = max(0, 4 - st.session_state.contador_ia_gratis)
        if not st.session_state.liberado_pago:
            if consultas_restantes > 0:
                st.info(f"🎁 Você tem **{consultas_restantes} consulta(s) gratuita(s)** restantes com o Engenheiro Virtual.")
            else:
                st.warning("⚠️ Suas 4 consultas gratuitas da IA acabaram. Realize o pagamento abaixo para liberar o acesso ilimitado.")

        for msg in st.session_state.mensagens_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.contador_ia_gratis >= 4 and not st.session_state.liberado_pago:
            st.markdown("---")
            st.markdown("### 🔒 Desbloqueie o Assistente IA Ilimitado")
            st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
            col_pag1, col_pag2 = st.columns(2, gap="large")

            with col_pag1:
                st.markdown("### 1️⃣ Forma de Pagamento (Pix / Cartão)")
                st.markdown(
                    '<a href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00" target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <div class="pix-box-baixo">
                        <p style="margin: 0 0 5px 0; font-size: 14px; font-weight: bold;">Ou pague via Pix Direto:</p>
                        <p style="margin: 0; font-size: 13px;">Chave Pix (Telefone):</p>
                        <code style="font-size: 16px; background: rgba(0,0,0,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold;">+5564993044147</code>[span_3](start_span)[span_3](end_span)
                        <p style="margin: 5px 0 0 0; font-size: 12px;">Favorecido: <b>CAC CONTABILIZANDO</b></p>[span_4](start_span)[span_4](end_span)
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_pag2:
                st.markdown("### 2️⃣ Liberar com Comprovante")
                comprovante_texto = st.text_area(
                    "Comprovante de Pagamento:", 
                    key="comp_ia_chat", 
                    placeholder="Cole o ID do Pix ou dados da transferência...",
                    height=120
                )
                
                if st.button("✨ Validar e Liberar Acesso da IA", key="btn_gerar_ia_chat", type="primary", use_container_width=True):
                    if comprovante_texto.strip() != "":
                        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        st.session_state.historico_comprovantes.append({
                            "modulo": "Assistente IA Completo",
                            "comprovante": comprovante_texto.strip(),
                            "data": data_atual
                        })
                        st.session_state.liberado_pago = True
                        st.success("Acesso liberado com sucesso!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Insira o comprovante de pagamento.")

            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            if prompt_usuario := st.chat_input("Ex: 'Quantos blocos gastam no muro?' ou 'Quanto de cimento pro piso?'"):
                if not st.session_state.liberado_pago:
                    st.session_state.contador_ia_gratis += 1

                st.session_state.mensagens_chat.append({"role": "user", "content": prompt_usuario})
                with st.chat_message("user"):
                    st.markdown(prompt_usuario)

                with st.chat_message("assistant"):
                    with st.spinner("Consultando parâmetros de canteiro..."):
                        pergunta_lower = prompt_usuario.lower()
                        
                        # Motor IA Inteligente para Gírias e Linguagem Simples de Obra
                        if any(p in pergunta_lower for p in ["tijolo", "bloco", "tijolao", "tijolão", "material", "parede", "muro", "erguer", "levantar", "quantos"]):
                            if any(p in pergunta_lower for p in ["cimento", "argamassa", "reboco", "concreto", "chão", "piso", "contrapiso"]):
                                resposta_ia = (
                                    "📊 **Cimento para assentar blocos/tijolos:**\n\n"
                                    "Para cada metro quadrado (m²) de parede, gasta-se em média **metade de um saco até um saco de cimento** misturado com a areia. "
                                    "No total, para cada metro cúbico de argamassa de assentamento, vão cerca de **7 a 8 sacos de cimento**."
                                )
                            else:
                                resposta_ia = (
                                    "🧱 **Quantos blocos ou tijolos gastam por metro quadrado (m²):**\n\n"
                                    "- **Tijolo Baiano / Bloco Cerâmico (9x19x19cm):** Gasta uns **25 tijolos por m²** de parede.\n"
                                    "- **Bloco de Concreto (14x19x39cm):** Gasta uns **12,5 blocos por m²**.\n"
                                    "- **Tijolo Maciço (comum):** Gasta uns **90 a 100 tijolos por m²** (em pé).\n\n"
                                    "*(Dica: Compre sempre **5% a mais** para quebras!)*"
                                )

                        elif any(p in pergunta_lower for p in ["cimento", "saco", "sacos", "pó", "po", "argamassa", "reboco", "chapisco", "piso", "contrapiso", "concreto"]):
                            if any(p in pergunta_lower for p in ["piso", "contrapiso", "chão", "calcada", "calçada"]):
                                resposta_ia = (
                                    "🏠 **Cimento para Contrapiso ou Piso:**\n\n"
                                    "Para fazer um contrapiso de 5 cm de espessura, gasta-se mais ou menos **1,5 a 2 sacos de cimento de 50kg** para cada **10 metros quadrados (m²)** de piso aplicado."
                                )
                            elif any(p in pergunta_lower for p in ["reboco", "mão de obra", "parede"]):
                                resposta_ia = (
                                    "🎨 **Cimento para Reboco:**\n\n"
                                    "No reboco (com grossura de 2cm), gasta-se em média **4 a 5 kg de cimento por m²** de parede rebocada."
                                )
                            else:
                                resposta_ia = (
                                    "📦 **Contas gerais de cimento na obra:**\n\n"
                                    "- **Assentamento de bloco/tijolo:** Cerca de **5 a 6 kg de cimento** por m².\n"
                                    "- **Reboco (2cm):** Cerca de **4 a 5 kg de cimento** por m².\n"
                                    "- **Contrapiso (5cm):** Cerca de **1,5 a 2 sacos** para cada 10 m²."
                                )

                        elif any(p in pergunta_lower for p in ["ferro", "aço", "aco", "viga", "coluna", "baldrames", "estribo", "bitola"]):
                            resposta_ia = (
                                "⚙️ **Ferro e Aço (Vigas e Colunas):**\n\n"
                                "Para casas térreas comuns, a média fica em torno de **14 kg de aço por metro quadrado (m²)** de construção.\n"
                                "Use sempre ferro de boa procedência conforme as orientações de projeto!"
                            )

                        elif any(p in pergunta_lower for p in ["agua", "água", "esgoto", "cano", "tubo", "banheiro", "cozinha", "fossa"]):
                            resposta_ia = (
                                "🚰 **Hidráulica (Canos e Saídas):**\n\n"
                                "- Para **água fria**, use cano de **25mm**.\n"
                                "- Para **esgoto**, use cano de **100mm** na saída do vaso e **40mm/50mm** para pias e ralos."
                            )

                        else:
                            resposta_ia = (
                                f"Falei com o sistema aqui sobre **'{prompt_usuario}'**, mas para não errar na conta, "
                                "me diz exato: é para **parede (tijolo/bloco)**, **cimento/argamassa**, **piso**, ou **ferro**? "
                                "Assim eu te passo o número exato na lata!"
                            )
                        
                        st.markdown(resposta_ia)
                        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
                
                st.rerun()

    executar_com_controle_amostra("Assistente IA (Engenheiro Virtual Inteligente)", conteudo_ia)

# ==========================================
# 8. RODAPÉ DA APLICAÇÃO
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
