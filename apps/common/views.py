from flask import Blueprint,request,make_response,jsonify
from utils import restful,zlcache
from utils.captcha import Captcha
from io import BytesIO
import qiniu

bp = Blueprint("common",__name__,url_prefix='/c')


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp