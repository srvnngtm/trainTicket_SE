from flask import Flask , render_template, url_for, request, session, redirect,Markup
from flask_pymongo import PyMongo
import random

app =Flask(__name__)
app.config['MONGO_DBNAME'] = 'software'
app.config['MONGO_URI']= 'mongodb://saravanan:saravanan1@ds161315.mlab.com:61315/software'

mongo = PyMongo(app)

@app.route('/')
def index():
    
    return render_template('home.html',methods=['POST','GET'])



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
        tickets.insert({'from':request.form['fromstation'],'to':request.form['tostation'], 'date' : request.form['ticketdate'] ,\
                        'p1n':request.form['pn1'],'p2n':request.form['pn2'],'p3n':request.form['pn3'],'p4n':request.form['pn4'],'p5n':request.form['pn5'],'p6n':request.form['pn6'] })
    return redirect('/')


    
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
    
  


if __name__ =='__main__':

    app.run(debug=True)      