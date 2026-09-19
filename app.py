# 6. Chat IA Master Sênior
elif modulo == "Chat IA Master Sênior":
    st.markdown('<p class="main-header">💬 Chat IA Master Sênior</p>', unsafe_allow_html=True)
    st.write("Consulte inteligência artificial especializada em planejamento tributário brasileiro (LC 123/2006, CND, SPED).")
    
    # Inicializa o histórico de mensagens da IA no session_state se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe o histórico de mensagens anteriores na tela
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura a entrada do usuário pelo chat em tempo real
    if prompt := st.chat_input("Digite sua dúvida fiscal ou tributária para o Master:"):
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chama a IA utilizando a chave e as bibliotecas já configuradas na sua nuvem
        with st.chat_message("assistant"):
            try:
                import openai
                # A chave já está integrada no ambiente/secrets da sua nuvem
                client = openai.OpenAI()
                
                stream = client.chat.completions.create(
                    model="gpt-4o-mini", # Ajuste para o modelo que você utilizava se necessário
                    messages=[
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ],
                    stream=True,
                )
                
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # Caso ocorra qualquer exceção na chamada da API, exibe a mensagem de suporte
                resposta_erro = f"Olá! Sua mensagem foi recebida, mas verifiquei um detalhe na conexão da API: {e}"
                st.markdown(resposta_erro)
                st.session_state.messages.append({"role": "assistant", "content": resposta_erro})

    renderizar_botoes_acao("Chat IA Sênior", "Consulta e histórico integrados com a IA Sênior.")
