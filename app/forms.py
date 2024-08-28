from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CadastroPerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class CadastroOngForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar ONG')

class CadastroAnimalForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired()])
    especie = StringField('Espécie', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    submit = SubmitField('Cadastrar Animal')
