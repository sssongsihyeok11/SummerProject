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
app.config['JSON_AS_ASCII'] = False # 한글 데이터 깨짐 방지


@app.route('/')
def hello_html():
    return render_template('login.html')


# mail list 함수 -> render_template
#@app.route()
def show_list(id):
    
    sql = "SELECT * FROM mail_data WHERE Receiver_Address = %s"
    cur = mydb.cursor(buffered=True)
    cur.execute(sql,(id,))
    result = cur.fetchall()

    cur.close()
    
    return result
#   return render_template('.html')

# 로그인 기본 코드
@app.route('/login')
def login():
    sql = "SELECT * FROM e_mail_data.mail_participant"
    cur = mydb.cursor(buffered=True)
    cur.execute(sql)

    email = request.args.get('email_address')
    passwd = request.args.get('pass_word')
   
    for x in cur:
        if email == x[1] and passwd ==x[2]:
          mail_list = show_list(email)
          print(mail_list)
          return render_template('index.html',mail_list=mail_list)

    cur.close()
    return render_template('login.html')


# 단어 search 함수 -> render_template
@app.route('/search')
def search_contents():
    my_list=[]
    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data"
    cur.execute(sql)
    con = request.args.get('Content')
    for result in cur.fetchall():
       content = result[3]
       if (con) in content:
           my_list.append([result[1],result[3]])
    
    cur.close()
    sorted_list = sorted(my_list,key=lambda x:x[1])
    return render_template('search.html', search_list = sorted_list)
    
#메일 축적 함수 -> render_template, database
def insert_mail_list(id):
    mail_list = show_list(id)
    sender_address= input ("sender_address: ")
    receiver_address = input("receiver_address: ")
    content = input("content: ")
    mail_list.append([sender_address, receiver_address, content])

    return mail_list




# 검색 메일 목록 넘기기
@app.route('/send_search_contents')
def send_search_contents(str):
    send_search_list = search_contents(str)

    return jsonify(send_search_list)
#   return render_template('search_content.html', send_search_list = send_search_list)



#검색 정렬 함수
"""
@app.route('/search_sort')
def search_sort(str):

    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data WHERE Contents LIKE %s"
    cur.excute(sql, ('%' + str + '%',))

    result = cur.fetchall()

    cur.close()

    return render_template('search_sort.html', result = result)
"""



#print(search_sort("인하대"))

#검색 리스트 제거 함수, num은 index 
def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]

#def delete_search_list(str, num):
    sorted_list = search_sort(str)
    for x in range(len(sorted_list)):
      if sorted_list[x][0] == num :
          swap_elements(sorted_list, 0, x)
          sorted_list.pop(0)
          break
    return sorted_list

#print(delete_search_list("인하대", 5))


# 다수 제거 함수, 제거 갯수 최대 10개로 설정 ->render_template, database
#def multi_delete(str):
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

             count = count + 1
          break
    
    carbon(count)
    return sorted_list

# 탄소배출량 계산 함수
def carbon(num):
    carbon = num * 4
    print('약', carbon ,'g의 탄소배출을 막으셨어요!')


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







if __name__ =="__main__":
    app.run(host = "0.0.0.0", port='8080')
