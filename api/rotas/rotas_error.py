from flask import render_template
from . import r_


@r_.errorhandler(404)
def main():
    return render_template("pagina_erro.html", error={"code":404})