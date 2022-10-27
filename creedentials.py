import psycopg2
import psycopg2.extras
import uuid
import pandas.io.sql as sqlio
class Database:

    def __init__(self):
        self.hostname = 'localhost'
        self.username = 'postgres'
        self.password = 'rootroot'
        self.database = 'Trends_analysis'
        self.myConnection = psycopg2.connect( host=self.hostname, user=self.username, password=self.password, dbname=self.database )

    def select_data(self):
        try:
            query = """ select B.bigram_name,F.TF_IDF,A.article_id from Bigram_dimension B
                        JOIN fact_bigram F ON B.bigram_id=F.bigram_id 
                        JOIN Article_dimension A ON A.article_id=F.article_id;"""
            return sqlio.read_sql_query(query, self.myConnection)

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record:", error)

    def insert_into_fact_bigram(self,article_id="",time_id="",tf_idf="",bigram_id=""):
            try:
                cursor = self.myConnection.cursor()
                psycopg2.extras.register_uuid()
                query2 = """ INSERT INTO fact_bigram (bigram_id,article_id,time_id,tf_idf ) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (bigram_id,article_id,time_id,tf_idf)
                cursor.execute(query2, record_to_insert)
                self.myConnection.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record:", error)

    def insert_into_bigram_dimension(self,bigram_name="",bigram_id=""):
            try:
                cursor = self.myConnection.cursor()
                psycopg2.extras.register_uuid()
                query1 = """ INSERT INTO bigram_dimension ( bigram_id,bigram_name ) VALUES (%s,%s)"""
                record_to_insert = (bigram_id,bigram_name)
                cursor.execute(query1, record_to_insert)
                self.myConnection.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record:", error)

    def insert_into_article_dimension(self,url="",article_id="",author="",website=""):
            try:
                cursor = self.myConnection.cursor()
                psycopg2.extras.register_uuid()
                query3 = """ INSERT INTO article_dimension ( article_id,url,author,website ) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (article_id,url,author,website)
                cursor.execute(query3, record_to_insert)
                self.myConnection.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record:", error)
    
    def insert_into_time_dimension(self,time_id="",year="",month="",day=""):
            try:
                cursor = self.myConnection.cursor()
                psycopg2.extras.register_uuid()
                query4 = """ INSERT INTO time_dimension ( time_id,year,month,day ) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (time_id,year,month,day)
                cursor.execute(query4, record_to_insert)
                self.myConnection.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record:", error)
            
    