from main import app
from app.models import db, Client, User
from werkzeug.security import generate_password_hash

def criar_dados_iniciais():
    with app.app_context():
        print("🚀 Iniciando configuração inicial...")

        # 1. Verifica se já existe algum cliente
        if Client.query.first():
            print("⚠️ Já existem dados no banco. Operação cancelada para segurança.")
            return

        # 2. Cria a Primeira Empresa (Tenant)
        empresa = Client(name="Minha Empresa SaaS", plan="free")
        db.session.add(empresa)
        db.session.commit()
        print(f"✅ Empresa '{empresa.name}' criada com ID: {empresa.id}")

        # 3. Cria o Usuário Admin
        admin = User(
            nome="Administrador",
            email="admin@teste.com",
            senha=generate_password_hash("123456"), # Senha simples para teste
            tipo="admin",
            nivel="ADM",
            client_id=empresa.id
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário '{admin.nome}' criado com sucesso!")
        print("-" * 30)
        print("LOGIN: admin@teste.com")
        print("SENHA: 123456")
        print("-" * 30)

if __name__ == "__main__":
    criar_dados_iniciais()