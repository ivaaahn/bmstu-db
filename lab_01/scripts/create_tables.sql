\connect labs_db2 labs localhost 5432;

DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS order_statuses CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS order_details CASCADE;
DROP TABLE IF EXISTS customers_addresses CASCADE;
DROP TABLE IF EXISTS restaurants_addresses CASCADE;


CREATE TABLE "restaurants"
(
    "id"     SERIAL PRIMARY KEY,
    "name"   varchar NOT NULL UNIQUE,
    "rating" float   NOT NULL check ( rating >= 0.0 AND rating <= 5.0 )
);

CREATE TABLE "products"
(
    "id"            SERIAL PRIMARY KEY,
    "name"          varchar NOT NULL,
    "price"         float   NOT NULL check ( price >= 0.0 ),
    "restaurant_id" INT     NOT NULL
);

CREATE TABLE "customers"
(
    "id"            SERIAL PRIMARY KEY,
    "first_name"    varchar        NOT NULL,
    "last_name"     varchar,
    "birthdate"     date,
    "email"         varchar UNIQUE,
    "phone_number"  varchar UNIQUE NOT NULL,
    "registered_at" timestamp
);

CREATE TABLE "employees"
(
    "id"             SERIAL PRIMARY KEY,
    "first_name"     varchar        NOT NULL,
    "last_name"      varchar        NOT NULL,
    "employed_since" date           NOT NULL,
    "birthdate"      date,
    "rating"         float          NOT NULL check ( rating >= 0.0 AND rating <= 5.0 ),
    "salary"         float          NOT NULL check ( salary >= 0.0 ),
    "email"          varchar UNIQUE,
    "phone_number"   varchar UNIQUE NOT NULL
);

CREATE TABLE "order_statuses"
(
    "id"   SERIAL PRIMARY KEY,
    "name" varchar UNIQUE NOT NULL
);

CREATE TABLE "orders"
(
    "id"            SERIAL PRIMARY KEY,
    "customer_id"   int,
    "dst_address"   int,
    "src_address"   int,
    "restaurant_id" int,
    "employee_id"   int,
    "created_at"    timestamp DEFAULT (now()),
    "order_number"  int,
    "status"        int
);


CREATE TABLE "order_details"
(
    "order_id"   int NOT NULL,
    "product_id" int NOT NULL,
    "amount"     int NOT NULL check ( amount > 0 )
);

CREATE TABLE "customers_addresses"
(
    "id"          SERIAL PRIMARY KEY,
    "city"        varchar,
    "street"      varchar,
    "house"       int,
    "entrance"    int,
    "floor"       int,
    "flat"        int,
    "customer_id" int
);

CREATE TABLE "restaurants_addresses"
(
    "id"            SERIAL PRIMARY KEY,
    "city"          varchar,
    "street"        varchar,
    "house"         int,
    "restaurant_id" int
);

ALTER TABLE "products"
    ADD FOREIGN KEY ("restaurant_id") REFERENCES "restaurants" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("dst_address") REFERENCES "customers_addresses" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("src_address") REFERENCES "restaurants_addresses" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("restaurant_id") REFERENCES "restaurants" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("employee_id") REFERENCES "employees" ("id");

ALTER TABLE "orders"
    ADD FOREIGN KEY ("status") REFERENCES "order_statuses" ("id");

ALTER TABLE "order_details"
    ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "order_details"
    ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "customers_addresses"
    ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "restaurants_addresses"
    ADD FOREIGN KEY ("restaurant_id") REFERENCES "restaurants" ("id");