from flask import Flask, render_template, request
import pandas as pd
import datetime

app = Flask(__name__)

column_names = ['date','task']
df = pd.read_csv('./csv/tasks.csv')
tasks = df.to_numpy().tolist()

def saveCSV(array):
    #配列からDataframeへ
    tasks_df = pd.DataFrame(array, columns=column_names)
    tasks_df.to_csv('./csv/tasks.csv', index=False)

#todo一覧画面
@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('stockmain.html', tasks = tasks)
    else:
        #完了ボタンを押した時の動作
        if request.form.get('done') != None:
            done_index = int(request.form.get('done'))
            del tasks[done_index]
            saveCSV(tasks)
            return render_template('stockmain.html', tasks = tasks)
        #編集画面でタスクを編集した時の動作
        elif request.form.get('updated_task') != None:
            updated_task = request.form.get('updated_task')
            updated_index = request.form.get('updated_index')
            date_added = datetime.datetime.now().date()
            task = [date_added, updated_task]
            tasks[int(updated_index)] = task
            saveCSV(tasks)
            return render_template('stockmain.html', tasks = tasks)

#todoの新規作成
@app.route('/stockadd', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('stockadd.html')
    else:
        #HTMLのテキストボックスの情報
        added_task = request.form.get('new_task')
        date_added = datetime.datetime.now().date()
        task = [date_added, added_task]
        #配列に追加
        tasks.append(task)
        saveCSV(tasks)
        return render_template('stockadd.html')

#todoを更新
@app.route('/stockupdate', methods=['POST'])
def update_init():
    update_index = int(request.form.get('update'))
    return render_template('stockupdate.html', task_title = tasks[update_index][1], task_index = update_index)

if __name__ == '__main__':
    app.run(debug = True)
