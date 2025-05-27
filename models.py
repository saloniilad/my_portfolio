from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

class ContactSubmission(db.Model):
    """Model for storing contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.subject}>'

class Project(db.Model):
    """Model for storing portfolio projects"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.Text, nullable=False)  # Store as comma-separated values
    github_link = db.Column(db.String(255))
    demo_link = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    category = db.Column(db.String(50))  # For filtering (web, mobile, frontend, backend)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'
        
    @property
    def tech_list(self):
        """Convert stored technologies string to list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []
