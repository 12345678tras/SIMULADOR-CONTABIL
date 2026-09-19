# ==========================================
# 2. MÓDULO: CHAT IA MASTER SÊNIOR
# ==========================================
elif modulo == "💬 Chat IA Master Sênior":
    st.title("💬 Chat IA Master Sênior - Inteligência Natural & Contábil")
    st.markdown("Bate-papo estratégico, fluido e contextualizado com a IA.")

    # Inicializa o histórico visual e a sessão de chat real do Gemini
    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = [
            {"role": "assistant", "content": "Olá! Que bom conversar com você. Estou com o meu modo de conversa natural ativado, pronto para te ajudar com ideias, dúvidas ou estratégias tributárias. O que vamos conversar agora?"}
        ]

    # Cria ou recupera a sessão de chat contínua com a IA para manter o contexto
    if "chat_sessao_gemini" not in st.session_state and client_ai:
        st.session_state.chat_sessao_gemini = client_ai.chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": (
                    "Você é um parceiro consultivo, inteligente, caloroso e altamente empático. "
                    "Converse de forma natural, fluida e amigável (como um colega especialista conversando em um chat), "
                    "evitando respostas robóticas, listas excessivas ou tom puramente acadêmico, a menos que seja estritamente necessário. "
                    "Mantenha o foco em Direito Tributário, Contabilidade e Estratégia Empresarial."
                )
            }
        )

    # Exibe as mensagens na interface do Streamlit
    for msg in st.session_state.mensagens_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Captura a nova mensagem do usuário
    pergunta_usuario = st.chat_input("Digite sua mensagem para conversarmos...")
    if pergunta_usuario:
        if not verificar_bloqueio_antes_de_usar():
            st.rerun()

        descontar_um_uso()

        # Adiciona a mensagem do usuário no histórico visual
        st.session_state.mensagens_chat.append({"role": "user", "content": pergunta_usuario})
        with st.chat_message("user"):
            st.write(pergunta_usuario)

        # Envia a mensagem para a IA mantendo o histórico da conversa
        with st.chat_message("assistant"):
            with st.spinner("Pensando na resposta..."):
                try:
                    if client_ai and "chat_sessao_gemini" in st.session_state:
                        # Envia a mensagem usando a sessão contínua do chat
                        response = st.session_state.chat_sessao_gemini.send_message(pergunta_usuario)
                        resposta_ia = response.text
                    else:
                        resposta_ia = "⚠️ Chave do Gemini não configurada ou sessão indisponível."
                except Exception as e:
                    resposta_ia = f"Ops, tive um pequeno problema ao processar: {e}"
                
                st.write(resposta_ia)
                st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
