import entry as entry

Base = entry.db.Model


class Staff(Base):
    __tablename__ = 'staffs'
    __table_args__ = (
        # "useexisting": True,

        entry.db.UniqueConstraint(
            'first_name',
            'last_name',
            name='name'
        ),
        {'useexisting':True}

    )

    staff_id = entry.db.Column(entry.db.Integer, primary_key=True)
    gender = entry.db.Column(entry.db.Enum('male', 'female'), default='male', nullable=False)
    name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    password = entry.db.Column(entry.db.String(50), unique=False)
    age = entry.db.Column(entry.db.Integer, nullable=True)
    phone_number = entry.db.Column(entry.db.String(20), nullable=True, unique=True)
    salary = entry.db.Column(entry.db.Float, nullable=False)

    # department=entry.db.Column(entry.db.Enum(''))

    def __init__(self, gender=None, name=None, age=None, phone_number=None,
                 salary=None, password=None, ):
        self.gender = gender
        self.name = name
        self.password = password
        self.age = age
        self.phone_Number = phone_number
        self.salary = salary

    def __repr__(self):
        return '<User %r>' % (self.first_name + self.last_name)


class Patient(Base):
    __tablename__ = 'patients'
    __table_args__ = {"useexisting": True}
    patient_id = entry.db.Column(entry.db.Integer, primary_key=True)
    gender = entry.db.Column(entry.db.Enum('male', 'female'), default='male', nullable=False)
    name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    address = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    life_status = entry.db.Column(entry.db.Enum('recovery', 'dead', 'in_hospital'), unique=False, nullable=False)
    state_of_illness = entry.db.Column(entry.db.Enum('soft', 'urgent', 'very_urgent'), unique=False, nullable=False)
    symptom = entry.db.Column(entry.db.String(20), unique=False, nullable=False)

    # department=entry.db.Column(entry.db.Enum(''))

    def __init__(self, gender=None, name=None,  address=None, life_status=None, state_of_illness=None, symptom=None):
        self.gender = gender
        self.name = name
        self.address = address
        self.life_status = life_status
        self.state_of_illness = state_of_illness
        self.symptom = symptom

    def __repr__(self):
        return '<User %r>' % self.name


if __name__ == '__main__':
    app = entry.create_app()
    # 这里你要回顾一下Flask应该上下文管理了
    # 离线脚本:
    with app.app_context():
        entry.db.drop_all()
        entry.db.create_all()
