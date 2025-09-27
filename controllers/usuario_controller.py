import os
from flask import render_template,request,redirect,url_for,session,flash
from functools import wraps
from config import db
from models.usuario_model import Usuario 

# Decorator para exigir login
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa estar logado para acessar esta página!", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# Rota de login
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.name
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("E-mail ou senha inválidos!", "danger")

    return render_template("login.html", titulo="Login")


# Rota de logout
def logout():
    session.clear()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("login"))


# Rotas pra Uso do CRUD de Usuarios
# Rota para listar usuarios
@login_obrigatorio
def listar_usuarios():
  usuario = Usuario.query.all()
  return render_template("usuarios.html", titulo = "Lista de usuarios", usuarios = usuario)

# Rota para cadastrar usuarios
def cadastrar_usuario():
  if request.method == 'POST':
    
    name = request.form["name"]
    email =  request.form["email"]
    senha = request.form["password"]
    

    novo_usuario = Usuario(name=name, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return redirect(url_for("listar_produtos"))  # Por boas Praticas e sguro finalizar a sessao  db.session.close()
    
  return render_template("cadastrar_usuario.html", titulo="Cadastro de Usuarios")

# Rota para editar usuarios
@login_obrigatorio
def editar_usuario(id):
  usuario = Usuario.query.get(id)
  
  #Testa se o usuario foi encontrado ou nao
  if not usuario:
    return render_template("404.html", descErro="Usuario nao Encontado")
  
  if request.method == "POST":
    usuario.name = request.form["name"]
    usuario.email = request.form["email"]
    usuario.senha = request.form["password"]
    
    
    
    # Salvando alteracoes no BD 
    db.session.commit()
    return redirect(url_for("listar_usuarios"))

  # Renderizando a pagina de editar usuario passando o usuario a ser editado  
  return render_template("editar_usuario.html", titulo= "Edicao de Usuario", usuario = usuario)

# Rota para deletar usuarios
@login_obrigatorio
def deletar_usuario(id):
  usuario = Usuario.query.get(id)
    
  # Testa se usuario foi encontrado ou nao
  if not usuario:
    return render_template("404.html", descErro="Usuario nao Encontado")  
  
  # Abrindo a sessao do BD e deletando o usuario encontrado
  db.session.delete(usuario)
  # Comitando a alteracao do BD
  db.session.commit()
  
  return redirect(url_for("listar_usuarios"))
