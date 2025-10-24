"""
Interface gráfica para seleção de usuário por nome.
Code by: Marco Antonio Samuelsson
Data: 11/09/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação de bibliotecas necessárias para o funcionamento do código
#   Bibliotecas externas:
#       customtkinter: cria interface gráfica
#       tkinter: auxilia na manipulação de elementos gráficos
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Bibliotecas internas:
#       manipulador: pega o caminho do ícone usado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import customtkinter as ctk
import tkinter
from app.adm_files.manipulator import manipulador
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Configurações iniciais
DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe para seleção de usuário
#   Esta classe cria uma janela para seleção de um usuário a partir de uma lista fornecida.
#   Parâmetros:
#       main_app: referência à aplicação principal
#       user_list: lista de usuários disponíveis para seleção
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Window_UserSelector(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Construtor da classe
#   Inicializa a janela de seleção de usuário
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, main_app, user_list):
        self.main_app = main_app
        super().__init__()
        self.grab_set()
        self.title("Select User")
        self.wm_iconbitmap(manipulador().icon_terminator) # Ícone da janela
        # Desabilita o redimensionamento da janela
        self.resizable(False, False)
        # Define as dimensões da janela
        width = 300
        height = 150
        self.geometry(f"{width}x{height}")
        
        # Centraliza a janela
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Define a cor padrão da janela
        self.bg_color = "#333333"

        # Container principal
        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color=self.bg_color)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        # Configura a grade do container principal
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)

        # Formulário
        self.form_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.form_container.grid(row=0, column=0, columnspan=2, sticky="n")

        # Combobox com nomes de usuários
        self.combo_user = ctk.CTkComboBox(self.form_container, values=user_list, state="readonly", width=200)
        self.combo_user.set("Select a user")
        self.combo_user.pack(pady=(10, 5))

        # Botão de confirmação
        self.confirm_button = ctk.CTkButton(self.form_container, text="Confirm", command=self.confirm_selection, fg_color="#089c4c", font=("Arial", 15, "normal"))
        self.confirm_button.pack(pady=(5, 10))
        # Fecha a janela ao clicar fora
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para confirmar a seleção do usuário
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def confirm_selection(self):
        selected_user = self.combo_user.get()
        self.main_app.selected_user = selected_user
        self.destroy()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para fechar a janela
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def on_closing(self):
        self.destroy()