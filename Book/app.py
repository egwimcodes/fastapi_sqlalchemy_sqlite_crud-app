from fastapi import FastAPI, Depends, HTTPException, status
from .schemas import BookType
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

#########################
app = FastAPI()
#########################
models.Base.metadata.create_all(engine)


# ######## start obtaining a database session ########
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ######## end obtaining a database session


# ####### GET ALL METHOD #######
@app.get('/')
def home(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


# ####### GET SINGLE METHOD ######
@app.get('/{book_id}')
def get_book(book_id=int, db: Session = Depends(get_db)):
    get_a_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if get_a_book:
        return get_a_book
    return {'message': f'Book with id of {book_id} not found'}


# #####  CREATE A BOOK POST
@app.post('/')
def addbook(book: BookType, db: Session = Depends(get_db)):
    newbook = db.query(models.Book).filter(models.Book.title == book.title).first()

    if newbook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='book with the same title already exist')
    newbook = models.Book(
        title=book.title,
        author=book.author,
        synopsis=book.synopsis,
        published=book.published
    )
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    return {'Post Message': 'Book added successfully ☺'}


# #### UPDATE A BOOK POST
@app.put('/{book_id}')
def updatebook(book_id: int, book: BookType, db: Session = Depends(get_db)):
    bookupdate = db.query(models.Book).filter(models.Book.id == book_id).first()
    if bookupdate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Book with the id of {book_id} not found')
    bookupdate.title = book.title
    bookupdate.author = book.author
    bookupdate.synopsis = book.synopsis
    bookupdate.published = book.published
    db.add(bookupdate)
    db.commit()
    return {'message': f'Book with the id of {book_id} updated successfully'}


@app.delete('/{book_id}')
def deletebook(book_id=int, db: Session = Depends(get_db)):
    delet_a_book = db.query(models.Book).filter(models.Book.id == book_id)
    if delet_a_book is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Book with the id of {book_id} not found')
    delet_a_book.delete()
    db.commit()
    return {'message': f'Book with the id of {book_id} deleted successfully'}
