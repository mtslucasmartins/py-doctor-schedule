import re

class CPFValidator:

    def __init__(self, cpf):
        self.cpf = cpf

    @classmethod
    def pad(cls, cpf):
        return cpf.zfill(11)

    @classmethod
    def clean(cls, cpf):
        _translate = lambda cpf: ''.join(re.findall(r"\d", cpf))
        return _translate(cpf)

    @classmethod
    def format(self):
        pass

    def valid(self):
        copy = self.cpf

        if len(re.sub(r'(\d)\1+', r'\1', copy)) == 1:
            return False

        copy = CPFValidator.clean(copy)
        copy = CPFValidator.pad(copy)

        base = copy[:9]
        dv   = copy[9:]

        soma = 0

        for i in range(9, 11):
            for j in range(i):
                soma += int(base[j]) * ((i + 1) - j)

            digito = 0 if (soma % 11 < 2) else (11 - (soma % 11))
            base = '{}{}'.format(base, digito);

            if digito != int(dv[i - 9]):
                return False

            soma = 0

        return True


if __name__ == "__main__":
    print(CPFValidator("09878613950").valid())