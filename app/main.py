import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from app import schemas, models
import psycopg2
from app.database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall() # Use fetchall while getting multiple posts
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db), response_model=schemas.Post):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found.")
    return  post
       
# After post creation, status code 201 should sent back.
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # do not use """ INSERT INTO posts (title, content) VALUES ({post.title}, {post.content})""", if user types a title like INSERT into, it will raise an error
    #cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content))
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = models.Post(title=post.title, content=post.content) # instead of writing one by one, use **post.dict()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# status code 204 should be sent back if the deletion is succesfull.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db)):
    #cursor.execute(""" DELETE * FROM posts WHERE id = %s RETURNİNG * """, (str(id)))
    #deleted_post = cursor.fetcone()
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    
    post_query.delete(synchronize_session=False)

    db.commit()


    # Using the line below won't work, after sending status code 204 you cannot simply return another data.
    # return {"message":f"Post {id} deleted."}

    # Instead, use this:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id:int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %S, WHERE id = %s RETURNİNG * """, (post.title, post.content, str(id)))
    #updated_post = cursor.fetcone()
    post_query  = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    
    post_query.update(post, synchronize_session=False)
    db.commit()
    
    return f"Post {id} is updated."



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**dict(user)) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users", response_model=List[schemas.UserResponse])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/users/id", response_model=List[schemas.UserResponse])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,port=8001, host="0.0.0.0")
