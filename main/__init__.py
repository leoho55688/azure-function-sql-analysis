import os
from dotenv import load_dotenv
load_dotenv()

import azure.functions as func
from fastapi import Depends, FastAPI
import pymssql

import query

class Default(dict):
    def __missing__(self, key):
      return ''

app = FastAPI(
    title='leo-sample-app',
    version=0.1,
    root_path='/v1',
    contact={
        'name': 'Leo Ho',
        'url': 'https://leoho-profile.vercel.app/',
        'email': 'leohokahei@gmail.com'
    } 
)

def get_db():
    db = pymssql.connect(
        server=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        as_dict=True
    )
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def index():
    return{
        'success': True,
        'message': 'Hello World'
    }

@app.get('/product')
async def product(id: int = None, name: str = None, limit: int = 10, db: pymssql.Connection = Depends(get_db)):
    if id and name:
        return{
            'success': False,
            'message': 'please query with product id or name only'
        }
    
    queryStr = query.PRODUCT_QUERY.format_map(
        Default(
            top=f'TOP {limit}',
            condition=f'WHERE ProductID = {id}' if id else (f'WHERE Name LIKE \'%{name}%\'' if name else '')
        )
    )
    
    cursor = db.cursor()
    cursor.execute(queryStr)
    result = cursor.fetchall()
    cursor.close()

    return{
        'success': True,
        'result': result
    }

@app.get('/product/profit')
async def product_profit(limit: int = 10, db: pymssql.Connection = Depends(get_db)):
    queryStr = query.TOP_Profitable_PRODUCT.format_map(
        Default(
            top=f'TOP {limit}'
        )
    )

    cursor = db.cursor()
    cursor.execute(queryStr)
    result = cursor.fetchall()
    cursor.close()
    
    return{
        'succeess': True,
        'result': result
    }

@app.get('/customer/city')
async def customer_city(limit: int = 10, db: pymssql.Connection = Depends(get_db)):
    queryStr = query.TOP_SALES_CUSTOMER_CITY.format_map(
        Default(
            top=f'TOP {limit}'
        )
    )

    cursor = db.cursor()
    cursor.execute(queryStr)
    result = cursor.fetchall()
    cursor.close()
    
    return{
        'succeess': True,
        'result': result
    }

@app.get('/customer/gender')
async def customer_gender(db: pymssql = Depends(get_db)):
    queryStr = query.TOTAL_SALES_CUSTOMER_GENDER

    cursor = db.cursor()
    cursor.execute(queryStr)
    result = cursor.fetchall()
    cursor.close()
    
    return{
        'succeess': True,
        'result': result
    }