import uvicorn
import pyrebase
from fastapi import FastAPI
from models import LoginSchema,SignUpSchema
from fastapi.responses import JSONResponse

from firebase_admin import credentials, auth
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.exceptions import HTTPException
from fastapi.requests import Request

app = FastAPI(
    description="This is a simple app to show Firebase Auth with FastAPI",
    title="Firebase Auth",
    docs_url="/"
)

# Montar la carpeta 'static' para servir HTML, JS, CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2 para servir la plantilla principal
templates = Jinja2Templates(directory="templates")

#-------------------------FIREBASE SETTING----------------------------#

import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyBj1Nykm_x8oCfyv8JgwnghP_FjzSOKyRc",
  "authDomain": "social-auth-106f3.firebaseapp.com",
  "projectId": "social-auth-106f3",
  "storageBucket": "social-auth-106f3.firebasestorage.app",
  "messagingSenderId": "360391791742",
  "appId": "1:360391791742:web:87b5e4c5d59154bfb4742f",
  "measurementId": "G-4TDTFDR9ZP",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)

#-------------------------FIREBASE SETTING END----------------------------#

# Endpoint API para verificar el token social (Endpoint desacoplado)
@app.post("/api/login-social")
async def api_social_login(request: Request):
    # Esperamos un JSON {"id_token": "..."} desde JS
    data = await request.json()
    id_token = data.get("id_token")
    
    if not id_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing ID token")
        
    try:
        # Verificamos el token en el servidor
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token['email']
        
        # Aquí puedes generar tu propia cookie de sesión o JWT si lo necesitas
        # para futuras peticiones a otras APIs protegidas.
        
        return {
            "status": "success",
            "message": "Token verified server-side",
            "user_uid": uid,
            "email": email
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")



# @app.post('/signup')
# async def create_an_account(user_data:SignUpSchema):
#     email = user_data.email
#     password = user_data.password

#     try:
#         user = auth.create_user(
#             email = email,
#             password = password
#         )

#         return JSONResponse(content={"message" : f"User account created successfuly for user {user.uid}"},
#                             status_code= 201
#                )
#     except auth.EmailAlreadyExistsError:
#         raise HTTPException(
#             status_code=400,
#             detail= f"Account already created for the email {email}"
#         )





# @app.post('/login')
# async def create_access_token(user_data:LoginSchema):
#     email = user_data.email
#     password = user_data.password

#     try:
#         user = firebase.auth().sign_in_with_email_and_password(
#             email = email,
#             password = password
#         )

#         token = user['idToken']

#         return JSONResponse(
#             content={
#                 "token":token
#             },status_code=200
#         )

#     except:
#         raise HTTPException(
#             status_code=400,detail="Invalid Credentials"
#         )

# @app.post('/ping')
# async def validate_token(request:Request):
#     headers = request.headers
#     jwt = headers.get('authorization')

#     user = auth.verify_id_token(jwt)

#     return user["user_id"]

# if __name__ == "__main__":
#     uvicorn.run("main:app",reload=True)