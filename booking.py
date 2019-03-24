from flask import Flask , render_template, url_for, request, session, redirect,Markup
from flask_pymongo import PyMongo
import random

app =Flask(__name__)
app.config['MONGO_DBNAME'] = 'software'
app.config['MONGO_URI']= 'mongodb://saravanan:saravanan1@ds161315.mlab.com:61315/software'

mongo = PyMongo(app)


pnr=mongo.db.pnr

@app.route('/')
def index():
    
    return render_template('login.html',methods=['POST','GET'])


@app.route('/login',methods=['POST','GET'])
def login():
    users=mongo.db.users
    login_user=users.find_one({'name':request.form['username']})
    
    if login_user:
        if request.form['password']==login_user['password']:
            session['user']=request.form['username']
            return render_template('home.html',user=session['user'])
    return 'invalid username or password'   


@app.route('/reg', methods =['POST','GET'])
def reg():
    return render_template('reg.html')


@app.route('/register', methods =['POST','GET'])
def register():
    if request.method=='POST':
        users=mongo.db.users
        existing_user =users.find_one({'name':request.form['username']})
        
        if existing_user is None:
            users.insert({'name':request.form['username'],'password':request.form['pass']})
            session['user']=request.form['username']
            return render_template('home.html',user=session['user'])
        return 'the username is already exists!'
    return render_template('reg.html')




@app.route('/book_unres',methods=['POST','GET'])
def book_unres():
    
    return render_template('unreserved.html')



@app.route('/faq',methods=['POST','GET'])
def faq():
    
    return render_template('faq.html')



@app.route('/book_plat',methods=['POST','GET'])
def book_plat():
    
    return render_template('platform.html')



@app.route('/berth_calc',methods=['POST','GET'])
def berth_calc():
    
    return render_template('berth.html')


@app.route('/book',methods=['POST','GET'])
def book():
    return render_template('book.html')


@app.route('/book_res',methods=['POST','GET'])

def book_res():
    if request.method=='POST':
        tickets=mongo.db.tickets
        pnr_number=pnr.find_one({})
        pnrnum=int(pnr_number['pnr'])
        tickets.insert({'user':session['user'],'pnr':pnrnum,'from':request.form['fromstation'],'to':request.form['tostation'], 'date' : request.form['ticketdate'] ,\
                        'p1n':request.form['pn1'],'p2n':request.form['pn2'],'p3n':request.form['pn3'],'p4n':request.form['pn4'],'p5n':request.form['pn5'],'p6n':request.form['pn6'] })
    pnrnum=int(pnrnum)+1
    pnr.delete_one({})
    pnr.insert({'pnr':pnrnum})
    return render_template('home.html',user=session['user'])


    
@app.route('/enquiry',methods=['POST','GET'])
def enquiry():
    return render_template('enquiry.html',enquiry_output="Enter Train number or Station name")    
    
delays=['delayed by 1 minute','delayed by 2 minutes','delayed by 3 minutes','delayed by 4 minutes','delayed by 5 minutes','delayed by 10 minutes','delayed by 15 minutes','delayed by 20 minutes','delayed by 25 minutes','delayed by 30 minutes','delayed by 35 minutes','ahead by 1 minute ','ahead by 2 minutes','ahead by 3 minutes','ahead by 4 minutes','ahead by 5 minutes']   
trains=list(range(12601,12630))


@app.route('/enquiry_train_no',methods=['POST','GET'])
def enquiry_train_no():
    if request.form['train_no']!='':
        req_train=request.form['train_no']
    else:
        req_train=0
    if int(req_train) in trains :
        return render_template('enquiry.html',enquiry_output=delays[random.randrange(16)])
    else:
        return render_template('enquiry.html',enquiry_ouput='Invalid train number')



station_delays={"chennai": "<br>Train 12601 delayed by 3 minutes<br> Train 12602 delayed by 4 minutes<br> Train 12603 delayed by 5 minutes<br> Train 12604 delayed by 30 minutes<br> Train 12605 delayed by 3 minutes<br> ",\
               "madurai": "<br> Train 12606 is on time <br> Train 12607  ahead by 7 minutes<br> Train 12608  delayed by 11 minutes<br> Train 12609 delayed by 14 minutes<br> Train 12610 ahead by 2 Minutes<br> Train 12611 is on time<br>",\
               "coimbatore":"<br>Train 12612 delayed by 5 minutes<br> Train 12613 delayed by 11 minutes<br> Train 12614 ahead by 7 minutes<br> Train 12615 is on time <br> Train 12616 delayed by 3 minutes<br> Train 12617 delayed by 4 minutes<br> ",\
               "bangalore":"<br>Train 12618 delayed by 5 minutes<br> Train 12619 delayed by 30 minutes<br> Train 12620 delayed by 3 minutes<br> Train 12621 is on time <br> Train 12622 ahead by 7 minutes<br> Train 12623 delayed by 11 minutes<br>",\
               "mumbai":"<br>Train 12624 delayed by 14 minutes<br> Train 12625 ahead by 2 Minutes<br> Train 12626 is on time<br> Train 12627 delayed by 5 minutes<br> rain 12628 delayed by 11 minut<br> Train 12629 ahead by 7 minutes<br> Train 12630 is on time <br>"}


@app.route('/enquiry_station_single',methods=['POST','GET'])
def enquiry_station_single():
    return render_template('enquiry.html',enquiry_output=Markup(station_delays[request.form['station']]))
    
  
@app.route('/profile',methods=['POST','GET'])
def profile():
    tix=''
    tickets=mongo.db.tickets
    num_of_entries = tickets.find({'user':session['user']}).count()
    for i in range(num_of_entries):
        buffer = tickets.find_one({'user':session['user']})
        tickets.delete_one({'user':session['user']})
        #print(buffer)
        tix=tix + '<tr><td> ' + str(buffer['pnr'])+ '</td><td> '+ str(buffer['from'])+ '</td><td> '+ str(buffer['to']) + '</td></tr>' 
        tickets.insert_one(buffer)
    
    return render_template('profile.html',name=session['user'],tickets=Markup(tix))

if __name__ =='__main__':
    app.secret_key='mysecret'
    app.run(debug=True)      