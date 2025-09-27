from config import db

# Inicializacao do BD 
class Usuario(db.Model):
  __tablename__ = "usuarios"
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  senha = db.Column(db.String(200), nullable=False)  # lembre-se de criptografar!
  

#Funcao de referencia apenas pra informar sobre a criacao do BD
def __repr__(self):
  return f"< Usuario {self.name}>"