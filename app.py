from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello Flask!"
def data():
    import Database
    return Database.select_all()
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = "8080")
    


    #hi
    #hello
    #helloooo
    #보이니
    #아무거나
    #현종바보