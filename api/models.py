import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

# --- Configuração de segurança ---
# Use variáveis de ambiente para não expor senhas diretamente no código
os.environ.setdefault('DB_HOST', os.getenv('DB_HOST'))
os.environ.setdefault('DB_PORT', os.getenv('DB_PORT'))
os.environ.setdefault('DB_USER', os.getenv('DB_USER'))
os.environ.setdefault('DB_PASSWORD', os.getenv('DB_PASSWORD'))  # deixe vazio se não tiver senha
os.environ.setdefault('DB_NAME', os.getenv('DB_NAME'))  # troque pelo seu DB

class MySQLConn:
    def __init__(self):
        self.conn=mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        # database=os.getenv("DB_NAME")
        )
        if self.conn.is_connected():
            print("✅ Conexão estabelecida com sucesso ao MySQL!")
            print("Conectado ao MySQL (XAMPP) com sucesso!")
            self.cursor = self.conn.cursor()
            
            # 1️⃣ Criar o banco de dados
            db_name=os.getenv("DB_NAME")
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"📦 Banco de dados {db_name}")
            #----------------------------------------------------------#
            self.conn.database=db_name
            
            # 2️⃣ Criar tabela
            criar_tabela="""
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                senha VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                data_criacao DATE DEFAULT (CURRENT_DATE())
            )
            """
            
            self.cursor.execute(criar_tabela)
            print("🧱 Tabela 'usuario' criada/verificada.")
            # ----------------------------------------------------
            
    def parametro_create(self, nome, email, senha):
        try:
            # 3️⃣ Inserir dados de exemplo
            # ----------------------------------------------------
            inserir_query="""
            INSERT INTO usuario (nome, email, senha)
            VALUES (%s,%s,%s)
            """

            senha=bcrypt.hashpw(str(senha).encode('utf-8'), bcrypt.gensalt())

            usuarios=[
                (nome, email, senha),
                ]
            
            self.cursor.executemany(inserir_query, usuarios)
            self.conn.commit()
            print(f"💾 {self.cursor.rowcount} registros inseridos na tabela usuario.")
            
        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")

        finally:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔒 Conexão encerrada com segurança.")

    def parametro_read(self):
        try:
            # 4️⃣ Consultar e exibir dados
            # ----------------------------------------------------
            self.cursor.execute("SELECT id, nome, email, senha, data_criacao FROM usuario")
            resultado=self.cursor.fetchall()
            print(resultado)
            print("\n👥 Usuarios cadastrados:")
            print("-----------------------------------------------------")
            for linha in resultado:
                print(f"ID: {linha[0]} | Nome: {linha[1]} | Email: {linha[2]} | Hash encriptado: {linha[3]} | Data de Criação: {linha[4]}")

            # cursor.execute("SHOW DATABASES;")
            # for db in cursor:
            #     print(db)
            # # cursor=conn.cursor()
            # cursor.execute("SELECT NOW();")
            # resultado=cursor.fetchone()
            # print(f"🕒 Data/hora do servidor MySQL: {resultado}")

        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")

        finally:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔒 Conexão encerrada com segurança.")
    
    def parametro_readline(self, param:list):
        try:
            # 4️⃣ Consultar e exibir dados
            # ----------------------------------------------------
            if param[0]!='id':
                sql=f"SELECT * FROM usuario WHERE {param[0]}='{param[1]}' LIMIT 1;"
            else:
                sql=f"SELECT * FROM usuario WHERE {param[0]}={param[1]} LIMIT 1;"
            
            self.cursor.execute(sql)

            resultado=self.cursor.fetchall()
            print("\n📊 Usuario cadastrado:")
            print("-----------------------------------------------------")
            

            for linha in resultado:
                print(f"ID: {linha[0]} | Nome: {linha[1]} | Email: {linha[3]} | Hash encriptado: {linha[2]} | Data de Criação: {linha[4]}")
                usuario={
                    "ID":linha[0],
                    "Username":linha[1],
                    "Email":linha[3],
                    "Hash":linha[2],
                    "Data":linha[4]
                }

        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")

        finally:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔒 Conexão encerrada com segurança.")
            return usuario
            
    def parametro_delete(self, id):
        try:
            sql=f"DELETE FROM usuario WHERE id={id}"
            self.cursor.execute(sql)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"🗑️ {self.cursor.rowcount} registro(s) excluído(s) da tabela usuario.")
            else:
                print("⚠️ Nenhum registro encontrado para exclusão.")
        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")
        finally:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔒 Conexão encerrada com segurança.")

    def parametro_update(self, id, *args):
        try:
             
            #alterar={f"valor_{i}":valor for i, valor in enumerate(args)}
            pass

        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")

        finally:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔒 Conexão encerrada com segurança.")

    def excluir_tabela(self, tabela):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {tabela}")
            self.conn.commit()
            print(f"✅ Tabela '{tabela}' excluída com sucesso!")
        except mysql.connector.Error as e:
            print(f"❌ Erro ao excluir tabela: {e}")
        finally:
            if self.conn.is_connected():
                self.conn.close()




# for i,v in enumerate(MySQLConn().parametro_read()):
#     print(f"{i}ª -> {v}")