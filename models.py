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
    first_name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    last_name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    password = entry.db.Column(entry.db.String(50), unique=False)
    birth = entry.db.Column(entry.db.DATE, nullable=True)
    age = entry.db.Column(entry.db.Integer, nullable=True)
    phone_Number = entry.db.Column(entry.db.String(20), nullable=True, unique=True)
    salary = entry.db.Column(entry.db.Float, nullable=False)

    # department=entry.db.Column(entry.db.Enum(''))

    def __init__(self, gender=None, first_name=None, last_name=None, birth=None, age=None, phone_Number=None,
                 salary=None, password=None, ):
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.birth = birth
        self.age = age
        self.phone_Number = phone_Number
        self.salary = salary

    def __repr__(self):
        return '<User %r>' % (self.first_name + self.last_name)


class Patient(Base):
    __tablename__ = 'patients'
    __table_args__ = {"useexisting": True}
    patient_id = entry.db.Column(entry.db.Integer, primary_key=True)
    gender = entry.db.Column(entry.db.Enum('male', 'female'), default='male', nullable=False)
    first_name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    last_name = entry.db.Column(entry.db.String(50), unique=False, nullable=False)
    street_number = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    street_name = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    apt_number = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    city = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    state = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    zip = entry.db.Column(entry.db.String(20), unique=False, nullable=False)
    password = entry.db.Column(entry.db.String(50), unique=False)
    birth = entry.db.Column(entry.db.DATE, nullable=True)
    age = entry.db.Column(entry.db.Integer, nullable=True)
    phone_Number = entry.db.Column(entry.db.String(20), nullable=True, unique=True)
    life_status = entry.db.Column(entry.db.Enum('recovery', 'dead', 'in_hospital'), unique=False, nullable=False)
    state_of_illness = entry.db.Column(entry.db.Enum('soft', 'urgent', 'very_urgent'), unique=False, nullable=False)
    symptom = entry.db.Column(entry.db.String(20), unique=False, nullable=False)

    # department=entry.db.Column(entry.db.Enum(''))

    def __init__(self, gender=None, first_name=None, last_name=None, street_number=None, street_name=None,
                 apt_number=None, city=None, state=None, zip=None, password=None, birth=None,
                 age=None, phone_Number=None, life_status=None, state_of_illness=None, symptom=None):
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.street_name = street_name
        self.street_number = street_number
        self.apt_number = apt_number
        self.city = city
        self.state = state
        self.zip = zip
        self.password = password
        self.birth = birth
        self.age = age
        self.phone_Number = phone_Number
        self.life_status = life_status
        self.state_of_illness = state_of_illness
        self.symptom = symptom

    def __repr__(self):
        return '<User %r>' % (self.first_name + self.last_name)


if __name__ == '__main__':
    app = entry.create_app()
    # 这里你要回顾一下Flask应该上下文管理了
    # 离线脚本:
    with app.app_context():
        entry.db.drop_all()
        entry.db.create_all()
