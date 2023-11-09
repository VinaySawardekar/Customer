from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

USER = os.getenv('DB_USER')
HOST = os.getenv('DB_HOST')
PASSWORD = os.getenv('DB_PASSWORD')

conn = pymysql.connect(
    database="customer",
    user="customer_admin",
    password="customer_admin",
    host="customer.cqe6hr1jmhxb.ap-south-1.rds.amazonaws.com",
    port=3306
)


