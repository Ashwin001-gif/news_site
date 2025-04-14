from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


from routers import articles
from database import engine
from models import Base


# Initialize FastAPI app
app = FastAPI()

# Mount the static folder to serve static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates folder for rendering HTML files
templates = Jinja2Templates(directory="app/templates")

# Homepage route rendering an HTML template (frontend)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# You can keep your API route (like articles) intact here
@app.get("/api/articles")
def get_articles():
    # Your existing API logic
    return {"message": "Articles data will go here!"}

# You can add other routes for the backend as needed
