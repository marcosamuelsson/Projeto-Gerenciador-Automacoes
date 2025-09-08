""" 
Código para leitura e execução de programas agendados automaticamente com base em horários e dias específicos.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações de bibliotecas necessárias
#   asyncio: Para operações assíncronas.
#   datetime: Para manipulação de datas e horas.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import asyncio
from datetime import datetime
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe principal para leitura e execução de programas agendados.
#   Esta classe verifica periodicamente a lista de programas cadastrados e executa aqueles que estão agendados para o horário e dia atuais.
#   A verificação é feita a cada 'check_interval' segundos, que pode ser configurado na inicialização da classe.
#   A classe mantém um dicionário de tarefas agendadas para evitar execuções duplicadas.
#   A execução dos programas é feita de forma assíncrona, permitindo que múltiplas tarefas sejam gerenciadas simultaneamente.
#   Métodos:
#       __init__: Inicializa a classe com o runner, banco de dados de programas e intervalo de verificação.
#       start: Inicia o loop assíncrono para verificação e agendamento de tarefas.
#       stop: Para o loop de verificação e cancela todas as tarefas agendadas.
#       check_and_schedule: Verifica os programas agendados e agenda aqueles que devem ser executados.
#       A função 'check_and_schedule' lê a lista de programas do banco de dados, verifica o horário e dia atuais, e agenda a execução dos programas conforme necessário.
#       Cada entrada na lista de agendamento deve estar no formato "HH:MM-Day", onde "HH:MM" é o horário e "Day" é o dia da semana (ex: "Monday", "Tuesday").
#       Se o horário e dia atuais corresponderem a uma entrada na lista de agendamento, o programa é executado utilizando o método 'tasks_ondemmand' do runner.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class read_schedule():
    def __init__(self, runner, programs_db, check_interval = 15):
        self.runner = runner
        self.db_programs = programs_db
        self.check_interval = check_interval
        self.scheduled_tasks = {}
        self.loop = asyncio.get_event_loop()
        self.running = True
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para iniciar o loop assíncrono para verificação e agendamento de tarefas.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    async def start(self):
        while self.running:
            # Verifica e agenda tarefas conforme necessário
            await self.check_and_schedule()
            # Aguarda o próximo intervalo de verificação
            await asyncio.sleep(self.check_interval)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para o loop de verificação e cancela todas as tarefas agendadas.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def stop(self):
        self.running = False
        # Cancela todas as tarefas agendadas
        for task_id, task in list(self.scheduled_tasks.items()):
            # Verifica se a tarefa ainda está em execução antes de cancelar
            if not task.done() and not task.cancelled():
                task.cancel()
            # Remove a tarefa do dicionário
            self.scheduled_tasks.pop(task_id, None)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que verifica os programas agendados e agenda aqueles que devem ser executados.
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    async def check_and_schedule(self):
        # Lê a lista de programas do banco de dados
        programs = self.db_programs.get_all()
        # Obtém o horário e dia atuais
        now = datetime.now()
        # Formata o horário atual como 'HH:MM' e obtém o dia da semana
        current_time = now.strftime('%H:%M')
        # Formata o dia atual como nome completo do dia da semana. Ex: Monday, Tuesday
        current_day = now.strftime('%A')  
        # Itera sobre cada programa na lista
        for program in programs:
            # Lê a lista de agendamento do programa
            schedule_raw = program.get("schedule_list", "")
            # Se a lista de agendamento estiver vazia, pula para o próximo programa
            if not schedule_raw:
                continue
            
            # Divide a lista de agendamento em entradas individuais
            schedule_entries = [entry.strip() for entry in schedule_raw.split(",") if entry.strip()]
            # Itera sobre cada entrada na lista de agendamento
            for entry in schedule_entries:
                try:
                    # Divide a entrada em horário e dia
                    time_part, day_part = entry.split("-")
                    time_part = time_part.strip()
                    day_part = day_part.strip()
                    # Cria um ID único para a tarefa agendada
                    task_id = f"{program['id']}_{time_part}_{day_part}"
                    # Verifica se o horário e dia atuais correspondem à entrada de agendamento
                    if time_part == current_time and day_part == current_day and task_id not in self.scheduled_tasks:
                        # Agenda a execução do programa
                        task = self.loop.create_task(
                            # Chama o método tasks_ondemmand do runner para executar o programa
                            self.runner.tasks_ondemmand(
                                "Automatic",
                                id=len(self.runner.automatic_tasks)+1,
                                name=f"{program['id']} - {program['program_name']}",
                                type_program=program["program_type"],
                                path=program["program_path"],
                                parameters=program["parameters"]
                            )
                        )
                        # Atribui o ID da tarefa para referência futura
                        task.exec_id = str(task_id)
                        # Adiciona a tarefa ao dicionário de tarefas agendadas
                        self.runner.automatic_tasks.append(task)
                        self.scheduled_tasks[task_id] = task
                except ValueError:
                    continue