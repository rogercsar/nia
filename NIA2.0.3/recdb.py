import sqlite3
import os

def recover_database(corrupted_db_path, recovered_db_path):
    try:
        # Conectar ao banco de dados corrompido
        corrupted_db = sqlite3.connect(corrupted_db_path)
        cursor = corrupted_db.cursor()

        # Verificar a integridade do banco de dados corrompido
        cursor.execute("PRAGMA integrity_check")
        integrity_check_result = cursor.fetchone()[0]
        if integrity_check_result != "ok":
            print("Banco de dados corrompido: integridade não verificada")
            return

        # Conectar ao novo banco de dados
        if os.path.exists(recovered_db_path):
            os.remove(recovered_db_path)
        recovered_db = sqlite3.connect(recovered_db_path)
        recovered_cursor = recovered_db.cursor()

        # Copiar todas as tabelas e dados do banco de dados corrompido para o novo banco de dados
        for line in corrupted_db.iterdump():
            if line not in ('BEGIN;', 'COMMIT;'):
                recovered_cursor.execute(line)
        recovered_db.commit()
        
        print("Banco de dados recuperado com sucesso")
    except Exception as e:
        print(f"Erro ao recuperar o banco de dados: {e}")
    finally:
        corrupted_db.close()
        recovered_db.close()

# Caminho do banco de dados corrompido e novo banco de dados
corrupted_db_path = 'C:\\Users\\roger\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\chatterbot\\storage\\database.db'
recovered_db_path = 'C:\\Users\\roger\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\chatterbot\\storage\\recovered.db'

# Recuperar o banco de dados
recover_database(corrupted_db_path, recovered_db_path)
