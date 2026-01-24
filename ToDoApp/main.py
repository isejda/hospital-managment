from fastapi import FastAPI, status
from .models import Base
from .database import engine
from .routers import auth, users, hospital
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="ToDoApp/static"), name="static")
@app.get("/")
def test():
    return RedirectResponse(url="/hospital/departments", status_code=status.HTTP_302_FOUND)

@app.get('/healthy')
def health_check():
    return {'status': 'healthy'}

app.include_router(hospital.router)
app.include_router(auth.router)
app.include_router(users.router)
