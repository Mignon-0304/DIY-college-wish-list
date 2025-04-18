from bs4 import BeautifulSoup
from flask import Flask, redirect, request, url_for
from urllib.error import *
from urllib.request import urlopen

app = Flask(__name__)


ACDM=['文學院','社會科學院','工學院','管理學院','電機資訊學院','生命科學院','創新設計學院','共同教育中心','理學院','醫學院','生物資源兼農學院','公共衛生學院','法律學院','國際學院','重點科技研究學院','進修推廣學院']
orders=['0','2','4', '6', '8','10','12','14','1','3','5','7', '9', '11','13','15']
Academies=[]
path = 'output.txt'
apartments=[]
get=[]
AAmounts=[0]
m=[0, 0, 0, 0]
Capital=[]
Name=[0]

@app.route('/')
def name():
  html = '''<form action='/academy', methods=['GET']>
  你的名字:<input type='text' name='name' required='required'><br><br>
  '''
  html+='''<input type='submit'></form>'''
  return html


@app.route('/academy')
def academy():
  m[0]=0
  m[1]=0
  m[2]=0
  if (m[3]==0):
    Name[0]= request.values.get('name')
    m[3]+=1
  html='''
  <h1>志願清單<h1>
  <h3><font size="2" face="微軟正黑體">學測快到了，目標要設得高才爬得遠，我們向台大看齊，來打造一份志願清單吧！<h3><br>'''
  html+='''  <form action='/apartment', methods=['GET']>'''
  html+='''
  <label for="academy" >想認識的學院:</label>
  <select id="academy" name='academy'>
  <option value="文學院"> 文學院 </option>
  <option value="社會科學院"> 社會科學院 </option>
  <option value="工學院"> 工學院 </option>
  <option value="管理學院"> 管理學院 </option>
  <option value="電機資訊學院"> 電機資訊學院 </option>
  <option value="生命科學院"> 生命科學院 </option>
  <option value="創新設計學院"> 創新設計學院 </option>
  <option value="共同教育中心"> 共同教育中心 </option>
  <option value="理學院"> 理學院 </option>>
  <option value="醫學院"> 醫學院 </option>
  <option value="生物資源兼農學院"> 生物資源兼農學院 </option>
  <option value="公共衛生學院"> 公共衛生學院 </option>
  <option value="法律學院"> 法律學院 </option
  <option value="國際學院"> 國際學院 </option>
  <option value="重點科技研究學院"> 重點科技研究學院 </option>
  <option value="進修推廣學院"> 進修推廣學院 </option>
  </select>'''

  html+='''<input type='submit'></form>'''

  return html

@app.route('/apartment', methods=['GET'])
def apartment():
  a = request.values.get('academy')
  for i in range(16):
    if(ACDM[i] == a) and (m[0] == 0):
      Academies.append(ACDM[i])
      m[0]+=1
  for i in range(16):
    if(a == ACDM[i]):
      order = orders[i]

  URL="https://www.ntu.edu.tw/academics/academics_list.html"
  html = urlopen(URL).read().decode(encoding='utf-8')
  soup = BeautifulSoup(html, "html.parser")
  style = "order:{}".format(order)
  text = soup.find('article', style=style)
  APMa = text.findAll('a')
  html = '''
  <h2><font color="#4682B4">以下為此學院的各學系，請挑選學系排入志願序：</font></h2>
  <h3>點選連結了解該系詳細資訊！(另開視窗)</h3>
  '''
  html +='''<form action='/list', methods=['GET']>'''
  for i in APMa:
    name = i.get_text()
    href = i.get('href')
    html += '''
    <input type="checkbox" name="check" value={}><a href={} target="_blank"><font size='3'> {} </font></a><br><br>'''.format(name,href,name)
  html +='''
  <p>選好了嗎？</p>
  <input type='submit'></form>
  '''

  return html



@app.route('/list', methods=['GET'])
def list():
  get=request.values.getlist('check')
  if(m[1]==0):
    AAmounts.append(len(get))
    m[1]+=1
  for i in get:
    if i not in apartments:
      apartments.append(i)

  b=len(apartments)-len(get)
  aca_now=Academies[(len(Academies)-1)]

  data = ''
  with open("output.txt",'r') as f:
    data = f.readlines()
  f = open(path, 'a')
  s = aca_now + '\n'
  if (m[2]==0):
    print(aca_now, file=f)
    m[2]+=1
  for i in  range(len(get)):
    s = apartments[b+i] + '\n'
    if s not in data:
      print(apartments[b+i].strip(), file=f)
  f.close()

  html='''
  <h1>志願清單（草稿）</h1>'''

  html +='<ol>'
  p=0
  n=1
  for i in range(len(apartments)+len(Academies)):
    with open("output.txt",'r') as f:
        data = f.readlines()[i]
    if(i == p):
      html += '</ol>'
      html += '<h3>'
      html += data
      html += '</h3>'
      p += AAmounts[n]+1
      n+=1
      html += '<ol>'
    else:
      html +='<li>'
      html += data
      html += '<br>'
  html +="</ol><br><br>"

  html +='''
  <p>想要更多?按這裡返回學院選單：</p>
  <a href="/academy">選擇學院</a><br>
  <p>改變心意了?沒問題!按這裡清除所有志願並重新選擇：</p>
  <a href="/delete">一鍵清除</a><br>
  <p>我已經確定我的志願清單了！</p>
  <a href="/sure">前往最終頁面</a>
  '''
  return html

@app.route('/delete')
def delete():
  html ='''
  是否清空已選擇的志願?
  <form action='/realdelete', methods=['GET']>
  <label for="radio"><br>
  <input type="radio" name='delete' id="radio" value="是">是</label><br>
  <label for="radio"><br>
  <input type="radio" name='delete' id="radio" value="否">否(返回上頁)</label><br>
  '''
  html +='''<input type='submit'></form>'''
  return html

@app.route('/realdelete', methods=['GET'])
def realdelete():
  ans = request.values.get('delete')
  if(ans == "是"):
    f = open('output.txt', 'w')
    f.truncate(0)
    Academies.clear()
    apartments.clear()
    AAmounts.clear()
    AAmounts.append(0)
    return redirect(url_for('academy'))
  else:
    return redirect(url_for('list'))


@app.route('/sure', methods=['GET'])
def sure():
  html='''
  <h1><u>{}</u>的志願清單</h1>'''.format(Name[0])

  html +='<ol>'
  p=0
  n=1
  for i in range(len(apartments)+len(Academies)):
    with open("output.txt",'r') as f:
        data = f.readlines()[i]
    if(i == p):
      html += '</ol>'
      html += '<h3>'
      html += data
      html += '</h3>'
      p += AAmounts[n]+1
      n+=1
      html += '<ol>'
    else:
      html +='<li>'
      html += data
      html += '<br>'
  html +="</ol><br><br>"
  html += '''
  <img src="https://i.pinimg.com/564x/f8/81/e5/f881e56ef0c07b51d06dd10b01a77329.jpg" width="40%">
  <p><font color="#FA8072"><i>{}加油！希望我們都能達到我們心中的理想！</i></font></p>
  '''.format(Name[0])

  return html



with open("output.txt", "r+") as f:
  f.truncate(0)
Academies.clear()
apartments.clear()
AAmounts.clear()
AAmounts.append(0)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
