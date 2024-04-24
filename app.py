from errno import errorcode
import os
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask,request,render_template,redirect,session,url_for,jsonify
import json
from werkzeug.utils import secure_filename
import mysql.connector

from flask_mysqldb import MySQL
msg=""
class TumorDetectorr:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict_result(self, img):
        image=cv2.imread(img)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((64, 64))
        image=np.array(image)
        input_img = np.expand_dims(image, axis=0)
        result = np.argmax(self.model.predict(input_img), axis=-1)
        return result
    
    def get_class_name(self, class_no):
        if class_no == 0:
            return "NO.There is not brain tumor on this picture"
        elif class_no == 1:
            return "YES.There is  braint tumor on this picture"


app=Flask(__name__)
tumor_detector = TumorDetectorr("TumorMozga10EpochsCategorical.h5")




def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="users",
            connect_timeout=60 
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST or err.errno == errorcode.ER_SERVER_SHUTDOWN:
            print("Lost connection to MySQL server. Reconnecting...")
            return connect_to_mysql()
        else:
            raise

connection = connect_to_mysql()

cursor=connection.cursor()
app.secret_key="super secret key"

@app.route('/')
def indexx():
    return render_template("login.html")

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        msg=""
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'static', 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        value = tumor_detector.predict_result(file_path)
        result = tumor_detector.get_class_name(value.item())
        return jsonify({"result": result, "file_path": file_path, "file_name": f.filename,msg:msg})

    return jsonify({"error": "Invalid request"})

@app.route("/index", methods=["POST"])
def indexPost():
    msg = "a"
    
    if request.method == "POST":
        ime = request.form.get('imee')
        sifra = request.form.get('sifraa')
        slika = request.form.get('slika')
        rezultat = request.form['rezultatA']
        doktor=request.form.get('doktor')
        if ime is not None and sifra is not None and slika is not None and rezultat is not None : 
            cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (doktor,))
            doc_id_result = cursor.fetchone()
            doc_id = doc_id_result[0] if doc_id_result else None
            cursor.execute('INSERT INTO `pacijent`( `pac_ime`, `pac_sifra`, `slika`, `rezultat`, `doc_id`)  VALUES (%s, %s, %s, %s,%s )',
                           (ime, sifra, slika, rezultat,doc_id))
            connection.commit() 
            msg="Korisnik dodat uspešno!"
        else:
            msg = "Svi podaci nisu dostupni za dodavanje korisnika."

    return render_template("index.html", msg=msg)

@app.route('/delete/<int:id>', methods=['DELETE'])

def deletePacijent(id):
    if request.method=="DELETE":
        cursor.execute("DELETE FROM `pregled` WHERE pr_id=%s", (id,))
        connection.commit()
        msg = "Uspješno izbrisan korisnik"
        return redirect(url_for('pregledTermina'))

@app.route("/update/<int:id>",methods=["PATCH"])
def updatePacijent(id):
    if request.method=="PATCH":
        imePac=request.form.get("ime")
        print(imePac)
        sifra=request.form.get("sifra")
        slika=request.form.get("slika")
        rezultat = request.form.get("rezultatt")
        doktor=request.form.get("doktor")
        print(imePac,sifra,slika,doktor,rezultat)
        cursor.execute( "UPDATE `pacijent` SET `pac_ime`=%s, `pac_sifra`=%s, `slika`=%s, `rezultat`=%s, `doc_id`=%s WHERE pac_id=%s",(imePac, sifra, slika, rezultat, doktor, id,))
        connection.commit()
        msg = "Uspješno izbrisan korisnik"
        return jsonify({"message": "Uspješno ažurirano."}), 200

@app.route("/addrecord/<int:id>",methods=["PATCH"])
def updateRecord(id):
    if request.method=="PATCH":        
        cursor.execute("UPDATE pregled SET odobreno='DA' WHERE pr_id=%s", (id,))
        connection.commit()
        return jsonify({"message": "Uspješno ažurirano."}), 200


@app.route("/index")
def index():
    return render_template("index.html",ime=session["ime"])

@app.route("/i/unosTermina",methods=["POST","GET"])
def unosTermina():
    cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (session["ime"],))
    doc_id_result = cursor.fetchone()
    cursor.fetchall()  

    cursor.execute('SELECT `pac_id` FROM `pacijent` WHERE `pac_ime` = %s', (session["ime"],))
    pac_id_result = cursor.fetchone()
    cursor.fetchall()

    cursor.execute('SELECT `med_ime` FROM `medicinske_sestra` WHERE `med_ime` = %s', (session["ime"],))
    medSestra = cursor.fetchone()
    cursor.fetchall()

    imenaDoc=[]
    imenaPac=[]
    if doc_id_result:
        name="doktor"
    elif pac_id_result:
        name="pacijent"
    elif medSestra:
        name="medSestra"
        cursor.execute('SELECT `medses_id` FROM `medicinske_sestra` WHERE `med_ime` = %s', (session["ime"],))
        med_id_result = cursor.fetchone()
        med_id = med_id_result[0]
    if request.method=="GET":

        if doc_id_result:

            del imenaDoc[:]
            del imenaPac[:]
            cursor.execute('select p.pac_ime from pacijent as p join doktor as d on d.doc_id=p.doc_id where doc_ime=%s ',(session["ime"],))
            ll=cursor.fetchall()
            for element in ll:
                ime = element[0]
                imenaPac.append(ime)
            imenaDoc.append(session["ime"])


        elif pac_id_result:

            del imenaPac[:]
            del imenaDoc[:]
            imenaPac.append(session["ime"])
            cursor.execute('select d.doc_ime from pacijent as p join doktor as d on d.doc_id=p.doc_id where pac_ime=%s ',(session["ime"],))
            imenaDoc=cursor.fetchone()
        elif medSestra:
            del imenaDoc[:]
            del imenaPac[:]
            cursor.execute('select DISTINCT  p.pac_ime from pacijent as p join doktor as d on d.doc_id=p.doc_id  ')
            ll=cursor.fetchall()
            for element in ll:
                ime = element[0]
                imenaPac.append(ime)
            
            cursor.execute('select DISTINCT  d.doc_ime from pacijent as p join doktor as d on d.doc_id=p.doc_id  ')
            lll=cursor.fetchall()
            for elementt in lll:
                imee = elementt[0]
                imenaDoc.append(imee)
    if request.method=="POST":
        doktor = request.form.get('doktor')
        pacijent = request.form.get('pacijent')
        datum = request.form.get('datum')
        cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (doktor,))
        doc_id_result = cursor.fetchone()
        doc_id = doc_id_result[0]
        cursor.execute('SELECT `pac_id` FROM `pacijent` WHERE `pac_ime` = %s', (pacijent,))
        pac_id_result = cursor.fetchone()
        pac_id = pac_id_result[0]
        
        print("IMEEE",medSestra)
        if name=="doktor":
            cursor.execute("INSERT INTO `pregled`( `doc_id`, `pac_id`, `datum`,odobreno) VALUES (%s,%s,%s,'da')",(doc_id,pac_id,datum))
        elif name=="pacijent" :
            cursor.execute("INSERT INTO `pregled`( `doc_id`, `pac_id`, `datum`) VALUES (%s,%s,%s)",(doc_id,pac_id,datum))
        elif name=="medSestra":
            
            cursor.execute("INSERT INTO `pregled`( `doc_id`, `pac_id`, `datum`,med_id) VALUES (%s,%s,%s,%s)",(doc_id,pac_id,datum,med_id))
   
        connection.commit() 
    return render_template("unosTermina.html",pacijenti=imenaPac,doktori=imenaDoc,name=name)


@app.route("/medPage",methods=["GET"])
def medPage():
    return redirect(url_for("unosTermina"))


@app.route("/userPage",methods=["GET"])
def userPage():
    doktorr=[]
    cursor.execute('select d.doc_ime from pacijent as p join doktor as d on d.doc_id=p.doc_id where pac_ime=%s ',(session["ime"],))
    doktorr=cursor.fetchone()
    
    cursor.execute('SELECT * FROM `pacijent` where pac_ime=%s ',(session["ime"],))
    vrijednosti=cursor.fetchall()
    
    return render_template("userPage.html",ime=session["ime"],kor=vrijednosti,doktor=doktorr)

@app.route("/index/pregledPacijenata",methods=["GET","PATCH"])
def pregledPacijenata():
    cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (session["ime"],))
    doc_id_result = cursor.fetchone()
    doc_id = doc_id_result[0] if doc_id_result else None
    cursor.execute('SELECT * FROM pacijent  where doc_id=%s',(doc_id,))
    rec=cursor.fetchall()
    json_data = json.dumps({'rec': rec})
    return render_template("pregledPacijenata.html",data=rec,json_data=json_data,name="Pyhton") 

@app.route("/i/pregledTermina",methods=["GET","DELETE","PATCH"])
def pregledTermina():
    msg=""
    cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (session["ime"],))
    doc_id_result = cursor.fetchone()
    cursor.execute('SELECT `pac_id` FROM `pacijent` WHERE `pac_ime` = %s', (session["ime"],))
    pac_id_result = cursor.fetchone()
    vrijednosti=None
    if doc_id_result:
        doc_id = doc_id_result[0] 
        cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.doc_id = %s and p.odobreno != "DA" and DATE(p.datum) >= CURRENT_DATE ORDER BY p.datum', (doc_id,))
        vrijednosti=cursor.fetchall()
        name="doktor"
    if pac_id_result:
        pac_id = pac_id_result[0] 
        cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.pac_id = %s and p.odobreno != "DA" and DATE(p.datum) >= CURRENT_DATE ORDER BY p.datum', (pac_id,))
        vrijednosti=cursor.fetchall()
        name="pacijent"
    elif vrijednosti ==[]:
        msg="Nemamo trenutno unesenih termina za vas"

    return render_template("pregledTermina.html",data=vrijednosti,msg=msg,name=name)

@app.route("/i/pregledDanasnjih")
def pregledDanasnjih():
    msg=""
    cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (session["ime"],))
    doc_id_result = cursor.fetchone()
    vrijednosti=[]
    
    doc_id = doc_id_result[0] 
    cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.doc_id = %s and p.odobreno = "DA" and DATE(p.datum) = CURRENT_DATE ORDER BY p.datum', (doc_id,))
    vrijednosti=cursor.fetchall()
    
    if vrijednosti ==[]:
        msg="Nemate danas termina za pregled"
    return render_template("pregledDanasnjih.html",data=vrijednosti,msg=msg)

@app.route("/i/pregledodobrenihTermina")
def pregledTerminaSvih():
    cursor.execute('SELECT `doc_id` FROM `doktor` WHERE `doc_ime` = %s', (session["ime"],))
    doc_id_result = cursor.fetchone()
    cursor.execute('SELECT `pac_id` FROM `pacijent` WHERE `pac_ime` = %s', (session["ime"],))
    pac_id_result = cursor.fetchone()
    cursor.execute('SELECT `medses_id` FROM `medicinske_sestra` WHERE `med_ime` = %s', (session["ime"],))
    sestra_result = cursor.fetchone()
    vrijednosti=[]
    msg=""
    name=""
    if doc_id_result:
        vrijednosti=[]
        doc_id = doc_id_result[0] 
        cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.doc_id = %s and p.odobreno = "DA" and DATE(p.datum) >= CURRENT_DATE  ORDER BY p.datum', (doc_id,))
        vrijednosti=cursor.fetchall()
        name="doktor"
    if pac_id_result:
        vrijednosti=[]
        pac_id = pac_id_result[0] 
        cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.pac_id = %s and p.odobreno = "DA" and DATE(p.datum) >= CURRENT_DATE ORDER BY p.datum', (pac_id,))
        vrijednosti=cursor.fetchall()
        name="pacijent"
    elif sestra_result:
        vrijednosti=[]
        ses_id = sestra_result[0] 
        cursor.execute('SELECT * FROM pregled as p JOIN doktor as d ON p.doc_id = d.doc_id JOIN pacijent as pa ON pa.pac_id = p.pac_id WHERE p.med_id= %s  and DATE(p.datum) >= CURRENT_DATE ORDER BY p.datum',(ses_id,) )
        vrijednosti=cursor.fetchall()
        name="medSestra"

    if vrijednosti ==[]:
        msg="Nemamo trenutno unesenih termina za vas"
    return render_template("pregledOdobrenihTermina.html",data=vrijednosti,msg=msg,name=name)

@app.route('/login', methods=['GET',"POST"])
def login():

    msg=""
    if request.method=="POST":
        ime=request.form['ime']
        sifra=request.form['sifra']   
        cursor.execute('SELECT * FROM `pacijent` WHERE pac_ime=%s and pac_sifra=%s',(ime,sifra))
        pacijent=cursor.fetchone()
        cursor.execute('SELECT * FROM `doktor` WHERE doc_ime=%s and doc_sifra=%s',(ime,sifra))
        doktor=cursor.fetchone()
        cursor.execute('SELECT * FROM `medicinske_sestra` WHERE med_ime=%s and med_sifra=%s',(ime,sifra))
        sestra=cursor.fetchone()
        if pacijent or doktor or sestra:
            
            if doktor!=None and doktor[4]=="doktor":
                session['prijavljen']=True
                session["ime"]=doktor[1]
                return redirect(url_for('index'))
            elif pacijent!=None and pacijent[6]=="pacijent":
                session['prijavljen']=True
                session["ime"]=pacijent[1]
                return redirect(url_for('userPage'))
            elif sestra!=None and sestra[3]=="sestra":
                session['prijavljen']=True
                session["ime"]=sestra[1]
                return redirect(url_for('medPage'))
                

        else:
            msg="The name or password is currently not found in our database. Please try again"
    return render_template("login.html",msg=msg)

@app.route("/logout")
def logout():
    session.pop("prijavljen",None)
    session.pop("ime",None)
    return redirect(url_for("login"))







if __name__ == '__main__':
    app.run(debug=True)


