-- Running PGSQL using Docker (https://hub.docker.com/_/postgres?tab=description)

-- docker run -d \
--     --name pgsql-udacity \
--     -p 5432:5432 \
--     -e POSTGRES_PASSWORD=passwd123 \
--     postgres
--     -v /mnt/c/apps_database/pgsql:/var/lib/postgresql/data \

-- tested using https://sqliteonline.com/

-- creating tables

create table drivers (
  id serial primary key,
  first_name varchar,
  last_name varchar
);

create table vehicles (
  id serial primary key,
  make varchar,
  model varchar,
  driver_id integer references drivers(id)
);

-- adding drivers and vehicles data

INSERT INTO drivers (first_name, last_name) VALUES ('jack', 'sparrow');
INSERT INTO drivers (first_name, last_name) VALUES ('jack', 'black');
INSERT INTO drivers (first_name, last_name) VALUES ('jack', 'skellington');
INSERT INTO drivers (first_name, last_name) VALUES ('jack', 'burton');
INSERT INTO drivers (first_name, last_name) VALUES ('jack', 'frost');

SELECT * FROM drivers;

INSERT INTO vehicles (make, model, driver_id) 
VALUES ('East Indiaman Galleon',
        'Black Pearl', 
        (SELECT id FROM drivers WHERE last_name = 'sparrow'));
        
INSERT INTO vehicles (make, model, driver_id) 
VALUES ('Birdhouse',
        'Skate',
        (SELECT id FROM drivers WHERE last_name = 'black'));

INSERT INTO vehicles (make, model, driver_id) 
VALUES ('Goody Santa Claus',
        'Sleigh Ride',
        (SELECT id FROM drivers WHERE last_name = 'skellington'));
        
INSERT INTO vehicles (make, model, driver_id) 
VALUES ('Freightliner',
        'FLC-120',
        (SELECT id FROM drivers WHERE last_name = 'burton'));

SELECT * FROM drivers;

SELECT * FROM vehicles v
LEFT JOIN drivers d
ON d.id = v.driver_id;


-- SELECT Using limits (https://www.postgresql.org/docs/current/queries-limit.html)
SELECT * FROM drivers
LIMIT 3;


-- removing vehicle from driver 2
-- https://www.postgresql.org/docs/current/sql-delete.html
DELETE FROM vehicles
WHERE vehicles.driver_id IN (SELECT drivers.id FROM drivers WHERE last_name = 'black');

INSERT INTO vehicles (make, model, driver_id) 
VALUES ('Torguga',
        'Barnacle fishing boat', 
        (SELECT id FROM drivers WHERE last_name = 'sparrow'));


SELECT * FROM vehicles
WHERE vehicles.driver_id IN (SELECT drivers.id FROM drivers WHERE last_name = 'sparrow');

-- https://www.postgresql.org/docs/12/tutorial-join.html
SELECT * FROM drivers 
LEFT JOIN vehicles ON vehicles.driver_id = drivers.id
WHERE drivers.id = '2';

SELECT v.make, v.model, d.first_name, d.last_name FROM vehicles v
JOIN drivers d ON d.id = v.driver_id
WHERE d.last_name = 'sparrow';

-- SUM, COUNT https://www.postgresql.org/docs/8.2/functions-aggregate.html
SELECT * FROM drivers d
JOIN vehicle v ON v.

SELECT COUNT(drivers.id) AS Owners FROM vehicles
JOIN drivers ON vehicles.driver_id = drivers.id
WHERE vehicles.make = 'East Indiaman Galleon';

SELECT d.last_name as Owner,  COUNT(v.model) AS Vehicles FROM vehicles v
JOIN drivers d ON d.id = v.driver_id
GROUP BY d.last_name;


-- https://www.postgresqltutorial.com/postgresql-alter-table/
ALTER TABLE vehicles 
ADD COLUMN color varchar;

-- https://www.postgresqltutorial.com/postgresql-update-join/
UPDATE 
    vehicles V
SET 
    color = 'stripped white'
FROM 
    drivers D
WHERE 
    V.driver_id = D.id AND
    D.last_name = 'burton';


-- 
ALTER TABLE drivers
ADD COLUMN alias_name VARCHAR;

ALTER TABLE drivers
ADD COLUMN address VARCHAR;


-- 
update drivers d
set alias_name = 'Captain',
        address = 'All Seas'
WHERE last_name = 'sparrow';

update drivers d
set alias_name = 'Pumpkin King',
	address = 'Halloween Town'
WHERE last_name = 'skellington';

update drivers d
set alias_name = 'JB',
	address = 'Hollywood'
WHERE last_name = 'black';

update drivers d
set alias_name = 'Trucker',
	address = 'Merica'
WHERE last_name = 'burton';

update drivers d
set alias_name = 'Old Zero',
	address = 'Arctic Regions'
WHERE last_name = 'frost';

SELECT * from drivers;


-- https://www.postgresqltutorial.com/postgresql-timestamp/
SET timezone = 'america/sao_paulo';

SHOW timezone;

ALTER TABLE vehicles
ADD COLUMN registered timestamptz;

SELECT * FROM vehicles;

UPDATE vehicles
SET registered = NOW();

SELECT * FROM vehicles;

UPDATE vehicle
SET registered = '2020-06-22 12:10:25-07';


-- https://www.postgresqltutorial.com/postgresql-interval/
