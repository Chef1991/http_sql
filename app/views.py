from app import app
from flask import request, Response, render_template
import queries
import json


# /db/<db_name>/table?user=asdf&pass=asdf&host=opt
@app.route("/db/<db_name>/table", methods=["GET"])
def get_all_tables(db_name):
    table_query = "SELECT table_schema, table_name, table_type FROM information_schema.tables"
    uname = request.args.get('user')
    pwd = request.args.get('pass')
    host = request.args.get('host')
    if host is None:
        host = "localhost"
    if pwd is None:
        pwd = ""
    con_str = "postgresql://{}:{}@{}/{}".format(uname, pwd, host, db_name)
    session = queries.Session(con_str)
    tables = []
    for row in session.query(table_query):
        print(row)
        table = {
                "schema": row['table_schema'], 
                "name": row["table_name"], 
                "type": row["table_type"]
        }
        print(table)
        tables.append(table)
    session.close()
    return Response(json.dumps(tables), mimetype='application/json')

# /table/<table_name>?user=asdf&pass=asdf&host=opt
@app.route("/db/<db_name>/table/<table_name>")
def describe_table(db_name, table_name):
    query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}'".format(table_name)
    uname = request.args.get('user')
    pwd = request.args.get('pass')
    host = request.args.get('host')
    if host is None:
        host = "localhost"
    if pwd is None:
        pwd = ""
    con_str = "postgresql://{}:{}@{}/{}".format(uname, pwd, host, db_name)
    session = queries.Session(con_str)
    columns = []
    for row in session.query(query):
        columns.append(row)
    session.close()
    return Response(json.dumps(columns), mimetype='application/json')

# /db/<db_name>/query?user=asdf&pass=asdf&host=obt&query=asdf
@app.route('/db/<db_name>/query')
def query(db_name):
    uname = request.args.get('user')
    pwd = request.args.get('pass')
    host = request.args.get('host')
    query = request.args.get('query')
    if host is None:
        host = "localhost"
    if pwd is None:
        pwd = ""
    con_str = "postgresql://{}:{}@{}/{}".format(uname, pwd, host, db_name)
    session = queries.Session(con_str)
    results = []
    for row in session.query(query):
        results.append(row)
    session.close()
    return Response(json.dumps(results), mimetype='application/json')


@app.route('/')
def index():
    return render_template('index.html')



