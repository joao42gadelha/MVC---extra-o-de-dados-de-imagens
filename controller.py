from motor_ocr import processar_fichas_dinamicas

def executar_fluxo_ocr(dados_imagens, callback_status=None):
    print(f"Iniciando processamento de {len(dados_imagens)} ficha(s)...")
    processar_fichas_dinamicas(dados_imagens, callback_status)