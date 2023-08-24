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
#asdf
# 로그인 기본 코드
@app.route('/login',methods =['GET','POST'])
def login():
    sql = "SELECT * FROM e_mail_data.mail_participant"
    cur = mydb.cursor(buffered=True)
    cur.execute(sql)

    email = request.args.get('email_address')
    passwd = request.args.get('pass_word')
   
    for x in cur:
        if email == x[1] and passwd ==x[2]:
          mail_list = show_list(email)
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
           my_list.append([result[0],result[1],result[3]])
    
    cur.close()
    sorted_list = sorted(my_list,key=lambda x:x[2])
    for x in range(len(sorted_list)):
       sorted_list[x][0]=x+1

    return render_template('search.html', search_list = sorted_list)

def search_contents_list():
    my_list=[]
    cur = mydb.cursor()
    sql = "SELECT * FROM e_mail_data.mail_data"
    cur.execute(sql)
    con = request.args.get('Content')
    for result in cur.fetchall():
       content = result[3]
       if (con) in content:
           my_list.append([result[0],result[1],result[3]])
    
    cur.close()
    sorted_list = sorted(my_list,key=lambda x:x[2])
    for x in range(len(sorted_list)):
       sorted_list[x][0]=x+1

    return sorted_list    

#메일 추가
def insert_mail_data(sender, receiver, title, content):
    cur = mydb.cursor()
    sql = "INSERT INTO mail_data (Sender_Address, Receiver_Address, Title, Content) VALUES (%s, %s, %s, %s)"
    val = (sender, receiver, title, content)
    cur.execute(sql, val)
    mydb.commit()
    cur.close()

#광고 메일 merge함수
def specific_mail_merge():
   cur = mydb.cursor()
   merge_list =[]
   total_merge_list=[]
   con = ''
   sql = "SELECT * FROM e_mail_data.mail_data WHERE Title LIKE %s"
   keyword = '%' + '(광고)' + '%'
   cur.execute(sql, (keyword,))

   selected_mails = cur.fetchall()
   for x in range(len(selected_mails)): 
     merge_list.append(selected_mails[x])
     merge_list.append('--------------------------------------------------')
   for y in range(len(merge_list)):
      con = merge_list[0][4]
      if merge_list[y] =='--------------------------------------------------':
         continue
      else:
         if y in range(len(merge_list)):
            con+=merge_list[y][4]
            
   total_merge_list.append(['광고통합주소','메일탄소@*****.com','광고통합제목',con])
   insert_mail_data(total_merge_list[0][0],total_merge_list[0][1],total_merge_list[0][2],total_merge_list[0][3])
   return total_merge_list

def general_mail_merge():
   cur = mydb.cursor()
   
   sql = "SELECT * FROM e_mail_data.mail_data"
   cur.execute(sql)
   result = cur.fetchall()
   

   for x in range(len(result)):
      con =result[x][4]
      for y in range(len(result)):   
           if result[x][1]==result[y][1]:
              con = result[y][3] + ' ' + result[y][4] + '-------------------------------------------------'
      insert_mail_data(result[x][1],result[x][2],'병합메일',con)
      con =''
   cur.close()

#검색 리스트 제거 함수, num은 index 
def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]


def delete_search_list():
   want_to_delete_list = request.args.get('checkbox')
   cur = mydb.cursor()
   sql = "Delete FROM e_mail_data.mail_data WHERE Number = '%d'"
   list = search_contents_list()
   for x in range(len(want_to_delete_list)):
     for y in range(len(list)):
        if y==want_to_delete_list[x]:
           cur.execute(sql,(y,))
    

# 다수 제거 함수, 제거 갯수 최대 10개로 설정 ->render_template, database
#def multi_delete(str):
#    sorted_list = search_sort(str)
#    want_to_delete_list = []
#    for i in range(10):
#        input(i)
#        want_to_delete_list.append(i)

#    for x in range(len(sorted_list)):
#        for y in range(len(want_to_delete_list)):
#          if sorted_list[x][0] == want_to_delete_list[y]:
#             swap_elements(sorted_list, 0, x)
#             sorted_list.pop(0)

#            count = count + 1
#          break
    
#    carbon(count)
 #   return sorted_list


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

print (cal_mail_list())
# 탄소배출량 계산 함수
def carbon():
    value_of_mail = cal_mail_list()
    return render_template('reward.html',canbon=value_of_mail)

if __name__ =="__main__":
    app.run(host = "0.0.0.0", port='8080')

