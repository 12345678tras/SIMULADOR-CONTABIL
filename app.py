# --- MÓDULO 10: CHAT IA (BLINDADO CONTRA ERRO 404) ---
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
                resposta_ia = None
                
                # Tentativa com o nome de modelo correto da SDK nova
                modelos_para_testar = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-flash']
                
                for mod in modelos_para_testar:
                    try:
                        response = client_ai.models.generate_content(
                            model=mod,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.2
                            )
                        )
                        if response and response.text:
                            resposta_ia = response.text
                            break
                    except Exception:
                        continue

                if resposta_ia:
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})
                else:
                    st.error("Erro ao processar com a IA. Verifique se a sua chave de API está ativa e configurada corretamente.")
