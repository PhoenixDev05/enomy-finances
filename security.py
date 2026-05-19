import bcrypt
class security:
    def __init__(self):
        pass

    def hashPassword(self, plainPass):
        passwordByte = plainPass.encode('utf-8')
        salt = bcrypt.gensalt()
        hashPass = bcrypt.hashpw(passwordByte,salt)

        return hashPass.decode('utf-8')
    
    def verifyPass(self, plainPass, hash):
        passwordByte = plainPass.encode('utf-8')
        hashByte = hash.encode('utf-8')

        return bcrypt.checkpw(passwordByte,hashByte)