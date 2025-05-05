-- Create database
DROP DATABASE IF EXISTS bookstore;
CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Books table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    cover_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'created',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Adding some sample books to the 'books' table
INSERT INTO books (title, author, description, price, stock, cover_url) VALUES
('The Pragmatic Programmer', 'Andrew Hunt and David Thomas', 'Classic book on software engineering practices.', 39.99, 10, 'https://m.media-amazon.com/images/I/510NRcB7AAL._SY445_SX342_.jpg'),
('Clean Code', 'Robert C. Martin', 'A handbook of agile software craftsmanship.', 34.50, 8, 'https://m.media-amazon.com/images/I/41bOkXnNBjL._SY445_SX342_.jpg'),
('Introduction to Algorithms', 'Cormen, Leiserson, Rivest, and Stein', 'Comprehensive textbook on algorithms.', 89.00, 5, 'https://m.media-amazon.com/images/I/61Mw06x2XcL._SY425_.jpg'),
('Fluent Python', 'Luciano Ramalho', 'Clear, practical guide to Python’s most powerful features.', 45.00, 6, 'https://m.media-amazon.com/images/I/411qhFCwczL._SY445_SX342_.jpg'),
('Deep Learning', 'Ian Goodfellow, Yoshua Bengio, Aaron Courville', 'Fundamentals of deep learning techniques.', 72.00, 4, 'https://m.media-amazon.com/images/I/A10G+oKN3LL._SY522_.jpg'),
('Dom Casmurro', 'Machado de Assis', 'Dom Casmurro conta a história de Bento Santiago (Bentinho), que se apaixona por Capitu na adolescência, desafiando a vontade da mãe, Dona Glória, que queria que ele fosse padre. O romance explora o relacionamento turbulento do casal, marcado por ciúmes e suspeitas de traição, culminando numa separação e na partida de Capitu e do filho, Ezequiel, para a Europa.', 39.99, 20, 'https://m.media-amazon.com/images/I/61Sl2sWG7xS._SY522_.jpg');
