from flask import Flask
from flask_restful import Api
from resources.tarefa import Tarefas, Tarefa
from resources.utilizador import UtilizadorRegisto, UtilizadorLogin
from models.utilizador import UtilizadorModel
from con_sql_alchemy import bd
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

# Configurações
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
app.config["JWT_SECRET_KEY"] = "a_minha_chave_secreta_longa_e_intransmissivel"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config["PROPAGATE_EXCEPTIONS"] = True  

# CRIAR ROTAS(endpoints) para fazer os pedidos
api.add_resource(UtilizadorRegisto, "/registro")
api.add_resource(UtilizadorLogin, "/login")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:tarefa_id>")  


def criar_admin():
    if UtilizadorModel.find_user_by_email("admin@admin.com") is None:
        admin = UtilizadorModel("admin", "admin@admin.com", "admin123", "admin")
        admin.save_user()

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()
        criar_admin()
    app.run(debug=True) 