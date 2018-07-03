from flask import Flask
from flask import request
import json
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/severeTree',methods=["POST"])
def severe_tree():
    data = pd.DataFrame(json.loads(request.data))                             # 0==mild, 1==moderate, 2==severe
    if data['hb'] < 5.55:
        return 0
    if data['food'] < 2.5:
        if data['hb'] < 5.95:
            return 1
        else:
            return 2
    else:
        if data['age'] < 50:
            if data['sys'] < 167.5:
                if data['type'] == 2:   # gestacional==0, type1==1 y type2==2
                    if data['hb'] < 5.85:
                        return 1
                    else:
                        return 2
                elif data['type'] == 1:
                    if data['sys'] < 146:
                        if data['plas'] < 150:
                            return 2
                        else:
                            return 1
                    else:
                        return 2
                else:
                    return 2
            else:
                return 1
        else:
            if data['weight'] < 61:
                return 1
            else:
                if data['hb'] < 5.95:
                    return 1
                else:
                    return 2



@app.route('/prevalence',methods=["POST"])
def prevalence():
    data = pd.DataFrame(json.loads(request.data))                               # 0==no, 1==yes
    if data['plas'] <= 116: #primera altura, izquierda
        if data['pedi'] <= 0.201: #segunda altura, izquierda
            return 0
        else: #segunda altura, derecha
            if data['preg'] <= 2:
                return 0
            else:
                return 1
    else:
        if data['preg'] <= 7:
            if data['pedi'] <= 0.564:
                if data['plas'] <= 162:
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            if data['pedi'] <= 1:
                return 1
            else:
                return 0



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
