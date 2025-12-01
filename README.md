# 🛍️ Gerenciador de Produtos - API

Sistema completo de gerenciamento de produtos com interface gráfica moderna, desenvolvido em Python com CustomTkinter e integração com API REST.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Capturas de Tela](#capturas-de-tela)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O **Gerenciador de Produtos** é uma aplicação desktop com interface gráfica moderna que permite gerenciar um catálogo de produtos através de uma API REST. O sistema oferece funcionalidades completas de CRUD (Create, Read, Update, Delete) com visualizações gráficas e análises estatísticas dos produtos cadastrados.

### ✨ Destaques

- 🎨 Interface moderna e intuitiva com tema dark
- 📊 Dashboards com gráficos interativos
- 🔐 Sistema de autenticação seguro
- 📸 Upload de imagens de produtos
- 🔄 Operações assíncronas (não trava a interface)
- 📈 Análise de dados em tempo real

## 🚀 Funcionalidades

### 🔐 Sistema de Login
- Autenticação via API com token JWT
- Validação de credenciais
- Feedback visual do status da conexão
- Armazenamento seguro do token durante a sessão

### 📋 Listagem de Produtos
- Visualização completa de todos os produtos
- Tabela interativa com scroll horizontal e vertical
- **Dashboard com 2 gráficos de pizza:**
  - Distribuição por faixa de preço (≤R$100, R$101-200, >R$200)
  - Distribuição por categoria de produtos
- Atualização em tempo real
- Estatísticas visuais dos produtos

### ➕ Cadastro de Produtos
- Formulário completo com validação de campos
- Campos disponíveis:
  - Nome do produto
  - Descrição detalhada
  - Preço (R$)
  - Categoria (dropdown com opções pré-definidas)
  - Valor do frete (R$)
  - Upload de imagem do produto
- Validação de tipos de dados
- Feedback de sucesso/erro
- Limpeza automática dos campos após cadastro

### 🗑️ Exclusão de Produtos
- Lista completa de produtos com IDs visíveis
- Seleção de ID por duplo clique na tabela
- Confirmação antes de excluir
- Atualização automática da lista após exclusão
- Prevenção de exclusões acidentais

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+** - Linguagem de programação
- **CustomTkinter 5.0+** - Framework de interface gráfica moderna
- **Tkinter** - Biblioteca GUI nativa do Python

### Bibliotecas Python
```python
customtkinter      # Interface gráfica moderna
tkinter           # Widgets nativos
requests          # Requisições HTTP para API
matplotlib        # Geração de gráficos
threading         # Operações assíncronas
collections       # Estruturas de dados (Counter)
```

### API
- **Base URL:** `http://apipf.jogajuntoinstituto.org`
- **Autenticação:** JWT Bearer Token
- **Formato:** JSON

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Conexão com a internet (para acesso à API)

## 💻 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/gerenciador-produtos.git
cd gerenciador-produtos
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install customtkinter
pip install matplotlib
pip install requests
```

Ou use o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python gerenciador_produtos.py
```

## 📖 Como Usar

### Passo 1: Login

1. Abra a aplicação
2. Na aba **🔐 Login**, insira suas credenciais:
   - Email: `seu@email.com` (exemplo)
   - Senha: `senha` (exemplo)
3. Clique em **Fazer Login**
4. Aguarde a confirmação de sucesso

### Passo 2: Listar Produtos

1. Navegue até a aba **📋 Listar Produtos**
2. Clique em **🔄 Atualizar Lista e Gráficos**
3. Visualize:
   - Tabela completa com todos os produtos
   - Gráfico de pizza: distribuição por faixa de preço
   - Gráfico de pizza: distribuição por categoria

### Passo 3: Cadastrar Produto

1. Vá para a aba **➕ Cadastrar**
2. Preencha todos os campos:
   - Nome do produto
   - Descrição
   - Preço (somente números)
   - Categoria (selecione no dropdown)
   - Frete (somente números)
   - Imagem (opcional - clique em 📁 Selecionar)
3. Clique em **✅ Cadastrar Produto**
4. Aguarde a confirmação

### Passo 4: Excluir Produto

1. Acesse a aba **🗑️ Excluir**
2. Clique em **🔄 Atualizar Lista** para ver todos os produtos
3. **Opção 1:** Digite o ID manualmente
4. **Opção 2:** Dê duplo clique no produto desejado na tabela
5. Clique em **🗑️ Excluir Produto**
6. Confirme a exclusão

## 📁 Estrutura do Projeto

```
gerenciador-produtos/
│
├── gerenciador_produtos.py    # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
│
└── .venv/                      # Ambiente virtual (não versionar)
```

### Estrutura do Código

```python
GerenciadorProdutosGUI
├── __init__()                    # Inicialização
├── criar_interface()             # Cria abas principais
│
├── criar_aba_login()            # Interface de login
├── criar_aba_listagem()         # Interface de listagem
├── criar_aba_cadastro()         # Interface de cadastro
├── criar_aba_exclusao()         # Interface de exclusão
│
├── fazer_login()                # Autenticação
├── listar_produtos()            # Busca produtos
├── cadastrar_produto()          # Adiciona produto
├── deletar_produto()            # Remove produto
│
├── criar_grafico_precos()       # Gera gráficos
├── atualizar_tabela()           # Atualiza tabelas
└── get_headers()                # Headers com token
```

## 🌐 API Endpoints

### Autenticação

**POST** `/login`
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "msg": "Usuário logado com sucesso!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Produtos

**GET** `/`
- Lista todos os produtos
- Headers: `Authorization: Bearer {token}`

**POST** `/`
- Cadastra novo produto
- Headers: `Authorization: Bearer {token}`
- Body: `multipart/form-data`

**DELETE** `/{id}`
- Deleta produto por ID
- Headers: `Authorization: Bearer {token}`

## 📊 Capturas de Tela

### Tela de Login
Interface de autenticação com feedback visual em tempo real.

### Dashboard de Produtos
Visualização completa com tabela e gráficos de análise estatística.

### Formulário de Cadastro
Formulário intuitivo com validação e upload de imagens.

### Gerenciamento de Exclusões
Lista completa com seleção interativa por duplo clique.

## 🎨 Personalização

### Alterar Tema

```python
# No início do arquivo
ctk.set_appearance_mode("dark")  # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

### Alterar URL da API

```python
BASE_URL = "http://sua-api.com"
LOGIN_ENDPOINT = "/seu-endpoint"
```

### Adicionar Novas Categorias

No método `criar_aba_cadastro()`:
```python
self.entry_categoria = ctk.CTkComboBox(
    frame_form, 
    values=["Calçados", "Acessórios", "Roupas", "Nova Categoria"],
    # ...
)
```

## 🐛 Solução de Problemas

### Erro: "Token não encontrado"
- Verifique suas credenciais de login
- Confirme que a API está online
- Tente fazer login novamente

### Gráficos não aparecem
- Certifique-se de que `matplotlib` está instalado
- Verifique se há produtos cadastrados
- Reinicie a aplicação

### Erro de conexão
- Verifique sua conexão com a internet
- Confirme se a URL da API está correta
- Verifique se a API está online

### Imagem não carrega
- Use apenas formatos: JPG, JPEG, PNG, GIF
- Verifique o tamanho do arquivo (limite da API)
- Confirme se o arquivo não está corrompido

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Siga os passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Mantenha o código limpo e documentado
- Siga o padrão PEP 8 para Python
- Adicione comentários explicativos quando necessário
- Teste todas as funcionalidades antes de submeter

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para facilitar o gerenciamento de produtos.

---

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

- Abra uma [Issue](https://github.com/seu-usuario/gerenciador-produtos/issues)
- Entre em contato: seu-email@exemplo.com

## 🎓 Aprendizado

Este projeto foi desenvolvido como parte de estudos em:
- Data Science
- Análise de Dados
- QA (Quality Assurance)
- Desenvolvimento de Interfaces Gráficas
- Integração com APIs REST

## 🔮 Roadmap

Funcionalidades planejadas para versões futuras:

- [ ] Edição de produtos existentes
- [ ] Filtros avançados de busca
- [ ] Exportação de dados para CSV/Excel
- [ ] Relatórios em PDF
- [ ] Modo claro/escuro alternável
- [ ] Backup automático de dados
- [ ] Suporte a múltiplos idiomas
- [ ] Cache local de produtos

## 📚 Recursos Adicionais

- [Documentação CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Documentação Matplotlib](https://matplotlib.org/stable/contents.html)
- [Documentação Requests](https://requests.readthedocs.io/)

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**
