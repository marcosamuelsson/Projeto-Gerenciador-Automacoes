""" 
Código para criar uma base de dados utilizando SQLAlchemy
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas
#   Biblioteca SQLAlchemy para manipulação de banco de dados
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#         
from sqlalchemy.ext.declarative import declarative_base

# Cria a classe base para declarar as classes definitivas
Base = declarative_base()