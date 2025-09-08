""" 
Código para a interface gráfica de seleção do tipo de programa para cadastro na interface de registro de programas.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações necessárias para a interface do Director
#   ctk -> customtkinter
#   tkinter -> Biblioteca padrão do Python para interfaces gráficas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import customtkinter as ctk
import tkinter
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Configurações iniciais do customtkinter
#   Modo escuro e tema verde
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe principal da interface de seleção do tipo de programa
#   Herda de ctk.CTkToplevel para criar uma janela filha    
#   Métodos:
#       __init__: Inicializa a janela, configura layout e widgets
#       confirm_selection: Captura a seleção do usuário e fecha a janela
#       on_closing: Fecha a janela ao clicar no "X"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Window_Selector(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método construtor da classe
#   Parâmetros:
#      main_app: Referência para a janela principal que chamou esta janela
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
    def __init__(self, main_app):
        # main_app -> Referência para a janela principal que chamou esta janela
        self.main_app = main_app
        # Chama o construtor da classe pai (CTkToplevel)
        super().__init__()
        # grab_set -> Faz com que a janela atual seja modal, ou seja, bloqueia a interação com outras janelas até que esta seja fechada
        self.grab_set()
        # Define o título da janela
        self.title("Select the Type")
        # Impede o redimensionamento da janela
        self.resizable(False, False)
        # Define o tamanho da janela
        width = 300
        height = 150
        # Define a geometria da janela
        self.geometry(f"{width}x{height}")

        # Centraliza a janela na tela
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Definindo uma cor padrão
        self.bg_color = "#333333"

        # main_container -> Frame principal que contém todos os widgets
        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color=self.bg_color)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        
        # Layout grid configuration
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)

        # form_container -> Frame que contém o formulário de seleção
        self.form_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.form_container.grid(row=0, column=0, columnspan=2, sticky="n")

        # combo_type -> Combobox para seleção do tipo de programa. Ele é preenchido com três opções: "Executable", "Prep" e "Python"
        self.combo_type = ctk.CTkComboBox(self.form_container, values=["Executable", "Prep", "Python"], state="readonly", width=200)
        self.combo_type.set("Select the type of program")
        self.combo_type.pack(pady=(10, 5))
        # confirm_button -> Botão para confirmar a seleção. Ao ser clicado, chama o método confirm_selection
        self.confirm_button = ctk.CTkButton(self.form_container, text="Confirm", command=self.confirm_selection, fg_color="#089c4c", font=("Arial", 15, "normal"))
        self.confirm_button.pack(pady=(5, 10))
        # Define a ação ao clicar no "X" da janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para confirmar a seleção do tipo de programa
#   Captura o valor selecionado na combobox e armazena na variável value_type da janela principal
#   Fecha a janela de seleção
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def confirm_selection(self):
        # Seleciona valor da combobox
        select_value = self.combo_type.get()
        # Atribui o valor selecionado à variável value_type da janela principal
        self.main_app.value_type = select_value
        # Fecha a janela de seleção
        self.destroy()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para fechar a janela ao clicar no "X"
#   Destroi a janela atual
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def on_closing(self):
        self.destroy()             # Fecha a janela de seleção