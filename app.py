elif menu == "Alertas de Oportunidades Fiscais":
  st.title("⚡ Alertas de Oportunidades Fiscais")
  st.markdown(
      "Identificação ativa de créditos tributários não aproveitados e"
      " benefícios setoriais."
  )

  st.warning(
      "⚠️ **Oportunidade Detectada:** Potenciais créditos de PIS/COFINS"
      " monofásico não apurados nos últimos 60 dias."
  )
  st.success(
      "✅ **Benefício Disponível:** Redução de alíquota efetiva para o setor"
      " de atuação."
  )

  if "varredura_executada" not in st.session_state:
    st.session_state.varredura_executada = False

  # Botão com largura total para evitar cortes visuais
  if st.button(
      "🔍 Executar Varredura de Oportunidades Fiscais",
      type="primary",
      use_container_width=True,
  ):
    with st.spinner("Executando varredura analítica na base de dados..."):
      time.sleep(1.0)
    st.session_state.varredura_executada = True
    registrar_log("Varredura de oportunidades fiscais executada localmente.")

  if st.session_state.varredura_executada:
    st.success("🚀 Varredura concluída com sucesso! Relatório gerado:")

    df_oportunidades = pd.DataFrame({
        "Tributo / Base": [
            "PIS/COFINS Monofásico",
            "Incentivo Setorial Regional",
        ],
        "Potencial Recuperável": ["R$ 8.450,00", "R$ 6.100,00"],
        "Status": ["Disponível para Compensação", "Aplicável imediatamente"],
    })
    st.dataframe(df_oportunidades, use_container_width=True)
