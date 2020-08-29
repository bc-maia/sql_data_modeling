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
