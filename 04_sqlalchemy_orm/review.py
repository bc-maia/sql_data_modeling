from app import db, Person

if __name__ == "__main__":
    person1 = Person(name="Mr. PotatoHead")
    person2 = Person(name="Ms. PotatoHead")
    person3 = Person(name="PotatoBoy")
    db.session.add(person1)
    db.session.add_all([person2, person3])
    db.session.commit()

    print(Person.query.first())

    boy = Person.query.filter_by(name="PotatoBoy").first()
    print(boy.name)

    print(Person.query.get(4))