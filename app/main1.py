from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth, database, email,mail
from sqlalchemy import text

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/users/")
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users=crud.get_users(db=db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=401, detail="No User Found!!!")
    return users

@app.get("/getuser/{user_id}")
async def get_user_by_id(user_id:int, db: Session = Depends(get_db)):
    user=crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="No Such User Found!!!")
    return user

@app.post("/register/")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    password_hash = auth.get_password_hash(password)
    user = crud.create_user(db, username, email, password_hash)
    return {"message": "User registered successfully. Await admin approval."}

# @app.get("/getusers/")
# def get_users(db: Session = Depends(get_db)):
#     user = crud.get_users(db)
#     return {"message": f"User123"}
    # user = crud.get_users(db)
    # if user:
        # return {"message": f"User"}
    # raise HTTPException(status_code=404, detail="User not found")


# @app.get("/users/{user_id}", response_model=schemas.User)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db=db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.post("/approve/{user_id}")
# def approve_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud.approve_user(db, user_id)
#     # print(user)
#     if user:
#         email.send_email(user.email, "Approval Notification", f"Your account has been approved. You can now log in.")
#         return {"message": "User approved and email sent."}
#     raise HTTPException(status_code=404, detail="User not found")



@app.post("/login/")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is approved
    if not user.approved:
        raise HTTPException(status_code=403, detail="User not approved by admin")

    return {"message": "Login successful", "user": {"username": user.username, "email": user.email}}


@app.post("/approveuser/{user_id}")
def approve_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.approve_user(db, user_id)
    # print(user)
    if user:
        mail.send_email(user.email)
        return {"message": "User approved and email sent."}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/clear")
def clear_users(db: Session = Depends(get_db)):
    db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
    db.commit()
    return {"message": "Users deleted successfully."}