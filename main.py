from flask.views import MethodView
from flask import render_template, Flask, request, session
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = '467d4dc4eef096f79f88522dfd8fbe661a1c437c'


class ShowUsers(MethodView):

    def get(self):
        if 'flag_ready' not in session:
            session['flag_ready'] = False
        if 'fir_true' not in session:
            session['fir_true'] = 100
            session['sec_true'] = 100

        if 'history1' not in session:
            session['history1'] = []
            session['history2'] = []

        if 'num_his' not in session:
            session['num_his'] = []

        return render_template('main.html', his1=session['history1'], his2=session['history2'],
                               numhis=session['num_his'], ran=len(session['history2']),
                               message='Теперь введите двузначное число', firtrue=session['fir_true'],
                               sectrue=session['sec_true'])

    def check_num(self):

        if 'fir_true' not in session:
            fir_true = 100
            sec_true = 100

            session['fir_true'] = fir_true
            session['sec_true'] = sec_true

        message = 'Теперь введите двузначное число'
        spirit = True
        if str(request.form['Number']).isdigit():
            if session['flag_ready'] and request.form['Number'] and len(request.form['Number']) == 2 and \
                    int(request.form['Number']) > 0:
                spirit = False
                if 'history1' not in session:
                    session['history1'] = []
                    session['history2'] = []

                if 'num_his' in session:

                    num_his = session['num_his']
                    num_his.append(request.form['Number'])
                    session['num_his'] = num_his
                else:
                    num_his = []
                    session['num)his'] = num_his.append(request.form['Number'])

                trues = [int(session['nums'][0]), int(session['nums'][1])]
                if int(request.form['Number']) in trues:
                    if trues.index(int(request.form['Number'])) == 0:
                        session['fir_true'] += 1
                        session['sec_true'] -= 1
                    else:
                        session['sec_true'] += 1
                        session['fir_true'] -= 1
                else:
                    session['fir_true'] -= 1
                    session['sec_true'] -= 1

                message = 'Загадайте новое двузначное число'
                session['flag_ready'] = False

        elif not session['flag_ready']:
            message = 'Для начала загадайте число'

        return render_template('main.html', spirit=spirit, his1=session['history1'], his2=session['history2'],
                               numhis=session['num_his'], nums=session['nums'], ran=len(session['history1']),
                               message=message, firtrue=session['fir_true'], sectrue=session['sec_true'])

    def make_rand_num(self):

        session.permanent = False
        if 'fir_true' not in session:
            session['fir_true'] = 100
            session['sec_true'] = 100

        if 'history1' in session:
            history1 = session['history1']
            history2 = session['history2']

        else:
            history1 = []
            history2 = []

        if 'num_his' not in session:
            session['num_his'] = []

        if not session['flag_ready']:
            nums = []
            for i in range(0, 2):
                nums.append(random.randint(10, 99))
            history1.append(nums[0])
            history2.append(nums[1])
            session['nums'] = nums

        session['history1'] = history1
        session['history2'] = history2
        session['flag_ready'] = True

        return render_template('main.html', spirit=True, his1=session['history1'], his2=session['history2'],
                               numhis=session['num_his'], nums=session['nums'], ran=len(history2),
                               message='Теперь введите двузначное число', firtrue=session['fir_true'],
                               sectrue=session['sec_true'])

    def post(self):
        if 'Number' in request.form:
            return self.check_num()
        else:
            return self.make_rand_num()


app.add_url_rule('/', view_func=ShowUsers.as_view('show_users'))

app.run(debug=True)
