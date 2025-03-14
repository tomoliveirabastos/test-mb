from fastapi import FastAPI

app = FastAPI()

# "from" é uma keyword do python, não é possivel usa-la como variavel
@app.get("/{pair}/mms")
async def index(from_timestamp: float, to_timestamp: float, range: int):
    return {
        "from": from_timestamp
    }