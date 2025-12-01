import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
import tkinter as tk
import requests
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import Counter

# Configurações da API
BASE_URL = "http://apipf.jogajuntoinstituto.org"
LOGIN_ENDPOINT = "/login"

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GerenciadorProdutosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Produtos - API")
        self.root.geometry("1100x750")
        
        self.token = None
        self.image_path = None
        self.produtos_lista = []
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal com abas
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Criar abas
        self.tabview.add("🔐 Login")
        self.tabview.add("📋 Listar Produtos")
        self.tabview.add("➕ Cadastrar")
        self.tabview.add("🗑️ Excluir")
        
        # Configurar cada aba
        self.criar_aba_login()
        self.criar_aba_listagem()
        self.criar_aba_cadastro()
        self.criar_aba_exclusao()
        
    def criar_aba_login(self):
        tab = self.tabview.tab("🔐 Login")
        
        # Frame central
        frame_central = ctk.CTkFrame(tab)
        frame_central.place(relx=0.5, rely=0.4, anchor='center')
        
        ctk.CTkLabel(frame_central, text="Email:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, sticky='e', padx=10, pady=15
        )
        self.entry_email = ctk.CTkEntry(frame_central, width=350, height=40, font=ctk.CTkFont(size=13))
        self.entry_email.grid(row=0, column=1, padx=10, pady=15)
        self.entry_email.insert(0, "fabinho_marquez@hotmail.com.br")
        
        ctk.CTkLabel(frame_central, text="Senha:", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=1, column=0, sticky='e', padx=10, pady=15
        )
        self.entry_senha = ctk.CTkEntry(frame_central, width=350, height=40, show='*', font=ctk.CTkFont(size=13))
        self.entry_senha.grid(row=1, column=1, padx=10, pady=15)
        self.entry_senha.insert(0, "1234")
        
        ctk.CTkButton(
            frame_central, 
            text="Fazer Login",
            command=self.fazer_login,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        ).grid(row=2, column=0, columnspan=2, pady=25)
        
        # Status do login
        self.label_status_login = ctk.CTkLabel(
            tab, 
            text="", 
            font=ctk.CTkFont(size=13)
        )
        self.label_status_login.place(relx=0.5, rely=0.6, anchor='center')
        
    def criar_aba_listagem(self):
        tab = self.tabview.tab("📋 Listar Produtos")
        
        # Botão de atualizar
        ctk.CTkButton(
            tab, 
            text="🔄 Atualizar Lista e Gráficos", 
            command=self.listar_produtos,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        ).pack(pady=15)
        
        # Frame principal vertical: tabela acima, gráfico abaixo
        frame_principal = tk.Frame(tab, bg='#2b2b2b')
        frame_principal.pack(fill='both', expand=True, padx=15, pady=10)

        # Frame da tabela (parte superior)
        frame_tabela = tk.Frame(frame_principal, bg='#2b2b2b')
        frame_tabela.pack(side='top', fill='both', expand=True, padx=(0, 5), pady=(0, 5))
        
        # Label da tabela
        label_tabela = tk.Label(
            frame_tabela,
            text="Lista de Produtos",
            font=('Arial', 14, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        label_tabela.pack(pady=5)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabela, orient='vertical')
        scroll_x = tk.Scrollbar(frame_tabela, orient='horizontal')
        
        # Treeview com estilo customizado
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 10))
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       borderwidth=0,
                       font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        self.tree_produtos = ttk.Treeview(
            frame_tabela,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            style="Treeview"
        )
        
        scroll_y.configure(command=self.tree_produtos.yview)
        scroll_x.configure(command=self.tree_produtos.xview)
        
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        self.tree_produtos.pack(side='left', fill='both', expand=True)
        
        # Frame do gráfico (parte inferior) - altura fixa
        self.frame_grafico = tk.Frame(frame_principal, bg='#2b2b2b', height=300)
        self.frame_grafico.pack(side='bottom', fill='x')
        self.frame_grafico.pack_propagate(False)
        
    def criar_grafico_precos(self, produtos):
        """Cria dois gráficos de pizza lado a lado: por faixa de preço e por categoria."""

        # Limpar todos os widgets do frame
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        if not produtos:
            label_vazio = tk.Label(
                self.frame_grafico,
                text="Sem dados para exibir",
                font=('Arial', 14),
                bg='#2b2b2b',
                fg='white'
            )
            label_vazio.pack(pady=20)
            return

        # === PROCESSAR DADOS ===
        # Faixas de preço
        ate_100 = ate_200 = acima_200 = 0
        for p in produtos:
            try:
                preco = float(p.get('price', 0))
                if preco <= 100:
                    ate_100 += 1
                elif preco <= 200:
                    ate_200 += 1
                else:
                    acima_200 += 1
            except:
                continue

        # Categorias
        categorias = [p.get('category', 'Outros') for p in produtos]
        count_cats = Counter(categorias)

        # === CRIAR FIGURA LADO A LADO ===
        fig = Figure(figsize=(10, 4), facecolor='#2b2b2b', dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # --- PIZZA 1: Faixa de Preço ---
        valores_preco = [ate_100, ate_200, acima_200]
        labels_preco = ['≤ R$100', 'R$101-200', '> R$200']
        cores_preco = ['#2ecc71', '#f1c40f', '#e74c3c']

        dados_preco = [(l, v, c) for l, v, c in zip(labels_preco, valores_preco, cores_preco) if v > 0]
        if dados_preco:
            labs_p, vals_p, cols_p = zip(*dados_preco)
            wedges, texts, autotexts = ax1.pie(vals_p, labels=labs_p, colors=cols_p, autopct='%1.1f%%', startangle=90, textprops={'color':'white'})
            for t in texts + autotexts:
                t.set_color('white')
        else:
            ax1.text(0.5, 0.5, 'Sem dados', ha='center', va='center', color='white')

        ax1.set_title('Por Faixa de Preço', color='white', fontsize=12, fontweight='bold')
        ax1.set_facecolor('#2b2b2b')

        # --- PIZZA 2: Categoria ---
        if count_cats:
            labels_cat = list(count_cats.keys())
            sizes_cat = list(count_cats.values())
            # cores ciclicas
            cores_cat = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c', '#34495e']
            wedges2, texts2, autotexts2 = ax2.pie(sizes_cat, labels=labels_cat, autopct='%1.1f%%', colors=(cores_cat * 10)[:len(labels_cat)])
            for t in texts2 + autotexts2:
                t.set_color('white')
        else:
            ax2.text(0.5, 0.5, 'Sem dados', ha='center', va='center', color='white')

        ax2.set_title('Por Categoria', color='white', fontsize=12, fontweight='bold')
        ax2.set_facecolor('#2b2b2b')

        # === RENDERIZAR NO TKINTER ===
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg='#2b2b2b')
        canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)

        # FORÇAR ATUALIZAÇÃO
        self.frame_grafico.update_idletasks()
        canvas_widget.update()
        
    def criar_aba_cadastro(self):
        tab = self.tabview.tab("➕ Cadastrar")
        
        # Frame scrollável
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Título
        ctk.CTkLabel(
            scroll_frame, 
            text="Cadastrar Novo Produto",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)
        
        # Frame do formulário
        frame_form = ctk.CTkFrame(scroll_frame)
        frame_form.pack(pady=10, padx=20, fill='both')
        
        # Nome
        ctk.CTkLabel(frame_form, text="Nome:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, sticky='w', padx=15, pady=12
        )
        self.entry_nome = ctk.CTkEntry(frame_form, width=450, height=40, font=ctk.CTkFont(size=12))
        self.entry_nome.grid(row=0, column=1, padx=15, pady=12, sticky='ew')
        
        # Descrição
        ctk.CTkLabel(frame_form, text="Descrição:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=1, column=0, sticky='nw', padx=15, pady=12
        )
        self.text_descricao = ctk.CTkTextbox(frame_form, width=450, height=100, font=ctk.CTkFont(size=12))
        self.text_descricao.grid(row=1, column=1, padx=15, pady=12, sticky='ew')
        
        # Preço
        ctk.CTkLabel(frame_form, text="Preço (R$):", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=2, column=0, sticky='w', padx=15, pady=12
        )
        self.entry_preco = ctk.CTkEntry(frame_form, width=450, height=40, font=ctk.CTkFont(size=12))
        self.entry_preco.grid(row=2, column=1, padx=15, pady=12, sticky='ew')
        
        # Categoria
        ctk.CTkLabel(frame_form, text="Categoria:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=3, column=0, sticky='w', padx=15, pady=12
        )
        self.entry_categoria = ctk.CTkComboBox(
            frame_form, 
            values=["Calçados", "Acessórios", "Roupas"],
            width=450,
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.entry_categoria.grid(row=3, column=1, padx=15, pady=12, sticky='ew')
    
        
        # Frete
        ctk.CTkLabel(frame_form, text="Frete (R$):", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=4, column=0, sticky='w', padx=15, pady=12
        )
        self.entry_frete = ctk.CTkEntry(frame_form, width=450, height=40, font=ctk.CTkFont(size=12))
        self.entry_frete.grid(row=4, column=1, padx=15, pady=12, sticky='ew')
        
        # Imagem
        ctk.CTkLabel(frame_form, text="Imagem:", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=5, column=0, sticky='w', padx=15, pady=12
        )
        frame_img = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_img.grid(row=5, column=1, sticky='w', padx=15, pady=12)
        
        self.label_imagem = ctk.CTkLabel(
            frame_img, 
            text="Nenhuma imagem selecionada",
            text_color="gray"
        )
        self.label_imagem.pack(side='left', padx=(0, 10))
        
        ctk.CTkButton(
            frame_img, 
            text="📁 Selecionar",
            command=self.selecionar_imagem,
            width=120,
            height=35,
            corner_radius=8
        ).pack(side='left')
        
        frame_form.grid_columnconfigure(1, weight=1)
        
        # Botão de cadastrar
        ctk.CTkButton(
            scroll_frame,
            text="✅ Cadastrar Produto",
            command=self.cadastrar_produto,
            width=250,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=25)
        
    def criar_aba_exclusao(self):
        tab = self.tabview.tab("🗑️ Excluir")
        
        # Frame superior para o campo de ID e botão
        frame_superior = ctk.CTkFrame(tab)
        frame_superior.pack(fill='x', padx=15, pady=15)
        
        ctk.CTkLabel(
            frame_superior, 
            text="ID do Produto:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side='left', padx=10)
        
        self.entry_id_delete = ctk.CTkEntry(
            frame_superior, 
            width=200, 
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.entry_id_delete.pack(side='left', padx=10)
        
        ctk.CTkButton(
            frame_superior,
            text="🗑️ Excluir Produto",
            command=self.deletar_produto,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side='left', padx=10)
        
        ctk.CTkButton(
            frame_superior,
            text="🔄 Atualizar Lista",
            command=self.atualizar_lista_exclusao,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        ).pack(side='left', padx=10)
        
        # Frame para a tabela de produtos
        frame_tabela = ctk.CTkFrame(tab)
        frame_tabela.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Label da tabela
        ctk.CTkLabel(
            frame_tabela,
            text="Lista de Produtos Disponíveis",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # Scrollbars
        scroll_y = ctk.CTkScrollbar(frame_tabela, orientation='vertical')
        scroll_x = ctk.CTkScrollbar(frame_tabela, orientation='horizontal')
        
        # Treeview (usar o mesmo estilo da outra tabela)
        self.tree_produtos_delete = ttk.Treeview(
            frame_tabela,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            style="Treeview"
        )
        
        scroll_y.configure(command=self.tree_produtos_delete.yview)
        scroll_x.configure(command=self.tree_produtos_delete.xview)
        
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        self.tree_produtos_delete.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Binding para duplo clique
        self.tree_produtos_delete.bind('<Double-1>', self.selecionar_id_produto)
        
    def selecionar_id_produto(self, event):
        """Seleciona o ID do produto ao dar duplo clique na tabela"""
        item = self.tree_produtos_delete.selection()
        if item:
            valores = self.tree_produtos_delete.item(item[0])['values']
            if valores:
                self.entry_id_delete.delete(0, 'end')
                self.entry_id_delete.insert(0, str(valores[0]))  # Assumindo que ID é a primeira coluna
        
    def fazer_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha email e senha!")
            return
        
        def login_thread():
            try:
                self.label_status_login.configure(text="🔄 Fazendo login...", text_color="#3498db")
                
                response = requests.post(
                    f"{BASE_URL}{LOGIN_ENDPOINT}",
                    json={"email": email, "password": senha},
                    headers={"accept": "application/json", "Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("msg") == "Usuário logado com sucesso!":
                        self.token = data.get("token")
                        
                        if self.token:
                            self.label_status_login.configure(
                                text="✅ Login realizado com sucesso!",
                                text_color="#2ecc71"
                            )
                            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                        else:
                            self.label_status_login.configure(
                                text="❌ Token não encontrado",
                                text_color="#e74c3c"
                            )
                            messagebox.showerror("Erro", "Token não encontrado na resposta")
                    else:
                        self.label_status_login.configure(
                            text=f"❌ {data.get('msg')}",
                            text_color="#e74c3c"
                        )
                        messagebox.showerror("Erro", data.get('msg'))
                else:
                    self.label_status_login.configure(
                        text=f"❌ Erro: {response.status_code}",
                        text_color="#e74c3c"
                    )
                    messagebox.showerror("Erro", f"Erro no login: {response.status_code}")
                    
            except Exception as e:
                self.label_status_login.configure(
                    text=f"❌ Erro: {str(e)}",
                    text_color="#e74c3c"
                )
                messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")
        
        Thread(target=login_thread, daemon=True).start()
    
    def get_headers(self):
        if not self.token:
            messagebox.showwarning("Atenção", "Faça login primeiro!")
            return None
        
        return {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json"
        }
    
    def atualizar_tabela(self, tree, produtos):
        """Atualiza uma tabela com os produtos"""
        # Limpar tabela
        for item in tree.get_children():
            tree.delete(item)
        
        if produtos:
            # Configurar colunas
            colunas = list(produtos[0].keys())
            tree['columns'] = colunas
            tree['show'] = 'headings'
            
            for col in colunas:
                tree.heading(col, text=col.upper())
                tree.column(col, width=120)
            
            # Inserir dados
            for produto in produtos:
                valores = [produto.get(col, '') for col in colunas]
                tree.insert('', 'end', values=valores)
    
    def listar_produtos(self):
        headers = self.get_headers()
        if not headers:
            return
        
        def listar_thread():
            try:
                response = requests.get(BASE_URL, headers=headers)
                
                if response.status_code == 200:
                    produtos = response.json()
                    self.produtos_lista = produtos
                    
                    # USAR root.after para atualizar a interface na thread principal
                    self.root.after(0, lambda: self.atualizar_interface_listagem(produtos))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao listar produtos: {response.status_code}"))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na requisição: {str(e)}"))
        
        Thread(target=listar_thread, daemon=True).start()
    
    def atualizar_interface_listagem(self, produtos):
        """Atualiza a tabela e os gráficos na thread principal"""
        # Atualizar tabela
        self.atualizar_tabela(self.tree_produtos, produtos)
        
        # Criar gráficos
        self.criar_grafico_precos(produtos)
        
        if produtos:
            messagebox.showinfo("Sucesso", f"{len(produtos)} produtos listados!")
        else:
            messagebox.showinfo("Info", "Nenhum produto encontrado")
    
    def atualizar_lista_exclusao(self):
        """Atualiza a lista de produtos na aba de exclusão"""
        headers = self.get_headers()
        if not headers:
            return
        
        def listar_thread():
            try:
                response = requests.get(BASE_URL, headers=headers)
                
                if response.status_code == 200:
                    produtos = response.json()
                    self.produtos_lista = produtos
                    
                    # Atualizar tabela de exclusão
                    self.atualizar_tabela(self.tree_produtos_delete, produtos)
                    
                    if produtos:
                        messagebox.showinfo("Sucesso", f"{len(produtos)} produtos carregados!")
                    else:
                        messagebox.showinfo("Info", "Nenhum produto encontrado")
                else:
                    messagebox.showerror("Erro", f"Erro ao listar produtos: {response.status_code}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na requisição: {str(e)}")
        
        Thread(target=listar_thread, daemon=True).start()
    
    def selecionar_imagem(self):
        filename = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            self.image_path = filename
            nome_arquivo = filename.split('/')[-1]
            self.label_imagem.configure(text=nome_arquivo, text_color="#2ecc71")
    
    def cadastrar_produto(self):
        headers = self.get_headers()
        if not headers:
            return
        
        nome = self.entry_nome.get()
        descricao = self.text_descricao.get("1.0", "end-1c")
        preco = self.entry_preco.get()
        categoria = self.entry_categoria.get()
        frete = self.entry_frete.get()
        
        if not all([nome, descricao, preco, categoria, frete]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        try:
            preco = float(preco)
            frete = float(frete)
        except ValueError:
            messagebox.showerror("Erro", "Preço e frete devem ser números!")
            return
        
        def cadastrar_thread():
            try:
                data = {
                    "name": nome,
                    "description": descricao,
                    "price": str(preco),
                    "category": categoria,
                    "shipment": str(frete)
                }
                
                files = {}
                if self.image_path:
                    files["image"] = open(self.image_path, "rb")
                
                response = requests.post(
                    BASE_URL,
                    headers=headers,
                    data=data,
                    files=files
                )
                
                if self.image_path and "image" in files:
                    files["image"].close()
                
                if response.status_code in [200, 201]:
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                    # Limpar campos
                    self.entry_nome.delete(0, 'end')
                    self.text_descricao.delete("1.0", "end")
                    self.entry_preco.delete(0, 'end')
                    self.entry_categoria.set("")
                    self.entry_frete.delete(0, 'end')
                    self.image_path = None
                    self.label_imagem.configure(text="Nenhuma imagem selecionada", text_color="gray")
                else:
                    messagebox.showerror("Erro", f"Erro ao cadastrar: {response.status_code}\n{response.text}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na requisição: {str(e)}")
        
        Thread(target=cadastrar_thread, daemon=True).start()
    
    def deletar_produto(self):
        headers = self.get_headers()
        if not headers:
            return
        
        produto_id = self.entry_id_delete.get()
        
        if not produto_id:
            messagebox.showwarning("Atenção", "Digite o ID do produto!")
            return
        
        if not messagebox.askyesno("Confirmar", f"Deseja realmente excluir o produto ID {produto_id}?"):
            return
        
        def deletar_thread():
            try:
                response = requests.delete(
                    f"{BASE_URL}/{produto_id}",
                    headers=headers
                )
                
                if response.status_code in [200, 204]:
                    messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                    self.entry_id_delete.delete(0, 'end')
                    # Atualizar lista após exclusão
                    self.atualizar_lista_exclusao()
                else:
                    messagebox.showerror("Erro", f"Erro ao deletar: {response.status_code}\n{response.text}")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na requisição: {str(e)}")
        
        Thread(target=deletar_thread, daemon=True).start()


if __name__ == "__main__":
    root = ctk.CTk()
    app = GerenciadorProdutosGUI(root)
    root.mainloop()