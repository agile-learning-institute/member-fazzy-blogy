from api.models.blogmodels import User

def is_admin(user_id):
    user = User.query.get(user_id)
    return user.role == 'admin' if user else False