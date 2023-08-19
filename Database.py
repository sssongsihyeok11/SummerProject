import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="thdtlgur123",
    database="txt"
)

def select_all(): #조회 함수생성
    
    cur = mydb.cursor()                     #커서 객체생성
    sql ='''SELECT * FROM txt.people'''     #조회 SQL

    cur.execute(sql)                        #커서를 통한 SQL실행
    select_all_result = cur.fetchall()      #커서의 결과를 담는 객체

    for x in select_all_result:
        print(x)

select_all()                                #함수 실행