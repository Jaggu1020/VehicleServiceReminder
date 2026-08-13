import os
import mysql.connector
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from datetime import date

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    return connection


@app.route("/")
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total_vehicles = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM service_records
        WHERE next_due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
    """)
    due_soon = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM service_records
        WHERE next_due_date < CURDATE()
    """)
    overdue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_vehicles=total_vehicles,
        due_soon=due_soon,
        overdue=overdue
    )

@app.route("/add-vehicle", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        owner_name = request.form["owner_name"]
        registration_number = request.form["registration_number"]
        vehicle_model = request.form["vehicle_model"]
        current_km = request.form["current_km"]

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO vehicles
            (owner_name, registration_number, vehicle_model, current_km)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            owner_name,
            registration_number,
            vehicle_model,
            current_km
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/vehicles")

    return render_template("add_vehicle.html")

@app.route("/vehicles")
def vehicles():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vehicles ORDER BY id DESC")
    vehicle_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("vehicles.html", vehicles=vehicle_list)

@app.route("/add-service", methods=["GET", "POST"])
def add_service():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        vehicle_id = request.form["vehicle_id"]
        service_type = request.form["service_type"]
        last_service_date = request.form["last_service_date"]
        next_due_date = request.form["next_due_date"]
        next_due_km = request.form["next_due_km"]
        notes = request.form["notes"]

        query = """
            INSERT INTO service_records
            (vehicle_id, service_type, last_service_date,
             next_due_date, next_due_km, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            vehicle_id,
            service_type,
            last_service_date,
            next_due_date,
            next_due_km,
            notes
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/service-records")

    cursor.execute("""
        SELECT id, registration_number, vehicle_model
        FROM vehicles
        ORDER BY registration_number
    """)

    vehicle_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("add_service.html", vehicles=vehicle_list)


@app.route("/service-records")
def service_records():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            service_records.service_type,
            service_records.last_service_date,
            service_records.next_due_date,
            service_records.next_due_km,
            vehicles.registration_number
        FROM service_records
        JOIN vehicles
            ON service_records.vehicle_id = vehicles.id
        ORDER BY service_records.id DESC
    """

    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("service_records.html", records=records)

@app.route("/reminders")
def reminders():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            service_records.service_type,
            service_records.next_due_date,
            vehicles.registration_number,
            vehicles.vehicle_model
        FROM service_records
        JOIN vehicles ON service_records.vehicle_id = vehicles.id
        WHERE service_records.next_due_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        ORDER BY service_records.next_due_date
    """)

    reminders_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "reminders.html",
        reminders=reminders_list,
        today=date.today()
    )

@app.route("/delete-vehicle/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/vehicles")
if __name__ == "__main__":
    app.run(debug=True)