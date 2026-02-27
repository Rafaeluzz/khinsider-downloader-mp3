import customtkinter as ctk
import os
from PIL import Image
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class OtimizadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Otimizador de Assets v1.0")
        self.geometry("450x350")

        self.label = ctk.CTkLabel(self, text="OTIMIZADOR DE IMAGENS", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)

        self.info = ctk.CTkLabel(self, text="Selecione as fotos (JPG, PNG, WEBP)\nReduza o peso sem perder qualidade.", text_color="gray")
        self.info.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="SELECIONAR ARQUIVOS", command=self.otimizar, height=50, font=ctk.CTkFont(weight="bold"))
        self.btn.pack(pady=25)

        self.status = ctk.CTkLabel(self, text="Pronto para processar", text_color="white")
        self.status.pack()

    def otimizar(self):
        # Correção UX: Selecionar arquivos diretamente
        arquivos_selecionados = filedialog.askopenfilenames(
            title="Selecione as fotos para otimizar",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp *.jfif")]
        )
        
        if not arquivos_selecionados: return

        pasta_origem = os.path.dirname(arquivos_selecionados[0])
        pasta_saida = os.path.join(pasta_origem, "Imagens_Otimizadas")
        
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        cont = 0
        try:
            self.status.configure(text="Otimizando...", text_color="yellow")
            self.update()

            for caminho_completo in arquivos_selecionados:
                arquivo_nome = os.path.basename(caminho_completo)
                img = Image.open(caminho_completo)
                
                # Garantia de compatibilidade de cores (RGB)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Compressão otimizada
                nome_final = os.path.join(pasta_saida, arquivo_nome)
                img.save(nome_final, "JPEG", optimize=True, quality=80)
                cont += 1

            self.status.configure(text=f"Sucesso! {cont} arquivos prontos.", text_color="#2ecc71")
            messagebox.showinfo("Concluído", f"Finalizado!\n{cont} imagens salvas em:\n/Imagens_Otimizadas")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar: {e}")
            self.status.configure(text="Erro técnico", text_color="red")

if __name__ == "__main__":
    app = OtimizadorApp()
    app.mainloop()