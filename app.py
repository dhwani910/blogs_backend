from flask import Flask, request, Response
from flask_cors import CORS
import json
import mariadb
import dbcreds
# import sys



app = Flask(__name__)
CORS(app)


def connect():
      return mariadb.connect(
         user = dbcreds.user,
         password = dbcreds.password,
         host = dbcreds.host,
         port = dbcreds.port,
         database = dbcreds.database
    )

# End points for post page    

@app.route('/api/blogs', methods=['GET','POST', 'PATCH', 'DELETE'])


def blogPage():
    if request.method == 'GET':
        conn = None
        cursor = None
        result = None
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            result = cursor.fetchall()
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (result != None):
                return Response(
                    json.dumps(result, default=str),
                    mimetype = "application/json",
                    status=200
                ) 
            else: 
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )       
    elif request.method == 'POST':
        conn = None
        cursor = None
        result = None
        post = request.get_json()
        content = post["content"]
        # b_content = request.json.get(content)
        # print(post.get('content'))
        
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts(content) VALUES (?)", [content])
            conn.commit()
            result = cursor.rowcount
            print("###########",result)
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            # if(result == 1):    
                return Response(
                    "successfully created!",
                    mimetype="text/html",
                    status=201
                )
            else:
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )    
        return Response(
            "error",
            mimetype="text/html",
            status=400
        )          
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        result = None
        post = request.get_json()
        content = post["content"]
        post_id = request.json.get("id")
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE posts SET content=? WHERE id = ? ", ["content, post_id"])
            conn.commit()
            result = cursor.rowcount
            print("########", result)
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    "updated successfully...",
                    mimetype="text/html",
                    status=204
                ) 
            else:
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )                      
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        result = None
        post_id = request.json.get("id")
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id = ?", [post_id])
            conn.commit()
            result = cursor.rowcount
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    "Deleted!",
                    mimetype="text/html",
                    status=201
                ) 
            else:
                return Response(
                    "something wrong",
                    mimetype="text/html",
                    status=500
                )    


# End points for user

def connect():
      return mariadb.connect(
         user = dbcreds.user,
         password = dbcreds.password,
         host = dbcreds.host,
         port = dbcreds.port,
         database = dbcreds.database
    )

@app.route('/users', methods = ['GET','POST', 'PATCH', 'DELETE'])


def users():
    if request.method == 'GET':
        conn = None
        cursor = None
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", [username, password])
            result = cursor.fetchone()
            users=[]
            for item in result:
                user = {
                    "id": item[0],
                    "username": item[1],
                    "password": item[2]
                }
                users.append(user)
            print(result)
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    json.dumps(result, default=str),
                    mimetype = "application/json",
                    status=200
                ) 
            else: 
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )       
    elif request.method == 'POST':
        conn = None
        cursor = None
        user = request.json
        
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", [username, password])
            conn.commit()
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    "successfully created!",
                    mimetype="text/html",
                    status=201
                )
            else:
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )    
        return Response(
            "error",
            mimetype="text/html",
            status=400
        )          
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        user = request.json
        user_id = request.json
       
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", ["password", "user_id"])  
            conn.commit()
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    "updated successfully...",
                    mimetype="text/html",
                    status=204
                ) 
            else:
                return Response(
                    "something wrong..",
                    mimetype="text/html",
                    status=500
                )                      
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        user_id = request.json
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", [user_id])
            conn.commit()
        except Exception as ex:
            print("error")
            print(ex)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
                return Response(
                    "Deleted!",
                    mimetype="text/html",
                    status=201
                ) 
            else:
                return Response(
                    "something wrong",
                    mimetype="text/html",
                    status=500
                )    



