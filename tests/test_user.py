
from datetime import datetime
import pytest

from models import User

user_dict_model = {
    'id': None, 
    'cpf': '444.420.445-11', 
    'email': 'mts.lucasmartins@gmail.com', 
    'fullname': 'Lucas Martins', 
    'username': 'mtslucasmartins', 
    'password': 'naotemsenha', 
    'created_at': datetime.now(), 
    'updated_at': datetime.now()
}

user_json = user_dict_model.copy()
del user_json['password']


def test_create_user():
    user = User(cpf=user_dict_model.get('cpf'), email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha', 
                created_at=user_dict_model.get('created_at'), updated_at=user_dict_model.get('updated_at'))
    assert user.json() == user_json


def test_create_user_from_dict():
    user = User(**user_dict_model)
    assert user.json() == user_json


def test_create_user_without_cpf():
    with pytest.raises(Exception) as ex:
        user = User(email='mts.lucasmartins@gmail.com', fullname='Lucas Martins',
                    username='mtslucasmartins', password='naotemsenha')
    assert "Informe o CPF!" in str(ex.value)


def test_create_user_without_email():
    with pytest.raises(Exception) as ex:
        user = User(cpf=user_dict_model.get('cpf'), fullname='Lucas Martins',
                    username='mtslucasmartins', password='naotemsenha')
    assert "Informe o Email!" in str(ex.value)


def test_create_user_without_fullname():
    with pytest.raises(Exception) as ex:
        user = User(cpf=user_dict_model.get('cpf'), email='mts.lucasmartins@gmail.com',
                    username='mtslucasmartins', password='naotemsenha')
    assert "Informe o Nome Completo!" in str(ex.value)
    
def test_create_user_check_valid_cpf():
    user = User(cpf=user_dict_model.get('cpf'), email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha')
    # generates a hash from the password.
    valid = User.check_cpf(user.cpf)
    # checks if the password match
    assert valid

def test_create_user_check_invalid_cpf_1():
    user = User(cpf='12345678910', email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha')
    # generates a hash from the password.
    valid = User.check_cpf(user.cpf)
    # checks if the password match
    assert not valid

def test_create_user_check_invalid_cpf_2():
    user = User(cpf='11111111111', email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha')
    # generates a hash from the password.
    valid = User.check_cpf(user.cpf)
    # checks if the password match
    assert not valid

def test_create_user_check_invalid_cpf_2():
    user = User(cpf='1111111111', email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha')
    # generates a hash from the password.
    valid = User.check_cpf(user.cpf)
    # checks if the password match
    assert not valid

def test_create_user_without_password():
    with pytest.raises(Exception) as ex:
        user = User(cpf=user_dict_model.get('cpf'), email='mts.lucasmartins@gmail.com',
                    fullname='Lucas Martins', username='mtslucasmartins')
    assert "Informe uma Senha!" in str(ex.value)


def test_create_user_check_password():
    user = User(cpf=user_dict_model.get('cpf'), email='mts.lucasmartins@gmail.com',
                fullname='Lucas Martins', username='mtslucasmartins', password='naotemsenha')
    # generates a hash from the password.
    hash = User.hash_password(user.password)
    # checks if the password match
    assert User.check_password('naotemsenha', hash)

