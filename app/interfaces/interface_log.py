"""
Código para a interface de visualização de arquivos .txt utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias para o funcionamento da interface de visualização de logs
#       customtkinter: para a criação da interface gráfica customizada
#       tkinter: para widgets padrão
#       CTkMessagebox: para exibir caixas de mensagem personalizadas
#       os: para manipulação de arquivos e verificação de existência
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import customtkinter as ctk
import tkinter
from CTkMessagebox import CTkMessagebox
import os
from app.adm_files.manipulator import manipulador
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Configuração do modo de aparência e tema padrão do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # ou qualquer outro tema
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe principal da interface de visualização de logs
#   Herda de CTkToplevel para criar uma janela separada
#   Métodos principais da classe:
#       __init__: construtor da classe que inicializa a interface e seus componentes
#       _load_txt: lê os dados do arquivo .txt criado para armazenar os logs
#       _on_close: define o como e o que fazer quando a janela for fechada
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class TextViewerApp(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método construtor para inicializar a janela de visualização de log.
#   Parâmetros:
#       program_path (str): Caminho do arquivo de log a ser exibido
#       program_name (str): Nome do programa relacionado ao log
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, program_path, program_name):
        super().__init__()
        # Armazena os parâmetros recebidos
        self.program_path = program_path
        self.program_name = program_name
        self.bg_color = "#000811"  # Cor de fundo padrão
        self.configure(bg=self.bg_color)  # Aplica cor de fundo
        # Acresenta o ícone ao app
        self.wm_iconbitmap(default=manipulador().icon_terminator)
        # Configura título e dimensões da janela
        self.title(f"Allocation Log - {self.program_name}")
        width = 600
        height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Cria o frame container principal com cor de fundo
        self.container_frame = ctk.CTkFrame(self, fg_color=self.bg_color, bg_color=self.bg_color)
        self.container_frame.pack(fill=tkinter.BOTH, expand=True)
        
        # Cria o frame do texto com padding interno
        self.text_frame = ctk.CTkFrame(self.container_frame, fg_color=self.bg_color, bg_color=self.bg_color)
        self.text_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        # Cria o widget de texto para exibir o conteúdo do log
        self.textbox = tkinter.Text(
            self.text_frame,
            wrap="word",           # Quebra automática de linha
            bg=self.bg_color,      # Fundo preto
            fg="white",           # Texto branco
            font=("Arial", 12),   # Fonte padrão
            relief="flat",        # Remove bordas visuais
        )
        self.textbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        # Adiciona uma barra de rolagem vertical ao widget de texto
        self.scrollbar = tkinter.Scrollbar(self.text_frame, command=self.textbox.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.textbox.config(yscrollcommand=self.scrollbar.set)

        # Carrega o conteúdo do arquivo de log
        self._load_txt()

        # Configura ação ao fechar a janela
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Traz a janela para frente e bloqueia interação com a principal
        self.grab_set()
        self.focus_force()           # Garante foco
        self.lift()                  # Garante que fique no topo
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que carrega o conteúdo do arquivo de log (.txt) e exibe no widget de texto.
#   Caso o arquivo não exista, exibe uma mensagem de erro.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def _load_txt(self):        
        if not os.path.exists(self.program_path):
            CTkMessagebox(
                title="Error",
                message=f"The log for '{self.program_name}' does not exist.\nPath not found:\n{self.program_path}",
                icon="warning",
                button_color="#089c4c"
            )
            return

        # Lê o conteúdo do arquivo e insere no widget de texto
        with open(self.program_path, "r", encoding="utf-8") as file:
            content = file.read()

        self.textbox.delete("1.0", tkinter.END)      # Limpa o conteúdo anterior
        self.textbox.insert(tkinter.END, content)     # Insere o novo conteúdo
        self.textbox.see(tkinter.END)                 # Rola até o final do texto
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado ao fechar a janela. Destroi a janela de log.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def _on_close(self):  
        self.destroy()