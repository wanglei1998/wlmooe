from flask import Blueprint,request,make_response,jsonify
from utils import restful,zlcache
from utils.captcha import Captcha
from io import BytesIO
import qiniu
import config

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

@bp.route('/uptoken/')
def uptoken():
    access_key = config.UEDITOR_QINIU_ACCESS_KEY
    secret_key = config.UEDITOR_QINIU_SECRET_KEY
    q = qiniu.Auth(access_key,secret_key)

    bucket = config.UEDITOR_QINIU_BUCKET_NAME
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})
