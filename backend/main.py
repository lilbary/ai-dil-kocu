from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database, ai_service, auth, schemas
from database import engine

# Veritabanı tablolarını oluşturur
database.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Dil Koçu API")

@app.get("/")
def read_root():
    return {"mesaj": "Harika! FastAPI sunucusu başarıyla çalışıyor."}

# --- REGISTER (KAYIT) ---
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")
    
    try:
        hashed_pw = auth.get_password_hash(user.password)
        new_user = models.User(email=user.email, hashed_password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id": new_user.id, "email": new_user.email}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

# --- LOGIN (GİRİŞ YAP) ---

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ANALİZ ---
class AnalysisRequest(BaseModel):
    text: str

@app.post("/analyze-text")
def analyze_english(
    request: AnalysisRequest, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        ai_feedback = ai_service.get_ai_feedback(request.text)
        new_analysis = models.Analysis(
            original_text=request.text,
            feedback=ai_feedback,
            user_id=current_user.id
        )
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        return new_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail="Analiz başarısız oldu.")

# --- GEÇMİŞ ---
@app.get("/my-history")
def get_history(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    history = db.query(models.Analysis).filter(
        models.Analysis.user_id == current_user.id
    ).order_by(models.Analysis.created_at.desc()).all()
    return history
@app.delete("/delete-analysis/{analysis_id}")
def delete_analysis(
    analysis_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id, 
        models.Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı veya yetkin yok kanka.")

    try:
        db.delete(analysis)
        db.commit()
        return {"mesaj": "Analiz başarıyla silindi."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Silme işlemi başarısız.")
    
@app.get("/me")
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user 