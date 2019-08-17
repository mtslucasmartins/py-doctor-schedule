from flask_restful import Resource, reqparse

from models.user import User

def parse_request():
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('fullname', help='This field cannot be blank', required=True)
    request_parser.add_argument('email', help='This field cannot be blank', required=True)
    request_parser.add_argument('cpf', help='This field cannot be blank', required=True)
    request_parser.add_argument('password', help='This field cannot be blank', required=True)
    return request_parser.parse_args()


def validate_signup(request_args):
    user_email = request_args.get('email')
    user_fullname = request_args.get('fullname')
    user_password = request_args.get('password')
    user_cpf = request_args.get('cpf')
   
    # valida email do usuário.
    if (user_email is None) or (user_email == ''):
        return (False, ({ 'error': 'error', 'error_description': 'Informe o seu Email.', 'field': 'email'}, 400))

    # verifica senha do usuario.
    if (user_password is None) or (user_password == '')  or (len(user_password) < 6):
        return (False, ({ 'error': 'error', 'error_description': 'Informe uma senha válida.', 'field': 'password'}, 400))

    # verifica nome do usuario.
    if (user_fullname is None) or (user_fullname == ''):
        return (False, ({ 'error': 'error', 'error_description': 'Informe o seu Nome Completo.', 'field': 'fullname'}, 400))
        
    # verifica nome do usuario.
    if (user_cpf is None) or (user_cpf == ''):
        return (False, ({ 'error': 'error', 'error_description': 'Informe o CPF.', 'field': 'cpf'}, 400))

    # verifica cpf do usuário.
    # elif User.check_cpf(user_cpf) is not None:
    #     return (False, ({ 'error': 'error', 'error_description': 'O CPF informado não é válido', 'field': 'cpf'}, 400))

    # verifica cpf do usuário.
    elif User.find_by_cpf(user_cpf) is not None:
        return (False, ({ 'error': 'error', 'error_description': 'Este CPF já está cadastrado.', 'field': 'cpf'}, 409))

    # verifica se o email já está cadastrado.
    elif User.find_by_email(user_email) is not None:
        return (False, ({ 'error': 'error', 'error_description': 'Este email já está cadastrado.', 'field': 'email'}, 409))

    return (True, None)


class SignUp(Resource):

    def post(self):
        request_args = parse_request()
        (valid, error_response) = validate_signup(request_args)
        if not valid:
            return error_response
        try:
            user_model = User(
                username = request_args.get('email'),
                password = request_args.get('password'),
                fullname = request_args.get('fullname'),
                email = request_args.get('email'), 
                cpf = request_args.get('cpf'),
            )
            user_model.register()
            return {'status': 'success', 'record': user_model.json()}, 201
        except Exception as ex:
            print(ex)
            return {'status': 'error'}
      
