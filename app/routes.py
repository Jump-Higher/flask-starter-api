from app import app
from app.controllers import user, auth, roles, send
 
app.route('/register2',methods = ['POST'])(send.register2)

app.route('/user/<id>',methods = ['GET'])(user.read_user)
app.route('/user/update/<id>',methods = ['PUT'])(user.update_user)
app.route('/users',methods = ['GET'])(user.list_user)
app.route('/user/delete/<email>', methods=['DELETE'])(user.delete_user)

app.route('/user/update_role/<id>',methods = ['PATCH'])(user.update_user_role) 
app.route('/activate_user2/<activation_token>', methods=['PATCH'])(user.activate_user2)
app.route('/user/deactivate/<id>',methods = ['PATCH'])(user.deactivate_user)
   
app.route('/role/create', methods = ['POST'])(roles.create_role)
app.route('/role/update/<id>', methods = ['PUT'])(roles.edit_role)
app.route('/role/<id>', methods=['GET'])(roles.read_role)
app.route('/roles', methods=['GET'])(roles.roles)

#app.route('/role/delete', methods = ['DELETE'])(roles.bulk_delete_roles)
#app.route('/roles', methods = ['GET'])(roles.read_roles)

app.route('/login', methods=['POST'])(auth.login)

@app.route('/')
def home():
    return "WELCOME TO FLASK STARTER API"
