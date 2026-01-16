INSERT INTO books (isbn, title, author, stock, price) VALUES
('9780132350884', 'Clean Code', 'Hashem', 10, 30.00),
('9780201616224', 'The OOP Programmer', 'Ali', 5, 40.00),
('9780131103627', 'The C Programming Language', 'Rami', 3, 50.00);

INSERT INTO customers (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com');

INSERT INTO orders (customer_id) VALUES (1);

INSERT INTO order_items (order_id, isbn, qty) VALUES
(1, '9780132350884', 1); 