CREATE DATABASE IF NOT EXISTS expense_manager;

USE expense_manager;

-- Table for storing participants (persons)
CREATE TABLE IF NOT EXISTS person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table for storing expenses
CREATE TABLE IF NOT EXISTS expense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    amount DECIMAL(10, 2),
    date DATE,
    payer_id INT,
    FOREIGN KEY (payer_id) REFERENCES person(id)
);

-- Table for linking expenses to participants and tracking amounts due
CREATE TABLE IF NOT EXISTS expense_participant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_id INT,
    person_id INT,
    amount_due DECIMAL(10, 2),
    FOREIGN KEY (expense_id) REFERENCES expense(id),
    FOREIGN KEY (person_id) REFERENCES person(id)
);

-- Table for recording money transfers between participants
CREATE TABLE IF NOT EXISTS transfer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) DEFAULT 'Reimbursement',
    amount DECIMAL(10, 2),
    from_person_id INT,
    to_person_id INT,
    date DATE,
    FOREIGN KEY (from_person_id) REFERENCES person(id),
    FOREIGN KEY (to_person_id) REFERENCES person(id)
);
