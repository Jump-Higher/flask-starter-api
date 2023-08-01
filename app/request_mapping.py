def create_user(json_body):
    data = {
        "name": json_body['name'],
        "username": json_body['username'],
        "password": json_body['password'],
        "email": json_body['email']
    }
    return data

def update_user(json_body):
    data = {
        "name": json_body['name'],
        "username": json_body['username'],
        "password": json_body['password'],
        "email": json_body['email'],
        "address" : json_body['address'],
        "rt" : json_body['rt'],
        "rw" : json_body['rw'],
        "kelurahan_desa" : json_body['kelurahan_desa'],
        "kecamatan" : json_body['kecamatan']
    }
    return data
