\connect labs_db2 labs localhost 5432;

COPY customers FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/customers.csv' DELIMITER ',' CSV;
COPY customers_addresses FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/customers_addresses.csv' DELIMITER ',' CSV;
COPY employees FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/employees.csv' DELIMITER ',' CSV;
COPY order_statuses FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/order_statuses.csv'  DELIMITER ',' CSV;
COPY restaurants FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/restaurants.csv' DELIMITER ';' CSV;
COPY restaurants_addresses FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/restaurants_addresses.csv' DELIMITER ',' CSV;
COPY products FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/products2.csv' DELIMITER ';' CSV;
COPY orders FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/orders.csv' DELIMITER ',' CSV;
COPY order_details FROM '/home/ivaaahn/dev/bmstu/bmstu-db/lab_01/data/order_details.csv' DELIMITER ',' CSV;
--
