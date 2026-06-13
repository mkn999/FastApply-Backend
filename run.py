from flask import Flask,jsonify,request
import sqlite3 #inbuilt in python

app = Flask(__name__)  #in the line we initalize our flask app from Flask Class


jobs=[]

def get_db():
    conn = sqlite3.connect("jobs.db")
    return conn


@app.route("/")
def landing():
    return jsonify([
        {
            "id":1,
            "id":"Kia",
        },
        {
            "id":1,
            "name":"Honda",
        },
    ]) #can also return a list of objects

@app.route("/jobs")
def profile():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * from jobs")
    rows = cursor.fetchall()
    jobs = []
    for row in rows:
        jobs.append({ #format the data from backend
            "id":row[0],
            "title":row[1],
            "company":row[2]
        })

    return jsonify(jobs)


@app.route("/job/<int:id>")#dynamic route which act as a template
def test(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?",
                   (id,) #tuple is expected
                   )

    row = cursor.fetchone()
    if row :
        return jsonify(row)
    else:
        return jsonify({
            "error": "Job description not found" #fallback for no job
        })


#keyword / filter "? -> is called as query parameter"
@app.route("/search")
def search():
    keyword = request.args.get("keyword") #used to get the keyword
    return f"You searched for {keyword}"


@app.route("/postjob", methods=["POST"])
def create_job():

    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()
    #add data to database
    cursor.execute("""INSERT INTO jobs (title,company) VALUES(?,?)""", (data["title"],data["company"]))
    conn.commit()

    return jsonify({
            "message":"Job created",
    })


@app.route("/removejob/<int:id>",methods=["DELETE"]) #/removejob/1
def deleteJob(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    print(cursor.rowcount)
    if cursor.rowcount == 0:
        return jsonify({
            "message":"Job id not valid for deletion",
        })
    else:
        return jsonify({
            "message":"Job Deleted",
        })

@app.route("/updatejob/<int:id>",methods=["PUT"]) #/removejob/1
def updateJob(id):
    conn = get_db()
    cursor = conn.cursor()
    data = request.get_json() #get data from request
    cursor.execute("UPDATE jobs SET title = ?, company = ? WHERE id = ?", (data["title"],data["company"],id))
    conn.commit()
    print(cursor.rowcount)
    if cursor.rowcount == 0:
        return jsonify({
            "message":"Job id not valid for updation",
        })
    else:
        return jsonify({
            "message":"Job Updated",
        })

if __name__ == "__main__": #used to indicate the start (only starts if directly executed)
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)