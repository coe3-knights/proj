from flask import jsonify, request, url_for
from app import db
from app.models import User, Project
from app.api import api
from app.api.auth import token_auth,basic_auth
from app.api.errors import badRequest, errorResponse
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user
from app.api.email import sendPaswordRequest




@api.route('/login', methods=['GET', 'POST'])
def login():
      try:
         login_data = request.get_json()
      except:
            return badRequest('no details provided')

      login_data = request.get_json()
      email = login_data.get('email')
      password = login_data.get('password')   
      user = User.query.filter_by(email=email).first()

      if not user:
           return badRequest('no user exists with such email')
              
      if check_password_hash(user.pwhash,password):
            token = user.generate_auth_token() 
            login_user(user, remember=login_data.get('remember_me')) 
            return jsonify({'login' : 'User successfully logged in',
        'token': token})  
      return jsonify({'message' : 'password is incorrect'}) 
        


@api.route("/logout", methods=["POST"])
def logout():
  # we have to revoke the token or leave it like that to expire by itself
  logout_user()
  return jsonify({'message':'Logged out successfully'})


@api.route('/signup', methods=['POST'])
def createUser():
      try:
         new_user = request.get_json() 
      except:
            return badRequest('no details provided')
      
      if 'username' not in new_user or 'email' not in new_user or 'password' not in new_user:
          return badRequest('no username, password or email')      
       
      username_object = User.query.filter_by(username=new_user['username']).first() 
      email_object = User.query.filter_by(email=new_user['email']).first()
       
      if email_object and username_object: 
         return badRequest('email address  and username already exists!')
      if username_object:
         return badRequest('username already exists!') 
      if email_object:  
         return badRequest('email address already used!')

      User(new_user['firstname'], new_user['lastname'], new_user['username'], new_user['email'], new_user['password'], new_user['institution'], new_user['department'], new_user['programme']).save()
      
      return jsonify({'message' : 'User Registered'}) 
  
    


@api.route('/student/<string:username>', methods=['GET','POST'])
@token_auth.login_required
def updateUser(username):
    student = User.query.filter_by(username=username).first()
    if student is None:
         return badRequest('user does not exist')

    if request.method == 'POST':
            try:
                data = request.get_json() 
            except:
                  return badRequest('no details provided') 

            if current_user.username != student.username:
                return errorResponse(403, 'You cannot perform this action')

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
    if user != current_user:
       return errorResponse(403, 'You cannot perform this action')

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'account deleted'})




@api.route('/student/request_password_reset', methods=['POST'])
def requestPasswordReset():
    try:
        req_data = request.get_json()
    except:
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
        new_password = request.get_json['new_password']
    except:
        return badRequest('no details provided') 

    user.setResetPassword(new_password)
    db.session.commit()
    return jsonify({'message', 'reset success'}), 200




@api.route('/student/<string:username>/projects', methods=['GET'])
@token_auth.login_required
def getUserUploads(username):
      student = User.query.filter_by(username=username).first()
      if student is None:
          return badRequest('user does not exist') 

      if current_user.username != student.username:
          return errorResponse(403, 'You cannot perform this action')

      user = User.query.filter_by(username=username).first_or_404()
      payload = Project.query.filter_by(author=user)\
          .order_by(Project.submit_date.desc())

      return jsonify(payload)