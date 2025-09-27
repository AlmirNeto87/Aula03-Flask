import os
from flask import render_template,request,redirect,url_for
from config import db
from models.produto_model import Produto
from werkzeug.utils import secure_filename
from controllers.usuario_controller import login_obrigatorio

#Rotas pra Uso do CRUD de Produtos
def home():
  return render_template("index.html", titulo = "Home Page")

@login_obrigatorio  
def listar_produtos():
  produto = Produto.query.all()
  return render_template("produtos.html", titulo = "Lista de produtos", produtos = produto)

@login_obrigatorio
def cadastrar_produto():
  if request.method == 'POST':
    
    name = request.form["name"]
    price =  float(request.form["price"])
    imagem_file = request.files.get("imagem")
    caminho_imagem = None
    #Testa se a imagem foi salva na variavel
    if imagem_file:
      # Testa com uma funcao nativa do python se o nome do arquivo e seguro
      filename = secure_filename(imagem_file.filename)
      # Salva o caminho do arquivo na pasta images
      caminho_imagem = f"images/{filename}" 
      # Salva o arquivo no caminho certo 
      imagem_file.save(os.path.join("static", caminho_imagem))

    novo_produto = Produto(name=name, price=price, imagem=caminho_imagem)
    db.session.add(novo_produto)
    db.session.commit()
    
    return redirect(url_for("listar_produtos"))  # Por boas Praticas e sguro finalizar a sessao  db.session.close()
    
  return render_template("cadastrar_produto.html", titulo="Cadastro de Produtos")

@login_obrigatorio
def editar_produto(id):
  produto = Produto.query.get(id)
  
  #Testa se o produto foi encontrado ou nao
  if not produto:
    return render_template("404.html", descErro="Produto nao Encontado")
  
  if request.method == "POST":
    produto.name = request.form["name"]
    produto.price = float(request.form["price"])
    
    imagem_file = request.files.get("imagem")
    caminho_imagem = None
    #Testa se a imagem foi salva na variavel
    if imagem_file:
      # Testa com uma funcao nativa do python se o nome do arquivo e seguro
      filename = secure_filename(imagem_file.filename)
      # Salva o caminho do arquivo na pasta images
      caminho_imagem = f"images/{filename}" 
      # Salva o arquivo no caminho certo 
      imagem_file.save(os.path.join("static", caminho_imagem))
      # Salvando novo caminho da imagem no campo imagem de produto
      produto.imagem = caminho_imagem
    
    # Salvando alteracoes no BD 
    db.session.commit()
    return redirect(url_for("listar_produtos"))

  # Renderizando a pagina de editar produto passando o produto a ser editado  
  return render_template("editar_produto.html", titulo= "Edicao de Produto", produto = produto)

@login_obrigatorio
def deletar_produto(id):
  produto = Produto.query.get(id)
    
  # Testa se produto foi encontrado ou nao
  if not produto:
    return render_template("404.html", descErro="Produto nao Encontado")  
  
  # Abrindo a sessao do BD e deletando o produto encontrado
  db.session.delete(produto)
  # Comitando a alteracao do BD
  db.session.commit()
  
  return redirect(url_for("listar_produtos"))


# Rotas extras
def sobre():
  return render_template("sobre.html", titulo="Sobre")
def contatos():
  return render_template("contatos.html", titulo="Sobre")

# Rotas de tratamento de erros
def page_not_found(e):
  return render_template('404.html', error_code=404, error_message="Página não encontrada."), 404
  
def internal_server_error(e):
  return render_template('404.html', error_code=500, error_message="Erro interno no servidor. Tente novamente mais tarde."), 500
