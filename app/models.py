from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Client(db.Model):
    """
    Cliente (tenant) - A empresa que "possui" os dados do sistema.
    Esta é a tabela central para multi-tenancy.
    """
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    plan = db.Column(db.String(50), default='free', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    users = db.relationship('User', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    customers = db.relationship('Customer', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    loans = db.relationship('Loan', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    documents = db.relationship('Document', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    payment_histories = db.relationship('PaymentHistory', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    installments = db.relationship('Installment', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    configurations = db.relationship('Configuration', back_populates='client', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Client {self.name}>'


class User(db.Model):
    """
    Usuários do sistema (operadores, administradores, etc.)
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), default='operador', nullable=False)
    nivel = db.Column(db.String(50), default='Operador', nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='users')
    
    # Unique constraint: email deve ser único por client
    __table_args__ = (db.UniqueConstraint('email', 'client_id', name='uq_user_email_client'),)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Customer(db.Model):
    """
    Clientes do financeiro (pessoas físicas/jurídicas que fazem empréstimos)
    """
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf_cnpj = db.Column(db.String(20), nullable=False)
    rg = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    telefone_secundario = db.Column(db.String(20))
    chave_pix = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    referencia = db.Column(db.String(255), nullable=False)
    telefone_referencia = db.Column(db.String(20), nullable=False)
    endereco_referencia = db.Column(db.String(255), nullable=False)
    observacoes = db.Column(db.Text)
    empresa = db.Column(db.String(100), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='customers')
    
    # Unique constraint: cpf_cnpj deve ser único por client
    __table_args__ = (db.UniqueConstraint('cpf_cnpj', 'client_id', name='uq_customer_cpf_client'),)
    
    # Relacionamentos com outras tabelas
    loans = db.relationship('Loan', back_populates='customer', lazy='dynamic', cascade='all, delete-orphan')
    documents = db.relationship('Document', back_populates='customer', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='customer', lazy='dynamic', cascade='all, delete-orphan')
    payment_histories = db.relationship('PaymentHistory', back_populates='customer', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.nome}>'


class Loan(db.Model):
    """
    Empréstimos/Cobranças
    """
    __tablename__ = 'cobrancas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    descricao = db.Column(db.Text)
    valor_original = db.Column(db.Numeric(10, 2), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    multa = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    juros = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    valor_total = db.Column(db.Numeric(10, 2))
    taxa_juros = db.Column(db.Numeric(5, 2), default=0, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pendente', nullable=False)
    forma_pagamento = db.Column(db.String(50))
    numero_parcelas = db.Column(db.Integer, default=1, nullable=False)
    parcela_atual = db.Column(db.Integer, default=1, nullable=False)
    tipo_cobranca = db.Column(db.String(50), default='Única', nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='loans')
    
    # Relacionamento com Customer
    customer = db.relationship('Customer', back_populates='loans')
    
    # Relacionamentos com outras tabelas
    payments = db.relationship('Payment', back_populates='loan', lazy='dynamic', cascade='all, delete-orphan')
    payment_histories = db.relationship('PaymentHistory', back_populates='loan', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='loan', lazy='dynamic', cascade='all, delete-orphan')
    installments = db.relationship('Installment', back_populates='loan', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Loan {self.id} - {self.descricao}>'


class Document(db.Model):
    """
    Documentos dos clientes
    """
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    nome_ficheiro = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='documents')
    
    # Relacionamento com Customer
    customer = db.relationship('Customer', back_populates='documents')
    
    def __repr__(self):
        return f'<Document {self.nome_ficheiro}>'


class Payment(db.Model):
    """
    Pagamentos individuais
    """
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cobranca_id = db.Column(db.Integer, db.ForeignKey('cobrancas.id'), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False, default=date.today)
    observacao = db.Column(db.Text)
    forma_pagamento = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='payments')
    
    # Relacionamentos
    loan = db.relationship('Loan', back_populates='payments')
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Payment {self.id} - R$ {self.valor_pago}>'


class PaymentHistory(db.Model):
    """
    Histórico de pagamentos (mantido para compatibilidade)
    """
    __tablename__ = 'historico_pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cobranca_id = db.Column(db.Integer, db.ForeignKey('cobrancas.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    forma_pagamento = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='payment_histories')
    
    # Relacionamentos
    loan = db.relationship('Loan', back_populates='payment_histories')
    customer = db.relationship('Customer', back_populates='payment_histories')
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<PaymentHistory {self.id}>'


class Notification(db.Model):
    """
    Notificações enviadas
    """
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cobranca_id = db.Column(db.Integer, db.ForeignKey('cobrancas.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.Text)
    status = db.Column(db.String(50), default='Enviada', nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='notifications')
    
    # Relacionamentos
    customer = db.relationship('Customer', back_populates='notifications')
    loan = db.relationship('Loan', back_populates='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.tipo}>'


class Installment(db.Model):
    """
    Parcelas de empréstimos
    """
    __tablename__ = 'parcelas'
    
    id = db.Column(db.Integer, primary_key=True)
    cobranca_id = db.Column(db.Integer, db.ForeignKey('cobrancas.id'), nullable=False)
    numero_parcela = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pendente', nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    data_pagamento = db.Column(db.Date)
    forma_pagamento = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    multa_manual = db.Column(db.Numeric(10, 2))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='installments')
    
    # Relacionamento com Loan
    loan = db.relationship('Loan', back_populates='installments')
    
    def __repr__(self):
        return f'<Installment {self.numero_parcela} - R$ {self.valor}>'


class Configuration(db.Model):
    """
    Configurações do sistema
    """
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Text)
    descricao = db.Column(db.Text)
    
    # Foreign Key para Client (multi-tenancy)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='configurations')
    
    # Unique constraint: chave deve ser única por client
    __table_args__ = (db.UniqueConstraint('chave', 'client_id', name='uq_config_chave_client'),)
    
    def __repr__(self):
        return f'<Configuration {self.chave}>'

