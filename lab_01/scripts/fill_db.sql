\connect labs_db labs localhost 5432;

\COPY customers FROM './data/customers.csv' DELIMITER ',' CSV;
\COPY customers_addresses FROM './data/customers_addresses.csv' DELIMITER ',' CSV;
\COPY employees FROM './data/employees.csv' DELIMITER ',' CSV;
\COPY order_statuses FROM './data/order_statuses.csv'  DELIMITER ',' CSV;
\COPY restaurants FROM './data/restaurants.csv' DELIMITER ';' CSV;
\COPY restaurants_addresses FROM './data/restaurants_addresses.csv' DELIMITER ',' CSV;
\COPY products FROM './data/products2.csv' DELIMITER ';' CSV;
\COPY orders FROM './data/orders.csv' DELIMITER ',' CSV;
\COPY order_details FROM './data/order_details.csv' DELIMITER ',' CSV;
