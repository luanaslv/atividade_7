import sqlite3
import datetime

# Função que cria a tabela "academia.db" no banco
def criar_tabela():
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            AlunoID INTEGER PRIMARY KEY,
            nome TEXT,
            data_nascimento TEXT,
            data_matricula TEXT,
            atividades TEXT,
            pago BOOLEAN
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para matricular um novo aluno, considerando nome, data_nascimento e atividades
def matricular_aluno(nome, data_nascimento, atividades):
    data_matricula = datetime.date.today()
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO alunos (nome, data_nascimento, data_matricula, atividades, pago)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, data_nascimento, data_matricula, atividades, False))
    conexao.commit()
    conexao.close()

# Função para listar alunos matriculados através de uma query básica de SELECT
def listar_alunos():
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT AlunoID, nome, data_nascimento, atividades FROM alunos')
    alunos = cursor.fetchall()
    conexao.close()
    return alunos

# Função para verificar atrasos de matrícula, se baseando na data atual da query
def verificar_atrasos():
    hoje = datetime.date.today()
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT AlunoID, nome, data_matricula FROM alunos')
    alunos = cursor.fetchall()
    atrasados = []
    for aluno in alunos:
        data_matricula = datetime.datetime.strptime(aluno[2], "%Y-%m-%d").date()
        if hoje > data_matricula:
            atrasados.append((aluno[0], aluno[1], data_matricula))
    conexao.close()
    return atrasados

# Função para calcular o valor a ser pago de acordo com o valor por atividade e a quantidade de atvidades totais (retornada pela função len)
def calcular_valor(AlunoID_aluno):
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT atividades FROM alunos WHERE AlunoID = ?', (AlunoID_aluno,))
    atividades = cursor.fetchone()
    conexao.close()
    if atividades:
        atividades = atividades[0].split(',')
        valor_por_atividade = 10
        valor_total = len(atividades) * valor_por_atividade
        return valor_total
    return 0

# Função para definir o pagamento por aluno
def definir_pagamento(AlunoID_aluno):
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('UPDATE alunos SET pago = 1 WHERE AlunoID = ?', (AlunoID_aluno,))
    conexao.commit()
    conexao.close()

# Função para encontrar aniversariantes do dia no qual consultamos aluno por aluno com um for e atribuimos uma condição if para determinar uma igualdade do dia de hoje e da data de nascimento
def encontrar_aniversariantes():
    hoje = datetime.date.today()
    conexao = sqlite3.conexaoect("academia.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT AlunoID, nome, data_nascimento FROM alunos')
    alunos = cursor.fetchall()
    aniversariantes = []
    for aluno in alunos:
        data_nascimento = datetime.datetime.strptime(aluno[2], "%Y-%m-%d").date()
        if hoje.month == data_nascimento.month and hoje.day == data_nascimento.day:
            aniversariantes.append((aluno[0], aluno[1]))
    conexao.close()
    return aniversariantes

def chama_menu():
    menu = """
### Sistema de Gestão de Academia ###
1. Matricular novo aluno
2. Listar alunos matriculados
3. Verificar atrasos de matrícula
4. Calcular valor a ser pago
5. Definir pagamento
6. Encontrar aniversariantes do dia
0. Sair
"""
    return menu

# Para usar a função, basta chamar chama_string() para obter o menu como uma string.

if __name__ == "__main__":
    criar_tabela()

    #menu principal para chamar as ações do sistema, através de uma lógica condicional if, elif e else
    while True:
        
        chama_menu()
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            nome = input("Nome do aluno: ")
            data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
            atividades = input("Atividades (separadas por vírgula): ")
            matricular_aluno(nome, data_nascimento, atividades)
            print("Aluno matriculado com sucesso!")

        elif opcao == "2":
            alunos = listar_alunos()
            if alunos:
                print("\n### Alunos Matriculados ###")
                for aluno in alunos:
                    print(f"Código: {aluno[0]}, Nome: {aluno[1]}, Data de Nascimento: {aluno[2]}, Atividades: {aluno[3]}")
            else:
                print("Nenhum aluno matriculado.")
        
        elif opcao == "3":
            atrasados = verificar_atrasos()
            if atrasados:
                print("\n### Alunos com Atraso na Matrícula ###")
                for atrasado in atrasados:
                    print(f"Código: {atrasado[0]}, Nome: {atrasado[1]}, Data de Matrícula: {atrasado[2]}")
            else:
                print("Nenhum atraso na matrícula.")
        
        elif opcao == "4":
            AlunoID_aluno = int(input("Informe o código do aluno: "))
            valor = calcular_valor(AlunoID_aluno)
            print(f"Valor a ser pago: R$ {valor}")
        
        elif opcao == "5":
            AlunoID_aluno = int(input("Informe o código do aluno: "))
            definir_pagamento(AlunoID_aluno)
            print("Pagamento definido com sucesso!")

        elif opcao == "6":
            aniversariantes = encontrar_aniversariantes()
            if aniversariantes:
                print("\n### Aniversariantes do Dia ###")
                for aniversariante in aniversariantes:
                    print(f"Código: {aniversariante[0]}, Nome: {aniversariante[1]}")
            else:
                print("Nenhum aniversariante hoje.")

        elif opcao == "0":
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")
