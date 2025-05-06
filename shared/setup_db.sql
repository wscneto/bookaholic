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
('Introduction to Algorithms', 'Cormen, Leiserson, Rivest, and Stein', 'Comprehensive textbook on algorithms.', 89.00, 45, 'https://m.media-amazon.com/images/I/61Mw06x2XcL._SY425_.jpg'),
('Fluent Python', 'Luciano Ramalho', 'Clear, practical guide to Python’s most powerful features.', 45.00, 6, 'https://m.media-amazon.com/images/I/411qhFCwczL._SY445_SX342_.jpg'),
('Deep Learning', 'Ian Goodfellow, Yoshua Bengio, Aaron Courville', 'Fundamentals of deep learning techniques.', 72.00, 14, 'https://m.media-amazon.com/images/I/A10G+oKN3LL._SY522_.jpg'),
('Dom Casmurro', 'Machado de Assis', "Dom Casmurro tells the story of Bento Santiago (Bentinho), who falls in love with Capitu as a teenager, defying the wishes of his mother, Dona Glória, who wanted him to become a priest. The novel explores the couple's turbulent relationship, marked by jealousy and suspicions of betrayal, culminating in a separation and the departure of Capitu and their son, Ezequiel, to Europe.", 39.99, 20, 'https://m.media-amazon.com/images/I/61Sl2sWG7xS._SY522_.jpg'),
('The Brothers Karamazov', 'Fyodor Dostoyevsky', "Fyodor Dostoyevsky's powerful meditation on faith, meaning and morality.", 99.59, 39, 'https://m.media-amazon.com/images/I/81IE8AwMvqL._SY522_.jpg'),
('Crime and Punishment', 'Fyodor Dostoyevsky', "Raskolnikov, a destitute and desperate former student, wanders through the slums of St Petersburg and commits a random murder without remorse or regret.", 27.49, 25, 'https://m.media-amazon.com/images/I/81bAXZAp-GL._SY522_.jpg'),
('The Count of Monte Crist', 'Alexandre Dumas', "Thrown in prison for a crime he has not committed, Edmond Dantes is confined to the grim fortress of if.", 62.29, 9, 'https://m.media-amazon.com/images/I/41EiXfNY6wL._SY445_SX342_.jpg'),
('The Picture of Dorian Gray', 'Oscar Wilde', "An astounding novel of decadence and the secret live within from one of Ireland's greatest writers", 20.00, 17, 'https://m.media-amazon.com/images/I/61FdXlJX0-L._SY522_.jpg'),
('Pride and Prejudice', 'Jane Austen', "Austen's most popular novel, the unforgettable story of Elizabeth Bennet and Mr. Darcy.", 24.79, 26, 'https://m.media-amazon.com/images/I/81NLDvyAHrL._SY522_.jpg'),
('The Adventures of Tom Sawyer', 'Mark Twain', "Whether forming a pirate gang to search for buried treasure or spending a quiet time at home, sharing his medicine with Aunt Polly's cat, the irrepressible Tom Sawyer evokes the world of boyhood in nineteenth century rural America.", 19.89, 20, 'https://m.media-amazon.com/images/I/819Z9rCY2FL._SY522_.jpg'),
('The Adventures Of Sherlock Holmes', 'Sir Arthur Conan Doyle', "Literature's greatest detective team investigates adozen of their best-known cases, including The Speckled Band, The Red-Headed League, The Five Orange Pips, and A Scandal in Bohemia.", 33.00, 7, 'https://m.media-amazon.com/images/I/91X7AWlxegL._SY522_.jpg'),
('Dubliners', 'James Joyce', "James Joyce's Dubliners is a vivid and unflinching portrait of 'dear dirty Dublin' at the turn of the twentieth century.", 76.19, 12, 'https://m.media-amazon.com/images/I/81qqdM42mmL._SY522_.jpg'),
('The Complete Works of William Shakespeare', 'William Shakespeare', "No library is complete without the classics! This leather-bound edition includes the complete works of the playwright and poet William Shakespeare, considered by many to be the English language's greatest writer.", 157.76, 5, 'https://m.media-amazon.com/images/I/5166F6oMO0L._SY445_SX342_.jpg'),
('Confessions', 'Saint Augustine of Hippo', "In his own day the dominant personality of the Western Church, Augustine of Hippo today stands as perhaps the greatest thinker of Christian antiquity, and his Confessions is one of the great works of Western literature.", 100.55, 14, 'https://m.media-amazon.com/images/I/81kMWeENuVL._SY522_.jpg'),
('The Elements', 'Euclid', "The Elements is a mathematical treatise written c. 300 BC by the Ancient Greek mathematician Euclid.", 216.00, 3, 'https://m.media-amazon.com/images/I/716lhzVPBhL._SY522_.jpg');
