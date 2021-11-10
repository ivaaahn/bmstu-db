CREATE TABLE IF NOT EXISTS table1
(
    id              INTEGER,
    var1            VARCHAR,
    valid_from_dttm DATE,
    valid_to_dttm   DATE
);

CREATE TABLE IF NOT EXISTS table2
(
    id              INTEGER,
    var2            VARCHAR,
    valid_from_dttm DATE,
    valid_to_dttm   DATE
);

INSERT INTO Table1 (id, var1, valid_from_dttm, valid_to_dttm)
VALUES (1, 'A', '2018-09-01', '2018-09-15'),
       (1, 'B', '2018-09-16', '5999-12-31');

INSERT INTO Table2 (id, var2, valid_from_dttm, valid_to_dttm)
VALUES (1, 'A', '2018-09-01', '2018-09-18'),
       (1, 'B', '2018-09-19', '5999-12-31');


WITH times AS (
    SELECT DISTINCT t1.id,
                    var1,
                    var2,
                    greatest(t1.valid_from_dttm, t2.valid_from_dttm) AS valid_from_dttm,
                    least(t1.valid_to_dttm, t2.valid_to_dttm)        AS valid_to_dttm
    FROM table1 t1
             JOIN table2 t2
                  ON t1.id = t2.id
)
select * from times;

-- SELECT *
-- FROM times
-- WHERE valid_from_dttm <= valid_to_dttm
-- ORDER BY valid_from_dttm;

