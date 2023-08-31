from flask_sqlalchemy import SQLAlchemy

employees = db_session.query(Employee).all()
for employee in employees:
    print(f'{employee.name}さん 勤続{employee.year}年')
