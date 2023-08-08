#API Key encryption
from cryptography.fernet import Fernet
import os

class Setup():

    path_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..") #change this line if needed

    def set_up_credentials():
        """Run this Method to set up the credential management"""

        api_key = input("Enter your API key:")
        api_secret = input("Enter your API secret:")

        Setup._write_api_key(api_key)
        Setup._write_api_secret(api_secret)

        print(f"\nSuccessfully encrypted and saved key and secret")
        print(f"API key:\t{Setup._get_api_key()}\nAPI secret:\t{Setup._get_api_secret()}")


    def _write_api_key(api_key):
    
        #generate key
        key = Fernet.generate_key()
        f = open(os.path.join(Setup.path_file,"refKey_key.txt"), "wb")
        f.write(key)
        f.close()

        ### 3. encrypt the password and write it in a file
        refKey = Fernet(key)
        mypwdbyt = bytes(api_key, 'utf-8') # convert into byte
        encryptedPWD = refKey.encrypt(mypwdbyt)
        f = open(os.path.join(Setup.path_file,"encryptedPWD_key.txt"), "wb")
        f.write(encryptedPWD)
        f.close()

        return "ok"

    def _write_api_secret(api_secret):

        #generate key
        key = Fernet.generate_key()
        f = open(os.path.join(Setup.path_file,"refKey_secret.txt"), "wb")
        f.write(key)
        f.close()

        ### 3. encrypt the password and write it in a file
        refKey = Fernet(key)
        mypwdbyt = bytes(api_secret, 'utf-8') # convert into byte
        encryptedPWD = refKey.encrypt(mypwdbyt)
        f = open(os.path.join(Setup.path_file,"encryptedPWD_secret.txt"), "wb")
        f.write(encryptedPWD)
        f.close()

        return "ok"

    def _get_api_key():

        # read encrypted pwd and convert into byte
        with open(os.path.join(Setup.path_file,"encryptedPWD_key.txt")) as f:
            encpwd = ''.join(f.readlines())
            encpwdbyt = bytes(encpwd, 'utf-8')
        f.close()

        # read key and convert into byte
        with open(os.path.join(Setup.path_file,"refKey_key.txt")) as f:
            refKey = ''.join(f.readlines())
            refKeybyt = bytes(refKey, 'utf-8')
        f.close()

        # use the key and encrypt pwd
        keytouse = Fernet(refKeybyt)
        myPass = (keytouse.decrypt(encpwdbyt))
        
        return str(myPass)[2:-1]

    def _get_api_secret():

        # read encrypted pwd and convert into byte
        with open(os.path.join(Setup.path_file,"encryptedPWD_secret.txt")) as f:
            encpwd = ''.join(f.readlines())
            encpwdbyt = bytes(encpwd, 'utf-8')
        f.close()

        # read key and convert into byte
        with open(os.path.join(Setup.path_file,"refKey_secret.txt")) as f:
            refKey = ''.join(f.readlines())
            refKeybyt = bytes(refKey, 'utf-8')
        f.close()

        # use the key and encrypt pwd
        keytouse = Fernet(refKeybyt)
        myPass = (keytouse.decrypt(encpwdbyt))

        return str(myPass)[2:-1]

if __name__ == "__main__":
    Setup.set_up_credentials()