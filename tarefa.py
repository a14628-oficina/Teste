# Este "tarefa.py" serve para os Gets, Posts...
from flask_restful import Resource, reqparse
from models.tarefa import TarefaModel
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

ESTADOS = ["Pendente", "Em curso", "Concluída"]  # estados permitidos

# Funções auxiliares (retiram do token o id e o tipo do utilizador autenticado)
def utilizador_atual_id():
    return int(get_jwt_identity())

def e_admin():
    return get_jwt()["tipo"] == "admin"

class Tarefas(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="O título da tarefa é obrigatório")
    argumentos.add_argument("descricao", type=str, default="")
    argumentos.add_argument("estado", type=str, default="Pendente")

    # Consultar tarefas
    @jwt_required()
    def get(self):
        if e_admin():
            tarefas = TarefaModel.query.all()  # admin vê todas as tarefas
        else:
            tarefas = TarefaModel.query.filter_by(utilizador_id=utilizador_atual_id()).all()  # utilizador só vê as suas
        return {"tarefas": [tarefa.json() for tarefa in tarefas]}, 200

    # Criar
    @jwt_required()
    def post(self):
        dados = Tarefas.argumentos.parse_args()
        if dados["estado"] not in ESTADOS:
            return {"mensagem": "Estado inválido. Use: Pendente, Em curso ou Concluída."}, 400
        # A tarefa fica automaticamente associada ao utilizador autenticado
        nova_tarefa = TarefaModel(dados["titulo"], dados["descricao"], dados["estado"], utilizador_atual_id())
        try:
            nova_tarefa.save_tarefa()
            return nova_tarefa.json(), 201
        except:
            return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500

class Tarefa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="O título da tarefa é obrigatório")
    argumentos.add_argument("descricao", type=str, default="")
    argumentos.add_argument("estado", type=str, required=True, help="O estado da tarefa é obrigatório")

    # Consultar uma tarefa
    @jwt_required()
    def get(self, tarefa_id):
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada."}, 404
        if not e_admin() and tarefa.utilizador_id != utilizador_atual_id():
            return {"mensagem": "Sem permissões para aceder a esta tarefa."}, 403
        return tarefa.json(), 200

    # Atualizar
    @jwt_required()
    def put(self, tarefa_id):
        dados = Tarefa.argumentos.parse_args()
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada."}, 404
        if not e_admin() and tarefa.utilizador_id != utilizador_atual_id():
            return {"mensagem": "Sem permissões para alterar esta tarefa."}, 403
        if dados["estado"] not in ESTADOS:
            return {"mensagem": "Estado inválido. Use: Pendente, Em curso ou Concluída."}, 400
        try:
            tarefa.update_tarefa(dados["titulo"], dados["descricao"], dados["estado"])
            tarefa.save_tarefa()
            return tarefa.json(), 200
        except:
            return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500

    # Apagar
    @jwt_required()
    def delete(self, tarefa_id):
        tarefa = TarefaModel.find_tarefa(tarefa_id)
        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada."}, 404
        if not e_admin() and tarefa.utilizador_id != utilizador_atual_id():
            return {"mensagem": "Sem permissões para eliminar esta tarefa."}, 403
        try:
            tarefa.delete_tarefa()
            return {"mensagem": "Tarefa removida com sucesso"}, 200
        except:
            return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500
