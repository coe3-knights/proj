from flask import g, jsonify, request, url_for, render_template
from app import db
from app.models import User, Project
from app.api import api, apib
from app.api.auth import token_auth,basic_auth
from app.api.errors import badRequest, errorResponse
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user
from app.api.email import sendPaswordRequest




@api.route('/login', methods=['GET', 'POST'])
def login():
      try:
          request.get_json()
      except:
          return badRequest('content-type must be json')

      login_data = request.get_json()
      if login_data == {}:
          return badRequest('no details provided')

      email = login_data.get('email')
      password = login_data.get('password')   
      user = User.query.filter_by(email=email).first()

      if not user:
           return badRequest('no user exists with such email')
              
      if check_password_hash(user.pwhash,password):
            token = str(user.generate_auth_token()) 
            login_user(user, remember=login_data.get('remember_me')) 
            return jsonify({'login' : 'User successfully logged in',
                            'token': token})  
      return badRequest('password is incorrect')
        


@api.route("/logout", methods=["POST"])
@token_auth.login_required
def logout():
  # we have to revoke the token or leave it like that to expire by itself
  logout_user()
  return jsonify({'message':'Logged out successfully'})


@api.route('/signup', methods=['POST'])
def createUser():
      try:
          request.get_json()
      except:
          return badRequest('content-type must be json')

      new_user = request.get_json()
      if new_user == {}:
          return badRequest('no details provided')
      
      if 'username' not in new_user or 'email' not in new_user or 'password' not in new_user:
          return badRequest('no username, password or email')

      if len(new_user['password']) < 1:
        return badRequest('password must be at least a characters long!')     
       
      username_object = User.query.filter_by(username=new_user['username']).first() 
      email_object = User.query.filter_by(email=new_user['email']).first()
       
      if email_object and username_object: 
         return badRequest('email address  and username already exists!')
      if username_object:
         return badRequest('username already exists!') 
      if email_object:  
         return badRequest('email address already used!')

      User(new_user['firstname'], new_user['lastname'], new_user['username'], new_user['email'], new_user['password'], new_user['institution'], new_user['department']).save()
      
      return jsonify({'message' : 'User Registered'}), 201
  
    


@api.route('/student/<string:username>', methods=['GET','POST'])
@token_auth.login_required
def updateUser(username):
    student = User.query.filter_by(username=username).first()
    if student is None:
         return badRequest('user does not exist')

    if request.method == 'POST':
            try:
                request.get_json() 
            except:
                return badRequest('content-type must be json')
            
            data = request.get_json()
            if data == {}:
                return badRequest('no details provided')

            if current_user.username != student.username:
                return errorResponse(401, 'You cannot perform this action')

            if data:
              for key in data:
                setattr(student, key, data[key])
                 
              db.session.commit()
            return jsonify({'message' : 'user updated'})   
    elif request.method == 'GET': 
         return jsonify({'username' : student.username,
                         'email' : student.email
                        })      

           

             

@api.route('/student/<string:username>', methods=['DELETE'])
@token_auth.login_required
def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    if user != g.current_user:
       return errorResponse(401, 'You cannot perform this action')

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'account deleted'})




@api.route('/student/request_password_reset', methods=['POST'])
def requestPasswordReset():
    try:
        request.get_json()
    except:
        return badRequest('json object not found in request')

    req_data = request.get_json()
    if req_data == {}:
        return badRequest('no details provided') 

    if 'email' not in req_data:
        return badRequest('user email required')
    user = User.query.filter_by(email=req_data['email']).first()
    if user:
      try:
         sendPaswordRequest(user)
         return jsonify({'message' : 'please check your email'})
      except:
         return errorResponse(502, 'mail not sent')
    return badRequest('email not registered')


@api.route('/student/reset_password/<token>', methods=['GET','POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return badRequest('user already logged in')
    user = User.verifyPasswordResetToken(token)
    if not user:
        return badRequest('invalid or expired token')
    try:
        request.get_json('')
    except:
        return badRequest('no details provided') 

    new_password = request.get_json('new_password')
    if len(new_password) < 1:
        return badRequest('password must be at least a characters long!')

    user.setResetPassword(new_password)
    db.session.commit()
    return jsonify({'message', 'reset success'}), 200




@api.route('/student/<string:username>/projects', methods=['GET'])
@token_auth.login_required
def getUserUploads(username):
      student = User.query.filter_by(username=username).first()
      if student is None:
          return badRequest('user does not exist') 

      if g.current_user.id != student.id:
          return errorResponse(401, 'You cannot perform this action')

      #user = User.query.filter_by(username=username).first_or_404()
      projects = Project.query.filter_by(author=g.current_user)\
          .order_by(Project.submit_date.desc())

      if projects is None:
        return jsonify({'message' : 'No project uploaded yet!'})

      output = []
      for project in projects:
        project_data = {}
        project_data['title'] = project.title
        project_data['authors'] = project.authors
        project_data['filename'] = project.filename
        project_data['size'] = len(project.file_data)
        project_data['date_created'] = project.date_created
        project_data['pdf_page_count'] = project.pdf_page_count
        output.append(project_data)

      return jsonify(output)


@apib.route('/')
def index():
      return render_template('web.html')


