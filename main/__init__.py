import azure.functions as func
from fastapi import FastAPI

app = FastAPI(
    title='leo-sample-app',
    version=0.1,
    contact={
        'name': 'Leo Ho',
        'url': 'https://leoho-profile.vercel.app/',
        'email': 'leohokahei@gmail.com'
    } 
)

@app.get("/test")
async def index():
    return{
        "success": True,
        "message": "Hello World"
    }