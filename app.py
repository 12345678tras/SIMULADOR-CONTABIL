from google import genai

def gerar_resposta_ia_moderna(prompt):
    try:
        gemini_api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            gemini_api_key = st.secrets["GEMINI_API_KEY"]
        elif os.environ.get("GEMINI_API_KEY"):
            gemini_api_key = os.environ.get("GEMINI_API_KEY")

        if not gemini_api_key:
            return "⚠️ Chave de API do Gemini não configurada nos Secrets."

        client = genai.Client(api_key=gemini_api_key)
        # Usando o modelo padrão oficial atual da biblioteca moderna
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        if response and hasattr(response, "text") and response.text:
            return response.text
    except Exception as e:
        return f"⚠️ Erro ao processar na IA: {e}"
    return "⚠️ Nenhuma resposta retornada."
