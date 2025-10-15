import psycopg2 as PDB
from psycopg2 import errorcodes

class PostgresDB:

    def __init__(self,name,userr,psw,hostt,portt):
        self.dbName = name
        self.user = userr
        self.password = psw
        self.host = hostt
        self.port = portt
        self.connectData = self.InitialDB()
        self.isconnecting = False 
        
    def InitialDB(self):
        connectData = PDB.connect(
            database = self.dbName,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )
        return connectData

    def ConnectToDB(self):
        try:
            self.cur = self.connectData.cursor()
            self.cur.execute('SELECT VERSION()')
            results = self.cur.fetchall()
            self.connectData.commit()
            self.isconnecting = True
            print("Sql Connecting!")
            print("Database Version : {0} ".format(results))
        except PDB.Error as e:
            if e.errno == errorcodes.ERROR_IN_ASSIGNMENT:
                print("ERROR_IN_ASSIGNMENT")
            elif e.errno == errorcodes.DATA_EXCEPTION:
                print("DATA_EXCEPTION")
            else:
                print(e)

    def CloseDB(self):
        if self.isconnecting == True :
            self.cur.close();
            self.connectData.close()
        else :
            print("DB 從未被啟動")

    def AddTable(self,dbname) :
        self.cur=self.connectData.cursor()
        self.cur.execute(f"""CREATE TABLE {dbname} (
                           UserID SMALLSERIAL PRIMARY KEY, 
                           LineID text NOT NULL,            
                           Lat text NOT NULL,
                           Lon text NOT NULL,
                           TimeStamp text NOT NULL
                           );"""
                        )
        self.connectData.commit()

    # 新增資料
    def AddData (self,database_name,data_type,value) :
        sql = "INSERT INTO " + database_name + " (" + data_type + ") " + "VALUES" + " (" + value + ");"
        self.cur.execute(sql)

        # 提交交易 important
        self.connectData.commit()

    # 修改單一資料
    def ChangeData (self,database_name,data_type,value,target_data_element,target) :
        self.cur.execute(f"UPDATE {database_name} SET ({data_type}) = ({value}) WHERE {target_data_element} = '{target}';")

        # 提交交易  important
        self.connectData.commit()

    # 刪除單一資料
    def DeleteData (self,database_name,target_data_element,target) :
        sql = "DELETE FROM " + database_name + " WHERE "+ target_data_element + "=" + target
        self.cur.execute(sql)
        # 提交交易  important
        self.connectData.commit()

    def GetTableAllData (self,dbName) :    
        self.cur.execute("SELECT * FROM " + dbName)
        data = self.cur.fetchall()
        return data

    def GetOneData(self,dbName,rrange,target_data_element,target):
        self.cur.execute(f"SELECT {rrange} FROM {dbName} WHERE {target_data_element} = '{target}';")
        data = self.cur.fetchone()
        return data

    def OtherCmd(self,cmd) :
        self.cur.execute(cmd)
        # 提交交易  important
        self.connectData.commit()