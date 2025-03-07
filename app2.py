import json
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
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

def listar_equipamentos():
    listbox_equipamentos.delete(0, tk.END)
    for i, equipamento in enumerate(equipamentos):
        listbox_equipamentos.insert(i, f"{equipamento['id']} - {equipamento['cliente']} ({equipamento['tipo']}) - {equipamento['status']}")

def atualizar_campos():
    for widget in frame_detalhes.winfo_children():
        widget.destroy()
    
    tipo = combo_tipo.get()
    campos = []
    checkboxes = {}
    
    if tipo == "Notebook":
        campos = ["Marca", "Modelo"]
        checkboxes = {"Acompanha Carregador": tk.BooleanVar()}
    elif tipo == "Impressora":
        campos = ["Marca", "Modelo"]
        checkboxes = {"Acompanha Cabo de Alimentação": tk.BooleanVar(), "Acompanha Cabo de Força": tk.BooleanVar()}
    elif tipo == "Desktop":
        checkboxes = {"Acompanha Cabo de Força": tk.BooleanVar(), "Acompanha Teclado": tk.BooleanVar(), "Acompanha Mouse": tk.BooleanVar()}
    
    global entradas_detalhes
    entradas_detalhes = {}
    
    for i, campo in enumerate(campos):
        lbl = tk.Label(frame_detalhes, text=campo + ":")
        lbl.grid(row=i, column=0)
        entry = tk.Entry(frame_detalhes)
        entry.grid(row=i, column=1)
        entradas_detalhes[campo] = entry
    
    for j, (campo, var) in enumerate(checkboxes.items(), start=len(campos)):
        chk = tk.Checkbutton(frame_detalhes, text=campo, variable=var)
        chk.grid(row=j, columnspan=2, sticky='w')
        entradas_detalhes[campo] = var

def cadastrar_equipamento():
    cliente = entry_cliente.get()
    tipo = combo_tipo.get()
    defeito = entry_defeito.get()
    
    if not cliente or not tipo or not defeito:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
        return
    
    detalhes = {campo: (entrada.get() if isinstance(entrada, tk.Entry) else entrada.get()) for campo, entrada in entradas_detalhes.items()}
    data_recebimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Recebido"
    
    equipamento = {
        "id": len(equipamentos) + 1,
        "cliente": cliente,
        "tipo": tipo,
        "defeito": defeito,
        "detalhes": detalhes,
        "data_recebimento": data_recebimento,
        "status": status
    }
    
    equipamentos.append(equipamento)
    salvar_dados()
    messagebox.showinfo("Sucesso", "Equipamento cadastrado com sucesso!")
    entry_cliente.delete(0, tk.END)
    entry_defeito.delete(0, tk.END)
    combo_tipo.set("")
    atualizar_campos()
    listar_equipamentos()

def alterar_status():
    selecionado = listbox_equipamentos.curselection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um equipamento para alterar o status!")
        return
    
    index = selecionado[0]
    novo_status = simpledialog.askstring("Alterar Status", "Digite o novo status:")
    if novo_status:
        equipamentos[index]["status"] = novo_status
        salvar_dados()
        listar_equipamentos()

def editar_registro():
    selecionado = listbox_equipamentos.curselection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um equipamento para editar!")
        return
    
    index = selecionado[0]
    equipamento = equipamentos[index]
    entry_cliente.delete(0, tk.END)
    entry_cliente.insert(0, equipamento["cliente"])
    combo_tipo.set(equipamento["tipo"])
    entry_defeito.delete(0, tk.END)
    entry_defeito.insert(0, equipamento["defeito"])
    atualizar_campos()
    
    equipamentos.pop(index)
    salvar_dados()
    listar_equipamentos()

def excluir_registro():
    selecionado = listbox_equipamentos.curselection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um equipamento para excluir!")
        return
    
    index = selecionado[0]
    equipamentos.pop(index)
    salvar_dados()
    listar_equipamentos()
    messagebox.showinfo("Sucesso", "Equipamento excluído com sucesso!")

# Criando a interface gráfica
root = tk.Tk()
root.title("Controle de Equipamentos")
root.geometry("700x500")

frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

lbl_cliente = tk.Label(frame_cadastro, text="Nome do Cliente:")
lbl_cliente.grid(row=0, column=0)
entry_cliente = tk.Entry(frame_cadastro)
entry_cliente.grid(row=0, column=1)

lbl_tipo = tk.Label(frame_cadastro, text="Tipo de Equipamento:")
lbl_tipo.grid(row=1, column=0)
combo_tipo = ttk.Combobox(frame_cadastro, values=["Notebook", "Impressora", "Desktop"], state="readonly")
combo_tipo.grid(row=1, column=1)
combo_tipo.bind("<<ComboboxSelected>>", lambda e: atualizar_campos())

lbl_defeito = tk.Label(frame_cadastro, text="Defeito Relatado:")
lbl_defeito.grid(row=2, column=0)
entry_defeito = tk.Entry(frame_cadastro)
entry_defeito.grid(row=2, column=1)

frame_detalhes = tk.Frame(root)
frame_detalhes.pack(pady=10)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_equipamento)
btn_cadastrar.grid(row=3, columnspan=2, pady=5)

btn_alterar = tk.Button(root, text="Alterar Status", command=alterar_status)
btn_alterar.pack()

btn_editar = tk.Button(root, text="Editar Registro", command=editar_registro)
btn_editar.pack()

btn_excluir = tk.Button(root, text="Excluir Registro", command=excluir_registro)
btn_excluir.pack()

frame_lista = tk.Frame(root)
frame_lista.pack(pady=10)

listbox_equipamentos = tk.Listbox(frame_lista, width=80)
listbox_equipamentos.pack()

listar_equipamentos()
root.mainloop()
