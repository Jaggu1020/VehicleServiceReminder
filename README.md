# Vehicle Service Reminder and Maintenance Management System

A Flask and MySQL web application to manage vehicle details, service history, and maintenance reminders.

## Features

- Add and view registered vehicles
- Add vehicle service records
- View service history
- Dashboard showing total vehicles, due-soon, and overdue services
- Maintenance reminder page for services due within 7 days
- Delete a vehicle and its related service records
- Safety-related service types: brake inspection, tyre inspection, seat-belt inspection, and airbag warning-light check

## Technologies Used

- Python
- Flask
- MySQL 8.0
- HTML
- CSS
- Jinja2 Templates

## Project Structure

```text
VehicleServiceReminder/
├── app.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── add_vehicle.html
│   ├── vehicles.html
│   ├── add_service.html
│   ├── service_records.html
│   └── reminders.html
└── static/
    └── style.css
```

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/Jaggu1020/VehicleServiceReminder
cd VehicleServiceReminder
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Open MySQL Workbench and run `database.sql`.

4. Create a `.env` file in the project folder using `.env.example` as reference.

5. Add your MySQL password in `.env`.

6. Start the application:

```bash
python app.py
```

7. Open this URL in a browser:

```text
http://127.0.0.1:5000
```

## Database Tables

- `vehicles` — stores vehicle and owner details.
- `service_records` — stores completed service details and future due dates.


## Future Enhancements

- Edit vehicle and service records
- Search functionality
- Email or SMS reminder notifications
- User login system
- Download service-history reports
