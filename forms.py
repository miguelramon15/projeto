from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3)])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=18, max=999)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=14, max=14)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3)])
    preco = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    descricao = StringField('Descrição', validators=[DataRequired()])
    quantidade_estoque = IntegerField('Quantidade em Estoque', validators=[DataRequired(), NumberRange(min=0)])
    imagem = FileField('Imagem do Produto')
    submit = SubmitField('Salvar')

class VendaForm(FlaskForm):
    cliente_id = IntegerField('ID do Cliente', validators=[DataRequired()])
    produto_id = IntegerField('ID do Produto', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Registrar Venda')