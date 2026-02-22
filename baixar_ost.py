import subprocess
import os

def baixar_album_khinsider(url):
    # Define o caminho da pasta Downloads
    pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Muda o diretório de execução para a pasta Downloads
    os.chdir(pasta_downloads)
    
    print(f"Iniciando download na pasta: {pasta_downloads}")
    
    # Executa o comando khidl (da biblioteca instalada)
    # --format mp3 garante que baixe em mp3 (pode ser flac se disponível)
    try:
        subprocess.run(["khidl", "download", url, "--format", "mp3"], check=True)
        print("\n--- Download concluído! Verifique sua pasta de Downloads ---")
    except Exception as e:
        print(f"Erro ao baixar: {e}")

if __name__ == "__main__":
    link = input("Cole o link do álbum do khinsider: ").strip()
    if "downloads.khinsider.com" in link:
        baixar_album_khinsider(link)
    else:
        print("Link inválido. Certifique-se de que o link é do site khinsider.")