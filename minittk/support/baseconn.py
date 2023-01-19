# -*- encoding: utf-8 -*-
from abc import *
import pymysql


class BaseConnection(pymysql.Connection, metaclass=ABCMeta):
    @abstractmethod
    def run_query(self, query, fetch=None):
        pass

    @abstractmethod
    def use(self, db):
        """
        Use database
        Usage:
        self.use("Database")
        """
        pass

    @abstractmethod
    def drop(self, drop_type, name):
        """
        Drop
        Usage:
         - drop a table: self.drop('table', 'tableName')
         - drop a database: self.drop('database', 'dbName')
        """
        pass

    @abstractmethod
    def select(self, *args, table_name):
        """
        Select data from a table
        Usage:
         - self.select('*', table_name='table')
         - self.select('column1', 'column2', ..., table_name='table')
        """
        pass

    @abstractmethod
    def insert(self, table_name, *values):
        """
        Insertion
        Usage:
         - self.insert('table', 1, 2, 3, 4)
        """
        pass
