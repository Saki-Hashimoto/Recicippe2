
import os
import pandas as pd
import datetime
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

#---------------layout1234------------------#

@app.route("/layout1")
def layout1():
    return render_template('layout1.html')

@app.route("/layout2")
def layout2():
    return render_template('layout2.html')

@app.route("/layout3")
def layout3():
    return render_template('layout3.html')

@app.route("/layout4")
def layout4():
    return render_template('layout4.html')

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

column_names = ['date','task']
df = pd.read_csv('./csv/tasks.csv')
tasks = df.to_numpy().tolist()

def saveCSV(array):
    tasks_df = pd.DataFrame(array, columns=column_names)
    tasks_df.to_csv('./csv/tasks.csv', index=False)

@app.route('/stockmain', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('stockmain.html', tasks = tasks)
    else:
        if request.form.get('done') != None:
            done_index = int(request.form.get('done'))
            del tasks[done_index]
            saveCSV(tasks)
            return render_template('stockmain.html', tasks = tasks)
        elif request.form.get('updated_task') != None:
            updated_task = request.form.get('updated_task')
            updated_index = request.form.get('updated_index')
            date_added = datetime.datetime.now().date()
            task = [date_added, updated_task]
            tasks[int(updated_index)] = task
            saveCSV(tasks)
            return render_template('stockmain.html', tasks = tasks)

@app.route('/stockadd', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('stockadd.html')
    else:
        added_task = request.form.get('new_task')
        date_added = datetime.datetime.now().date()
        task = [date_added, added_task]
        tasks.append(task)
        saveCSV(tasks)
        return render_template('stockadd.html')

@app.route('/stockupdate', methods=['POST'])
def update_init():
    update_index = int(request.form.get('update'))
    return render_template('stockupdate.html', task_title = tasks[update_index][1], task_index = update_index)

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


