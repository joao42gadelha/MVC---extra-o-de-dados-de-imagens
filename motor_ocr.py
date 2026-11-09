import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()
chave = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=chave)

def extrair_dados_dinamicos(caminho_imagem, tipo_atend, tipo_ambulancia):
    instrucao_ia = f"""
    Analise a imagem desta ficha de atendimento.
    Extraia as seguintes informações e retorne EXCLUSIVAMENTE em formato JSON estrito, sem '```json':
    
    {{
      "Data do Atendimento": "",
      "Numero da Ficha": "",
      "Nome do Paciente": "",
      "Data de Nascimento": "",
      "Local de Origem": "",
      "Local de Destino": "",
      "Tipo de Atendimento": "{tipo_atend}",
      "Tipo de Ambulancia": "{tipo_ambulancia}"
    }}
    
    Mantenha os campos "Tipo de Atendimento" e "Tipo de Ambulancia" fixos com os valores repassados.
    """
    
    ficheiro_up = client.files.upload(file=caminho_imagem)
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[ficheiro_up, instrucao_ia]
    )
    return resposta.text

def processar_fichas_dinamicas(dados_imagens, callback_status=None):
    lista_de_dados = []
    total_imagens = len(dados_imagens)

    print(f"\n--- Iniciando lote com {total_imagens} ficha(s) ---")

    for indice, (caminho, config) in enumerate(dados_imagens.items(), start=1):
        nome_arquivo = os.path.basename(caminho)
        print(f"[{indice}/{total_imagens}] Processando: {nome_arquivo}...")
        
        # Mudar para LARANJA (Em processo)
        if callback_status:
            callback_status(caminho, "processando")
        
        try:
            texto = extrair_dados_dinamicos(caminho, config["atendimento"], config["ambulancia"])
            texto_limpo = texto.strip().removeprefix("```json").removesuffix("```").strip()
            
            dicionario_ficha = json.loads(texto_limpo)
            lista_de_dados.append(dicionario_ficha)
            
            # Mudar para VERDE (Enviado / Sucesso)
            if callback_status:
                callback_status(caminho, "sucesso")
                
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")
            # Mudar para ERRO se falhar
            if callback_status:
                callback_status(caminho, "erro")

    if lista_de_dados:
        df = pd.DataFrame(lista_de_dados)
        df.to_excel("fichas_aph_consolidadas.xlsx", index=False)
        print(f"✅ Lote finalizado! {len(lista_de_dados)}/{total_imagens} fichas exportadas para o Excel com sucesso.")
    else:
        print("❌ Nenhum dado válido extraído.")