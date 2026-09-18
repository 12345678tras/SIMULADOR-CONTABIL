import os
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Painel Mestre - Tubarão Construtor",
    page_icon="🦈",
    layout="wide",
)

# ==========================================
# SEGURANÇA E AUTENTICAÇÃO
# ==========================================


def verificar_seguranca():
    """Garante que o acesso seja restrito e seguro, validando o estado da sessão."""
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.sidebar.title("🔐 Acesso Restrito")
        chave_digitada = st.sidebar.text_input(
            "Digite a chave de segurança:", type="password"
        )

        # Defina sua chave de segurança de forma segura (ex: via variáveis de ambiente)
        chave_mestra = os.getenv("CHAVE_MESTRA_TUBARAO", "tubarao_secure_2026")

        if st.sidebar.button("Entrar"):
            if chave_digitada == chave_mestra:
                st.session_state.autenticado = True
                st.sidebar.success("Acesso autorizado!")
                st.rerun()
            else:
                st.sidebar.error("Chave inválida! Acesso negado.")
        return False
    return True


# ==========================================
# MÓDULO DE VOZ DA IA (FALA)
# ==========================================


def falar_com_usuario(texto_mensagem):
    """Utiliza recursos de síntese de voz para que a IA fale a resposta em áudio."""
    import gtts
    from io import BytesIO

    try:
        tts = gtts.gTTS(text=texto_mensagem, lang="pt", tld="com.br")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.warning(f"Não foi possível reproduzir a fala da IA: {e}")


# ==========================================
# APLICAÇÃO PRINCIPAL
# ==========================================


def main():
    st.title("🦈 Painel Mestre - Tubarão Construtor")
    st.write(
        "Ambiente seguro e protegido. Todos os protocolos de segurança estão ativos."
    )

    # Executa a barreira de segurança
    if not verificar_seguranca():
        return

    # Área restrita / Painel Administrativo
    st.sidebar.success("Painel Administrativo Ativo")
    if st.sidebar.button("Encerrar Sessão"):
        st.session_state.autenticado = False
        st.rerun()

    st.divider()

    # Interface de Interação com a IA falante
    st.subheader("🤖 Central de Comando por Voz e Texto")

    entrada_usuario = st.text_input(
        "Digite seu comando ou pergunta para o sistema:"
    )

    if st.button("Enviar Comando"):
        if entrada_usuario:
            # Resposta simulada da IA com base no comando seguro
            resposta_ia = f"Comando processado com segurança pelo sistema central. Sua solicitação sobre '{entrada_usuario}' foi executada com sucesso."

            st.success(resposta_ia)

            # A IA fala a resposta em voz alta
            falar_com_usuario(resposta_ia)
        else:
            st.warning("Por favor, digite um comando válido.")


if __name__ == "__main__":
    main()
