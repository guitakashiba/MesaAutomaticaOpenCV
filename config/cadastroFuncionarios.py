import time
import cv2
import os
import tkinter as tk
import sqlite3
import pandas as pd
import openpyxl
from tkinter import messagebox


janela = tk.Tk()
janela.title('Cadastro de Funcionarios')
janela. geometry("400x320")

path = r'/MesaAutomatica/config/imagens/usuarios'
def cadastrar_funcionarios():
    global nome_aux
    nome_aux = entry_nome.get()

    conexao = sqlite3.connect('bancoUser.db')

    if conexao:
        print("Conexão ok")
    else:
        print("Conexão not ok")

    c = conexao.cursor()

    #Inserir dados na tabela:
    c.execute("INSERT INTO People (Nome, Matricula, Altura) VALUES (:Nome,:Matricula,:Altura)",
              {
                  'Nome': entry_nome.get().lower(),
                  'Matricula': entry_matricula.get(),
                  'Altura': entry_altura.get(),
              })

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()

    # #Apaga os valores das caixas de entrada
    entry_nome.delete(0, "end")
    entry_matricula.delete(0, "end")
    entry_altura.delete(0, "end")

    cad_faces()


def exporta_funcionarios():
    conexao = sqlite3.connect('bancoUser.db')
    c = conexao.cursor()

    # Inserir dados na tabela:
    c.execute("SELECT * FROM People")
    funcionarios_cadastrados = c.fetchall()
    funcionarios_cadastrados = pd.DataFrame(funcionarios_cadastrados, columns=['id', 'Nome', 'Matricula', 'Altura'])
    funcionarios_cadastrados.to_excel('funcionarios.xlsx')

    print("Planilha exportada!")

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


def cad_faces():
    fotos = 20

    cam = cv2.VideoCapture(0)
    name = str(nome_aux)
    print(name)

    if name:
        try:
            tk.messagebox.showinfo('Aviso', 'Olhe para a camera!')
            time.sleep(3)

            os.chdir(path)
            os.mkdir(name)
            os.chdir(name)

            for i in range(fotos):
                ret, img = cam.read()

                cv2.imshow("Rosto", img)
                cv2.imwrite(name + str(i) + '.png', img)
                print("Fotos capturadas %d" % i)

                if i == fotos - 1:
                    print(name, "cadastrado com sucesso")
                    break
        except FileExistsError:
            tk.messagebox.showinfo('Aviso', 'Funcionário já cadastrado!')
            print("path", name, "já existe")

    os.chdir(path)
    cam.release()
    cv2.destroyAllWindows()


# Rótulos Entradas:


label_nome = tk.Label(janela, text= 'Nome')
label_nome.grid(row=0,column=0, padx=10, pady=10)

label_matricula = tk.Label(janela, text='Matricula')
label_matricula.grid(row=1, column=0, padx=10, pady=10)

label_altura = tk.Label(janela, text='Altura')
label_altura.grid(row=2, column=0, padx=10, pady=10)


# Caixas Entradas:

nome_aux = tk.StringVar()
entry_nome = tk.Entry(janela, width=35, textvariable=nome_aux)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

entry_matricula = tk.Entry(janela, width =35)
entry_matricula.grid(row=1, column=1, padx=10, pady=10)

entry_altura = tk.Entry(janela, width =35)
entry_altura.grid(row=2, column=1, padx=10, pady=10)


# Botão de Cadastrar

botao_cadastrar = tk.Button(text='Cadastrar Funcionario', command=cadastrar_funcionarios)
botao_cadastrar.grid(row=4, column=0,columnspan=2, padx=10, pady=10, ipadx=80)


# Botão de Exportar

botao_exportar = tk.Button(text='Exportar para Excel', command=exporta_funcionarios)
botao_exportar.grid(row=6, column=0,columnspan=2, padx=10, pady=10, ipadx=80)

janela.mainloop()
