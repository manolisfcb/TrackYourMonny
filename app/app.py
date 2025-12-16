from fastapi import FastAPI


app = FastAPI()



@app.get("/hello-world")
def home():
    return {"message": "Welcome to trackyourmony!"}