from app import app
from app.controllers import user, auth, roles, send

app.route('/user/create',methods = ['POST'])(user.create_user)
app.route('/user/create',methods = ['GET'])(user.get_create_user)
app.route('/user/<id>',methods = ['GET'])(user.read_user)
app.route('/user/update/<id>',methods = ['PUT'])(user.update_user)
app.route('/user/delete/<id>',methods = ['PATCH'])(user.delete_user)
app.route('/users',methods = ['GET'])(user.list_user)
app.route('/user/update_role/<id>',methods = ['PATCH'])(user.update_user_role)
app.route('/send', methods=['POST'])(send.send_email)

app.route('/role/create', methods = ['POST'])(roles.create_role)
app.route('/roles', methods = ['GET'])(roles.read_roles)
app.route('/role/update/<id>', methods = ['PUT'])(roles.edit_role)
app.route('/role/delete', methods = ['DELETE'])(roles.bulk_delete_roles)
app.route('/roles', methods=['GET'])(roles.list_role)

app.route('/login', methods=['POST'])(auth.login)

@app.route('/')
def home():
    return "WELCOME TO FLASK STARTER API"
