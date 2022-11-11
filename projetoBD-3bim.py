from random import randint
import PySimpleGUI as sg
import mysql.connector
import datetime

#####################################################################################################################################
def janelaCartao():
    cvv = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))         
    validade = (datetime.date.today() + datetime.timedelta(days = 365 * 2))
    layout2 = [
        [sg.Text("Mestre Cards Deluxe", font=("Arial", 20))],
        [sg.Text("Número do Cartão:", size=(15, 1), font = ("Arial", 12)), sg.Text(f"{codigo}")],
        [sg.Text("CVV:", size=(15, 1), font = ("Arial", 12)), sg.Text(f"{cvv}")],
        [sg.Text("Validade:", size=(15, 1), font = ("Arial", 12)), sg.Text(f"{validade}")],
        [sg.Text("Nome do dono:", size=(15, 1), font = ("Arial", 12)), sg.Text(f"{valores['nome']}")],
        [],
        [],
        [sg.Image(filename="hehe.png")]
    ]

    janela = sg.Window("Aprovador de Cartao", layout2)

    while True:
        evento, valores2 = janela.read()
        if evento == sg.WIN_CLOSED:
            break   
#####################################################################################################################################
def formarNumeroCartao():
    total = 0
    aux = 0
    codigoCartao = "697212"
    for c in range(9):
        codigoCartao += str(randint(0, 9))

    total = 0
    codigoCartao2 = ""

    for c in range(len(codigoCartao)):
        if int(c) % 2 == 1:
            aux = int(codigoCartao[c]) * 2
            while int(aux) >= 10:
                pDig = aux // 10 % 10
                sDig = aux // 1 % 10
                aux = str(pDig + sDig)
            total += int(aux)

    for c in range(len(codigoCartao)):
        if int(c) % 2 == 0:
            total += int(codigoCartao[c])

    digitoVerificador = ((total // 10 + 1) * 10) - total

    codigoCartao += str(digitoVerificador)

    for c in range(len(codigoCartao)):
        codigoCartao2 += codigoCartao[c]
        if (c+1) % 4 == 0:
            codigoCartao2 += " "
    return codigoCartao2
#####################################################################################################################################
try:
    global conexao
    conexao = mysql.connector.Connect(host="localhost", database="criarCartao", user="root", password="")
    if conexao.is_connected():
        infobanco = conexao.get_server_info()
        print(f"Conectado ao servidor - Versão {infobanco}")
        print("Conexão ok")
        global comandosql
        comandosql = conexao.cursor()
        comandosql.execute("select database();")
        nomebanco = comandosql.fetchone()
        print(f"Banco acessado: {nomebanco}")
    else:
        print("Conexão não realizada")
        text = "Conexão com banco não realizada, reinicie o programa!"
except Exception as erro:
    print(f"Erro: {erro}")
    text = f"Erro: {erro}"

cursor = conexao.cursor()
#####################################################################################################################################
layout = [
    [sg.Text("Nome:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="nome")],
    [sg.Text("Idade:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="idade")],
    [sg.Text("CPF:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="cpf")],
    [sg.Text("Email:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="email")],
    [sg.Text("Telefone:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="tel")],
    [sg.Text("Serasa Score:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="score")],
    [sg.Text("Salário:", size=(15, 1), font = ("Arial", 12)), sg.InputText(key="sal")],
    [sg.Button("OK"), sg.Button("Cancel")],
    [],
    [sg.Text("", key="resultado")]
]

janela = sg.Window("Aprovador de Cartao", layout)

while True:
    evento, valores = janela.read()
    text = ""
    aprovado = 0
    if evento == sg.WIN_CLOSED or evento == "Cancel":
        break

    if evento == "OK":
        testeVerificacao = 0
        for c in valores:
            if valores[c] == "":
                testeVerificacao = 1
                text = "Insira todos os dados corretamente."
            break

        try:
            valido = 0
            if testeVerificacao == 0:
                if int(valores["idade"]) < 16:
                    text = "Idade insuficiente.\n"
                    valido = 1
                if int(valores["score"]) < 500:
                    text = "Serasa SCORE insuficiente.\n"
                    valido = 1
                if int(valores["idade"]) < 0 or int(valores["idade"]) > 130:
                    text = "Idade inválida"
                    valido = 1
                if int(valores["score"]) < 0 or int(valores["score"]) > 1000:
                    text = "Pontuação do Serasa inválida"
                    valido = 1
                if valido == 0:
                    text = "Aprovado"
                    codigo = formarNumeroCartao()
                    janelaCartao()
        except:
            text = "Insira todos os dados corretamente."

        janela["resultado"].update(f"{text}")

try:
    cursor.execute(f'insert into dados values ("{valores["nome"]}","{valores["idade"]}, "{valores["telefone"]}, "{valores("email")}", "{valores("cpf")}",{int(valores("score"))}, {float(valores("sal"))});')
    conexao.commit()
except:
    print("Falho")
finally:
    cursor.close()
    conexao.close()


janela.close()