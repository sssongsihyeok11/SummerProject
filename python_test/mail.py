from flask import Flask, request, jsonify, render_template
import mysql.connector

# 사용할 database 주소
mydb = mysql.connector.connect(
    host = "localhost", #192.168.56.1
    user = "root",
    passwd="thdtlgur123",
    database="e_mail_data"    
)

app = Flask(__name__)


# 단어 search 함수
def search_contents(str):

    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data"
    cur.execute(sql)
    
    for result in cur.fetchall():
       content = result[2]
       if (str) in content:
           print(result)

search_contents("인하대")


# 로그인 기본 코드
@app.route('/login')
def login():
    username = request.args.get('user_name')
    passwd = request.args.get('pass_word')
    email = request.args.get('email_address')
    print(username, passwd, email)

    if username == 'dave':
        return_data = {'auth': 'success'}
    else :
        return_data = {'auth': 'failed'}
    return jsonify(return_data)

@app.route('/html_test')
def hello_html():
    return render_template('login.html')


if __name__ =="__main__":
    app.run(host = "0.0.0.0", port='8081')

