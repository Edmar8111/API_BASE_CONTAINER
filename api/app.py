from flask import Flask, jsonify, request
import os

def ip_requeste(self, client):
    ip=request.headers.get('X-Forwarded-For', client)
    return str(ip)

# def require_key(func):
#    def wrapper():
def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]=123
    from .rotas import r_0, r_1, r_
    app.register_blueprint(r_)
    app.register_blueprint(r_0)
    app.register_blueprint(r_1)
    
    return app