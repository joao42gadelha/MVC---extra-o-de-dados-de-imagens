import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
chave = os.environ.get("GEMINI_API_KEY")

if not chave:
    print("❌ Baka! A chave GEMINI_API_KEY não foi encontrada no ficheiro .env!")
else:
    print("✨ A tentar ligar à IA com a biblioteca atualizada...")
    try:
        client = genai.Client(api_key=chave)
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Diga apenas 'Conexão bem sucedida, mestre!' e mais nada."
        )
        print(f"✅ Sucesso! A IA respondeu: {resposta.text}")
    except Exception as e:
        print(f"❌ Erro na ligação: {e}")