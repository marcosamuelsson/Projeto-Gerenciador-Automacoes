# Gerenciador de Automação

## Descrição

Este é um projeto pessoal desenvolvido em Python para gerenciar e executar automações personalizadas. O aplicativo oferece uma interface gráfica intuitiva para agendamento, execução e monitoramento de programas, com recursos de segurança, gerenciamento de usuários e logs detalhados. O sistema previne múltiplas execuções simultâneas e utiliza uma arquitetura modular para facilitar a manutenção e expansão.

**Autor:** Marco Antônio Samuelsson  
**Data de Criação:** 18/09/2025  
**Versão Atual:** 1.2.2  
**Linguagem Principal:** Python 3.x  

## Funcionalidades

- **Interface Gráfica Moderna:** Utiliza CustomTkinter para uma experiência de usuário fluida e responsiva.
- **Agendamento de Execuções:** Permite criar, importar e gerenciar cronogramas de execução de programas.
- **Gerenciamento de Programas:** Registro e controle de aplicativos e preparativos a serem executados.
- **Gerenciamento de Usuários:** Sistema de autenticação com hash de senhas para controle de acesso.
- **Visualização de Logs:** Interface dedicada para monitoramento de execuções e erros.
- **Configurações Personalizáveis:** Ajustes de configurações do sistema armazenadas em banco de dados.
- **Prevenção de Múltiplas Instâncias:** Sistema de lockfile para evitar execuções duplicadas.
- **Manipulação de Arquivos Excel:** Criação e importação de templates para agendamento.
- **Execução Assíncrona:** Utiliza asyncio para tarefas em background sem bloquear a interface.
- **Limpeza Automática:** Ferramentas para limpeza de pastas temporárias e manutenção do sistema.

## Tecnologias e Bibliotecas Utilizadas

### Linguagem e Framework
- **Python:** 3.8+ (recomendado)
- **CustomTkinter:** Para interface gráfica moderna e customizável.
- **Tkinter:** Base para widgets gráficos (incluído no CustomTkinter).

### Bibliotecas Externas
- `psutil`: Monitoramento de processos do sistema (instalação: `pip install psutil`).
- `openpyxl`: Manipulação de arquivos Excel (instalação: `pip install openpyxl`).
- `CTkMessagebox`: Caixas de diálogo customizadas para CustomTkinter.
- `Pillow (PIL)`: Manipulação de imagens para ícones e gráficos.

### Bibliotecas Padrão do Python
- `os`: Manipulação de sistema de arquivos.
- `sys`: Interação com o sistema operacional.
- `tempfile`: Criação de arquivos temporários.
- `ctypes`: Interação com bibliotecas C (usado para manipulação de janelas no Windows).
- `asyncio`: Programação assíncrona.
- `datetime`: Manipulação de datas e horas.
- `tkinter.ttk`: Widgets avançados do Tkinter.

### Banco de Dados
- **SQLite:** Banco de dados relacional leve, utilizado através de operações genéricas customizadas.
- Estrutura modular com classes específicas para usuários, programas e configurações.

## Padrões de Projeto Identificados

### Arquitetura em Camadas
O projeto segue uma arquitetura em camadas bem definida, separando responsabilidades:

- **Camada de Interface (interfaces/):** Contém todas as classes relacionadas à interface gráfica e interação com o usuário.
- **Camada de Dados (database/):** Gerenciamento de operações de banco de dados com classes genéricas e específicas.
- **Camada de Execução (executer/):** Lógica de execução de programas, leitura de agendamentos e limpeza.
- **Camada de Segurança (security/):** Hash de senhas e diálogos de autenticação.
- **Camada de Utilitários (adm_files/, images/):** Manipulação de arquivos, criação de ícones e templates.

### Padrão Singleton (Implícito)
- O sistema de lockfile previne múltiplas instâncias, implementando um padrão singleton a nível de aplicação.

### Padrão MVC (Model-View-Controller) Adaptado
- **Model:** Classes de banco de dados (UsersDB, ProgramsDB, SettingsDB) representam os dados.
- **View:** Interfaces gráficas em CustomTkinter.
- **Controller:** Lógica de negócio distribuída nas classes principais (App, Runner, etc.).

### Padrão Factory
- Uso de classes genéricas (GenericDBOperations) para criar operações específicas de banco de dados.

### Programação Orientada a Objetos (OOP)
- Extensivo uso de classes e herança (ex.: App herda de ctk.CTk).
- Encapsulamento com atributos privados e métodos públicos.
- Polimorfismo em operações de banco de dados.

### Programação Assíncrona
- Utiliza asyncio para execuções em background, seguindo boas práticas de concorrência.

## Estrutura do Projeto

```
Projeto-Gerenciador-Automacoes-main/
├── _app.py                          # Ponto de entrada principal com sistema de lock
├── extracao_banco_terminator.py     # Script de extração de dados do banco
├── diagram.txt                      # Diagrama UML das classes principais
├── app/
│   ├── adm_files/                   # Manipulação de arquivos administrativos
│   │   ├── create_excel_template.py # Criação de templates Excel
│   │   ├── manipulator.py           # Utilitários de manipulação de arquivos
│   │   └── __pycache__/
│   ├── database/                    # Camada de dados
│   │   ├── base.py                  # Configurações base do banco
│   │   ├── operationDBs.py          # Operações genéricas de DB
│   │   ├── programsDB.py            # Operações específicas para programas
│   │   ├── settingsDB.py            # Operações específicas para configurações
│   │   ├── usersDB.py               # Operações específicas para usuários
│   │   └── __pycache__/
│   ├── executer/                    # Camada de execução
│   │   ├── cleaner.py               # Limpeza de arquivos temporários
│   │   ├── read_schedule.py         # Leitura de agendamentos
│   │   ├── runner.py                # Executor de tarefas
│   │   └── __pycache__/
│   ├── images/                      # Utilitários gráficos
│   │   ├── create_icon.py           # Criação de ícones pixel art
│   │   ├── matriz_terminator.py     # Geração de matrizes visuais
│   │   └── __pycache__/
│   ├── interfaces/                  # Camada de interface
│   │   ├── director.py              # Diretor de janelas
│   │   ├── interface_log.py         # Visualizador de logs
│   │   ├── interface_settings.py    # Interface de configurações
│   │   ├── main.py                  # Janela principal do aplicativo
│   │   ├── register_apps.py         # Registro de aplicativos
│   │   ├── register_prep.py         # Registro de preparativos
│   │   ├── register_users.py        # Registro de usuários
│   │   ├── select_user.py           # Seletor de usuários
│   │   └── __pycache__/
│   └── security/                    # Camada de segurança
│       ├── password_dialog.py       # Diálogo de senha
│       ├── password_hash.py         # Utilitários de hash
│       └── __pycache__/
└── type_programs_terminator/        # Exemplos de programas
    └── programa_simulado.py         # Programa simulado para testes
```

## Instalação e Configuração

### Pré-requisitos
- **Python:** Versão 3.8 ou superior
- **Sistema Operacional:** Windows (compatível com ctypes para manipulação de janelas)

### Passos de Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/gerenciador-automacao.git
   cd gerenciador-automacao
   ```

2. **Instale as dependências:**
   ```bash
   pip install psutil openpyxl customtkinter CTkMessagebox Pillow
   ```

3. **Execute o aplicativo:**
   ```bash
   python _app.py
   ```

### Configuração Inicial
- Na primeira execução, o sistema criará automaticamente as pastas necessárias e o banco de dados SQLite.
- Configure usuários administradores através da interface de gerenciamento de usuários.
- Ajuste as configurações do sistema na seção de configurações.

## Uso

### Iniciando o Aplicativo
- Execute `_app.py` para iniciar a aplicação.
- O sistema verificará se já existe uma instância em execução e impedirá duplicatas.

### Funcionalidades Principais
1. **Visualizar Programas Executados:** Acesse a aba "Executados" para ver o histórico de execuções.
2. **Agendar Execuções:** Use "Agendar" para criar e importar cronogramas via Excel.
3. **Gerenciar Programas:** Registre novos aplicativos e preparativos na seção "Programas".
4. **Gerenciar Usuários:** Adicione e controle usuários na seção "Usuários".
5. **Configurações:** Ajuste parâmetros do sistema em "Configurações".
6. **Logs:** Visualize logs detalhados em "Logs".

### Criação de Templates Excel
- Use o botão "Criar Template" para gerar um arquivo Excel com a estrutura aceita para importação de agendamentos.

## Parâmetros Técnicos e Boas Práticas

### Configurações de Desenvolvimento
- **Modo de Aparência:** Dark mode padrão com tema verde.
- **Codificação:** UTF-8 para compatibilidade com caracteres especiais.
- **Tratamento de Exceções:** Extensivo uso de try-except para robustez.
- **Logs:** Sistema de logging para rastreamento de erros e execuções.

### Performance
- **Execução Assíncrona:** Tarefas pesadas rodam em background para manter a responsividade da interface.
- **Gerenciamento de Memória:** Limpeza automática de arquivos temporários.
- **Banco de Dados:** SQLite para leveza e portabilidade.

### Segurança
- **Hash de Senhas:** Utiliza algoritmos seguros para armazenamento de senhas.
- **Autenticação:** Verificação de usuários antes de operações sensíveis.
- **Prevenção de Execuções Múltiplas:** Lockfile baseado em PID.

### Manutenibilidade
- **Modularidade:** Código dividido em módulos independentes.
- **Documentação:** Comentários extensivos em português explicando funcionalidades.
- **Convenções de Nomenclatura:** Nomes descritivos em português para variáveis e métodos.

### Compatibilidade
- **Plataforma:** Desenvolvido para Windows, mas adaptável para outras plataformas.
- **Dependências:** Todas as bibliotecas são cross-platform.

## Contribuição

Como este é um projeto pessoal, modificações ou cópias devem ser autorizadas pelo autor. Para sugestões ou relatórios de bugs:

1. Abra uma issue no GitHub descrevendo o problema ou sugestão.
2. Forneça detalhes técnicos e passos para reproduzir.
3. Aguarde autorização antes de implementar mudanças.

## Licença

Este projeto é de propriedade pessoal de Marco Antônio Samuelsson. Qualquer uso, modificação ou distribuição deve ser autorizada explicitamente pelo autor.

## Suporte e Contato

Para suporte técnico ou dúvidas:
- **Email:** [seu-email@exemplo.com]
- **GitHub Issues:** Utilize a seção de issues do repositório

---

**Nota:** Este README foi gerado automaticamente baseado na análise completa do código fonte. Para atualizações, consulte o código diretamente ou entre em contato com o autor.
