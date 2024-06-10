import time

def log_test_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds")
        return result
    return wrapper

def verify_condition(condition, message="Verification failed"):
    if not condition:
        raise AssertionError(message)


# TODO >>> Add a Events Manager that can save events locally
# Events are temporary milestones that we can define to a test 
# This allows us to log events that we expect the test to complete.

from .common.sql_pool import SQLiteConnectionPool
import os
import pandas as pd

THIS_DIR = os.getcwd()

class Events_Manager:

    def __init__(self, Unit:str, path:str):
        """
        if unit == "*" select all units data
        """

        pool = SQLiteConnectionPool(3, os.path.join(THIS_DIR, "Data.db"))
        self.connection = pool.get_connection()

        self.Unit = Unit

        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Events (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Unit TEXT,
            StepCompleted TEXT,
            EventType TEXT, 
            EventKey TEXT,
            Time NUMBER
        )''')
        
    
    def drop_events_table(self) -> None:
        """Drop the Events table from the database."""
    
        try:
            cur = self.connection.cursor()
            
            sql_drop_table_query = """DROP TABLE IF EXISTS Events"""
            cur.execute(sql_drop_table_query)
            
            self.connection.commit()
            print("Events table has been removed.")
            
        except Exception as e:
            print(f"Error occurred while removing the Events table. Error: {e}")


    def List_Events(self) -> dict:
        
        cur = self.connection.cursor()
        
        if self.Unit == "*":
            sqlite_select_query = """SELECT * FROM Events"""
            cur.execute(sqlite_select_query)
        
        else:
            sqlite_select_query = """SELECT * FROM Events WHERE Unit = ?"""
            Data = ((self.Unit, ))
            cur.execute(sqlite_select_query, Data)
        
        df = cur.fetchall()
        df = pd.DataFrame(df, columns=['ID', 'Unit', 'StepCompleted', 'EventType', 'EventKey', 'Time'])
        dict_df = df.to_dict()
        
        return dict_df
    
    def Set_Event (self, step:str, event_type:str="Default", **kwargs):     

        """
        Set a event

        event_type: str - can be:
            - Default
            - Exception
            - Send
            - Receive
        
        if event_type is Send and Receive it needs a predefined `event_key:str` kwarg,
        the event key is a str and need to contain at least 16 digits that need to be random,
        to generate a valid key pair and have 100% sure that this isn't registered you can use the 
        helper `gen_valid_event_key.py` at Myscelium/tests/Logs/gen_valid_event_key.py

        """
        
        if self.Unit == "*":
            raise ValueError("Can't Set Event To Generalized Unit: '*'")

        if event_type in ["Default", "Exception", "Send", "Receive"]:
            pass
        else:
            raise ValueError("Event type can only be one of those: 'Default, Exception, Send, Receive'")

        events = pd.DataFrame.from_dict(self.List_Events())   

        for i in events.index:
            if events.loc[i, "StepCompleted"] == step:
                return
            else:
                continue

        cur = self.connection.cursor()

        ts = time.time()

        event_key = ""

        if event_type == "Send" or event_type == "Receive":

            if not ("event_key" in kwargs):
                raise "You need to to specify a event code to Send an Receive event_types"
            else:   
                pass

            event_key = kwargs["event_key"]

        Data = ((self.Unit, step, event_type, event_key, ts))

        sqlite_insert_with_param = """INSERT INTO Events (Unit, StepCompleted, EventType, EventKey, Time) VALUES (?, ?, ?, ?, ?);"""
        cur.execute(sqlite_insert_with_param, Data)
        self.connection.commit()

        return