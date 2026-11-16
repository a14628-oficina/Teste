from flask_restful import Resource, reqparse
from models.utilizador import UtilizadorModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token

class UtilizadorRegisto(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="O username do utilizador é obrigatório")
    argumentos.add_argument("email", type=str, required=True, help="O email do utilizador é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UtilizadorRegisto.argumentos.parse_args()
        if UtilizadorModel.find_user_by_email(dados["email"]):
            return {"mensagem": "Já existe um utilizador com este email."}, 400
        novo_utilizador = UtilizadorModel(dados["username"], dados["email"], dados["password"], "utilizador")
        try:
            novo_utilizador.save_user()
            return {"mensagem": "Utilizador criado com sucesso."}, 201
        except:
            return {"mensagem": "Erro interno ocorreu..."}, 500

class UtilizadorLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("email", type=str, required=True, help="O email do utilizador é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UtilizadorLogin.argumentos.parse_args()
        user = UtilizadorModel.find_user_by_email(dados["email"])

        if user and compare_digest(user.password, dados["password"]):
            token = create_access_token(identity=str(user.id), additional_claims={"tipo": user.tipo})
            return {"access_token": token}, 200
        return {"mensagem": "O email ou a password está incorreto"}, 401