import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Função para carregar dados do JSON
def load_landscapes():
    if os.path.exists("landscapes.json"):
        with open("landscapes.json", "r") as file:
            return json.load(file)
    return []

# Função para salvar dados no JSON
def save_landscapes(data):
    with open("landscapes.json", "w") as file:
        json.dump(data, file, indent=4)

# Função para cadastrar uma nova paisagem
def register_landscape():
    city = city_entry.get().strip()
    country = country_entry.get().strip()
    image_url = image_url_entry.get().strip()

    if city and country and image_url:
        landscapes.append({"city": city, "country": country, "image_url": image_url})
        save_landscapes(landscapes)
        refresh_table()
        city_entry.delete(0, tk.END)
        country_entry.delete(0, tk.END)
        image_url_entry.delete(0, tk.END)
        messagebox.showinfo("Cadastro", "Paisagem cadastrada com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

# Função para atualizar a tabela com os dados do JSON
def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for index, landscape in enumerate(landscapes):
        table.insert("", "end", values=(landscape["city"], landscape["country"], landscape["image_url"], "Editar/Excluir"))

# Função para excluir uma paisagem
def delete_landscape(index):
    landscapes.pop(index)
    save_landscapes(landscapes)
    refresh_table()
    messagebox.showinfo("Exclusão", "Paisagem excluída com sucesso!")

# Função para buscar paisagens
def search_landscapes(event):
    search_term = search_entry.get().lower()
    filtered_landscapes = [l for l in landscapes if search_term in l["city"].lower() or search_term in l["country"].lower()]
    for row in table.get_children():
        table.delete(row)
    for index, landscape in enumerate(filtered_landscapes):
        table.insert("", "end", values=(landscape["city"], landscape["country"], landscape["image_url"], "Editar/Excluir"))

# Função para editar uma paisagem
def edit_landscape(index):
    # Cria uma nova janela para editar os dados
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Paisagem")
    edit_window.geometry("400x300")
    edit_window.configure(bg="#f0f8ff")

    # Campos para edição
    tk.Label(edit_window, text="Cidade:", bg="#f0f8ff").pack(pady=5)
    edit_city = tk.Entry(edit_window)
    edit_city.pack(pady=5)
    edit_city.insert(0, landscapes[index]["city"])  # Preenche com o valor atual

    tk.Label(edit_window, text="País:", bg="#f0f8ff").pack(pady=5)
    edit_country = tk.Entry(edit_window)
    edit_country.pack(pady=5)
    edit_country.insert(0, landscapes[index]["country"])  # Preenche com o valor atual

    tk.Label(edit_window, text="Link da Paisagem:", bg="#f0f8ff").pack(pady=5)
    edit_image_url = tk.Entry(edit_window)
    edit_image_url.pack(pady=5)
    edit_image_url.insert(0, landscapes[index]["image_url"])  # Preenche com o valor atual

    # Função para salvar as edições
    def save_edit():
        new_city = edit_city.get().strip()
        new_country = edit_country.get().strip()
        new_image_url = edit_image_url.get().strip()

        if new_city and new_country and new_image_url:
            landscapes[index] = {"city": new_city, "country": new_country, "image_url": new_image_url}
            save_landscapes(landscapes)
            refresh_table()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            edit_window.destroy()  # Fecha a janela de edição
        else:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

    # Função para excluir a paisagem
    def confirm_delete():
        if messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir esta paisagem?"):
            delete_landscape(index)
            edit_window.destroy()  # Fecha a janela de edição

    # Botões para salvar edições e excluir paisagem
    save_button = tk.Button(edit_window, text="Salvar", command=save_edit, bg="#4a90e2", fg="white")
    save_button.pack(pady=10)
    
    delete_button = tk.Button(edit_window, text="Excluir", command=confirm_delete, bg="#d9534f", fg="white")
    delete_button.pack(pady=10)

# Interface gráfica
root = tk.Tk()
root.title("Cadastro e Lista de Paisagens")
root.geometry("700x500")
root.configure(bg="#f0f8ff")

# Entrada de dados
tk.Label(root, text="Cidade:", bg="#f0f8ff").pack()
city_entry = tk.Entry(root)
city_entry.pack()

tk.Label(root, text="País:", bg="#f0f8ff").pack()
country_entry = tk.Entry(root)
country_entry.pack()

tk.Label(root, text="Link da Paisagem:", bg="#f0f8ff").pack()
image_url_entry = tk.Entry(root)
image_url_entry.pack()

register_button = tk.Button(root, text="Cadastrar", command=register_landscape, bg="#28a745", fg="white")
register_button.pack(pady=10)

# Entrada de busca
search_entry = tk.Entry(root)
search_entry.pack()
search_entry.bind("<KeyRelease>", search_landscapes)

# Tabela de exibição
table = ttk.Treeview(root, columns=("city", "country", "image_url", "actions"), show="headings")
table.heading("city", text="Cidade")
table.heading("country", text="País")
table.heading("image_url", text="Link da Paisagem")
table.heading("actions", text="Ações")
table.pack(fill=tk.BOTH, expand=True)

# Função para associar ações de edição e exclusão à tabela
def table_action(event):
    selected_item = table.selection()[0]
    selected_index = table.index(selected_item)
    col_id = table.identify_column(event.x)
    
    # Coluna de ações, onde estão os botões
    if col_id == "#4":  # Verifica se a coluna é "Ações"
        edit_landscape(selected_index)

table.bind("<Double-1>", table_action)

# Carrega os dados iniciais e atualiza a tabela
landscapes = load_landscapes()
refresh_table()

root.mainloop()
