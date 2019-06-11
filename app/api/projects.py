from flask import jsonify, request, send_file, url_for, current_app
from io import BytesIO
from app import db
from app.models import Project, User
from app.api import api
from app.api.auth import token_auth
from app.api.errors import badRequest, errorResponse
from flask_login import current_user
from werkzeug.utils import secure_filename
from datetime import datetime


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
        project_data['date_created'] = project.date_created
        project_data['pdf_page_count'] = project.pdf_page_count
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
    project_data['supervisor'] = project.supervisor
    project_data['tags'] = project.tags
    project_data['filename'] = project.filename
    project_data['size'] = len(project.file_data)
    project_data['date_created'] = project.date_created

    return jsonify(project_data)



@api.route('/projects/upload', methods=['POST'])
#@token_auth.login_required
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
        
        try:
            date_in_req = datetime.strptime(request.form.get('date_created'), '%Y-%m-%d')
        except:
            return badRequest('wrong date format. expected "yyyy-mm-dd" in date_created field')
        
        filename = secure_filename(file.filename)   
        new_project = Project()
        try:
            new_project.owner =  current_user.id
            new_project.authors = request.form.get('authors')
            new_project.title = request.form.get('project_title')
            new_project.supervisor = request.form.get('supervisor')
            new_project.tags = request.form.get('tags')
            new_project.date_created = date_in_req
            new_project.hashFilename(filename)
            new_project.file_data = file.read()
            new_project.pdf_page_count = request.form.get('pdf_page_count')
            db.session.add(new_project)
            db.session.commit()
            return jsonify('upload success'), 201
        except:
            return jsonify({"message" : "its empty"})
    
    return errorResponse(415, 'upload a .pdf file!')
    

@api.route('/projects/download/<string:filename>')
#@token_auth.login_required
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
        project_data['supervisor'] = project.supervisor
        project_data['tags'] = project.tags
        project_data['filename'] = project.filename
        project_data['size'] = len(project.file_data)
        project_data['date_created'] = project.date_created
        project_data['pdf_page_count'] = project.pdf_page_count
       
        output.append(project_data)
        
    if output == []:
        return jsonify({'no match found'})

    return jsonify(output)


@api.route('/projects=/<string:filename>', methods=['DELETE'])
@token_auth.login_required
def deleteProject(filename):
    project = Project.query.filter_by(filename=filename).first()
    
    if project.owner != current_user.id:
        return errorResponse(401, 'action not allowed for this user')

    if project is None:
        return errorResponse(404, 'resource does not exist')
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message':'delete success'})
