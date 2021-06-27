from flask import Flask, render_template, request, session
import random

app = Flask(__name__, template_folder='Templates/')
app.config['SECRET_KEY'] = '467d4dc4eef096f79f88523dfd8fbe661a2c437c'


@app.route('/')
def main():
    if 'firtrue' not in session:
        firtrue = 100
        sectrue = 100

        session['firtrue'] = firtrue
        session['sectrue'] = sectrue

    if 'history1' not in session:
        session['history1'] = []
        session['history2'] = []

    history1 = session['history1']
    history2 = session['history2']
    if 'numhis' not in session:
        session['numhis'] = []

    return render_template('main.html', spirit=False, his1=history1, his2=history2, numhis=session['numhis'],
                           ran=len(history2), messsage='Теперь введите двузначное число', firtrue=session['firtrue'],
                           sectrue=session['sectrue'])


@app.route('/ready', methods=['post'])
def ready():
    nums = []
    if 'firtrue' not in session:
        firtrue = 100
        sectrue = 100

        session['firtrue'] = firtrue
        session['sectrue'] = sectrue

    for i in range(0, 2):
        nums.append(random.randint(10, 99))

    if 'history1' in session:

        history1 = session['history1']
        history2 = session['history2']

    else:
        history1 = []
        history2 = []

    if 'numhis' not in session:
        session['numhis'] = []

    history1.append(nums[0])
    history2.append(nums[1])

    session['history1'] = history1
    session['history2'] = history2

    session['nums'] = nums

    print(len(history2))

    session['flag_ready'] = True
    return render_template('main.html', spirit=True, nums=nums, his1=history1, his2=history2, numhis=session['numhis'],
                           ran=len(history2), message='Теперь введите число', firtrue=session['firtrue'],
                           sectrue=session['sectrue'])


@app.route('/commit', methods=['post'])
def commit():
    print(request.form)
    print(session)

    if 'firtrue' not in session:
        firtrue = 100
        sectrue = 100

        session['firtrue'] = firtrue
        session['sectrue'] = sectrue

    message = 'Теперь введите двузначное число'

    if session['flag_ready'] == True and request.form['Number'] and len(request.form['Number']) == 2:
        if 'history1' not in session:
            session['history1'] = []
            session['history2'] = []

        if 'numhis' in session:

            numhis = session['numhis']
            numhis.append(request.form['Number'])
            session['numhis'] = numhis
        else:
            numhis = []
            session['numhis'] = numhis.append(request.form['Number'])
            print(session['numhis'])
            session['flag_ready'] = False
        for i in range(len(session['nums'])):
            print('check', request.form['Number'],'and',session['nums'][i])
            if int(request.form['Number']) == int(session['nums'][i]):
                if i == 0:
                    session['firtrue'] += 1
                else:
                    session['sectrue'] += 1
            else:
                if i == 0:
                    session['firtrue'] -= 1
                else:
                    session['sectrue'] -= 1
        message = 'Загадайте новое число'

    elif not session['flag_ready']:
        message = 'Для начала загадайте число'

    elif not request.form['Number']:
        message = 'Теперь введите двузначное число'

    history1 = session['history1']
    history2 = session['history2']
    print(len(history2))

    return render_template('main.html', spirit=False, his1=history1, his2=history2, numhis=session['numhis'],
                           ran=len(history2), message=message,firtrue=session['firtrue'],
                           sectrue=session['sectrue'])


# if __name__ == "__main__":
#     app.run(debug=True)
