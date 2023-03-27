#this imports the cryptography package
from cryptography.fernet import Fernet

class Cipher:
    def __init__( self ):
        self.key = b'jaPbFhF4FJUc4yjDBtoez0MXR4Qt0IQm6TSOXHDIZRw='
        self.fernet = Fernet(self.key)
    def encrypt( self, data ):        
        return self.fernet.encrypt(data)

    def decrypt( self, data ):
        return self.fernet.decrypt(data)
    
    def getKey(self):
        x = re.search("^blockchain.*json$", node)
        if(x is False):
            with open('key.key','wb') as file:
                file.write(key)
        with open('key.key','rb') as file:
            return file.read()