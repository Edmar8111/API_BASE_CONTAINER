from flask import jsonify, render_template, request
from random import randint
from . import r_0, r_1
import requests
import threading
import jwt
import os
from . import rotas_error
from dotenv import load_dotenv
load_dotenv()

url_api="https://api.jikan.moe/v4/anime/" #url prefixa por id
url_api_="https://api.jikan.moe/v4/schedules/sunday?sfw" #url prefixa por dia da semana
url_api_0="https://api.jikan.moe/v4/top/anime?type=ova" #url prefixa type(ona, ova, etc...)
url_api_1="https://api.jikan.moe/v4/top/anime?sfw" #url prefixa top animes
url_api_2="https://api.jikan.moe/v4/anime?q=bleach&sfw" #url prefixa por nome
url_api_3="https://api.jikan.moe/v4/seasons/2009/fall?sfw" #url prefixa por ano e estação
url_api_4="https://api.jikan.moe/v4/top/anime?type=movie" #url prefixa por tipo(movie, tv, etc...)
url_api_5="https://api.jikan.moe/v4/seasons/upcoming" #url prefixa para animes que estão para lançar
url_api_5="https://api.jikan.moe/v4/seasons/now" #url prefixa para animes lançando agr

def retornar_url(valor):
    resposta=requests.get(url_api_1)
    if resposta.status_code==200:
        dados=resposta.json()['data']
        controlador=animes=[]
        for i in range(valor):
            a={}
            random_n=randint(0, 25)
            if random_n not in controlador and type(dados[random_n])==dict:
                for k in dados[random_n].keys():
                    a[f"{k}"]=dados[random_n][f"{k}"]
                animes.append(a)
                controlador.append(random_n)
        return animes

@r_0.route('/v1')
def main_(token=None):
    qtd_animes=requests.get(url_api).json()['pagination']['last_visible_page']
    anime=animes=list()
    try:
        for i,v in enumerate(retornar_url(10)):
            try:
                animes.append(dict(v))
            except:
                continue        
        
        if token!=None:
            try:
                token_decoded=jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
                info_user={
                    "user_id":token_decoded['user_id'],
                    "username":token_decoded['username'],
                    "exp":token_decoded['exp']
                }
                return render_template("base.html", dados={"animes":animes}, titulo="Top Animes", info_user=info_user)
                
            except jwt.ExpiredSignatureError:
                return rotas_error.main()
            except jwt.InvalidTokenError:
                return rotas_error.main()
       
        return render_template("base.html", dados={"animes":animes}, titulo="Top Animes")
    except:
        return jsonify({"Error":404})

@r_0.route("/dia")
def main_0():
    try:
        valor=request.args.get('dia')
        url=f"https://api.jikan.moe/v4/schedules/{valor}?sfw"
        animes=list()
        for i in requests.get(url).json()['data']:
            animes.append(i)
        return render_template("base.html", dados={"animes":animes}, titulo=f"{str(valor).capitalize()} animes!")
    except:
        return jsonify({"Erro":"404"})

@r_0.route("/busca")
def main_1():
    try:
        valor=request.args.get("busca")
        url=f"https://api.jikan.moe/v4/anime?q={valor}&sfw"
        animes=list()
        for i in requests.get(url).json()['data']:
            animes.append(i)
        return render_template("base.html", dados={"animes":animes}, titulo=f"Resultado para {str(valor).capitalize()} em animes!") 
    except:
        pass

@r_0.route("/favoritar")
def main_2():
    return