import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, comando_iniciar):
        super().__init__()
        self.title("Fichas Med+ | Triagem Visual OCR")
        self.geometry("900x620")
        self.comando_iniciar = comando_iniciar
        
        self.dados_imagens = {}
        self.botoes_imagens = {} # Guarda a referência de cada botão para mudar a cor
        self.imagem_atual = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Painel Esquerdo ---
        self.painel_esq = ctk.CTkFrame(self)
        self.painel_esq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.btn_carregar = ctk.CTkButton(self.painel_esq, text="Carregar Imagens", command=self.carregar_imagens)
        self.btn_carregar.pack(pady=10, padx=10, fill="x")

        self.lista_box = ctk.CTkScrollableFrame(self.painel_esq, label_text="Fichas Selecionadas (0)")
        self.lista_box.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.lbl_status = ctk.CTkLabel(self.painel_esq, text="Aguardando carregamento...", font=("Arial", 11, "italic"))
        self.lbl_status.pack(pady=(0, 5))

        self.btn_extrair = ctk.CTkButton(self.painel_esq, text="Extrair Dados (Excel)", fg_color="green", hover_color="darkgreen", command=self.iniciar_extracao)
        self.btn_extrair.pack(pady=10, padx=10, fill="x")

        # --- Painel Direito ---
        self.painel_dir = ctk.CTkFrame(self)
        self.painel_dir.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_preview = ctk.CTkLabel(self.painel_dir, text="Nenhuma imagem selecionada", width=450, height=450)
        self.lbl_preview.pack(pady=10)

        self.frame_controles = ctk.CTkFrame(self.painel_dir)
        self.frame_controles.pack(pady=10, padx=10, fill="x")

        self.var_atendimento = ctk.StringVar(value="Demanda")
        self.var_ambulancia = ctk.StringVar(value="USB")

        ctk.CTkLabel(self.frame_controles, text="Atendimento:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
        self.seg_atendimento = ctk.CTkSegmentedButton(self.frame_controles, values=["Demanda", "Contrato"], variable=self.var_atendimento, command=self.atualizar_estado)
        self.seg_atendimento.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame_controles, text="Ambulância:", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=10)
        self.seg_ambulancia = ctk.CTkSegmentedButton(self.frame_controles, values=["UTI", "USB"], variable=self.var_ambulancia, command=self.atualizar_estado)
        self.seg_ambulancia.grid(row=0, column=3, padx=10, pady=10)

    def carregar_imagens(self):
        arquivos = filedialog.askopenfilenames(title="Selecione as Fichas APH", filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        for arq in arquivos:
            if arq not in self.dados_imagens:
                self.dados_imagens[arq] = {"atendimento": "Demanda", "ambulancia": "USB"}
                nome_limpo = os.path.basename(arq)
                
                # Botão nasce VERMELHO (Não enviado / Pendente)
                btn = ctk.CTkButton(
                    self.lista_box, 
                    text=f"🔴 {nome_limpo}", 
                    fg_color="#D32F2F", 
                    hover_color="#B71C1C",
                    anchor="w", 
                    command=lambda a=arq: self.mostrar_imagem(a)
                )
                btn.pack(pady=2, fill="x")
                self.botoes_imagens[arq] = btn

        total = len(self.dados_imagens)
        self.lista_box.configure(label_text=f"Fichas Selecionadas ({total})")
        self.lbl_status.configure(text=f"{total} foto(s) pronta(s) para extração.")

    def atualizar_cor_botao(self, caminho_imagem, status):
        """Atualiza a cor e o ícone do botão em tempo real"""
        if caminho_imagem in self.botoes_imagens:
            btn = self.botoes_imagens[caminho_imagem]
            nome_limpo = os.path.basename(caminho_imagem)
            
            if status == "processando":
                btn.configure(text=f"🟠 {nome_limpo}", fg_color="#F57C00", hover_color="#E65100")
            elif status == "sucesso":
                btn.configure(text=f"🟢 {nome_limpo}", fg_color="#388E3C", hover_color="#2E7D32")
            elif status == "erro":
                btn.configure(text=f"❌ {nome_limpo}", fg_color="#B00020", hover_color="#880015")
            
            self.update_idletasks() # Força a interface a redesenhar a cor na hora

    def mostrar_imagem(self, caminho):
        self.imagem_atual = caminho
        estado = self.dados_imagens[caminho]
        
        self.var_atendimento.set(estado["atendimento"])
        self.var_ambulancia.set(estado["ambulancia"])
        
        img = Image.open(caminho)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(450, 450))
        self.lbl_preview.configure(image=img_ctk, text="")

    def atualizar_estado(self, _):
        if self.imagem_atual:
            self.dados_imagens[self.imagem_atual]["atendimento"] = self.var_atendimento.get()
            self.dados_imagens[self.imagem_atual]["ambulancia"] = self.var_ambulancia.get()

    def iniciar_extracao(self):
        if not self.dados_imagens:
            self.lbl_status.configure(text="❌ Erro: Selecione ao menos uma foto!")
            return
        self.lbl_status.configure(text="⏳ Processando lote... Aguarde.")
        self.comando_iniciar(self.dados_imagens, self.atualizar_cor_botao)
        self.lbl_status.configure(text="✅ Processamento concluído!")

def desenhar_janela(comando_iniciar):
    app = App(comando_iniciar)
    app.mainloop()