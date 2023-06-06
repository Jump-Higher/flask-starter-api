from app import app
from app.controllers import user, auth

app.route('/user/create',methods = ['POST'])(user.create_user)
app.route('/user/<id>',methods = ['GET'])(user.read_user)
app.route('/user/update/<id>',methods = ['PUT'])(user.update_user)
app.route('/user/delete/<id>',methods = ['DELETE'])(user.delete_user)
app.route('/users',methods = ['GET'])(user.list_user)

app.route('/login', methods=['POST'])(auth.login)

