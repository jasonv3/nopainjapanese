from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Post, Comment,Tag,posts_tags
from app.utils.decorator import permission_required


@bp.route('/tags/', methods=['POST'])
@token_auth.login_required
def create_tag():
    '''在某篇博客文章下面发表新tag'''
    data = request.get_json()
    
    if not data:
        return bad_request('You must post JSON data.')
    if 'tagname' not in data or not data.get('tagname').strip():
        return bad_request('Tagname is required.')
    querytag = Tag.query.filter_by(tagname=data.get('tagname', None)).first()
    if querytag is not None:
        response = jsonify(querytag.to_dict())
        response.status_code = 201
        # HTTP协议要求201响应包含一个值为新资源URL的Location头部
        response.headers['Location'] = url_for('api.get_tags')
        return response
 
    tag = Tag()
    tag.from_dict(data)
    # 必须先添加该评论，后续给各用户发送通知时，User.new_recived_comments() 才能是更新后的值
    db.session.add(tag)
    db.session.commit()  # 更新数据库，添加评论记录
    response = jsonify(tag.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_tags')
    return response


@bp.route('/tags/', methods=['GET'])
@token_auth.login_required
def get_tags():
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['TAGS_PER_PAGE'], type=int), 100)
    data = Tag.to_collection_dict(
        Tag.query.order_by(Tag.timestamp.desc()), page, per_page,
        'api.get_tags')
    return jsonify(data)

@bp.route('/tags/<int:id>', methods=['GET'])
def get_taginpost(id):
    '''返回一篇文章'''
    '''返回文章集合，分页'''
   
    res = db.engine.execute("select * from posts_tags where tag_id={} ".format(id))  
    mylist = []
    mylist=(list(res))
    mynewlist = []
    for u in mylist:
          mynewlist.append(u[0])
  

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    '''拥有独特的条件拼接方法'''
    data = Post.to_collection_dict(
        Post.query.order_by(Post.timestamp.desc()).filter(Post.id.in_(mynewlist)), page, per_page,
        'api.get_taginpost',id = id)
    return jsonify(data)


