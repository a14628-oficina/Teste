# Inicio da aplicação (app.py)
from flask import Flask
from flask_restful import Api
from resources.tarefa import Tarefas, Tarefa
from resources.utilizador import UtilizadorRegisto, UtilizadorLogin
from models.utilizador import UtilizadorModel
from con_sql_alchemy import bd
from flask_jwt_extended import JWTManager
from datetime import timedelta

# NOTA IMPORTANTE: antes de correr o programa temos de entrar no ambiente virtual(se ainda não estivermos) ". venv/bin/activate"
# depois podemos iniciar o servidor "python app.py"

app = Flask(__name__)
api = Api(app)  # variavel para dizer que estou a trabalhar na minha API
jwt = JWTManager(app)  # Inicializa o JWT para tratar da autenticação das páginas

# Configurações
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"  # vai criar uma base de dados com o nome tarefas.db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # serve para o servidor não mostrar os "logs" durante o processo da aplicação
app.config["JWT_SECRET_KEY"] = "a_minha_chave_secreta_longa_e_intransmissivel"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config["PROPAGATE_EXCEPTIONS"] = True  # deixa o JWT devolver o erro 401 quando falta o token

# CRIAR ROTAS(endpoints) para fazer os pedidos
api.add_resource(UtilizadorRegisto, "/registo")
api.add_resource(UtilizadorLogin, "/login")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:tarefa_id>")  # a class Tarefa recebe o parametro "tarefa_id" que é um inteiro

# Criação do administrador inicial (só é criado se ainda não existir)
def criar_admin():
    if UtilizadorModel.find_user_by_email("admin@admin.com") is None:
        admin = UtilizadorModel("admin", "admin@admin.com", "admin123", "admin")
        admin.save_user()

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()  # Cria todas as tabelas definidas no modelo SQLAlchemy
        criar_admin()
    app.run(debug=True)  # debug=true para aparecer oque retorna, como ainda estamos a testar a api vamos deixar o debug ativo
