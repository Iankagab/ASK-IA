from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# ---------------------------
# App + Config
# ---------------------------
app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates"
)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'database.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='minha-chave-secreta',
    SEND_FILE_MAX_AGE_DEFAULT=0,
    TEMPLATES_AUTO_RELOAD=True,
)

app.jinja_env.cache = {}
db = SQLAlchemy(app)

# ---------------------------
# Modelo ÚNICO (CSV)
# ---------------------------
class OrgaoJudiciario(db.Model):
    __tablename__ = 'orgao_judiciario'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(120), nullable=False, index=True)   # ex: "Civil", "Criminal"
    nome = db.Column(db.String(255), nullable=False)               # ex: "Fórum XYZ"
    endereco_completo = db.Column(db.String(500), nullable=False)  # endereço completo
    telefone = db.Column(db.String(120), nullable=True)            # telefone (pode ser nulo)

    def __repr__(self):
        return f'<OrgaoJudiciario {self.tipo} - {self.nome}>'

# ---------------------------
# Admin (apenas a nova tabela)
# ---------------------------
admin = Admin(app, name='Painel Admin', template_mode='bootstrap3')
admin.add_view(ModelView(OrgaoJudiciario, db.session))

# ---------------------------
# Rotas
# ---------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/opcoes', methods=['GET'])
def listar_opcoes():
    """Retorna os tipos distintos disponíveis em orgao_judiciario."""
    tipos = db.session.query(OrgaoJudiciario.tipo).distinct().order_by(OrgaoJudiciario.tipo.asc()).all()
    tipos = [t[0] for t in tipos]
    return jsonify({"count": len(tipos), "opcoes": tipos})

@app.route('/endereco', methods=['GET'])
def obter_endereco():
    """
    GET /endereco?opcao=Tipo
    Retorna lista de órgãos com nome, endereço e telefone.
    """
    opcao = request.args.get('opcao', '').strip()
    if not opcao:
        return jsonify({'error': 'Informe a opção.'}), 400

    regs = OrgaoJudiciario.query.filter_by(tipo=opcao).order_by(OrgaoJudiciario.nome.asc()).all()
    resultados = [{
        "nome": r.nome,
        "endereco_completo": r.endereco_completo,
        "telefone": r.telefone or ""
    } for r in regs]

    if not resultados:
        return jsonify({"count": 0, "resultados": [], "message": "Nenhum endereço cadastrado para essa opção."}), 200

    return jsonify({"count": len(resultados), "resultados": resultados})

# ---------------------------
# Bootstrap
# ---------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria só orgao_judiciario
    app.run(debug=True)
