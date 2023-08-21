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
list=[]

# mail list 함수
def show_list(id):
    cur = mydb.cursor()
    sql = "SELECT * FROM mail_data WHERE Receiver_Address LIKE %s"
    cur.execute(sql, (id,))
    result = cur.fetchall()

    cur.close()
    
    return result

print(show_list('ssongsh98@naver.com'))

# 단어 search 함수
def search_contents(str):
    
    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data"
    cur.execute(sql)
    
    for result in cur.fetchall():
       content = result[2]
       if (str) in content:
           list.append([result[0],result[1],result[2]])
    
    cur.close()

    return list

#검색 정렬 함수
def search_sort(str):
    search_list = search_contents(str)
    result = sorted(search_list,key=lambda x: x[2])
    return result

#sql 이용 검색 정렬 함수 (맞나싶네요ㅋㅋ)
def search_sort(str):
    
    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data WHERE Contents LIKE %s"
    cur.excute(sql, ('%' + str + '%',))

    result = cur.fetchall()
    
    cur.close()

    return result


#print(search_sort("인하대"))

#검색 리스트 제거 함수, num은 index
def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]

def delete_search_list(str, num):
    sorted_list = search_sort(str)
    for x in range(len(sorted_list)):
      if sorted_list[x][0] == num :
          swap_elements(sorted_list, 0, x)
          sorted_list.pop(0)
          break
    return sorted_list

print(delete_search_list("인하대", 5))


# 다수 제거 함수, 제거 갯수 최대 10개로 설정
def multi_delete(str):
    sorted_list = search_sort(str)
    want_to_delete_list = []
    for i in range(10):
        input(i)
        want_to_delete_list.append(i)

    for x in range(len(sorted_list)):
        for y in range(len(want_to_delete_list)):
          if sorted_list[x][0] == want_to_delete_list[y]:
             swap_elements(sorted_list, 0, x)
             sorted_list.pop(0)
          break
    
    return want_to_delete_list

# http protocol routing function
#@app.route('/', methods = ['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        keyword = request.form['keyword']
#        if keyword:
#            results = search_contents(keyword)
#            return render_template('index.html', results=results, keyword=keyword)
#        else:
#            return "Please enter a keyword."

#    return render_template('index.html')


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

