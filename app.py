from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
import io
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-jewelry-tracker' # Change for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jewelry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # In production use hashing
    role = db.Column(db.String(50), default='user') # admin, user

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    target_per_hour = db.Column(db.Integer, default=0)

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
    men_count = db.Column(db.Integer, default=0)
    women_count = db.Column(db.Integer, default=0)
    quantity = db.Column(db.Integer, default=0) # Added quantity field
    target_achieved = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    action = db.relationship('Action', backref=db.backref('logs', lazy=True))

class CalendarDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    is_working_day = db.Column(db.Boolean, default=True)
    hours = db.Column(db.Float, default=8.0)
    note = db.Column(db.String(200))

class ProjectGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
    target_quantity = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active') # active, completed, archived
    completion_date = db.Column(db.Date, nullable=True)
    completion_notes = db.Column(db.String(500), nullable=True)
    
    action = db.relationship('Action', backref=db.backref('goals', lazy=True))
    notes = db.relationship('ProjectNote', backref='project', lazy=True, cascade="all, delete-orphan")

class ProjectNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_goal.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BenchmarkConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_men = db.Column(db.Float, default=50.0)
    target_women = db.Column(db.Float, default=45.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Simple password check for prototype (use werkzeug.security in production)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    # Basic calculations for dashboard
    logs_today = DailyLog.query.filter(DailyLog.date >= today).all()
    total_logs = len(logs_today)
    
    # Calculate totals
    total_men = sum(log.men_count for log in logs_today)
    total_women = sum(log.women_count for log in logs_today)
    total_quantity = sum(log.quantity for log in logs_today)
    
    # --- Smart Alerts Logic ---
    alerts = []
    active_projects = ProjectGoal.query.filter_by(status='active').all()
    
    for project in active_projects:
        # Calculate current progress
        logs = DailyLog.query.filter(DailyLog.action_id == project.action_id, DailyLog.date >= project.start_date).all()
        current_quantity = sum(log.quantity for log in logs)
        remaining_quantity = project.target_quantity - current_quantity
        
        if remaining_quantity > 0:
            # Calculate remaining working hours from Calendar
            # Get days between tomorrow and deadline (inclusive)
            # If today is deadline, check if we have hours left (simplified: 0)
            
            # Simple approach: Sum hours of all working days from tomorrow to deadline
            working_days = CalendarDay.query.filter(
                CalendarDay.date > today,
                CalendarDay.date <= project.deadline,
                CalendarDay.is_working_day == True
            ).all()
            
            # Add hours from today if it's a working day (approximate remaining? For MVP assume full day or 0 if passed)
            # Let's count full days for simplicity + logic for holidays
            
            total_remaining_hours = sum(day.hours for day in working_days)
            
            # Avoid division by zero
            if total_remaining_hours > 0:
                required_rate = remaining_quantity / total_remaining_hours
            else:
                required_rate = remaining_quantity # Impossible if 0 hours
                alerts.append({
                    'level': 'critical',
                    'message': f"Project '{project.name}' is overdue! Need {remaining_quantity} more towers but no working hours left."
                })
                continue

            # Calculate actual avg productivity (Towers/Hour) - approximated by Towers / Staff (Daily)
            # A better metric would be Total Towers / Total Staff Hours Used. 
            # We don't track "Hours Worked" per log, just "Staff Count". 
            # let's assume 8h shift for historical calc.
            
            # Current Rate (Last 3 days avg)
            recent_start = today - pd.Timedelta(days=3)
            recent_logs = DailyLog.query.filter(DailyLog.action_id == project.action_id, DailyLog.date >= recent_start).all()
            
            recent_qty = sum(l.quantity for l in recent_logs)
            recent_staff = sum(l.men_count + l.women_count for l in recent_logs)
            
            # Avg per staff per day
            avg_per_staff_day = (recent_qty / recent_staff) if recent_staff > 0 else 0
            
            # Assume 8h shift to compare with Rate/Hour? 
            # Wait, required_rate is "Towers per Hour".
            # avg_per_staff_day is "Towers per Person-Day".
            # Let's convert required_rate to "Required People per Day (assuming 8h)".
            
            # Required Output Day = Required Rate * 8h
            # Required People = Required Output Day / Avg Per Staff Day
            
            required_daily_output = required_rate * 8.0 
            
            if avg_per_staff_day > 0:
                required_people = required_daily_output / avg_per_staff_day
                
                # Check current allocation
                current_staff_allocation = total_men + total_women # Today's staff
                # Logic gap: total_staff is for ALL actions. We need specific action staff.
                # logs_today has that.
                
                logs_today_action = [l for l in logs_today if l.action_id == project.action_id]
                current_action_staff = sum(l.men_count + l.women_count for l in logs_today_action)
                
                if current_action_staff < required_people:
                    shortage = round(required_people - current_action_staff, 1)
                    if shortage >= 1:
                        alerts.append({
                            'level': 'warning',
                            'message': f"Goal '{project.name}': Staff shortage! Need {shortage} more people to meet deadline."
                        })
    
    # --- Generate Timeline Data for Frontend ---
    for project in active_projects:
        # Create a list of days from start_date to deadline (or today + 7 days if deadline is far, but user asked for "calendar")
        # Let's show from start_date to deadline. If too long, maybe limit? 
        # Requirement: "calendar with quantity... last day deadline"
        
        timeline_days = []
        current = project.start_date
        # Limit to max 60 days to avoid UI explosion (can scroll)
        end_display = project.deadline
        
        # Iterate dates
        # Use pandas date_range or simple loop
        # We need logs for each day
        project_logs = DailyLog.query.filter(
            DailyLog.action_id == project.action_id, 
            DailyLog.date >= project.start_date,
            DailyLog.date <= end_display
        ).all()
        
        # Map date -> total quantity
        log_map = {}
        for l in project_logs:
            d_str = l.date.strftime('%Y-%m-%d')
            log_map[d_str] = log_map.get(d_str, 0) + l.quantity
            
        # Build timeline list
        # Check total days
        total_days = (end_display - project.start_date).days + 1
        
        for i in range(total_days):
            d = project.start_date + pd.Timedelta(days=i)
            # break if d > deadline (already controlled by range)
            
            d_str = d.strftime('%Y-%m-%d')
            qty = log_map.get(d_str, 0)
            
            is_done = qty > 0
            is_history = d < today
            
            timeline_days.append({
                'date': d,
                'quantity': qty,
                'is_done': is_done,
                'is_history': is_history
            })
            
        project.timeline = timeline_days
        # Also attach current progress explicitly
        project.current_quantity = sum(log.quantity for log in project_logs)

    return render_template('dashboard.html', 
                          user=current_user, 
                          logs=logs_today, 
                          total_logs=total_logs,
                          total_staff=total_men + total_women,
                          total_quantity=total_quantity,
                          promoted_alerts=alerts,
                          projects=active_projects,
                          now=today)

@app.route('/log/new', methods=['GET', 'POST'])
@login_required
def new_log():
    if request.method == 'POST':
        action_id = request.form.get('action_id')
        men_count = int(request.form.get('men_count', 0))
        women_count = int(request.form.get('women_count', 0))
        quantity = int(request.form.get('quantity', 0))
        notes = request.form.get('notes')
        
        # Validation
        if not action_id:
            flash('Please select an action.')
            return redirect(url_for('new_log'))
            
        log = DailyLog(
            user_id=current_user.id,
            action_id=int(action_id),
            men_count=men_count,
            women_count=women_count,
            quantity=quantity,
            notes=notes,
            target_achieved=False # Logic to determine this can be added later
        )
        db.session.add(log)
        db.session.commit()
        flash('Log entry added successfully!')
        return redirect(url_for('dashboard'))
        
    actions = Action.query.all()
    return render_template('log_entry.html', actions=actions)

@app.route('/history')
@login_required
def history():
    logs = DailyLog.query.order_by(DailyLog.timestamp.desc()).all()
    return render_template('history.html', logs=logs)

@app.route('/export')
@login_required
def export_data():
    logs = DailyLog.query.all()
    
    # Transform data for Excel
    data = []
    for log in logs:
        data.append({
            'Date': log.date,
            'Time': log.timestamp.strftime('%H:%M:%S'),
            'User': log.user.username,
            'Action': log.action.name,
            'Men Count': log.men_count,
            'Women Count': log.women_count,
            'Quantity': log.quantity,
            'Total Staff': log.men_count + log.women_count,
            'Notes': log.notes
        })
    
    df = pd.DataFrame(data)
    
    # Create a BytesIO buffer to save the Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Activity Logs')
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'jewelry_tracker_export_{datetime.utcnow().strftime("%Y%m%d")}.xlsx'
    )

@app.route('/api/stats')
@login_required
def get_stats():
    # Last 7 days data for chart
    end_date = datetime.utcnow().date()
    start_date = end_date - pd.Timedelta(days=6)
    
    logs = DailyLog.query.filter(DailyLog.date >= start_date).all()
    
    # Process with Pandas
    if not logs:
        return jsonify({'dates': [], 'quantities': [], 'productivity': []})
    
    data = []
    for log in logs:
        data.append({
            'date': log.date.strftime('%Y-%m-%d'),
            'quantity': log.quantity,
            'staff': log.men_count + log.women_count
        })
    
    df = pd.DataFrame(data)
    daily_stats = df.groupby('date').agg({'quantity': 'sum', 'staff': 'sum'}).reset_index()
    daily_stats['productivity'] = daily_stats.apply(lambda x: x['quantity'] / x['staff'] if x['staff'] > 0 else 0, axis=1)
    
    return jsonify({
        'dates': daily_stats['date'].tolist(),
        'quantities': daily_stats['quantity'].tolist(),
        'productivity': daily_stats['productivity'].fillna(0).tolist()
    })

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar_view():
    if request.method == 'POST':
        date_str = request.form.get('date')
        action = request.form.get('action')
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        day = CalendarDay.query.filter_by(date=date_obj).first()
        
        if not day:
            day = CalendarDay(date=date_obj)
            db.session.add(day)
            
        if action == 'toggle_working':
            day.is_working_day = not day.is_working_day
        elif action == 'update_details':
            day.hours = float(request.form.get('hours', 8.0))
            day.note = request.form.get('note', '')
            
        db.session.commit()
        return redirect(url_for('calendar_view'))

    # Generate calendar data for current month (or requested month)
    # For MVP, just show next 30 days
    today = datetime.utcnow().date()
    days_data = []
    
    for i in range(30):
        current_date = today + pd.Timedelta(days=i)
        day_db = CalendarDay.query.filter_by(date=current_date).first()
        
        is_weekend = current_date.weekday() >= 5
        
        # Default values if not in DB
        is_working = day_db.is_working_day if day_db else (not is_weekend)
        hours = day_db.hours if day_db else 8.0
        note = day_db.note if day_db else ''
        
        days_data.append({
            'date': current_date,
            'is_working': is_working,
            'hours': hours,
            'note': note,
            'is_weekend': is_weekend,
            'day_name': current_date.strftime('%A')
        })
        
    return render_template('calendar.html', days=days_data)

        
    return render_template('calendar.html', days=days_data)

@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        name = request.form.get('name')
        action_id = request.form.get('action_id')
        target_quantity = int(request.form.get('target_quantity', 0))
        deadline_str = request.form.get('deadline')
        
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        start_date = datetime.utcnow().date()
        
        project = ProjectGoal(
            name=name,
            action_id=int(action_id),
            target_quantity=target_quantity,
            start_date=start_date,
            deadline=deadline,
            status='active'
        )
        db.session.add(project)
        db.session.commit()
        flash('New goal created successfully!')
        return redirect(url_for('dashboard'))
        
    actions = Action.query.all()
    return render_template('project_form.html', actions=actions)

    actions = Action.query.all()
    return render_template('project_form.html', actions=actions)

@app.route('/projects/complete', methods=['POST'])
@login_required
def complete_project():
    project_id = request.form.get('project_id')
    notes = request.form.get('notes')
    
    project = ProjectGoal.query.get(int(project_id))
    if project:
        project.status = 'completed'
        project.completion_date = datetime.utcnow().date()
        project.completion_notes = notes
        db.session.commit()
        flash(f"Project '{project.name}' completed and archived.")
        
    return redirect(url_for('dashboard'))

@app.route('/projects/history')
@login_required
def project_history():
    completed_projects = ProjectGoal.query.filter_by(status='completed').order_by(ProjectGoal.completion_date.desc()).all()
    
    # Calculate stats for each project to show in history
    history_data = []
    for project in completed_projects:
        logs = DailyLog.query.filter(DailyLog.action_id == project.action_id, 
                                     DailyLog.date >= project.start_date,
                                     DailyLog.date <= project.completion_date).all()
        
        total_produced = sum(log.quantity for log in logs)
        
        # Determine if on time
        on_time = project.completion_date <= project.deadline
        
        # Get all notes for this project
        all_notes = ProjectNote.query.filter_by(project_id=project.id).order_by(ProjectNote.timestamp.desc()).all()
        
        history_data.append({
            'project': project,
            'total_produced': total_produced,
            'on_time': on_time,
            'delay_days': (project.completion_date - project.deadline).days if not on_time else 0,
            'notes_history': all_notes
        })
        
    return render_template('project_history.html', projects=history_data)

@app.route('/projects/<int:project_id>/notes', methods=['GET', 'POST'])
@login_required
def project_notes(project_id):
    project = ProjectGoal.query.get_or_404(project_id)
    
    if request.method == 'POST':
        content = request.json.get('content')
        if content:
            note = ProjectNote(project_id=project.id, content=content)
            db.session.add(note)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Note added'})
        return jsonify({'success': False, 'message': 'No content'}), 400

    # GET request - return notes list
    notes = ProjectNote.query.filter_by(project_id=project.id).order_by(ProjectNote.timestamp.asc()).all()
    notes_data = [{
        'id': n.id,
        'content': n.content,
        'timestamp': n.timestamp.strftime('%Y-%m-%d %H:%M')
    } for n in notes]
    
    return jsonify({'notes': notes_data})

    return jsonify({'notes': notes_data})

# --- Admin Benchmarks ---
def calculate_actual_productivity():
    # Fetch all logs with meaningful data
    logs = DailyLog.query.filter(DailyLog.quantity > 0).all()
    if not logs or len(logs) < 2:
        return None, None # Not enough data for regression

    # Prepare matrices for Least Squares
    # A * x = b
    # A = [[men_count, women_count], ...]
    # b = [quantity, ...]
    # x = [men_rate, women_rate]
    
    A = []
    b = []
    
    for log in logs:
        A.append([log.men_count, log.women_count])
        b.append(log.quantity)
        
    try:
        A = np.array(A)
        b = np.array(b)
        
        # Solving Ax = b for x
        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        
        men_rate_actual = max(0, round(x[0], 1))
        women_rate_actual = max(0, round(x[1], 1))
        
        return men_rate_actual, women_rate_actual
    except Exception as e:
        print(f"Regression failed: {e}")
        return None, None

@app.route('/admin/benchmarks', methods=['GET', 'POST'])
@login_required
def admin_benchmarks():
    # Only allow admin access
    if current_user.role != 'admin':
        flash('Access denied. Admin only.')
        return redirect(url_for('dashboard'))
        
    config = BenchmarkConfig.query.first()
    if not config:
        config = BenchmarkConfig()
        db.session.add(config)
        db.session.commit()
        
    if request.method == 'POST':
        try:
            config.target_men = float(request.form.get('target_men'))
            config.target_women = float(request.form.get('target_women'))
            config.last_updated = datetime.utcnow()
            db.session.commit()
            flash('Benchmarks updated successfully.')
        except ValueError:
            flash('Invalid input values.')
            
    # Calculate Actuals
    actual_men, actual_women = calculate_actual_productivity()
    
    return render_template('admin_benchmarks.html', 
                          config=config, 
                          actual_men=actual_men, 
                          actual_women=actual_women)

# --- Initialization ---
def init_db():
    if not os.path.exists('jewelry.db') and not os.path.exists('instance/jewelry.db'):
        # Just to be safe with paths
        pass
        
    db.create_all() # This creates tables if they don't exist
    print("Database tables verified/created.")
    
    # Simple migration for prototype: check if column quantity exists in daily_log
    try:
        import sqlite3
        # Connect to the correct database file
        db_file = 'instance/jewelry.db' if os.path.exists('instance/jewelry.db') else 'jewelry.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check quantity column
        cursor.execute("PRAGMA table_info(daily_log)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'quantity' not in columns:
            print("Migrating database: adding quantity column...")
            cursor.execute("ALTER TABLE daily_log ADD COLUMN quantity INTEGER DEFAULT 0")
            conn.commit()
            
        # Check ProjectGoal columns
        cursor.execute("PRAGMA table_info(project_goal)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'completion_date' not in columns:
             print("Migrating database: adding completion fields to project_goal...")
             cursor.execute("ALTER TABLE project_goal ADD COLUMN completion_date DATE")
             cursor.execute("ALTER TABLE project_goal ADD COLUMN completion_notes TEXT")
             conn.commit()
             
        # Check ProjectNote Link
        
        # Check Benchmark Config
        if not BenchmarkConfig.query.first():
            default_benchmark = BenchmarkConfig(target_men=55.0, target_women=45.0)
            db.session.add(default_benchmark)
            db.session.commit()
            print("Initialized default benchmarks.")
             
        conn.close()
    except Exception as e:
        print(f"Migration check failed (minor if db is new): {e}")
        
    with app.app_context():
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='logwin', role='admin')
            db.session.add(admin)
            
            # Add some default actions
            actions = ['Folding Towers', 'Packing', 'Assembly']
            for act_name in actions:
                if not Action.query.filter_by(name=act_name).first():
                    db.session.add(Action(name=act_name, target_per_hour=100))
            
            db.session.commit()
            print("Default admin and actions created.")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
