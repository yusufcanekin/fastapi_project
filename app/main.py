from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from . import schemas
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

try:
    conn = psycopg2.connect(host='localhost', database='fastapi_postgres', user='myuser', password='password', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DB connected")
except: 
    print("unseccesful")


# Stores posts for now, will be replaced by DB.
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}]


@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    if id > len(my_posts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    else:
        post = my_posts[id - 1]
        return {"post": my_posts[id - 1]}
    


# After post creation, status code 201 should sent back.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.Post):
    my_posts.append(new_post)
    return my_posts

# status code 204 should be sent back if the deletion is succesfull.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    if id > len(my_posts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    
    else:
        my_posts.pop(id -1)

        # Using the line below won't work, after sending status code 204 you cannot simply return another data.
        # return {"message":f"Post {id} deleted."}

        # Instead, use this:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id:int, post: schemas.Post):
    if id > len(my_posts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    else:
        my_posts[id - 1] = post
        return {"message":f"Post {id} is updated."}

# 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,port=8000, host="0.0.0.0")
