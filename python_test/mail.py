from flask import Flask, request, jsonify, render_template
import mysql.connector

# 사용할 database 주소
mydb = mysql.connector.connect(
    host = "localhost", #192.168.68.100
    user = "newuser",
    passwd="thdtlgur123!",
    database="e_mail_data"    
)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 한글 데이터 깨짐 방지


@app.route('/')
def hello_html():
    return render_template('login.html')


# mail list 함수 
def show_list(id):
    
    sql = "SELECT * FROM mail_data WHERE Receiver_Address = %s"
    cur = mydb.cursor(buffered=True)
    cur.execute(sql,(id,))
    result = cur.fetchall()

    cur.close()
    
    return result

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


def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]

#검색 리스트 내부에서 제거 함수, num은 index 
def delete_search_list(str, num):
    sorted_list = search_sort(str)
    for x in range(len(sorted_list)):
      if sorted_list[x][0] == num :
          swap_elements(sorted_list, 0, x)
          sorted_list.pop(0)
          break
    return sorted_list


# 다수 제거 함수, 제거 갯수 최대 10개로 설정 ->render_template, database
#def multi_delete(str): (수정 필)
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


#메일 리스트 갯수 함수
def cal_mail_list():
   my_list=[]
   cur =mydb.cursor()
   sql = "SELECT * FROM e_mail_data.mail_data"
   cur.execute(sql)
   result = cur.fetchall()
   for x in range(len(result)): 
     my_list.append(result[x])

   return len(my_list)

# 탄소배출량 계산 함수
def carbon():
    value_of_mail = cal_mail_list()
    return render_template('reward.html',canbon=value_of_mail)

if __name__ =="__main__":
    app.run(host = "0.0.0.0", port='8080')
