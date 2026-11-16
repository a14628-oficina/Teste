from con_sql_alchemy import bd

class TarefaModel(bd.Model):
    __tablename__ = "tarefa" 
    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    titulo = bd.Column(bd.String(100), nullable=False)
    descricao = bd.Column(bd.Text)
    estado = bd.Column(bd.String(20), nullable=False)
    utilizador_id = bd.Column(bd.Integer, bd.ForeignKey("utilizador.id"), nullable=False)  

    # Construtor
    def __init__(self, titulo, descricao, estado, utilizador_id):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        self.utilizador_id = utilizador_id

    def json(self):
        return {"id": self.id, "titulo": self.titulo, "descricao": self.descricao, "estado": self.estado, "utilizador_id": self.utilizador_id}

    @classmethod
    def find_tarefa(cls, id):
        tarefa = cls.query.filter_by(id=id).first()
        if tarefa:
            return tarefa
        return None

    def save_tarefa(self):
        bd.session.add(self)
        bd.session.commit()

    def update_tarefa(self, titulo, descricao, estado):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado

    def delete_tarefa(self):
        bd.session.delete(self)
        bd.session.commit()