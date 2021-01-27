import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

# konfigurasi file db
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "nyetok_barang.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
# buat model kolom database untuk stokbarang
class Stock(db.Model):
    namabarang = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    qytbarang = db.Column(db.String(80))
    hargabeli = db.Column(db.String(80))
    hargajual = db.Column(db.String(80))
    diskonbarang = db.Column(db.String(80))
    def __repr__(self):
        return "{} {} {} {} {}".format(self.namabarang,self.qytbarang,self.hargabeli,self.hargajual,self.diskonbarang)

#routing
#indeks - home.html
@app.route('/', methods=["GET", "POST"]) #index
def home():
    #nambah stock ke database
    stocks = None
    if request.form:
        try:
            stock = Stock(namabarang = request.form["namabarang"],qytbarang = request.form["qytbarang"],hargabeli = request.form["hargabeli"],hargajual = request.form["hargajual"],diskonbarang = request.form["diskonbarang"])
            db.session.add(stock)
            db.session.commit()
        except Exception as e:
            print("Gagal nambah Stock ")
            print(e)
    stocks = Stock.query.all()
    return render_template("home.html", stocks=stocks)

#Delete route 
#POST methods
@app.route("/delete", methods=["POST"]) #delete/hapus row
def delete():
    namabarang = request.form.get("namabarang")
    #commit penghapusan
    stock = Stock.query.filter_by(namabarang=namabarang).first()
    db.session.delete(stock)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)