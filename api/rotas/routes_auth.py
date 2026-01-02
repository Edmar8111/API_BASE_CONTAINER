from flask import render_template, request, redirect, url_for, jsonify
from . import r_1
from . import routes, rotas_error
import jwt
import os
from api.utils import util
import api.models as models
import bcrypt
import time


@r_1.route("/", methods=["GET",'POST'])
def main():
    if request.method=="POST":
        try:
            #Cria uma nova conta
            create_user=(request.form.get("valor_0"),request.form.get("valor_1"),request.form.get("valor_2"))
            if create_user[2]!=None:
                models.MySQLConn().parametro_create(nome=create_user[0], email=create_user[1], senha=create_user[2]) 
                return redirect(url_for('/auth/'))
            
            else:
                print("REQUESTE TOKEN")
                #Efetua o login
                usuario=request.form.get("valor_0")
                senha=request.form.get("valor_1")
                user_info=models.MySQLConn().parametro_readline(param=["email",usuario, senha])
                
                try:
                    if bcrypt.checkpw(str(senha).encode('utf-8'), user_info['Hash'].encode('utf-8')):
                        token=util.GerarTK("0", usuario).retornar_tk()
                        print(f"TOKEN GERADO -> {token}")
                        time.sleep(1.5)
                        return routes.main_(token)
                except:
                    pass

                # user_id=request.args.get("usuario") #-verificar no banco
                #decoded_token=jwt.decode(token, key=os.environ.get("SECRET_KEY"), algorithms=['HS256'])
                
            
        except Exception as e:
            return rotas_error.main()
     
    return render_template("pagina_auth.html")

