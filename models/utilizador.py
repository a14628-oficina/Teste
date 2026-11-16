from con_sql_alchemy import bd

class UtilizadorModel(bd.Model):
    __tablename__ = "utilizador"
    id = bd.Column(bd.Integer, primary_key=True, autoincrement=True)
    username = bd.Column(bd.String(80))
    email = bd.Column(bd.String(120), nullable=False)
    password = bd.Column(bd.String(80), nullable=False)
    tipo = bd.Column(bd.String(20), nullable=False)


    tarefas = bd.relationship("TarefaModel", backref="utilizador", cascade="all, delete-orphan")

    # Construtor
    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email
        self.password = password
        self.tipo = tipo

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email, "tipo": self.tipo}

    @classmethod
    def find_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_user_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None

    def save_user(self):
        bd.session.add(self)
        bd.session.commit()