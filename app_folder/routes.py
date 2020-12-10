# from flask import current_app as app
# from . import db, mail
from app_folder import app
from app_folder import db,mail
from flask_login import login_required,login_user,UserMixin,current_user,logout_user
from flask_mail import Message
from flask import render_template, redirect, request, flash, url_for
from .forms import LoginForm,RegistrationForm, ForgetPasswordForm, NewPasswordForm,AvailableForm,EventForm,EmailConfimationForm,monthswitchForm
from .models import User,Appointment,Available
from .util import ts,split_time_ranges
import os
import secrets
import calendar
from datetime import datetime,timedelta,date,time
from flask import request
import functools
from flask_socketio import send, emit,join_room, leave_room
from app_folder import socketio
import time

@app.route('/')
def home():
    '''
    this function would direct user to home page 

    args:
       none
    return:
       go to the home page
    '''
    # if current_user.is_authenticated:
    #     return redirect('/meeting')
    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    this function allows user to login
    go to successful.html page if login in successfully
    otherwise stay at login page

    args:
        none  
    return:
        index.html or login.html with form object
    '''
    if current_user.is_authenticated:
        flash('you have logined')
        return  redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        login_user(user,remember=form.remember_me.data)
        return redirect('/meeting')  
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    this function allows user to register the account
    go to login page if register successfully
    otherwise stay at register page

    args:
        none
    return:
        redirect to login page or register.html and register form 
    '''
    if current_user.is_authenticated:
        flash('you have logined')
        return render_template("index.html")
    form = RegistrationForm()

    if form.validate_on_submit():
        
        # image=request.files['photo']
        
        # picture_path = os.path.join(app.root_path,'static/img',image.filename)
        # image.save(picture_path)
        # print(picture_path)
        user = User(username=form.username.data, email=form.email.data, mailconfirm=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! ')
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    '''
    this function allows user to logout

    args:
        none
    return:
        redirect to home page
    '''
    logout_user()
    return redirect('/')

@app.route('/forget_password', methods=["GET","POST"])
def forget():
    '''
    this function allow user apply to reset password if they
    forget

    args:
        none
    return:
        A reset link include token send to user's email 
    '''
    form=ForgetPasswordForm()
    if form.validate_on_submit():
        subject="Password reset requested"
        email=form.email.data
        token=ts.dumps(email,salt='recover-key')
        recover_url=url_for('reset_with_token',token=token,_external=True)
        html=render_template('email/recover.html',recover_url=recover_url)
        mail.send_message(subject=subject,
                          html=html,
                          recipients=[email]) #recipients need list type
        return render_template('forget.html',form=form,done=1)
    return render_template('forget.html',form=form,done=0)



@app.route('/email/<token>',methods=["GET","POST"])
def reset_with_token(token):
    '''
    this function certificate the token from user and allow user
    to reset their password 

    args:
        none
    return:
        redirect to login page 
    '''
    try:
        email = ts.loads(token, salt='recover-key')
    except:
        os.abort()
    form=NewPasswordForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=email).first()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("reset_with_token.html",form=form,email=email)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# below is for milestone3 
# calendar.html
# meeting.html
# seting.html
# editevent.html
''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@app.route('/setting',methods=["GET","POST"])
@login_required
def setting():
    '''
    this function it to let creater set available time, toggle Email confirmation 
    and delete account

    args:
        none

    return:
        redirect to setting or go to setting page with available form
    '''
    form = AvailableForm()
    form2= EmailConfimationForm()
    if form.validate_on_submit():
        start = form.start_time.data
        end =form.end_time.data 
        length=form.length.data
        available= Available.query.filter_by(user_id=current_user.id).first()
        if available is not None:
            available.start_time=start
            available.end_time=end
            available.meeting_length=length
        else:
            Newavailable = Available(start_time=start, end_time=end,user_id=current_user.id,meeting_length=length)
            db.session.add(Newavailable)
        db.session.commit()
        print("submit form")
        return redirect("/setting")
    elif form2.validate_on_submit() and form.end_time.errors[0]!='Invalid end time':
        print("submit form2",form2.confirm.data)
        current_user.mailconfirm= form2.confirm.data
        db.session.commit()
        return redirect("/setting")
    else:
        available= Available.query.filter_by(user_id=current_user.id).first()
        if available is not None:
            start_time=available.start_time.strftime('%H:%M')
            end_time=available.end_time.strftime('%H:%M')
        else:
            start_time=None
            end_time=None
        return render_template("setting.html",form=form,form2=form2,start_time=start_time,end_time=end_time)
    

@app.route('/delete',methods=["GET","POST"])
@login_required
def delete():
    '''
    this function is to delete account in database and log out.
    Also delete all info related to this user(available time,appoinment) in database.
    
    args: 
        None
        
    return:
        redirect to login in page
    '''
    if current_user:
        user = User.query.filter_by(username=current_user.username).first()
        available_list=[]
        appointment_list=[]
        appointment_list=Appointment.query.filter(Appointment.user_id ==user.id).all()
        available_list=Available.query.filter(Available.user_id ==user.id).all()
        logout_user()
        db.session.delete(user)
        for i in appointment_list:
            db.session.delete(i)
        for i in available_list:
            db.session.delete(i)
        db.session.commit()
        flash("Deleted successfully!")
        return redirect("/login")
        
@app.route('/meeting',methods=["GET","POST"])
@login_required
def meeting():
    '''
    this function is to show all appoinment info of creators

    args: 
        None
        
    return:
        meeting.html and appointment list
    '''

    page = request.args.get('page', 1, type=int)
    appointment_list=[]
    user = User.query.filter_by(username=current_user.username).first()
    appointment_list = Appointment.query.filter(Appointment.user_id ==user.id)\
                    .order_by(Appointment.Date.desc())\
                    .paginate(page=page, per_page=5)
    return render_template("meeting.html",appointment_list=appointment_list)
   

@app.route('/<username>',methods=["GET","POST"])
def username(username):
    '''
    this function is to view availability of creater by going to creator's username page

    args: 
        username

    return:
        calendar.html,calendar of current month,creator's name and list of days in this month.
    '''
    form=monthswitchForm()
    user = User.query.filter_by(username=username).first()
    if user:#found this creator in database, then show calendar 
        date = datetime.today()
        if form.year.data is not None:
            date=date.replace(year = int(form.year.data))
        calendar.setfirstweekday(firstweekday=6)
        content = calendar.monthcalendar(date.year, date.month)#calendar.month_abbr[date.month]
        if form.validate_on_submit and form.value.data:
            if(form.value.data=='13'):
                print(form.value.data)
                date=date.replace(year = date.year + 1 )
                print(date.year)
                form.value.data='1'
            elif(form.value.data=='0'):
                print(form.value.data)
                date=date.replace(year = date.year - 1 )
                print(form.value.data)
                form.value.data='12'
                print(date.year)
            print(form.value.data)
            date=date.replace(month=int(form.value.data))
        else:
            form.value.data=date.month
        form.year.data=date.strftime("%Y")
        content = calendar.monthcalendar(date.year, date.month)#calendar.month_abbr[date.month]
        return render_template('calendar.html',date=date, content=content,name=username,form=form)
    else: #otherwise back to the home page
        return redirect("/")

@app.route('/editevent',methods=["GET","POST"])
def editevent():
    '''
    this function is to let guests select the avilable time slot store to the appoinment table

    args: 
        None
        
    return:
        Event form,editevent.html and creator's name or redirect to calendar page
    '''
    form =EventForm()
    choices=[]
    Date =datetime(int(request.args.get('year')),int(request.args.get('month')),int(request.args.get('day'))).date()
    name=request.args.get('instructor')
    choices=[]
    user=User.query.filter_by(username=name).first()
    if user: #found creator
        print(user.id)
        avilablility=Available.query.filter(Available.user_id ==user.id).first()
        if avilablility:#found available time
            start = datetime.combine(Date,avilablility.start_time)
            end = datetime.combine(Date,avilablility.end_time)
            choices=split_time_ranges(start,end,avilablility.meeting_length*60)
            #going to check any reserved appointment and not show  in the chocies.
            Appointment_list = Appointment.query.filter(Appointment.Date==Date,Appointment.user_id==user.id).all()
            if Appointment_list:
                for i in Appointment_list: 
                    start_time=datetime.combine(Date,i.start_time)
                    end_time=datetime.combine(Date,i.end_time)
                    start_time=datetime.strftime(start_time,'%H:%M:%S')
                    end_time=datetime.strftime(end_time,'%H:%M:%S')
                    List1=[]
                    time_slot=start_time+" "+end_time
                    List1.append(time_slot)
                    List1.append(time_slot)
                    choices.remove(List1)
                    print("delete sucess")
            form.availabletime.choices=choices
        else:#not found avilable time
            choices.append(["None","None"])
            form.availabletime.choices=choices
    else:
        return redirect("/")#not found then return to main page
    if form.validate_on_submit():
        #edit event if found creator successfully
        Time = form.availabletime.data
        list1=Time.split(' ')
        start=list1[0]
        end=list1[1]
        start_time = datetime.strptime(start,'%H:%M:%S').time()
        end_time = datetime.strptime(end, '%H:%M:%S').time() 
        print("success")
        appointment = Appointment(name=form.name.data,Date=Date, start_time=start_time,end_time=end_time,description=form.description.data,user_id=user.id,email=form.email.data)
        db.session.add(appointment)
        db.session.commit()
        return redirect("/"+name)
    return render_template("editevent.html",form=form,name=name,Date=Date)
##################   

@app.route('/deleteRecord',methods=["GET","POST"])
@login_required
def deleteRecord():
    email = request.args.get('email')
    Date = request.args.get('date')
    start = request.args.get('start')
    end = request.args.get('end')
    start_time = datetime.strptime(start,'%H:%M:%S').time()
    end_time = datetime.strptime(end, '%H:%M:%S').time() 
    appointment = Appointment.query.filter_by(email=email,Date=Date,start_time=start_time,end_time=end_time).first()
    db.session.delete(appointment)
    db.session.commit()
    return redirect('/meeting')

@app.route('/roomlink/<emailaddress>', methods=["GET","POST"])
def roomlink(emailaddress):
    '''
    this function allow user apply to reset password if they
    forget

    args:
        none
    return:
        A reset link include token send to user's email 
    '''
    
    subject="room link"
    print(emailaddress)
    email=emailaddress
    token=ts.dumps(email,salt='room-key')
    room_url=url_for('chatlogin',token=token,_external=True)
    html=render_template('email/roomlink.html',room_url=room_url)
    mail.send_message(subject=subject,
                        html=html,
                        recipients=[email]) #recipients need list type
    return redirect('/meeting')

@app.route('/chatlogin', methods=["GET","POST"])
@login_required
def chatlogin():
        #return redirect(url_for('chat',username=username)) 
    return render_template('chatLogin.html')

@app.route('/chat', methods=["GET","POST"])
def chat():
    name = request.args.get('username')
    return render_template('chat.html',username=name)

@socketio.on('message')
def on_message(msg):
    """Broadcast messages"""
    name=msg['username']
    msg=msg['msg']
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"name":name,"msg": msg, "time_stamp": time_stamp},broadcast=True)
