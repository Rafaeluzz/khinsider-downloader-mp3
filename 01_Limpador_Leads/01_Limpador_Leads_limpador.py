import customtkinter as ctk
import pandas as pd
import re
import os
from tkinter import filedialog, messagebox

# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LimpadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Limpador de Leads Pro v1.0")
        self.geometry("500x350")

        # Layout
        self.label_titulo = ctk.CTkLabel(self, text="HIGIENIZADOR DE LEADS", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(pady=(20, 10))

        self.label_sub = ctk.CTkLabel(self, text="Padronize nomes, telefones e remova duplicatas.", text_color="gray")
        self.label_sub.pack()

        self.btn_processar = ctk.CTkButton(self, text="SELECIONAR PLANILHA", command=self.processar, height=50, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=10)
        self.btn_processar.pack(pady=30)

        self.label_status = ctk.CTkLabel(self, text="Aguardando arquivo...", font=ctk.CTkFont(size=12))
        self.label_status.pack(pady=10)

    def processar(self):
        caminho_entrada = filedialog.askopenfilename(filetypes=[("Planilhas", "*.xlsx *.csv")])
        if not caminho_entrada: return

        try:
            self.label_status.configure(text="Processando...", text_color="yellow")
            self.update()

            # Leitura do arquivo
            df = pd.read_excel(caminho_entrada, engine='openpyxl') if caminho_entrada.endswith('xlsx') else pd.read_csv(caminho_entrada)
            
            # Padronização Universal de Colunas (Agressiva)
            original_cols = df.columns
            df.columns = [str(c).strip().upper() for c in df.columns]
            
            col_nome = next((c for c in df.columns if any(x in c for x in ["NOME", "CLIENTE", "USER"])), None)
            col_tel = next((c for c in df.columns if any(x in c for x in ["TEL", "ZAP", "WHATS", "CEL", "CONTATO"])), None)

            if not col_nome or not col_tel:
                # Fallback: assume as duas primeiras colunas se não achar nomes claros
                col_nome, col_tel = df.columns[0], df.columns[1]
                messagebox.showwarning("Aviso", "Cabeçalhos não identificados. Usando as duas primeiras colunas.")

            # Limpeza dos dados
            df[col_nome] = df[col_nome].fillna('Sem Nome').astype(str).str.title().str.strip()
            
            def limpar_tel(tel):
                num = re.sub(r'\D', '', str(tel))
                if len(num) >= 10 and not num.startswith('55'): return f"55{num}"
                return num

            df[col_tel] = df[col_tel].apply(limpar_tel)
            total_antes = len(df)
            df = df.drop_duplicates(subset=[col_tel])
            removidos = total_antes - len(df)

            # Salvar resultado
            caminho_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
            if caminho_saida:
                df.to_excel(caminho_saida, index=False)
                self.label_status.configure(text="Concluído com Sucesso!", text_color="#2ecc71")
                messagebox.showinfo("Sucesso", f"Processado!\nLeads limpos: {len(df)}\nDuplicatas: {removidos}")
            else:
                self.label_status.configure(text="Salçamento cancelado", text_color="white")

        except Exception as e:
            messagebox.showerror("Erro", f"Feche o arquivo se estiver aberto!\nErro: {e}")
            self.label_status.configure(text="Erro no processamento", text_color="red")

if __name__ == "__main__":
    app = LimpadorApp()
    app.mainloop()