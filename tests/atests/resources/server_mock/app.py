from fastapi import Request, FastAPI


app = FastAPI()


@app.post("/api/events")
async def get_body(request: Request):
    return await request.json()
