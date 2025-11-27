
import requests
import pandas as pd

# Configurações da API
BASE_URL = "http://apipf.jogajuntoinstituto.org"
LOGIN_ENDPOINT = "/login"  # Endpoint correto

# Credenciais de login - PREENCHA COM SUAS CREDENCIAIS
CREDENCIAIS = {
    "email": "fabinho_marquez@hotmail.com.br",  # MUDE PARA SEU EMAIL
    "password": "1234"  # MUDE PARA SUA SENHA
}

# Token será obtido automaticamente
TOKEN = None


def fazer_login():
    """Faz login na API e retorna o token"""
    global TOKEN
    try:
        print("🔐 Fazendo login...")
        
        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json=CREDENCIAIS,
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se o login foi bem sucedido
            if data.get("msg") == "Usuário logado com sucesso!":
                TOKEN = data.get("token")
                
                if TOKEN:
                    print("✅ Login realizado com sucesso!")
                    print(f"🎫 Token: {TOKEN[:50]}...")
                    return TOKEN
                else:
                    print("❌ Token não encontrado na resposta")
                    return None
            else:
                print(f"❌ Erro no login: {data.get('msg')}")
                return None
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return None


def get_headers():
    """Retorna headers com token válido"""
    if not TOKEN:
        fazer_login()
    
    return {
        "Authorization": f"Bearer {TOKEN}",
        "accept": "application/json"
    }


def listar_produtos():
    """Lista todos os produtos"""
    try:
        # Fazer login fresco antes de cada requisição
        fazer_login()
        # A API retorna produtos na raiz mesmo
        response = requests.get(BASE_URL, headers=get_headers())
        
        if response.status_code == 200:
            produtos = response.json()
            print("✅ Produtos listados com sucesso!")
            #print(json.dumps(produtos, indent=2, ensure_ascii=False))
            produtos = pd.DataFrame(produtos)
            return print(produtos)
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None


def cadastrar_produto(name, description, price, category, shipment, image_path=None):
    """Cadastra um novo produto"""
    try:
        # Fazer login fresco antes de cada requisição
        #fazer_login()
        # Dados do formulário (form-data)
        data = {
            "name": name,
            "description": description,
            "price": str(price),
            "category": category,
            "shipment": str(shipment)
        }
        
        # Se tiver imagem, adiciona ao files
        files = {}
        if image_path:
            files["image"] = open(image_path, "rb")
        
        response = requests.post(
            BASE_URL,
            headers=get_headers(),
            data=data,
            files=files
        )
        
        # Fecha o arquivo se foi aberto
        if image_path and "image" in files:
            files["image"].close()
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Produto cadastrado com sucesso!")
            print(response.json())
            return response.json()
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None


def deletar_produto(produto_id):
    """Deleta um produto"""
    try:
        # Fazer login fresco antes de cada requisição
        fazer_login()
        response = requests.delete(
            f"{BASE_URL}/{produto_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200 or response.status_code == 204:
            print("✅ Produto deletado com sucesso!")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False


# ========== EXEMPLOS DE USO ==========

if __name__ == "__main__":
    print("=" * 50)
    print("GERENCIADOR DE PRODUTOS - API")
    print("=" * 50)
    
    # 0. Fazer login automaticamente
    print("\n0️⃣ FAZENDO LOGIN:")
    if not fazer_login():
        print("❌ Não foi possível fazer login. Verifique as credenciais.")
        exit()
    
    # 1. Listar produtos
    print("\n1️⃣ LISTANDO PRODUTOS:")
    listar_produtos()
    
    # 2. Cadastrar novo produto (COMENTADO - descomente e ajuste conforme necessário)
    #print("\n2️⃣ CADASTRANDO NOVO PRODUTO:")
    #cadastrar_produto(
    #     name="Boné Chave",
    #     description="QuickSilver",
    #     price=89.90,
    #     category="Roupas",
    #     shipment=15.00,
    #     image_path= "https://surfalive.fbitsstatic.net/img/p/bone-quiksilver-gradient-broken-type-white-100491/279285-1.jpg?w=800&h=800&v=no-value"  # Coloque o caminho real da imagem ou deixe None
    # )
    
    #4. Deletar produto (substitua 123 pelo ID real)
    #print("\n4️⃣ DELETANDO PRODUTO:")
    #deletar_produto(2018)
    
    print("\n" + "=" * 50)