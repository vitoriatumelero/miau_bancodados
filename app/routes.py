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
def login():
    form = LoginForm()
    if form.validate_on_submit():
        perfil = Perfil.query.filter_by(email=form.email.data).first()
        if perfil and check_password_hash(perfil.senha, form.senha.data):
            login_user(perfil)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.listar_animais'))
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

        hashed_senha = generate_password_hash(form.senha.data, method='sha256')
        novo_perfil = Perfil(
            nome=form.nome.data,
            email=form.email.data,
            senha=hashed_senha
        )
        try:
            db.session.add(novo_perfil)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Agora você pode fazer login.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f'Erro ao cadastrar perfil: {str(e)}', 'danger')
    else:
        flash('Por favor, corrija os erros abaixo.', 'danger')

    return render_template('cadastro_perfil.html', form=form)

@main.route('/cadastro_ong', methods=['GET', 'POST'])
def cadastro_ong():
    form = CadastroOngForm()
    if form.validate_on_submit():
        ong = Ong(nome=form.nome.data, email=form.email.data, senha=generate_password_hash(form.senha.data, method='sha256'))
        db.session.add(ong)
        db.session.commit()
        flash('ONG cadastrada com sucesso!', 'success')
        return redirect(url_for('main.index'))
    return render_template('cadastro_ong.html', form=form)

@main.route('/cadastro_animal', methods=['GET', 'POST'])
def cadastro_animal():
    form = CadastroAnimalForm()
    if form.validate_on_submit():
        novo_animal = Animal(
            nome=form.nome.data,
            idade=form.idade.data,
            especie=form.especie.data,
            descricao=form.descricao.data
        )
        db.session.add(novo_animal)
        db.session.commit()
        flash('Animal cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_animais'))
    return render_template('cadastro_animal.html', form=form)

@main.route('/listar_animais')
def listar_animais():
    animais = Animal.query.all()
    return render_template('listar_animais.html', animais=animais)
