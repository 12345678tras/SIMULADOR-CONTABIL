# ==========================================
# CONTROLE DE USO ÚNICO POR E-MAIL (BLINDADO)
# ==========================================
def verificar_status_email(email):
    if not supabase:
        return "liberado"
    try:
        email_limpo = email.strip().lower()
        res = supabase.table("acessos_email").select("*").eq("email", email_limpo).execute()
        if res.data and len(res.data) > 0:
            return "bloqueado"
    except Exception as e:
        print(f"Erro ao consultar Supabase: {e}")
    return "liberado"

def registrar_novo_usuario(email, whatsapp, razao):
    if not supabase:
        return
    try:
        email_limpo = email.strip().lower()
        # Dupla checagem para evitar inserção duplicada por concorrência
        res = supabase.table("acessos_email").select("*").eq("email", email_limpo).execute()
        if not res.data or len(res.data) == 0:
            novo_registro = {
                "email": email_limpo,
                "whatsapp": whatsapp,
                "razao_social": razao,
                "contador": 1,
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            supabase.table("acessos_email").insert(novo_registro).execute()
            
            salvar_lead_arquivo({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Razao Social": razao,
                "WhatsApp": whatsapp,
                "E-mail": email_limpo,
                "Melhor Regime": "Teste Gratuito Realizado",
                "Economia (R$)": 0.0
            })
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
