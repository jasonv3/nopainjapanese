from flask import jsonify
from app.api import bp
from app.api.auth import token_auth
from app.models import Permission
from app.utils.decorator import permission_required

import socket
import base64
import sys
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha


#access_key_id = 'LTAI4G5ZZD14dyd76CYC2KRW'# 请填写您的AccessKeySecret。
#access_key_secret = 'gXUNKLlE4aSBXiJbF8HF6mGcgBK714'
# host的格式为 bucketname.endpoint ，请替换为您的真实信息。
#host = 'https://crazykay-tmp.oss-cn-shanghai.aliyuncs.com';
# callback_url为 上传回调服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
#callback_url = "https://dev.shunmiao.tech/backend/api/";

access_key_id = 'LTAI4G2ASuzRtnxP6CwVKFiX'
# 请填写您的AccessKeySecret。
access_key_secret = 'B2tGJ5sks3Zu6gr8OE9GsXbZKPfEN9'
# host的格式为 bucketname.endpoint ，请替换为您的真实信息。
host = 'https://musejapanese.oss-cn-beijing.aliyuncs.com';
# callback_url为 上传回调服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
callback_url = "https://www.nopainjapanese.com/backend/api/";
# 用户上传文件时指定的前缀。
# upload_dir = 'images/'
expire_time = 30

def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_token(upload_dir):
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire_syncpoint = 1612345678
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())
    print('policy_encode')
    print(policy_encode)
    h = hmac.new(access_key_secret.encode(), policy_encode, sha)
    print('h')
    print(h)
    sign_result = base64.encodestring(h.digest()).strip()
    print('sign_result')
    print(sign_result)

    callback_dict = {}
    callback_dict['callbackUrl'] = callback_url;
    callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}' \
                                    '&height=${imageInfo.height}&width=${imageInfo.width}';
    callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded';
    callback_param = json.dumps(callback_dict).strip()
    base64_callback_body = base64.b64encode(callback_param.encode());

    token_dict = {}
    token_dict['accessid'] = access_key_id
    token_dict['host'] = host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    print('signature')
    print(token_dict['signature'])
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    token_dict['callback'] = base64_callback_body.decode()
    result = json.dumps(token_dict)
    return result

@bp.route('/oss_image_token', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def ossImageToken():
    '''获得oss签名'''
    upload_dir = 'images/'
    token = get_token(upload_dir)
    return jsonify(json.loads(token))

@bp.route('/oss_audio_token', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def ossAudioToken():
    '''获得oss签名'''
    upload_dir = 'audios/'
    token = get_token(upload_dir)
    return jsonify(json.loads(token))


@bp.route('/osscallback', methods=['POST'])
def osscallback(server):
    '''oss上传回调'''
    # get public key
    pub_key_url = ''

    try:
        pub_key_url_base64 = server.headers['x-oss-pub-key-url']
        pub_key = httpserver.get_pub_key(pub_key_url_base64)
    except Exception as e:
        print(str(e))
        print('Get pub key failed! pub_key_url : ' + pub_key_url)
        server.send_response(400)
        server.end_headers()
        return

    # get authorization
    authorization_base64 = server.headers['authorization']

    # get callback body
    content_length = server.headers['content-length']
    callback_body = server.rfile.read(int(content_length))

    # compose authorization string
    auth_str = ''
    pos = server.path.find('?')
    if -1 == pos:
        auth_str = server.path + '\n' + callback_body.decode()
    else:
        auth_str = httpserver.get_http_request_unquote(server.path[0:pos]) + server.path[pos:] + '\n' + callback_body

    result = httpserver.verrify(auth_str, authorization_base64, pub_key)

    if not result:
        print('Authorization verify failed!')
        print('Public key : %s' % (pub_key))
        print('Auth string : %s' % (auth_str))
        server.send_response(400)
        server.end_headers()
        return

    # response to OSS
    resp_body = '{"Status":"OK"}'
    server.send_response(200)
    server.send_header('Content-Type', 'application/json')
    server.send_header('Content-Length', str(len(resp_body)))
    server.end_headers()
    server.wfile.write(resp_body.encode())