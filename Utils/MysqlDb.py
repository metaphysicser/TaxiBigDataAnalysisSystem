import pymysql as mysql
import pickle


class sqldbs(object) :

    def __init__(self, host = "localhost", password=  "", user = "root",charset = "utf8", port = "3306") :

        self.sql = mysql.connect(host = host, port = port,  password = password, user = user, charset = charset)

    def executeSql(self, cmd) :

        '''To execute a Mysql command
        None
        :param cmd: The command to execute
        :type cmd: str
        :returns: The result of the command executed
        :rtype: str
        '''

        try:
            cursor = self.sql.cursor()

            cursor.execute(cmd)

            results = cursor.fetchall()

            return results

        except Exception as e:

            print(e)

            self.sql.rollback()

    def executeManySql(self, cmd, data) :

        '''To execute many Mysql commands in same pattern
        None
        :param cmd: The command pattern to execute
        :type cmd: str
        :param data: The arguments to fix in the pattern
        :type data: list
        :returns: The result of the command executed
        :rtype: str
        '''

        try:
            cursor = self.sql.cursor()

            cursor.executemany(cmd, data)

            self.sql.commit()

            results = cursor.fetchall()

            return results

        except Exception as e:

            print(e)

            self.sql.rollback()

    def close(self) :

        self.sql.close()
