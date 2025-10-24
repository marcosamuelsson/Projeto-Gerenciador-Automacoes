"""  
Código para criar um ícone de pixel art a partir de uma matriz de cores.
Code by: Marco Antônio Samuelsson
Data: 18/9/2025
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias para o funcionamento do código.
#   Bibliotecas externas:
#       PIL: Biblioteca para manipulação de imagens (Python Imaging Library)
#           Image: Classe da PIL para criar e manipular imagens.
#           ImageDraw: Classe da PIL para desenhar em imagens.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Bibliotecas externas:
#       manipulador: para pegar o caminho onde o ícone deve ser salvo
#       color_matrix: importa a matrix de cores da imagem
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from PIL import Image, ImageDraw
from app.adm_files.manipulator import manipulador
from app.images.matriz_terminator import color_matrix  # Aqui você importa a matriz diretamente
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe para criar ícones de pixel art
#   Esta classe utiliza a matriz de cores para gerar um ícone de pixel art.
#   Utiliza a biblioteca PIL para manipulação de imagens.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class PixelArtIcon:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Contrutor da classe. 
#   Parâmtros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        self.manipulador = manipulador()
        self.color_matrix = color_matrix  # Agora isso funciona corretamente
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método 'create_icon': Cria o ícone de pixel art a partir da matriz de cores.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_icon(self):
        # Criar imagem pixel art
        altura = len(self.color_matrix)
        largura = len(self.color_matrix[0])
        img = Image.new("RGB", (largura, altura), "black")
        draw = ImageDraw.Draw(img)
        # Para cada pixel na matriz de cores...
        for y, row in enumerate(self.color_matrix):
            # Para cada coluna na linha...
            for x, color in enumerate(row):
                #... desenha o pixel com a cor correspondente 
                draw.rectangle([x, y, x+1, y+1], fill=color)

        # Salvar como ícone
        caminho_ícone = self.manipulador.icon_terminator
        img.save(caminho_ícone, format="ICO")