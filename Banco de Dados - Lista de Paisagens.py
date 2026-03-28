import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import webbrowser  # Importação necessária para abrir links

# --- Lógica de Dados ---

def load_landscapes():
    if os.path.exists("landscapes.json"):
        try:
            with open("landscapes.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []

def save_landscapes(data):
    with open("landscapes.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def open_url(url):
    """Abre o link no navegador padrão"""
    webbrowser.open_new(url)

# --- Funções da Interface ---

def register_landscape():
    city = city_entry.get().strip()
    country = country_entry.get().strip()
    landmark = landmark_entry.get().strip()
    image_url = image_url_entry.get().strip()

    if city and country and landmark and image_url:
        landscapes.append({
            "city": city, 
            "country": country, 
            "landmark": landmark, 
            "image_url": image_url
        })
        save_landscapes(landscapes)
        refresh_cards()
        for e in [city_entry, country_entry, landmark_entry, image_url_entry]:
            e.delete(0, tk.END)
        messagebox.showinfo("Cadastro", "Paisagem cadastrada com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")

def refresh_cards():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    search_term = search_entry.get().lower()
    
    for index, landscape in enumerate(landscapes):
        if (search_term in landscape["city"].lower() or 
            search_term in landscape["country"].lower() or 
            search_term in landscape.get("landmark", "").lower()):
            
            card = tk.Frame(scrollable_frame, bg="white", highlightbackground="#d1d1d1", 
                            highlightthickness=1, bd=0)
            card.pack(fill="x", padx=15, pady=8)

            info_frame = tk.Frame(card, bg="white")
            info_frame.pack(side="left", padx=15, pady=10, fill="x", expand=True)

            tk.Label(info_frame, text=f"{landscape['city']}, {landscape['country']}", 
                     font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x")
            
            tk.Label(info_frame, text=f"📍 Ponto Turístico: {landscape.get('landmark', 'N/A')}", 
                     font=("Arial", 10), bg="white", fg="#444", anchor="w").pack(fill="x")
            
            # Label do Link com evento de clique
            url = landscape['image_url']
            link_label = tk.Label(info_frame, text=url, 
                                 font=("Arial", 8, "underline"), bg="white", fg="#0000EE", 
                                 anchor="w", cursor="hand2", wraplength=500, justify="left")
            link_label.pack(fill="x")
            
            # Vincula o clique do mouse à função de abrir URL
            link_label.bind("<Button-1>", lambda e, u=url: open_url(u))

            btn_edit = tk.Button(card, text="Editar", bg="#4a90e2", fg="white", 
                                 relief="flat", padx=15,
                                 command=lambda i=index: edit_landscape(i))
            btn_edit.pack(side="right", padx=15, pady=10)

def search_landscapes(event):
    refresh_cards()

def edit_landscape(index):
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Paisagem")
    edit_window.geometry("400x400")
    edit_window.configure(bg="#f0f8ff")

    fields = [("Cidade:", "city"), ("País:", "country"), 
              ("Ponto Turístico:", "landmark"), ("Link da Imagem:", "image_url")]
    
    entries = {}
    for label_text, key in fields:
        tk.Label(edit_window, text=label_text, bg="#f0f8ff", font=("Arial", 9, "bold")).pack(pady=(10,0))
        entry = tk.Entry(edit_window, width=45)
        entry.pack(pady=5)
        entry.insert(0, landscapes[index].get(key, ""))
        entries[key] = entry

    def save_edit():
        landscapes[index] = {k: e.get().strip() for k, e in entries.items()}
        save_landscapes(landscapes)
        refresh_cards()
        messagebox.showinfo("Sucesso", "Dados atualizados!")
        edit_window.destroy()

    def confirm_delete():
        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            landscapes.pop(index)
            save_landscapes(landscapes)
            refresh_cards()
            edit_window.destroy()

    tk.Button(edit_window, text="Salvar Alterações", bg="#28a745", fg="white", 
              font=("Arial", 10, "bold"), command=save_edit, width=20).pack(pady=20)
    tk.Button(edit_window, text="Excluir Paisagem", bg="#d9534f", fg="white", 
              command=confirm_delete, width=20).pack()

# --- Estrutura da Janela Principal ---

root = tk.Tk()
root.title("📍 Explorador de Paisagens")
root.geometry("850x700")
root.configure(bg="#eef2f5")

header = tk.Frame(root, bg="#eef2f5", pady=20)
header.pack(fill="x")

input_frame = tk.Frame(header, bg="#eef2f5")
input_frame.pack()

labels = ["Cidade:", "País:", "Ponto Turístico:", "Link da Imagem:"]
entry_widgets = []
for i, text in enumerate(labels):
    tk.Label(input_frame, text=text, bg="#eef2f5", font=("Arial", 9)).grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entry = tk.Entry(input_frame, width=50)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry_widgets.append(entry)

city_entry, country_entry, landmark_entry, image_url_entry = entry_widgets

tk.Button(header, text="Cadastrar Paisagem", command=register_landscape, 
          bg="#28a745", fg="white", font=("Arial", 10, "bold"), pady=5, padx=20).pack(pady=10)

search_container = tk.Frame(root, bg="#eef2f5", padx=20, pady=10)
search_container.pack(fill="x")
tk.Label(search_container, text="🔍 Buscar:", bg="#eef2f5", font=("Arial", 10, "bold")).pack(side="left")
search_entry = tk.Entry(search_container)
search_entry.pack(side="left", fill="x", expand=True, padx=10)
search_entry.bind("<KeyRelease>", search_landscapes)

container = tk.Frame(root, bg="#eef2f5")
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg="#eef2f5", highlightthickness=0)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#eef2f5")

window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

landscapes = load_landscapes()
refresh_cards()

root.mainloop()
