import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Nome do arquivo onde os dados serão armazenados
FILE_NAME = "equipamentos.json"

# Carregar dados existentes
try:
    with open(FILE_NAME, "r") as file:
        equipamentos = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    equipamentos = []

def salvar_dados():
    with open(FILE_NAME, "w") as file:
        json.dump(equipamentos, file, indent=4)

def cadastrar_equipamento():
    cliente = entry_cliente.get()
    tipo = entry_tipo.get()
    defeito = entry_defeito.get()
    
    if not cliente or not tipo or not defeito:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
        return
    
    data_recebimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Recebido"
    
    equipamento = {
        "id": len(equipamentos) + 1,
        "cliente": cliente,
        "tipo": tipo,
        "defeito": defeito,
        "data_recebimento": data_recebimento,
        "status": status
    }
    
    equipamentos.append(equipamento)
    salvar_dados()
    messagebox.showinfo("Sucesso", "Equipamento cadastrado com sucesso!")
    entry_cliente.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_defeito.delete(0, tk.END)
    listar_equipamentos()

def listar_equipamentos():
    listbox_equipamentos.delete(0, tk.END)
    for eq in equipamentos:
        listbox_equipamentos.insert(tk.END, f"ID: {eq['id']} | Cliente: {eq['cliente']} | Tipo: {eq['tipo']} | Status: {eq['status']}")

def atualizar_status():
    try:
        selecionado = listbox_equipamentos.curselection()[0]
        id_eq = equipamentos[selecionado]['id']
        novo_status = entry_status.get()
        
        if not novo_status:
            messagebox.showwarning("Atenção", "O campo de status não pode estar vazio!")
            return
        
        for eq in equipamentos:
            if eq['id'] == id_eq:
                eq['status'] = novo_status
                salvar_dados()
                messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
                entry_status.delete(0, tk.END)
                listar_equipamentos()
                return
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um equipamento para atualizar o status!")

# Criando a interface gráfica
root = tk.Tk()
root.title("Controle de Equipamentos")
root.geometry("600x400")

frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

lbl_cliente = tk.Label(frame_cadastro, text="Nome do Cliente:")
lbl_cliente.grid(row=0, column=0)
entry_cliente = tk.Entry(frame_cadastro)
entry_cliente.grid(row=0, column=1)

lbl_tipo = tk.Label(frame_cadastro, text="Tipo de Equipamento:")
lbl_tipo.grid(row=1, column=0)
entry_tipo = tk.Entry(frame_cadastro)
entry_tipo.grid(row=1, column=1)

lbl_defeito = tk.Label(frame_cadastro, text="Defeito Relatado:")
lbl_defeito.grid(row=2, column=0)
entry_defeito = tk.Entry(frame_cadastro)
entry_defeito.grid(row=2, column=1)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_equipamento)
btn_cadastrar.grid(row=3, columnspan=2, pady=5)

frame_lista = tk.Frame(root)
frame_lista.pack(pady=10)

listbox_equipamentos = tk.Listbox(frame_lista, width=80)
listbox_equipamentos.pack()

frame_status = tk.Frame(root)
frame_status.pack(pady=10)

lbl_status = tk.Label(frame_status, text="Novo Status:")
lbl_status.grid(row=0, column=0)
entry_status = tk.Entry(frame_status)
entry_status.grid(row=0, column=1)

btn_atualizar = tk.Button(frame_status, text="Atualizar Status", command=atualizar_status)
btn_atualizar.grid(row=0, column=2, padx=5)

listar_equipamentos()
root.mainloop()
