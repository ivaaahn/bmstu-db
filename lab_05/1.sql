-- Вывод только данных, без названий столбцов
\t

-- Отключение выравнивания данных
\a

\o json/employees.json
select row_to_json(e) from employees e;