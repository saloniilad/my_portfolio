import os
import logging
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request
from models import db, ContactSubmission, Project

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

## Configure database to use SQLite for local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
logging.debug("Database configured with SQLite")


db_path = os.path.abspath('portfolio.db')
print(f"Database should be created at: {db_path}")

# Import forms after app initialization
from forms import ContactForm, ProjectForm

# Create tables
with app.app_context():
    try:
        db.create_all()
        logging.debug("Database tables created or already exist.")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    return render_template('index.html', active_page='home')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/projects')
def projects():
    # Get projects from database if available, otherwise use example data
    
    try:
            # Check if we have any projects in the database
            project_count = db.session.query(Project).count()
            
            if project_count > 0:
                # If we have projects in the database, use them
                projects_data = Project.query.all()
                logging.debug(f"Retrieved {len(projects_data)} projects from database")
                return render_template('projects.html', active_page='projects', projects=projects_data)
    except Exception as e:
            logging.error(f"Error retrieving projects from database: {e}")
    
    # If database not available or no projects, use example data
    projects_data = [
        {
            'title': 'E-Commerce Platform',
            'description': 'A fully functional online store with shopping cart, user authentication, and payment processing.',
            'technologies': ['Python', 'Flask', 'SQLAlchemy', 'JavaScript', 'Bootstrap'],
            'tech_list': ['Python', 'Flask', 'SQLAlchemy', 'JavaScript', 'Bootstrap'],
            'github_link': 'https://github.com/yourusername/ecommerce-platform',
            'demo_link': 'https://example.com/ecommerce-demo'
        },
        {
            'title': 'Task Management App',
            'description': 'A productivity application for managing tasks, projects, and deadlines with team collaboration features.',
            'technologies': ['React', 'Node.js', 'Express', 'MongoDB', 'Socket.io'],
            'tech_list': ['React', 'Node.js', 'Express', 'MongoDB', 'Socket.io'],
            'github_link': 'https://github.com/yourusername/task-manager',
            'demo_link': 'https://example.com/task-app-demo'
        },
        {
            'title': 'Weather Dashboard',
            'description': 'A weather application that displays current conditions and forecasts based on user location or search.',
            'technologies': ['JavaScript', 'HTML5', 'CSS3', 'Weather API', 'Geolocation API'],
            'tech_list': ['JavaScript', 'HTML5', 'CSS3', 'Weather API', 'Geolocation API'],
            'github_link': 'https://github.com/yourusername/weather-dashboard',
            'demo_link': 'https://example.com/weather-demo'
        }
    ]
    return render_template('projects.html', active_page='projects', projects=projects_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        
        try:
                # Create a new contact submission database entry
                new_submission = ContactSubmission()
                new_submission.name = form.name.data
                new_submission.email = form.email.data
                new_submission.subject = form.subject.data
                new_submission.message = form.message.data
                
                # Add and commit to database
                db.session.add(new_submission)
                db.session.commit()
                logging.debug(f"Saved contact submission from {new_submission.name}")
        except Exception as e:
                logging.error(f"Error saving contact submission: {e}")
                
        # Show success message and redirect
        flash('Your message has been sent! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', active_page='contact', form=form)

# Admin routes
@app.route('/admin')
def admin():
    """Admin dashboard to view contact submissions and projects"""
    contact_submissions = []
    projects = []
    
    
    try:
            # Get contact submissions from database
            contact_submissions = ContactSubmission.query.order_by(ContactSubmission.timestamp.desc()).all()
            logging.debug(f"Retrieved {len(contact_submissions)} contact submissions")
            
            # Get projects from database
            projects = Project.query.order_by(Project.title).all()
            logging.debug(f"Retrieved {len(projects)} projects")
    except Exception as e:
            logging.error(f"Error retrieving data for admin page: {e}")
    
    return render_template('admin.html', 
                          active_page='admin', 
                          contact_submissions=contact_submissions,
                          projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
def add_project():
    """Add a new project"""
    form = ProjectForm()
    
    if form.validate_on_submit():
        try:
            # Create new project
            new_project = Project()
            new_project.title = form.title.data
            new_project.description = form.description.data
            new_project.technologies = form.technologies.data
            new_project.github_link = form.github_link.data
            new_project.demo_link = form.demo_link.data
            new_project.category = form.category.data
            new_project.featured = form.featured.data
            
            # Save to database
            db.session.add(new_project)
            db.session.commit()
            
            flash('Project added successfully!', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            logging.error(f"Error adding project: {e}")
            flash('An error occurred while adding the project.', 'danger')
    
    return render_template('project_form.html', form=form)

@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    """Edit an existing project"""
    try:
        flash('Database not available.', 'danger')
        return redirect(url_for('admin'))
    except Exception as e:
        logging.error(f"Error checking database availability: {e}")
    try:
        project = Project.query.get_or_404(project_id)
        
        form = ProjectForm(obj=project)
        
        if form.validate_on_submit():
            # Update project
            project.title = form.title.data
            project.description = form.description.data
            project.technologies = form.technologies.data
            project.github_link = form.github_link.data
            project.demo_link = form.demo_link.data
            project.category = form.category.data
            project.featured = form.featured.data
            
            # Save changes
            db.session.commit()
            
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin'))
    except Exception as e:
        logging.error(f"Error editing project: {e}")
        flash('An error occurred while updating the project.', 'danger')
        return redirect(url_for('admin'))
    
    return render_template('project_form.html', form=form, project=project)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
