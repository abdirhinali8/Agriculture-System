from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@127.0.0.1/admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Used for flash messages

db = SQLAlchemy(app)


# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    user_type = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def save(self):
        """Save the current object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current object from the database."""
        db.session.delete(self)
        db.session.commit()


# Routes
@app.route('/')
def home():
    return render_template('dashboard/index.html')


@app.route('/user')
def user():
    users = User.query.all()
    return render_template('user/user.html', data=users)


@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        user_type = request.form['user_type']
        user_status = "user_status" in request.form  # Checkbox handling

        # Validation checks
        if not username or not fullname or not email or not user_type:
            flash('All fields are required!', 'error')
            return redirect(url_for('user_add'))

        # Create and save a new user
        new_user = User(
            username=username,
            full_name=fullname,
            email=email,
            user_type=user_type,
            is_active=user_status
        )
        new_user.save()

        flash(f"User {username} added successfully!", 'success')
        return redirect(url_for('user'))
    
    return render_template('user/user_add.html')


@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)  # Fetch user or return 404
    if request.method == 'POST':
        # Get and validate form data
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        user_type = request.form['user_type']
        user_status = "user_status" in request.form  # Checkbox handling

        # Validation checks
        if not username or not fullname or not email or not user_type:
            flash('All fields are required!', 'error')
            return redirect(url_for('user_edit', user_id=user_id))

        # Update user fields
        user.username = username
        user.full_name = fullname
        user.email = email
        user.user_type = user_type
        user.is_active = user_status
        user.save()

        flash(f"User {username} updated successfully!", 'success')
        return redirect(url_for('user'))

    return render_template('user/user_edit.html', data=user)


@app.route('/user/delete/<int:user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)  # Fetch user or return 404
    if request.method == 'POST':
        user.delete()
        flash(f"User {user.username} deleted successfully!", 'success')
        return redirect(url_for('user'))
    
    return render_template('user/user_delete.html', data=user)


# Create the tables in the database (run once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
