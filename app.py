from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

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

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=True)

    def save(self):
        """Save the current object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current object from the database."""
        db.session.delete(self)
        db.session.commit()

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    course = db.Column(db.String(255), nullable=True)  # Make sure this column exists if it's being queried


    def save(self):
        """Save the current object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current object from the database."""
        db.session.delete(self)
        db.session.commit()



class StudentForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    course = StringField('Course', validators=[Optional()])

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


# Customer Routes
@app.route('/customer')
def customer():
    customers = Customer.query.all()
    return render_template('customer/customer.html', data=customers)


@app.route('/customer/add', methods=['GET', 'POST'])
def customer_add():
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        # Validation checks
        if not customer_name or not email or not phone:
            flash('Name, Email, and Phone are required!', 'error')
            return redirect(url_for('customer_add'))

        # Create and save a new customer
        new_customer = Customer(
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address
        )
        new_customer.save()

        flash(f"Customer {customer_name} added successfully!", 'success')
        return redirect(url_for('customer'))

    return render_template('customer/customer_add.html')


@app.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
def customer_edit(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # Fetch customer or return 404
    if request.method == 'POST':
        # Get and validate form data
        customer_name = request.form['customer_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        # Validation checks
        if not customer_name or not email or not phone:
            flash('Name, Email, and Phone are required!', 'error')
            return redirect(url_for('customer_edit', customer_id=customer_id))

        # Update customer fields
        customer.customer_name = customer_name
        customer.email = email
        customer.phone = phone
        customer.address = address
        customer.save()

        flash(f"Customer {customer_name} updated successfully!", 'success')
        return redirect(url_for('customer'))

    return render_template('customer/customer_edit.html', data=customer)


@app.route('/customer/delete/<int:customer_id>', methods=['GET', 'POST'])
def customer_delete(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # Fetch customer or return 404
    if request.method == 'POST':
        customer.delete()
        flash(f"Customer {customer.customer_name} deleted successfully!", 'success')
        return redirect(url_for('customer'))

    return render_template('customer/customer_delete.html', data=customer)



# Student Routes
# Student Routes
@app.route('/student')
def student():
    students = Student.query.all()  # Make sure to use 'Student' with an uppercase 'S'
    return render_template('student/student.html', data=students)

                                    

@app.route('/student/add', methods=['GET', 'POST'])
def student_add():
    form = StudentForm()
    if form.validate_on_submit():
        student_name = form.student_name.data
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        course = request.form['course']


        if not student_name or not email or not phone:
            flash('Name, Email, and Phone are required!', 'error')
            return redirect(url_for('student_add'))

        new_student = Student(
            student_name=student_name,
            email=email,
            phone=phone,
            address=address,
            course=course,
        )
        new_student.save()

        flash(f"Student {student_name} added successfully!", 'success')
        return redirect(url_for('student'))

    return render_template('student/student_add.html', form=form)



@app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
def student_edit(student_id):
    student = Student.query.get_or_404(student_id)  # Fetch student or return 404
    if request.method == 'POST':
        # Get and validate form data
        student_name = request.form['student_name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        address = request.form['address']

        # Validation checks
        if not student_name or not email or not phone or not course:
            flash('Name, Email, Phone, and Course are required!', 'error')
            return redirect(url_for('student_edit', student_id=student_id))

        # Update student fields
        student.student_name = student_name
        student.email = email
        student.phone = phone
        student.course = course
        student.address = address
        student.save()

        flash(f"Student {student_name} updated successfully!", 'success')
        return redirect(url_for('student'))

    return render_template('student/student_edit.html', data=student)


@app.route('/student/delete/<int:student_id>', methods=['GET', 'POST'])
def student_delete(student_id):
    student = Student.query.get_or_404(student_id)  # Fetch student or return 404
    if request.method == 'POST':
        student.delete()
        flash(f"Student {student.student_name} deleted successfully!", 'success')
        return redirect(url_for('student'))

    return render_template('student/student_delete.html', data=student)



# Create the tables in the database (run once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
