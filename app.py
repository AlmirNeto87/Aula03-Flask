from flask import Flask
from config import db, DATABASE_URI
from controllers import produto_controller, usuario_controller

#Instanciando o objeto Flask a variavel app
app = Flask(__name__)

# Necessário para gerenciar sessões
app.secret_key = "sua_chave_super_secreta"  # troque por algo seguro

# Define qual o banco de dados usar
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# Desativa o rastreamento de modificações para economizar memória
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão com a aplicação
db.init_app(app)

# Definind rotas de login e logout
app.add_url_rule("/login", "login", usuario_controller.login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", usuario_controller.logout)


# Utilizacao das rotas sem o uso dos Decorators
app.add_url_rule("/", "home", produto_controller.home)
app.add_url_rule("/home", "home", produto_controller.home)

# Rotas para CRUD de Usuarios
app.add_url_rule("/usuarios", "listar_usuarios", usuario_controller.listar_usuarios)
app.add_url_rule("/usuarios/cadastro", "cadastrar_usuario", usuario_controller.cadastrar_usuario, methods=["GET", "POST"])
app.add_url_rule("/usuarios/editar/<int:id>", "editar_usuario", usuario_controller.editar_usuario, methods=["GET", "POST"])
app.add_url_rule("/usuarios/deletar/<int:id>", "deletar_usuario", usuario_controller.deletar_usuario)

# Rotas para CRUD de Produtos
app.add_url_rule("/produtos", "listar_produtos", produto_controller.listar_produtos)
app.add_url_rule("/produtos/cadastro", "cadastrar_produto", produto_controller.cadastrar_produto, methods=["GET", "POST"])
app.add_url_rule("/produtos/editar/<int:id>", "editar_produto", produto_controller.editar_produto, methods=["GET", "POST"])
app.add_url_rule("/produtos/deletar/<int:id>", "deletar_produto", produto_controller.deletar_produto)

# Rotas para paginas estaticas
app.add_url_rule("/sobre", "sobre", produto_controller.sobre)
app.add_url_rule("/contatos", "contatos", produto_controller.contatos)

# Registro dos manipuladores de erros
app.register_error_handler(404, produto_controller.page_not_found)
app.register_error_handler(500, produto_controller.internal_server_error)

# Cria as tabelas em falta no banco com contexto da aplicação
with app.app_context():
    db.create_all()


# Executa a aplicação
if __name__ == "__main__":
    app.run(debug=True)


