import sqlite3
from setup import DB_name
from emailer import New_mail

class Backup():

    def __init__(self):
        self.con = sqlite3.connect(DB_name.db_path)
        self.bck = sqlite3.connect(DB_name.backup_path)
        self.copy_db()

    def progress(self, status, remaining, total):
        print(f'Copied {total-remaining} of {total} pages...')

    def copy_db(self):
        try:
            with self.bck:
                self.con.backup(self.bck, pages=0, progress=self.progress)
            self.bck.close()
            self.con.close()
        
        except Exception as e:
            print(e)
            New_mail(e)

if __name__ == '__main__':
    
    new_backup = Backup()
    
    