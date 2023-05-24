from urllib.parse import parse_qs
from cgi import FieldStorage
import json


# gunicorn -b "127.0.0.1:8081" --workers=1 test_wsgi:application
def application(env, start_response):
    print("==================================================")
    # print(env)

    print("------- GET PARAMS -------")
    for k, v in parse_qs(env["QUERY_STRING"]).items():
        print(f"{k}   =   {v}")

    copy = env.copy()
    copy['QUERY_STRING'] = ""
    post = FieldStorage(fp=env['wsgi.input'], environ=copy, keep_blank_values=True)
    print("------- POST PARAMS -------")
    for k in post.keys():
        try:
            as_json = json.loads(k)
            print(json.dumps(as_json, ensure_ascii=True, indent=4))
        except ValueError:
            print(f"{k}  =  {post.getvalue(k)}")

    print("==================================================")

    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]