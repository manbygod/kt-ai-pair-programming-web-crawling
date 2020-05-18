from flask import Flask, request, render_template, session, redirect
from tools import db, crawl, datetime, words, download

app = Flask(__name__, static_folder="static", template_folder="templates")
app.env = 'development'
app.debug = True
app.secret_key = 'alkfa;das;lkfdja;sdkflj' #서버에서 session을 사용하려면 반드시 필요한 임의의 키

db_tool = db.DBTool()
crawl_tool = crawl.CrawlTool()
words_tool = words.WordsTool()

@app.route('/')
def index():
    return render_template("index.html", user = session.get('user'))

@app.route('/login', methods=['get', 'post'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html', isNameExisted=True)
    
    user = db_tool.selectUserName(request.form.get('userid'))
    
    if user is None:
        return render_template('login.html', msg="회원가입을 해주십시오", isNameExisted=False)  
    
    user = db_tool.selectUser(request.form.get('userid'), \
                    request.form.get('password') \
                )
    if user:
        session['user'] = user # session은 비어있는 딕셔너리와 같은 type으로 개발자가 임으로 key와 value를 지정 
        return redirect('/')
    else:
        return render_template('login.html', msg="패스워드 정보를 확인하세요", isNameExisted=True)  

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

@app.route('/join', methods=['get', 'post'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    
    user = db_tool.selectUserName(request.form.get('userid'))
    
    if user:
        return render_template('join.html', msg="이미 회원이십니다.")
    
    db_tool.insertUser(request.form.get('userid'), \
                       request.form.get('profile'), \
                       request.form.get('password') \
                    )
    
    return redirect('/')

@app.route('/withdrawal')
def withdrawal():
    user = session.get('user')
    
    if user:
        db_tool.deleteUser(user.get('name'))
        session.pop('user')
        
    return redirect('/')

@app.route('/news/ranking')
def news():
    
    date = request.args.get('date')
    if date is None:
        date = datetime.getToday('%Y%m%d')
    
    date = datetime.validate(date, "%Y%m%d")
    
    if date is None:
        return "날짜 입력 방식이 잘못 되었습니다.(YYYYMMDD)"
    news = crawl_tool.getDaumNews(date)
    
    # print(news)
    return render_template('news.html', news=news)

@app.route('/news/reply')
def newsReply():
    
    url = request.args.get('url')
    
    reply_count = request.args.get('reply_count')
    if reply_count is None:
        reply_count = '0'
    
    replys = crawl_tool.getReplyOfNews(url, reply_count)
    
    print(replys)
    
    return replys
    
    

@app.route('/news/words')
def wordcount():
    url = request.args.get('url')
    soup = crawl_tool.getTextNews(url)
    word_tup_list = words_tool.getWordCount(soup)
    
    return render_template('word_count.html', words=word_tup_list) 

@app.route('/downloads', methods=['get', 'post'])
def downloads():
    
    if request.method == 'GET':
        return render_template("download.html")
    
    keyword = request.form.get('keyword')
    
    return redirect(f'/downloads/{keyword}')

@app.route('/downloads/<keyword>')
def downloadImg(keyword):
    
    binary_list, link_list = crawl_tool.getGoogleImages(keyword)
    download.downloadImg(keyword, binary_list, link_list)
    
    return render_template("download.html", goo_img_links=link_list)

app.run()