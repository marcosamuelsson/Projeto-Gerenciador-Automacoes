""" 
Código para a criação de uma janela de diálogo para confirmação de senha utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação de bibliotecas necessárias
#       customtkinter: para criação da interface gráfica
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import customtkinter as ctk
from app.adm_files.manipulator import manipulador
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe que vai contruir a Interface de diálogo de senhas 
#   Possui os seguintes métodos:
#       __init__: construtor da classe que inicializa a interface e seus componenetes
#       change_visibility: altera a visibilidade da senha na janela
#       confirm: método que define a confirmação do usuário após digitar a senha
#                também define o que e como fazer caso o usuário fechar a janela repentinamente
#       get_passowrd: pega a senha digitada pelo usuário
#   Parâmetros:
#       ctk.CTkTopLevel: define que a janela fique sempre acima da janela principal sempre que acionada
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# 
class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Password Confirmation", user_or_adm = "ADM USER"):
        super().__init__(parent)
        self.title(title)
        self.iconbitmap(manipulador().icon_terminator)
        self.geometry("400x150")
        self.resizable(False, False)
        self.grab_set()

        # Centralizar a janela
        self.update_idletasks()  # Garante que a geometria esteja atualizada
        width = 400
        height = 230
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.password = None
        self.show_password = False

        self.label = ctk.CTkLabel(self, text=f"Type the password to confirm:\n{user_or_adm}")
        self.label.pack(pady=(20, 5))

        self.entry = ctk.CTkEntry(self, show="*")
        self.entry.pack(pady=5)

        self.toggle_button = ctk.CTkButton(self, text="Show", command=self.change_visibility, fg_color="#089c4c", font=("Arial", 15, "normal"))
        self.toggle_button.pack(pady=5)

        self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self.confirm, fg_color="#089c4c", font=("Arial", 15, "normal"))
        self.confirm_button.pack(pady=10)

        self.entry.bind("<Return>", lambda event: self.confirm())
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que altera a visibilidade da senha na janela
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_visibility(self):
        self.show_password = not self.show_password
        self.entry.configure(show="" if self.show_password else "*")
        self.toggle_button.configure(text="Hide" if self.show_password else "Show")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que define como e o que fazer quando:
#       o usuário confirmar a senha (senha pode estar certa ou errada);
#       fechar a janela repentinamente;
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def confirm(self):
        self.password = self.entry.get()
        self.destroy()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para pegar a senha inputada na janela
#   Usada em outras partes do APP
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def get_password(self):
        self.wait_window()
        return self.password