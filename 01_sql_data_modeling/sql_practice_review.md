### SQL Practice Exercises

Go to [this SQLFiddle of drivers and
vehicles](http://sqlfiddle.com/#!17/a114f/2), and try practicing SQL
using the exercises below.

#### **Manipulating & Querying Data**

1.  Insert a few records into both drivers and vehicles. Include 3
    records of drivers who have vehicles, belonging in the vehicles
    table.
2.  Select all driver records; select all vehicle records; select only 3
    vehicle records (using
    [LIMIT](http://www.postgresqltutorial.com/postgresql-limit/))
3.  Driver with ID 2 no longer owns any vehicles. Update the database to
    reflect this.
4.  Driver with ID 1 now owns a new vehicle in addition to the previous
    one they owned. Update the database to reflect this.

#### **Joins & Group Bys**

1.  Select all vehicles owned by driver with ID 3.
2.  Select all vehicles owned by driver with name 'Sarah' (without
    knowing their ID).
3.  Show a table of the number of vehicles owned per driver.
4.  Show the number of drivers that own a Nissan model.

#### **Structuring Data**

1.  Add information about vehicle color.
2.  Update all existing vehicle records to have a vehicle color.
3.  Add contact information (email, address) to the drivers table.

#### **Challenges**

Using Timestamps [(see help
here)](http://www.postgresqltutorial.com/postgresql-timestamp/),

1.  Update vehicles table to show date of registration information
2.  The DMV is looking to notify all drivers with a vehicle that needs
    their registration renewed in the next month. If vehicles need to
    renew their vehicles once every year after their date of
    registration, then write a query to fetch all drivers with at least
    1 vehicle that has an *upcoming* renewal in the next month, fetching
    their contact information as well as information about which
    vehicles need renewals. The DMV would like to run this query every
    time they need to contact all drivers that have an upcoming renewal
    in the next month.