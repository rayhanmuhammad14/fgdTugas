from flask import Flask, render_template,url_for, redirect, request, jsonify, session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'hallo'

client = MongoClient('mongodb+srv://rayhan10915:Iw9flIHrKqSHga5a@learningx.cy1fhy8.mongodb.net/')
db = client.fruit

@app.route('/')
def index():
    return render_template('dashboard.html')

# THIS IS A ADD AREA (INCLUDE HANDLER)
@app.route('/add')
def add():
    return render_template('AddFruit.html')

@app.route('/handleAdd', methods = ['POST'])
def handleAdd():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        gambar = request.files['gambar']
        deskripsi = request.form['deskripsi']
        
        if gambar:
            extNamaGambar = gambar.filename.split('/')[-1]
            filePath = f'static/assets/img/save_img/{extNamaGambar}'
            gambar.save(filePath)
        else:
            gambar = None 
    
        doc = {
            'nama' : nama,
            'harga' : harga,
            'gambar' : extNamaGambar,
            'deskripsi' : deskripsi
        }
        
        db.fruits.insert_one(doc)
        return redirect(url_for('dash'))
    
    else:
        return render_template('AddFruit.html')

# THIS IS FRUIT AREA (INCLUDE WITH HANDLER)
@app.route('/fruit', methods = ['GET'])
def dash():
    fruit = list(db.fruits.find({}))
    return render_template('index.html', fruit = fruit)

@app.route('/getFruit', methods = ['GET'])
def getFruit():
    fruit = list(db.fruits.find({},{'_id' : False}))
    return jsonify(fruit)

@app.route('/<_id>', methods = ['GET', 'POST'])
def edit(_id):
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        harga = request.form['harga']
        gambar = request.files['gambar']
        deskripsi = request.form['deskripsi']
        
        
        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi
        }
        
        if gambar:
            extNamaGambar = gambar.filename.split('/')[-1]
            filePath = f'static/assets/img/save_img/{extNamaGambar}'
            gambar.save(filePath)
            doc['gambar'] = extNamaGambar
        db.fruits.update_one({'_id' : ObjectId(id)},{'$set' : doc})
    id = ObjectId(_id)
    data = list(db.fruits.find({'_id' : id}))
    return render_template('EditFruit.html', data=data)

@app.route('/delete/<_id>')
def delete(_id):
    db.fruits.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000, debug=True)