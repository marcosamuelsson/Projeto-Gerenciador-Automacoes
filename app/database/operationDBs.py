""" 
Código para operações genéricas em bancos de dados utilizando SQLAlchemy.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias
#   sqlalchemy: Biblioteca ORM para interagir com bancos de dados relacionais.
#   create_engine: Função para criar uma conexão com o banco de dados.
#   sessionmaker: Função para criar uma fábrica de sessões.
#   Base: Classe base para definir modelos de banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe para operações genéricas em bancos de dados.
#   model_class: Classe do modelo do banco de dados (ex: UsersDB, ProgramsDB, SettingsDB).
#   database_url: URL de conexão com o banco de dados (ex: "sqlite:///C:/Terminator/Database/executerDB.db").
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class GenericDBOperations:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Construtor que inicializa a classe com a classe do modelo e a URL do banco de dados.
#   Cria a engine e a sessão para interagir com o banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, model_class, database_url):
        self.model_class = model_class
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para registrar um novo registro no banco de dados.
#   Parâmetros:
#       **kwargs: Argumentos nomeados correspondentes aos campos do modelo.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def register(self, **kwargs):
        new_record = self.model_class(**kwargs)
        self.session.add(new_record)
        self.session.commit()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para atualizar um registro existente no banco de dados.
#   record_id: ID do registro a ser atualizado.
#   **kwargs: Argumentos nomeados correspondentes aos campos do modelo a serem atualizados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def update(self, record_id, **kwargs):
        with self.Session() as session:
            record = session.query(self.model_class).get(record_id)
            if record:
                for key, value in kwargs.items():
                    setattr(record, key, value)
                session.commit()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para deletar um registro do banco de dados pelo ID.
#   Parâmetro:
#       record_id: ID do registro a ser deletado.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def delete(self, record_id):
        record = self.session.query(self.model_class).filter_by(id=record_id).first()
        if record:
            self.session.delete(record)
            self.session.commit()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para deletar registros do banco de dados com base em um valor específico de uma coluna.
#   Parâmetros
#       column_name: Nome da coluna a ser filtrada.
#       value: Valor a ser comparado para deletar os registros.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def delete_by_column(self, column_name, value):
        with self.Session() as session:
            session.query(self.model_class).filter(getattr(self.model_class, column_name) == value).delete()
            session.commit()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que pega todos os registros do banco de dados e retorna como uma lista de dicionários.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def get_all(self):
        records = self.session.query(self.model_class).all()
        result = []
        for record in records:
            result.append({column.name: getattr(record, column.name) for column in self.model_class.__table__.columns})
        return result
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que pega um registro do banco de dados com base em um valor específico de uma coluna.
#   Parâmetros:
#       column_name: Nome da coluna a ser filtrada.
#       value: Valor a ser comparado para pegar o registro.
#   Retorna o registro como um dicionário ou None se não encontrado.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def get_by_column(self, column_name, value):
        with self.Session() as session:
            result = session.query(self.model_class).filter(getattr(self.model_class, column_name) == value).first()
            return result.__dict__ if result else None