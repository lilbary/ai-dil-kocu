from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Kullanıcının analizlerine kolayca ulaşmak için:
    analyses = relationship("Analysis", back_populates="owner")

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String) # Kullanıcının yazdığı hatalı cümle
    feedback = Column(String)      
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Bu analizin hangi kullanıcıya ait olduğunu belirleyen anahtar (Foreign Key)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="analyses")