from flask import Flask
from flask import request
import json
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/severeTree',methods=["POST"])
def severe_tree():
    data = json.loads(request.data)                           # 0==mild, 1==moderate, 2==severe
    print('Severity classifier')
    print(data)
    if data['hb'] < 5.55:
        risk = 0
    else:
        if data['food'] < 2.5:
            if data['hb'] < 5.95:
                risk = 1
            else:
                risk = 2
        else:
            if data['age'] < 50:
                if data['sys'] < 167.5:
                    if data['type'] == 2:   # gestacional==0, type1==1 y type2==2
                        if data['hb'] < 5.85:
                            risk = 1
                        else:
                            risk = 2
                    elif data['type'] == 1:
                        if data['sys'] < 146:
                            if data['plas'] < 150:
                                risk = 2
                            else:
                                risk = 1
                        else:
                            risk = 2
                    else:
                        risk = 2
                else:
                    risk = 1
            else:
                if data['weight'] < 61:
                    risk = 1
                else:
                    if data['hb'] < 5.95:
                        risk = 1
                    else:
                        risk = 2
    #hay que ponerlo en formato json para mandarlo... de la siguiente manera se puede hacer. Habrá alguna manera más elegante fijo
    print('Answer')
    print(risk)
    sol = pd.DataFrame()
    sol['risk'] = [int(risk)]
    return sol.iloc[0].to_json()


@app.route('/prevalence',methods=["POST"])
def prevalence():
    data = json.loads(request.data)                               # 0==no, 1==yes
    print('Prevalence of gestational diabetes')
    print(data)
    if data['plas'] <= 116: #primera altura, izquierda
        if data['pedi'] <= 0.201: #segunda altura, izquierda
            yes_no = 0
        else: #segunda altura, derecha
            if data['preg'] <= 2:
                yes_no = 0
            else:
                yes_no = 1
    else:
        if data['preg'] <= 7:
            if data['pedi'] <= 0.564:
                if data['plas'] <= 162:
                    yes_no = 0
                else:
                    yes_no = 1
            else:
                yes_no = 1
        else:
            if data['pedi'] <= 1:
                yes_no = 1
            else:
                yes_no = 0
    print('Answer')
    print(risk)
    #hay que ponerlo en formato json para mandarlo... de la siguiente manera se puede hacer. Habrá alguna manera más elegante fijo
    sol = pd.DataFrame()
    sol['yes_no'] = [int(yes_no)]
    return sol.iloc[0].to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
