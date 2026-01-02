import os
import jwt
import datetime
from dotenv import load_dotenv
from models import MySQLConn
load_dotenv()



class GerarTK:
    def __init__(self, user_id, username):
        payload={
            "user_id":user_id,
            "username":username,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=1)
        }
        secret_key=os.environ.get("SECRET_KEY")
        self.token=jwt.encode(payload, key=secret_key, algorithm="HS256")
        print(self.token)
    def retornar_tk(self):
        return self.token
    
class CriarPastaUser:
    def __init__(self):
        return
 
print("a")