from email.policy import strict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
app = FastAPI()

# for dev, allow frontend (Vite default: http://localhost:5173)
origins = [
    "http://localhost:5173",
]
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ingredients(BaseModel):
    name: str
    quantity: str

class Recipe(BaseModel):
    name: str
    ingredients: list[Ingredients]
    steps: list[str]


class ChatRequest(BaseModel):
    dish_name: str

recipe_schema = Recipe.model_json_schema()

@app.post("/api/ai-chat", response_model=Recipe)
async def ai_chat(request: ChatRequest):
    response = client.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {"role": "system", "content": f"Generate a recipe for {request.dish_name}"}, 
        ],
        text_format=Recipe


    )
    recipe: Recipe = response.output_parsed
    return recipe


