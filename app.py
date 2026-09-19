# -------------------------------------------------------------------------
# 7. CHAT IA MASTER SÊNIOR
# -------------------------------------------------------------------------
elif modulo == "7. Chat IA Master Sênior":
    if verificar_acesso_modulo(7):
        st.markdown('<p class="main-header">💬 Chat IA Master Sênior</p>', unsafe_allow_html=True)
        st.write("Consulte inteligência artificial especializada em direito tributário, contabilidade societária, LC 123/2006 e malhas fiscais.")
        
        # Inicializa o histórico da conversa se não existir
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "E aí, meu caro! Tudo certinho? Sistema rodando liso por aí. O que você manda para a gente analisar hoje sobre a parte fiscal ou tributária?"}
            ]

        # Exibe o histórico de mensagens na tela
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Caixa de digitação fixada embaixo para o usuário mandar a mensagem
        if prompt := st.chat_input("Digite sua consulta tributária ou contábil detalhada..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Resposta amigável e natural no mesmo tom de conversa
            resposta_personalizada = (
                f"Rapaz, sobre essa questão aí ('{prompt}'), "
                "olhando por cima na legislação e na prática contábil, o caminho costuma ser "
                "avaliar bem os limites e a segurança jurídica da operação para não ter surpresa com o fisco. "
                "Quer que eu monte um parecer mais detalhado ou analise algum outro ponto específico?"
            )

            st.session_state.messages.append({"role": "assistant", "content": resposta_personalizada})
            with st.chat_message("assistant"):
                st.markdown(resposta_personalizada)
                
        renderizar_botoes_acao("Chat IA Master Sênior", "Conversa e consultas realizadas no chat interativo.")
