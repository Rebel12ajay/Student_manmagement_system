from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        age = request.form["age"]

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COALESCE(MAX(id), 100) + 1 FROM students")
        student_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO students (id, name, email, course, age) VALUES (?, ?, ?, ?, ?)",
            (student_id, name, email, course, age)
        )

        connection.commit()
        connection.close()

        return redirect("/students")

    return render_template("add_student.html")
@app.route("/students")
def view_students():

    search = request.args.get("search", "")

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM students
            WHERE CAST(id AS TEXT) LIKE ?
               OR name LIKE ?
               OR course LIKE ?
            ORDER BY id
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))
    else:
        cursor.execute("SELECT * FROM students ORDER BY id")

    students = cursor.fetchall()

    connection.close()

    return render_template("view_students.html", students=students)

@app.route("/delete/<int:id>")
def delete_student(id):

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    connection.commit()
    connection.close()

    return redirect("/students")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        age = request.form["age"]

        cursor.execute("""
            UPDATE students
            SET name = ?, email = ?, course = ?, age = ?
            WHERE id = ?
        """, (name, email, course, age, id))

        connection.commit()
        connection.close()

        return redirect("/students")

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    connection.close()

    return render_template("edit_student.html", student=student)
if __name__ == "__main__":
    app.run(debug=True)