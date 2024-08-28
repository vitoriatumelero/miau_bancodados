from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, CadastroPerfilForm, CadastroOngForm, CadastroAnimalForm
from app.models import Perfil, Ong, Animal
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        perfil = Perfil.query.filter_by(email=form.email.data).first()
        if perfil and check_password_hash(perfil.senha, form.senha.data):
            login_user(perfil)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))  # Redireciona para a página inicial ou outra página
        else:
            flash('Login inválido. Verifique suas credenciais.', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@main.route('/cadastro_perfil', methods=['GET', 'POST'])
def cadastro_perfil():
    form = CadastroPerfilForm()
    if form.validate_on_submit():
        perfil_existente = Perfil.query.filter_by(email=form.email.data).first()
        if perfil_existente:
            flash('Este email já está cadastrado. Por favor, faça login.', 'warning')
            return redirect(url_for('main.login'))

        # Hash da senha antes de salvar no banco de dados
        hashed_senha = generate_password_hash(form.senha.data, method='sha256')

        novo_perfil = Perfil(
            nome=form.nome.data,
            email=form.email.data,
            senha=hashed_senha  # Armazena a senha criptografada
        )
        db.session.add(novo_perfil)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('cadastro_perfil.html', form=form)



@main.route('/cadastro_ong', methods=['GET', 'POST'])
def cadastro_ong():
    form = CadastroOngForm()
    if form.validate_on_submit():
        ong = Ong(nome=form.nome.data, email=form.email.data, senha=form.senha.data)
        db.session.add(ong)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('cadastro_ong.html', form=form)


@main.route('/cadastrar_animal', methods=['GET', 'POST'])
@login_required
def cadastro_animal():
    form = CadastroAnimalForm()
    if form.validate_on_submit():
        # Cria uma instância de Animal com os dados do formulário
        novo_animal = Animal(
            nome=form.nome.data,
            idade=form.idade.data,
            especie=form.especie.data,
            descricao=form.descricao.data,
            ong_id=current_user.id  # Exemplo de como vincular o animal à ONG logada
        )
        db.session.add(novo_animal)
        db.session.commit()
        flash('Animal cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_animais'))  # Redireciona para a lista de animais

    return render_template('cadastrar_animal.html', form=form)

@main.route('/listar_animais')
def listar_animais():
    animais = Animal.query.all()  # Consulta todos os animais
    return render_template('listar_animais.html', animais=animais)
