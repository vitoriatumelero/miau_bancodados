from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Perfil(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    is_ong = db.Column(db.Boolean, default=False)

class Ong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    # Remova o relacionamento com Animal
    # animais = relationship('Animal', back_populates='ong')

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    ong_id = db.Column(db.Integer, ForeignKey('ong.id'), nullable=True)  # Defina nullable=True
    # Remova o relacionamento com Ong
    # ong = relationship('Ong', back_populates='animais')

#criar outra classe com a relacao ong e animal
#classe adocção
