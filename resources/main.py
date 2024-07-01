#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox
import scrapping
import db_queries

# PROGRAMA DESENVOLVIDO POR LUCAS WILLIAM MARTINS LIMA
# LinkedIn: https://www.linkedin.com/in/lucaswmlima
# Github: https://www.github.com/LucaswmLima
# Outros Trabalhos: portfolio-lucaswilliam.vercel.app

def screen():
    class ConectarDB:
        def __init__(self):
            self.con = sqlite3.connect('./data/base.db')
            self.cur = self.con.cursor()

        def inserir_registro(self, name):
            try:
                self.cur.execute(
                    f'INSERT INTO dealerships (name)VALUES ("{name}")')
            except Exception as e:
                print('\n[x] Falha ao inserir registro [x]\n')
                print('[x] Revertendo operação (rollback) %s [x]\n' % e)
                self.con.rollback()
            else:
                self.con.commit()
                print('\n[!] Registro inserido com sucesso [!]\n')
            
            db_queries.set_index()
            db_queries.max_sequence_set()

        def consultar_registros(self):
            return self.cur.execute('SELECT rowid, * FROM dealerships').fetchall()

        def consultar_ultimo_rowid(self):
            return self.cur.execute('SELECT MAX(rowid) FROM dealerships').fetchone()
        
        def atualizar_registro(self, rowid, newName):
            try:

                self.cur.execute(f'UPDATE dealerships SET name ="{newName}" WHERE id={rowid}')
            except Exception as e:
                print('\n[x] Falha ao atualizar registro [x]\n')
                print('[x] Revertendo operação (rollback) %s [x]\n' % e)
                self.con.rollback()
                db_queries.set_index()
                db_queries.max_sequence_set()
            else:
                self.con.commit()
                print('\n[!] Registro atualizado com sucesso [!]\n')
                db_queries.set_index()
                db_queries.max_sequence_set()

        def remover_registro(self, rowid):
            try:
                self.cur.execute("DELETE FROM dealerships WHERE rowid=?", (rowid,))
            except Exception as e:
                print('\n[x] Falha ao remover registro [x]\n')
                print('[x] Revertendo operação (rollback) %s [x]\n' % e)
                self.con.rollback()
                db_queries.set_index()
                db_queries.max_sequence_set()
            else:
                self.con.commit()
                print('\n[!] Registro removido com sucesso [!]\n')
                db_queries.set_index()
                db_queries.max_sequence_set()

    class Janela(tk.Frame):
        """Janela principal"""

        def __init__(self, master=None):
            """Construtor"""
            super().__init__(master)
            # Coletando informações do monitor
            self.treeview = None
            self.entry_documento = None
            largura = 800
            altura = 520
            tamanho = ('%sx%s' % (largura, altura))
            

            # Título da janela principal.
            master.title('Xentry Automation')
            master.iconbitmap("./assets/automation.ico")

            # Tamanho da janela principal.
            master.geometry(tamanho)
            root.resizable(width=0, height=0)

            # Instanciando a conexão com o banco.
            self.banco = ConectarDB()

            # Gerenciador de layout da janela principal.
            self.pack()

            # Criando os widgets da interface.
            self.criar_widgets()

        def criar_widgets(self):
            # Containers.
            frame6 = tk.Frame(self)
            frame6.pack(fill=tk.BOTH, expand=True, pady=(20,0))

            frame1 = tk.Frame(self)
            frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=(10,15))

            frame2 = tk.Frame(self)
            frame2.pack(fill=tk.BOTH, expand=True)

            frame5 = tk.Frame(self)
            frame5.pack(side=tk.BOTTOM, padx=5)

            frame4 = tk.Frame(self)
            frame4.pack(side=tk.BOTTOM, padx=5)

            frame3 = tk.Frame(self)
            frame3.pack(side=tk.BOTTOM, padx=5)

            # Labels.
            label_documento = tk.Label(frame1, text='Concessionária')
            label_documento.grid(row=0, column=0)

            label_documento = tk.Label(frame6, text='Usuário')
            label_documento.grid(row=0, column=0)

            label_documento = tk.Label(frame6, text='Senha')
            label_documento.grid(row=0, column=1)


            # label_assunto = tk.Label(frame1, text='Assunto')
            # label_assunto.grid(row=0, column=1)

            # label_recebido = tk.Label(frame1, text='Data recebimento')
            # label_recebido.grid(row=0, column=2)

            # Entrada de texto.
            self.entry_documento = tk.Entry(frame1)
            self.entry_documento.grid(row=1, column=0, pady=5,padx=(0,10))
            self.entry_documento.config(width=50)

            self.entry_documento1 = tk.Entry(frame6)
            self.entry_documento1.grid(row=1, column=0, pady=5,padx=(0,8))
            self.entry_documento1.config(width=24)

            self.entry_documento2 = tk.Entry(frame6)
            self.entry_documento2.grid(row=1, column=1, pady=5)
            self.entry_documento2.config(width=24, show= '*')

            # self.entry_assunto = tk.Entry(frame1)
            # self.entry_assunto.grid(row=1, column=1, padx=10)

            # self.entry_data = tk.Entry(frame1)
            # self.entry_data.grid(row=1, column=2)

            # Botão para adicionar um novo registro.
            button_adicionar = tk.Button(frame1, text='Adicionar', bg='#3498DB', fg='white', activebackground='#2980B9',
                                         activeforeground='white', relief="groove", width=10)
            # Método que é chamado quando o botão é clicado.
            button_adicionar['command'] = self.adicionar_registro
            button_adicionar.grid(row=0, column=3, rowspan=2, padx=10)

            # Botão para alterar um registro.
            button_adicionar = tk.Button(frame1, text='Alterar', bg='#3498DB', fg='white', activebackground='#2980B9',
                                         activeforeground='white', relief="groove", width=10)
            # Método que é chamado quando o botão é clicado.
            button_adicionar['command'] = self.att_registro
            button_adicionar.grid(row=0, column=4, rowspan=2, padx=1)

            # Botão para alterar um usuario.
            button_adicionar = tk.Button(frame6, text='Atualizar', bg='#E74C3C', fg='white', activebackground='#2980B9',
                                         activeforeground='white', relief="groove", width=10)
            # Método que é chamado quando o botão é clicado.
            button_adicionar['command'] = self.att_usuario
            button_adicionar.grid(row=0, column=4, rowspan=2, padx=20)
            
            # Treeview.
            self.treeview = tkk.Treeview(frame2, columns=('ID', 'Concessionária'))
            self.treeview.heading('#0', text='ID')
            self.treeview.heading('#1', text='Concessionária')
            self.treeview.column("#0", minwidth=100, width=100, stretch=False)
            self.treeview.column("#1", minwidth=600, width=600, stretch=False)
            self.treeview.column("#2", minwidth=0, width=0, stretch=False)
            # self.treeview.heading('#2', text='Assunto')
            # self.treeview.heading('#3', text='Data')

            vsb = tkk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
            vsb.place(x=30+652+2, y=148, height=202+20)

            self.treeview.configure(yscrollcommand=vsb.set)

            # Inserindo os dados do banco no treeview.
            for row in self.banco.consultar_registros():
                self.treeview.insert('', 'end', text=row[0], values=(row[2], ''))

            self.treeview.pack(fill=tk.BOTH, expand=True)

            # Botão para remover um item.
            button_excluir = tk.Button(frame1, text='Excluir', bg='#E74C3C', fg='white', activebackground='#C0392B',
                                       activeforeground='white', relief="groove", width=10, height=1)
            # Método que é chamado quando o botão é clicado.
            button_excluir['command'] = self.excluir_registro
            button_excluir.grid(row=0, column=5, rowspan=2, padx=10)

             # Botão para retomar a automação.
            button_excluir_data = tk.Button(frame5, text='Retomar automação', bg='#E74C3C', fg='white', activebackground='#C0392B',
                                       activeforeground='white', relief="groove", width=20, height=2)
            # Método que é chamado quando o botão é clicado.
            button_excluir_data['command'] = scrapping.start_mode_1
            button_excluir_data.pack(pady=10)

            # Botão para iniciar a automação
            button_start = tk.Button(frame4, text='Iniciar automação', bg='#3498DB', fg='white',
                                     activebackground='#2980B9', activeforeground='white', relief="groove", width=20,
                                     height=2)
            # Método que é chamado quando o botão é clicado.
            button_start['command'] = scrapping.start_mode_0
            button_start.pack(pady=(20,10))

            

        def adicionar_registro(self):
            # Coletando os valores.
            nameEntry = self.entry_documento.get()
            # assunto = self.entry_assunto.get()
            # data = self.entry_data.get()

            # Validação simples (utilizar datetime deve ser melhor para validar).
            # validar_data = re.search(r'(..)/(..)/(....)', data)
            # validar_data = 'ok'

            # Se a data digitada passar na validação
            if nameEntry != '':
                # Dados digitando são inseridos no banco de dados
                self.banco.inserir_registro(name=nameEntry)

                # # Coletando a ultima rowid que foi inserida no banco.
                # rowid = self.banco.consultar_ultimo_rowid()[0]

                # Atualizando os novos dados no treeview.
                for item in self.treeview.get_children():
                    self.treeview.delete(item)
                for row in self.banco.consultar_registros():
                    self.treeview.insert('', 'end', text=row[0], values=(row[2], ''))

            else:
                # Caso a data não passe na validação é exibido um alerta.
                messagebox.showerror('Erro', 'Insira a concessiorária!')
        
        def att_usuario(self):
            # Coletando os valores.
            userEntry = self.entry_documento1.get()
            passwordEntry = self.entry_documento2.get()

            # Se a data digitada passar na validação
            if userEntry != '' and passwordEntry != '':
                # Dados digitando são inseridos no banco de dados
                db_queries.update_user(userEntry,passwordEntry)
                db_queries.att_user()


            else:
                # Caso a data não passe na validação é exibido um alerta.
                messagebox.showerror('Erro', 'Insira a concessiorária!')

        def excluir_registro(self):
            # Verificando se algum item está selecionado.
            if not self.treeview.focus():
                messagebox.showerror('Erro', 'Nenhum item selecionado')
            else:
                # Coletando qual item está selecionado.
                item_selecionado = self.treeview.focus()

                # Coletando os dados do item selecionado (dicionário).
                rowid = self.treeview.item(item_selecionado)

                # Removendo o item com base no valor do rowid (argumento text do treeview).
                # Removendo valor da tabela.
                self.banco.remover_registro(rowid['text'])

                # Removendo valor do treeview.
                self.treeview.delete(item_selecionado)
        
        def att_registro(self):
            # Verificando se algum item está selecionado.
            if not self.treeview.focus():
                messagebox.showerror('Erro', 'Nenhum item selecionado')
            else:
                # Coletando qual item está selecionado.
                item_selecionado = self.treeview.focus()

                # Coletando os dados do item selecionado (dicionário).
                rowid = self.treeview.item(item_selecionado)
                newEntry = self.entry_documento.get()
            
            # Removendo o item com base no valor do rowid (argumento text do treeview).
                # Removendo valor da tabela.
                self.banco.atualizar_registro(rowid['text'],newName=newEntry)

            # Atualizando os novos dados no treeview.
                for item in self.treeview.get_children():
                    self.treeview.delete(item)
                for row in self.banco.consultar_registros():
                    self.treeview.insert('', 'end', text=row[0], values=(row[2], ''))


    root = tk.Tk()
    app = Janela(master=root)
    app.mainloop()


try:
    screen()

except:
    print("Algo de errado ocorreu verifique seus dados =(")

sys.exit()
