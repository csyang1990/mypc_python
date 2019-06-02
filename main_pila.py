from flask import Flask,request,render_template,abort
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import numpy as np
from datetime import datetime #, timedelta
import time, os
import sqlite3
import json
# pd.set_option('display.max_rows', 5)
# pd.set_option('display.max_columns', 99)

app = Flask(__name__)

# yfile = r'E:\근무표\필라테스2.xlsx'
# dfcust = pd.read_excel(yfile, sheet_name='고객정보')
# dfpeop = pd.read_excel(yfile, sheet_name='직원정보')
# dfregi = pd.read_excel(yfile, sheet_name='등록정보')
# dfpres = pd.read_excel(yfile, sheet_name='예약정보')
# dfwork = pd.read_excel(yfile, sheet_name='사용정보')
# dfgood = pd.read_excel(yfile, sheet_name='상품정보')
# dfmore = pd.read_excel(yfile, sheet_name='수당정보')
# dfschA = pd.read_excel(yfile, sheet_name='근무표A')
# dfschB = pd.read_excel(yfile, sheet_name='근무표B')
# dfschC = pd.read_excel(yfile, sheet_name='근무표C')

ysdtnew = ''
yjscust = yjspeop = yjsregi = yjswork = yjspres = yjsgood = yjsmore = yjsschA = yjsschB = yjsschC = yjspay = ''
ydfwork = ydfpeop = ydfmore = pd.DataFrame()
def yfqrydb():
    global ysdtnew
    global yjscust, yjspeop, yjsregi, yjswork, yjspres, yjsgood, yjsmore, yjsschA, yjsschB, yjsschC, yjspay
    global ydfwork, ydfpeop, ydfmore

    # ydbfile = r'E:\yangdbpila\ydfpila.db'
    # ysdtnew = time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(ydbfile)))
    # print('Netdt, Olddt : ', ysdtnew, ysdtnew)


    # time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getmtime(ydbfile)))
    yconnpila = sqlite3.connect(ydbfile)
    # dfcust.to_sql('tbcust', yconnpila, if_exists='replace', index=False)
    # dfpeop.to_sql('tbpeop', yconnpila, if_exists='replace', index=False)
    # dfregi.to_sql('tbregi', yconnpila, if_exists='replace', index=False)
    # dfwork.to_sql('tbwork', yconnpila, if_exists='replace', index=False)
    # dfpres.to_sql('tbpres', yconnpila, if_exists='replace', index=False)

    # dfgood.to_sql('tbgood', yconnpila, if_exists='replace', index=False)
    # dfmore.to_sql('tbmore', yconnpila, if_exists='replace', index=False)

    # dfschA.to_sql('tbschA', yconnpila, if_exists='replace', index=False)
    # dfschB.to_sql('tbschB', yconnpila, if_exists='replace', index=False)
    # dfschC.to_sql('tbschC', yconnpila, if_exists='replace', index=False)
    # yconnpila.commit()
    ydfcust = pd.read_sql('select * from tbcust order by 시작날짜 desc', yconnpila)
    ydfpeop = pd.read_sql('select * from tbpeop', yconnpila)
    ydfregi = pd.read_sql('select * from tbregi order by 등록일자 desc', yconnpila)
    ydfwork = pd.read_sql('select * from tbwork order by 사용일자 desc', yconnpila)
    ydfpres = pd.read_sql('select * from tbpres order by 예약일자 desc', yconnpila)
    ydfgood = pd.read_sql('select * from tbgood', yconnpila)
    ydfmore = pd.read_sql('select * from tbmore', yconnpila)
    ydfschA = pd.read_sql('select * from tbschA', yconnpila)
    ydfschB = pd.read_sql('select * from tbschB', yconnpila)
    ydfschC = pd.read_sql('select * from tbschC', yconnpila)
    ydfpay = pd.read_sql('select * from tbpay', yconnpila)
    yconnpila.close()

    ysdtnew = time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(ydbfile)))
    # print('Netdt, Olddt : ', ysdtnew, ysdtnew)
    print(ysdtnew, ydfcust.shape, ydfpeop.shape, ydfregi.shape, ydfwork.shape, ydfpres.shape, ydfgood.shape, ydfmore.shape, ydfschA.shape, ydfschB.shape, ydfschC.shape, ydfpay.shape)

    # 고객정보에 등록정보 사용정보 더하고 남은횟수 계산
    ydfregigrp = ydfregi.groupby(['고객이름'])['등록비'].agg(['sum', 'count'])
    ydfregigrp.columns = ['등록비총합', '등록횟수']
    ydfregigrpmrg = ydfcust.merge(ydfregigrp, on=['고객이름'], how='left')
    ydfregigrp2 = ydfregi.groupby(['고객이름'])['상품횟수'].agg(['sum'])
    ydfregigrp2.columns = ['상품총횟수']
    ydfregigrpmrg2 = ydfregigrpmrg.merge(ydfregigrp2, on=['고객이름'], how='left')
    ydfworkgrp = ydfwork.groupby(['고객이름'])['사용시간'].agg(['sum', 'count'])
    ydfworkgrp.columns = ['사용총시간', '사용횟수']
    ydfworkgrpmrg = ydfregigrpmrg2.merge(ydfworkgrp, on=['고객이름'], how='left')
    ydfworkgrpmrg['남은횟수'] = ydfworkgrpmrg['상품총횟수'] - ydfworkgrpmrg['사용총시간']

    

    # 출력물 구하기
    yjscust = ydfworkgrpmrg.to_json(orient='split')
    yjspeop = ydfpeop.to_json(orient='split')
    yjsregi = ydfregi.to_json(orient='split')
    yjswork = ydfwork.to_json(orient='split')
    yjspres = ydfpres.to_json(orient='split')
    yjsgood = ydfgood.to_json(orient='split')
    yjsmore = ydfmore.to_json(orient='split')
    yjsschA = ydfschA.to_json(orient='split')
    yjsschB = ydfschB.to_json(orient='split')
    yjsschC = ydfschC.to_json(orient='split')
    yjspay = ydfpay.to_json(orient='split')
    

# yjspeoppivmrg = ''
def yfgetpay(ymonth):
    # global yjspeoppivmrg

    # 사용정보에 급여정보 계산하기
    ydfworkt = ydfwork[ydfwork['사용일자'].str.contains(ymonth)]
    ydfwork2 = ydfworkt.copy()
    ydfwork2['상품종류2'] = ydfwork2['상품종류'].str[:2]
    ydfwork2['상품종류2'] = ydfwork2['상품종류2'].str.replace('개인|비기|기본', '일반', regex=True)
    ydfwork2['상품종류2'] = ydfwork2['상품종류2'] + ydfwork2['내외']
    ydfwork2piv = ydfwork2.pivot_table(values='사용시간', index='직원이름', columns='상품종류2', aggfunc='sum')
    ydfpeoppiv = ydfpeop[['직원이름', '센터', '직급']].merge(ydfwork2piv, on=['직원이름'], how='left')
    ydfpeoppiv['총일한시간'] = ydfpeoppiv.sum(axis=1)
    ydfpeoppiv['120초과'] = np.where(ydfpeoppiv['총일한시간'] > 120, ydfpeoppiv['총일한시간'] - 120, 0)
    ydfpeoppiv['100초과'] = np.where((ydfpeoppiv['총일한시간'] > 100) & (ydfpeoppiv['총일한시간'] <= 120), ydfpeoppiv['총일한시간'] - 100, 0)

    ydfpeoppivmrg = ydfpeoppiv.merge(ydfmore, on=['센터', '직급'], how='left').fillna(0)
    ydfpeoppivmrg['월급여'] = ydfpeoppivmrg['기본급'] \
                           + ydfpeoppivmrg['일반내'] * ydfpeoppivmrg['내일반'] + ydfpeoppivmrg['일반외'] * ydfpeoppivmrg['외일반'] \
                           + ydfpeoppivmrg['듀엣내'] * ydfpeoppivmrg['내듀엣'] + ydfpeoppivmrg['듀엣외'] * ydfpeoppivmrg['외듀엣'] \
                           + ydfpeoppivmrg['그룹내'] * ydfpeoppivmrg['내그룹'] + ydfpeoppivmrg['그룹외'] * ydfpeoppivmrg['외그룹'] \
                           + ydfpeoppivmrg['100초과'] * ydfpeoppivmrg['초과100'] + ydfpeoppivmrg['120초과'] * ydfpeoppivmrg['초과120']
    ydfpeoppivmrg['년월'] = ymonth

    # yjspeoppivmrg = ydfpeoppivmrg.to_json(orient='split')

    yconnpila = sqlite3.connect(ydbfile)
    ydfpeoppivmrg.to_sql('tbpay', yconnpila, if_exists='append', index=False)
    yconnpila.commit()
    yconnpila.close()
    print('yfgetpay', ymonth, ydfwork2.shape, ydfpeoppivmrg.shape)


@app.route('/')
def main():
    return render_template('main_pila.html')

@app.route('/admin')
def admin():
    return render_template('main_pila_admin.html')

@app.route('/AServer')
def AServer():
    return  json.dumps([ysdtnew, datetime.now().strftime('%m-%d %H:%M:%S')])

@app.route('/ACUST')
def ACUST():
    return yjscust
@app.route('/APEOP')
def APEOP():
    return yjspeop
@app.route('/AREGI')
def AREGI():
    return yjsregi
@app.route('/AWORK')
def AWORK():
    return yjswork
@app.route('/APRES')
def APRES():
    return yjspres

@app.route('/AGOOD')
def AGOOD():
    return yjsgood
@app.route('/AMORE')
def AMORE():
    return yjsmore

@app.route('/ASCHA')
def ASCHA():
    return yjsschA
@app.route('/ASCHB')
def ASCHB():
    return yjsschB
@app.route('/ASCHC')
def ASCHC():
    return yjsschC
@app.route('/APAY')
def APAY():
    return yjspay


if __name__ == '__main__':
    ydbfile = r'E:\yangdbpila\ydfpila.db'

    yfqrydb()

    ysched = BackgroundScheduler()
    ysched.add_job(yfqrydb, 'cron', minute='*/10')
    ysched.add_job(yfgetpay, 'cron', day='1', args=[datetime.now().strftime('%Y-%m')])
    ysched.start()

    app.run()
    # app.run(host='0.0.0.0', port=5000)
