from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db, get_current_user
import logging

# Setup logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    new_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    logger.info(f"Note created by user {user.email}: {new_note.id}")
    return new_note

@router.get("/", response_model=list[schemas.NoteOut])
def get_notes(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Role-Based Access Control logic
    if user.role == "admin":
        logger.info(f"Admin {user.email} fetching all notes")
        return db.query(models.Note).all()
    
    logger.info(f"User {user.email} fetching their own notes")
    return db.query(models.Note).filter(models.Note.owner_id == user.id).all()

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        logger.warning(f"Delete attempt for non-existent note {note_id} by {user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Authorization Check
    if note.owner_id != user.id and user.role != "admin":
        logger.warning(f"Unauthorized delete attempt for note {note_id} by {user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this note")

    db.delete(note)
    db.commit()
    logger.info(f"Note {note_id} deleted by {user.email}")
    return None

@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not db_note:
        logger.warning(f"Update attempt for non-existent note {note_id} by {user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Authorization Check
    if db_note.owner_id != user.id and user.role != "admin":
        logger.warning(f"Unauthorized update attempt for note {note_id} by {user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this note")

    db_note.title = note.title
    db_note.content = note.content

    db.commit()
    db.refresh(db_note)
    
    logger.info(f"Note {note_id} updated by {user.email}")
    return db_note