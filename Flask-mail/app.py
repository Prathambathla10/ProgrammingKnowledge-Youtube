from flask import Flask,render_template,request,redirect,url_for
from flask_mail import Mail,Message
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('DEL_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail=Mail(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit",methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]
        message = request.form["message"]
        msg = Message(subject, sender = os.getenv('DEL_EMAIL'), recipients = [os.getenv('REC_EMAIL')])
        msg.body = "Hello from"+name+",\n\n"+message
        mail.send(msg)
        return redirect(url_for("index"))
    
app.run(debug=True)