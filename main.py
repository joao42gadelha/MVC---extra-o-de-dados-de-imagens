from interface import desenhar_janela
from controller import executar_fluxo_ocr

if __name__ == "__main__":
    # Inicia a interface gráfica e injeta a função do controlador no botão
    desenhar_janela(comando_iniciar=executar_fluxo_ocr)