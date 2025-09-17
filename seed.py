import csv
import os
from app import app, db, OrgaoJudiciario

# Nome do arquivo CSV
CSV_FILE = "orgaos_judiciarios_jaragua_do_sul_com_telefones.csv"

def importar_csv():
    with app.app_context():
        # Garante que a tabela existe
        db.create_all()

        with open(CSV_FILE, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                orgao = OrgaoJudiciario(
                    tipo=row["tipo"].strip(),
                    nome=row["nome"].strip(),
                    endereco_completo=row["endereco_completo"].strip(),
                    telefone=row.get("telefone", "").strip()
                )
                db.session.add(orgao)
                count += 1
            db.session.commit()
            print(f"{count} registros importados com sucesso.")

if __name__ == "__main__":
    importar_csv()
