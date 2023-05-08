#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # READ RECORDS
    students1 = session.query(Student)
    print([student for student in students1])
    #OR
    students = session.query(Student).all()
    print(students)

    #SELECT CERTAIN COLUMNS
    names = session.query(Student.name).all()
    print(names)

    #ORDERING
    students_by_name = session.query(Student.name).order_by(Student.name).all()
    print(students_by_name)
    
    #IN DESCENDING ORDER
    students_by_grade_desc = session.query(Student.name, Student.grade).order_by(desc(Student.grade)).all()
    print(students_by_grade_desc)

    #LIMITING
    oldest_student = session.query(Student.name, Student.birthday).order_by(Student.birthday).limit(1).all()
    print(oldest_student)

    #FIRST() METHOD - quick way to execute a limit(1)
    oldest_student2 = session.query(Student.name, Student.birthday).order_by(Student.birthday).first()
    print(oldest_student2)

    #FUNC - from sqlalchemy i.e. sum() and count()
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    #FILTERING
    query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11).all()

    for record in query:
        print(record.name)

    #UPDATING
    for student in session.query(Student):
        student.grade += 1

    session.commit()
    print([(student.name, student.grade) for student in session.query(Student)])

    #UPDATE() CAN UPDATE WITHOUT CREATING OBJECTS FIRST
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    #DELETING DATA
    # query = session.query(Student).filter(Student.name == "Albert Einstein")
    # albert = query.first()
    # session.delete(albert)
    # session.commit()

    #OR
    # query = session.query(Student).filter(Student.name == "Albert Einstein")
    # query.delete()
    