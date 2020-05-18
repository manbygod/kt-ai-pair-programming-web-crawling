import re
import pymysql
from . import singleton
 
class DBTool(metaclass=singleton.Singleton):
 
    def __init__(self):
        
        self.db = pymysql.connect(
            user = 'root',
            passwd = 'christ',
            host = 'localhost',
            port = 3307,
            db ='web',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor # cursor가 데이터를 가져올 때 dictionary들의 list로 가져옴. 만약 .DictCursor를 안쓰면 튜플들의 튜플 형태로 가져옴
            )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def insertUser(self, userid, profile, password):
        
        query = f"""
        insert into user (name, profile, password) 
        values ('{userid}', '{ profile }', SHA2('{ password }', 256));
        """
        
        self.cursor.execute(query)
        self.db.commit()
        
    def deleteUser(self, userid):
        
        query = f"""
            delete from user where 
                name = '{userid}'
        """
        
        self.cursor.execute(query)
        self.db.commit()
        
    def selectUserName(self, userid):
        
        query = f"""
        select id, name from user where name = '{userid}'
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchone()
 
    def selectUser(self, userid, password):
        
        query = f"""
        select id, name from user where name = '{userid}' and password = SHA2('{ password }', 256)
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    # def execute(self, query, args={}):
    #     self.cursor.execute(query, args)
 
    # def executeOne(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchone()
    #     return row
 
    # def executeAll(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchall()
    #     return row
 
    # def commit(self):
    #     self.db.commit()