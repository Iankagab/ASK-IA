# create_db.py

from app import app, db, KnowledgeBase

# Dados iniciais para popular o banco
initial_data = [
    {
        "keywords": "cartório",
        "response": "Olá! Me conte um pouco mais do que você precisa, e assim poderei te direcionar ao endereço mais assertivo"
    }
]

def setup_database():
    with app.app_context():
        # Cria a tabela no banco de dados (se ela não existir)
        db.create_all()

        # Verifica se o banco já tem dados para não duplicar
        if KnowledgeBase.query.first() is None:
            print("Populando o banco de dados com dados iniciais...")
            for data in initial_data:
                new_entry = KnowledgeBase(keywords=data["keywords"], response=data["response"])
                db.session.add(new_entry)
            db.session.commit()
            print("Banco de dados populado!")
        else:
            print("O banco de dados já contém dados.")

if __name__ == '__main__':
    setup_database()