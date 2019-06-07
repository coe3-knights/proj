from flask import jsonify, request, send_file, url_for, current_app
from io import BytesIO
from app import db
from app.models import Project, User
from app.api import api
from app.api.auth import token_auth
from app.api.errors import badRequest, errorResponse
from flask_login import current_user
from werkzeug.utils import secure_filename


@api.route('/projects', methods=['GET'])
def explore():
    projects = Project.query.order_by(Project.submit_date.desc()).all()

    if projects is None:
        return jsonify({'message' : 'No project uploaded yet!'})

    output = []
    for project in projects:
        project_data = {}
        project_data['title'] = project.title
        project_data['authors'] = project.authors
        project_data['filename'] = project.filename
        project_data['size'] = len(project.file_data)
        project_data['submit_date'] = project.submit_date
        output.append(project_data)

    return jsonify(output)    
       


@api.route('/projects/<string:filename>')
def getProjectInfo(filename):
    project = Project.query.filter_by(filename=filename).first()

    if project is None:
        return errorResponse(404, 'resource does not exist')

    project_data = {}
    project_data['title'] = project.title
    project_data['authors'] = project.authors
    project_data['filename'] = project.filename
    project_data['size'] = len(project.file_data)
    project_data['submit_date'] = project.submit_date

    return jsonify(project_data)



@api.route('/projects/upload', methods=['POST'])
@token_auth.login_required
def upload():
    if 'input_file' not in request.files:
        return badRequest('no input file')
    file = request.files['input_file']
    
    if Project.allowed_file(file.filename):

        errors = []
        for field in ['project_title', 'authors']:
            if request.form.get(field) is None:
                errors.append(f"{field} field missing in request") 
        if errors != []:
            return badRequest(errors)
        
        filename = secure_filename(file.filename)   
        new_project = Project()
        new_project.owner =  current_user.id
        new_project.authors = request.form.get('authors')
        new_project.title = request.form.get('project_title')
        new_project.hashFilename(filename)
        new_project.file_data = file.read()
        db.session.add(new_project)
        db.session.commit()
        return jsonify('upload success'), 201
    
    return errorResponse(415, 'upload a .pdf file!')
    

@api.route('/projects/download/<string:filename>')
@token_auth.login_required
def download(filename):
    project = Project.query.filter_by(filename=filename).first()

    if project is None:
        return errorResponse(404, 'resource does not exist')

    return send_file(BytesIO(project.file_data), mimetype='application/pdf', attachment_filename=project.title+'.pdf', as_attachment=True)

@api.route('/projects/search')
def search():
    q = request.args.get('q')
    projects = Project.query.whoosh_search(q).all()
    users = User.query.whoosh_search(q).all()
  
    for user in users:
        for project in user.projects:
            projects.append(project)
            
    if projects is None:
         return jsonify({'message' : 'No project uploaded yet!'})

    output = []
    for project in projects:
        project_data = {}
        project_data['title'] = project.title
        project_data['authors'] = project.authors
        project_data['filename'] = project.filename
        project_data['size'] = len(project.file_data)
        project_data['submit_date'] = project.submit_date
        output.append(project_data)

    return jsonify(output)


@api.route('/projects=/<string:filename>', methods=['DELETE'])
@token_auth.login_required
def deleteProject(filename):
    project = Project.query.filter_by(filename=filename).first()

    if project is None:
        return errorResponse(404, 'resource does not exist')
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message':'delete success'})
