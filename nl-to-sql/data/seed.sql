PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    country TEXT NOT NULL,
    signup_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers VALUES
(1,'Asha Rao','India','2024-01-15'),
(2,'Daniel Smith','USA','2024-03-20'),
(3,'Mei Chen','Singapore','2024-06-11'),
(4,'Olivia Brown','UK','2025-01-08'),
(5,'Arjun Nair','India','2025-02-17');

INSERT INTO products VALUES
(1,'Laptop Pro','Electronics',1200.00),
(2,'Monitor 27','Electronics',400.00),
(3,'Keyboard','Accessories',80.00),
(4,'Headphones','Accessories',150.00),
(5,'Office Chair','Furniture',300.00);

INSERT INTO orders VALUES
(101,1,'2025-01-10'),
(102,2,'2025-02-14'),
(103,1,'2025-03-02'),
(104,3,'2025-04-18'),
(105,4,'2025-05-21'),
(106,5,'2025-06-09'),
(107,2,'2025-07-12'),
(108,1,'2025-08-03');

INSERT INTO order_items VALUES
(1,101,1,1,1200.00),
(2,101,3,2,80.00),
(3,102,2,2,400.00),
(4,103,4,2,150.00),
(5,104,1,1,1200.00),
(6,104,5,1,300.00),
(7,105,2,1,400.00),
(8,106,3,3,80.00),
(9,107,1,1,1200.00),
(10,108,5,2,300.00);
