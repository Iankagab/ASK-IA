import os
import pandas as pd
from app import app, db, OrgaoJudiciario

CSV_PATH = os.path.join(os.path.dirname(__file__), "orgaos_judiciarios_jaragua_do_sul_com_telefones.csv")

def importar_csv(reset=False):
    with app.app_context():
        if reset:
            db.session.query(OrgaoJudiciario).delete()
            db.session.commit()

        if not os.path.exists(CSV_PATH):
            print(f"Arquivo não encontrado: {CSV_PATH}")
            return

        df = pd.read_csv(CSV_PATH)

        colunas_esperadas = {"tipo", "nome", "endereco_completo", "telefone"}
        if not colunas_esperadas.issubset(set(df.columns)):
            raise ValueError(f"CSV deve conter colunas {colunas_esperadas}, mas tem {set(df.columns)}")

        inseridos = 0
        for _, row in df.iterrows():
            tipo = str(row["tipo"]).strip()
            nome = str(row["nome"]).strip()
            endereco = str(row["endereco_completo"]).strip()
            telefone = "" if pd.isna(row["telefone"]) else str(row["telefone"]).strip()
            if not (tipo and nome and endereco):
                continue
            db.session.add(OrgaoJudiciario(
                tipo=tipo,
                nome=nome,
                endereco_completo=endereco,
                telefone=telefone
            ))
            inseridos += 1

        db.session.commit()
        print(f"Importação concluída. Registros inseridos: {inseridos}")

if __name__ == "__main__":
    import sys
    reset_flag = len(sys.argv) > 1 and sys.argv[1].lower() == "reset"
    importar_csv(reset=reset_flag)
