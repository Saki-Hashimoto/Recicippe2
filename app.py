
import os
from flask import Flask, render_template, request
from getrecipe import GetRecipeURL
from predict import TestProcess
from stock import saveCSV

UPLOAD_FOLDER='./static/food_image'

app = Flask(__name__)

#---------------トップページ------------------#

@app.route("/")
def index():
    return render_template('index.html')

#--------------------------------------#

#---------------食材アップロード------------------#

@app.route('/foodupload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_user_files():
    if request.method == 'POST':
        upload_file = request.files['upload_file']
        img_path = os.path.join(UPLOAD_FOLDER,upload_file.filename)
        upload_file.save(img_path)
        name = TestProcess(img_path)
        return render_template('uploadresult.html',result=name, img_path=img_path)

#--------------------------------------#

#---------------在庫管理------------------#

# @app.route('/')
# def upload():
#     return render_template('stockmain.html')

# @app.route('/stockmain', methods=['GET', 'POST'])
# def upload_user_files():
#     if request.method == 'POST':
#         upload_file = request.files['upload_file']
#         img_path = os.path.join(UPLOAD_FOLDER,upload_file.filename)
#         upload_file.save(img_path)
#         name = saveCSV(img_path)
#         return render_template('uploadresult.html',result=name, img_path=img_path)

#--------------------------------------#

#---------------食材・条件入力------------------#
@app.route("/recipesearch",methods=['GET','POST'])
def calculation():
    if request.method == "GET":
        return render_template('calculation.html')

        
@app.route("/resultrecipe",methods=['GET','POST'])
def resultrecipe():
    if request.method == "GET":
        return render_template('resultrecipe.html')
    elif request.method == "POST":
        name = request.form['name']
        genre = request.form['genre']
        scene = request.form['scene']
        url_list, recipe_name_list, recipe_img_list, time_list = GetRecipeURL(name, genre, scene)
        return render_template('resultrecipe.html', list1 = recipe_name_list, list2 = recipe_img_list, list3 = url_list, list4 = time_list)       

if __name__ == "__main__":
    app.run(debug=True)

#--------------------------------------#


