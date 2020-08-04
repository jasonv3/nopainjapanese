from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Post, Comment,Tag,posts_tags,Word
from app.utils.decorator import permission_required
from jamdict import Jamdict



@bp.route('/words/<int:id>', methods=['GET'])
def get_wordinpost(id):
    '''返回一篇文章'''
    '''返回文章集合，分页'''
    res = db.engine.execute("select * from words where id={} ".format(id))  
    word = list(res)[0][1] 
    wordtocheck = word + str('%')

    data = {}
    jmd = Jamdict()
    result = jmd.lookup(wordtocheck)
    for entry in result.entries:
        key = entry.kana_forms[0].text
        data[key] = str(entry[0])
    return jsonify(data)