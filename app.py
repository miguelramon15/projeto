from flask import Flask, render_template, redirect, url_for, request, flash, session 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import ClienteForm, ProdutoForm, VendaForm
from models import db, Cliente, Produto, Venda

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'minha-chave-secreta'

users_db = {}  

db.init_app(app)

# Definição da Tabela de Usuários 
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(200), nullable=False)
   name = db.Column(db.String(50), nullable=False)
   cpf = db.Column(db.String(14), unique=True, nullable=False)
   data_nascimento = db.Column(db.String(10), nullable=False)
   endereco = db.Column(db.String(200), nullable=False)   

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_db.get(email)
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
    return render_template('login.html')  # Exibe a página de login

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users_db:
            # Aqui você pode adicionar a lógica para enviar um link de redefinição de senha por email
            flash(f'Link de redefinição de senha enviado para {email}.', 'info')
        else:
            flash('Email não encontrado.', 'danger')
    return render_template('forgot_password.html')  # Página para redefinir a senha

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        endereco = request.form['endereco']

        # Verificar se o email já está cadastrado
        if email in users_db:
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('register'))
        else:
            # Armazena as informações do usuário com hash da senha
            hashed_password = generate_password_hash(password)
            users_db[email] = {
                'password': hashed_password,
                'name': email.split('@')[0],
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'endereco': endereco
            }
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')  # Exibe a página de cadastro

@app.route('/welcome')
def welcome():
    if 'user' in session:
        user_email = session['user']
        user_name = users_db[user_email]['name']
        return render_template('welcome.html', usuario={'nome': user_name})
    else:
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('base'))


# Rota principal
#@app.route('/base')
#def index():
   # return render_template('base.html')

# Rotas para Clientes
@app.route('/clientes')
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/novo', methods=['GET', 'POST'])
def novo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            idade=form.idade.data,
            cpf=form.cpf.data,
            email=form.email.data,
            endereco=form.endereco.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('lista_clientes'))
    return render_template('form_cliente.html', form=form)

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        form.populate_obj(cliente)
        db.session.commit()
        flash('Cliente atualizado com sucesso!')
        return redirect(url_for('lista_clientes'))
    return render_template('form_cliente.html', form=form)

@app.route('/cliente/deletar/<int:id>')
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente deletado com sucesso!')
    return redirect(url_for('lista_clientes'))

# Rotas para Produtos
@app.route('/produtos')
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            preco=form.preco.data,
            descricao=form.descricao.data,
            quantidade_estoque=form.quantidade_estoque.data,
            imagem=form.imagem.data.filename
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('lista_produtos'))
    return render_template('form_produto.html', form=form)

@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        form.populate_obj(produto)
        db.session.commit()
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('lista_produtos'))
    return render_template('form_produto.html', form=form)

@app.route('/produto/deletar/<int:id>')
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!')
    return redirect(url_for('lista_produtos'))

# Rotas para Vendas
@app.route('/vendas')
def vendas():
    vendas = Venda.query.all()
    return render_template('vendas.html', vendas=vendas)

@app.route('/venda/nova', methods=['GET', 'POST'])
def nova_venda():
    form = VendaForm()
    if form.validate_on_submit():
        venda = Venda(
            cliente_id=form.cliente_id.data,
            produto_id=form.produto_id.data,
            quantidade=form.quantidade.data
        )
        produto = Produto.query.get(venda.produto_id)
        if produto.quantidade_estoque >= venda.quantidade:
            produto.quantidade_estoque -= venda.quantidade
            db.session.add(venda)
            db.session.commit()
            flash('Venda registrada com sucesso!')
        else:
            flash('Estoque insuficiente para a venda.')
        return redirect(url_for('vendas'))
    return render_template('form_venda.html', form=form)

# Rota para Relatórios e Gráficos
@app.route('/relatorios')
def relatorios():
    # Aqui você pode adicionar a lógica de geração de gráficos e relatórios
    # Exemplo fictício de dados para relatórios:
    vendas_por_cliente = {
        'João': 5,
        'Maria': 3,
        'Carlos': 8
    }
    return render_template('relatorios.html', vendas_por_cliente=vendas_por_cliente)

@app.route('/test_db')
def test_db():
    try:
        # Consulta o primeiro cliente na tabela
        cliente = Cliente.query.first()
        if cliente:
            return f"Banco de dados está funcionando! Primeiro cliente: {cliente.nome}"
        else:
            return "Banco de dados está funcionando, mas não há clientes cadastrados."
    except Exception as e:
        return f"Ocorreu um erro ao acessar o banco de dados: {e}"


if __name__ == '__main__':
    app.run(debug=True)

