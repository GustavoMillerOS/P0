import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

MODELOS_DISPONIVEIS = [
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.6-flash",
]

def inicializar_cliente() -> genai.Client:
    """Carrega variáveis de ambiente e inicializa o cliente Gemini."""
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Chave GEMINI_API_KEY não encontrada. Verifique o arquivo .env.")
    return genai.Client()

def padronizar_chamado(client: genai.Client, relato_usuario: str) -> str:
    """Envia o relato informal ao LLM com fallback entre modelos em caso de sobrecarga."""
    if not relato_usuario or not relato_usuario.strip():
        raise ValueError("O relato do problema não pode estar vazio.")

    prompt = f"""
    Atue como um analista de suporte técnico (Service Desk).
    Analise o relato informal abaixo e converta-o em um chamado técnico estruturado com os seguintes campos obrigatórios:
    - **Título do Chamado:** (curto e objetivo)
    - **Serviço/Equipamento Afetado:** (sistema, rede, hardware ou software identificado)
    - **Resumo Padronizado:** (descrição técnica clara do problema)
    - **Prioridade Sugerida:** (Baixa, Média ou Alta, acompanhada de uma breve justificativa)

    Relato do usuário: "{relato_usuario.strip()}"
    """
    

    ultimo_erro = None
    for modelo in MODELOS_DISPONIVEIS:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )
            return response.text
        except APIError as e:
            ultimo_erro = e
            if "503" in str(e) or "404" in str(e):
                print(f"[Aviso] Modelo {modelo} indisponível no momento. Alternando...")
                time.sleep(1)
                continue
            raise

    raise APIError(f"Todos os modelos estão sobrecarregados no momento. Detalhe: {ultimo_erro}")

def main():
    print("=== Padronizador Automático de Chamados (Service Desk) ===\n")
    try:
        client = inicializar_cliente()
        relato = input("Descreva o problema relatado pelo usuário:\n> ")
        
        print("\nAnalisando e estruturando chamado...\n")
        chamado_formatado = padronizar_chamado(client, relato)
        chamado_limpo = chamado_formatado.replace("**", "").replace("*", "")
        
        print("-" * 50)
        print(chamado_limpo)
        print("-" * 50)

    except ValueError as erro_validacao:
        print(f"\n[Aviso de Validação]: {erro_validacao}")
    except APIError as erro_api:
        print(f"\n[Erro na API do Gemini]: {erro_api}")
    except Exception as erro_geral:
        print(f"\n[Erro Inesperado]: {erro_geral}")

if __name__ == "__main__":
    main()