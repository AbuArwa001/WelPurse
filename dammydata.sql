USE `communitywelfare` ;
-- Insert dummy data into `members`
INSERT INTO `members` (name, email, password) VALUES
('John Doe', 'john.doe@example.com', 'password123'),
('Jane Smith', 'jane.smith@example.com', 'password123');

-- Insert dummy data into `beneficiaries`
INSERT INTO `beneficiaries` (memberId, name, relationship) VALUES
(1, 'Alice Doe', 'Daughter'),
(2, 'Bob Smith', 'Son');

-- Insert dummy data into `benefits`
INSERT INTO `benefits` (memberId, description, amount, dateReceived) VALUES
(1, 'Medical Assistance', 100.00, '2024-05-01'),
(2, 'Educational Grant', 200.00, '2024-05-02');

-- Insert dummy data into `contributions`
INSERT INTO `contributions` (memberId, amount, dateContributed) VALUES
(1, 50.00, '2024-05-03'),
(2, 75.00, '2024-05-04');

-- Insert dummy data into `welfares`
INSERT INTO `welfares` (name, description) VALUES
('Health and Wellness', 'Supporting health-related initiatives'),
('Education Fund', 'Providing educational scholarships');

-- Insert dummy data into `events`
INSERT INTO `events` (welfareId, title, description, eventDate) VALUES
(1, 'Health Fair', 'Annual health fair for community members', '2024-06-01'),
(2, 'Scholarship Awards', 'Awarding scholarships to outstanding students', '2024-06-02');

-- Insert dummy data into `roles`
INSERT INTO `roles` (name) VALUES
('President'),
('Treasurer');

-- Insert dummy data into `memberroles`
INSERT INTO `memberroles` (memberId, roleId) VALUES
(1, 1),
(2, 2);

-- Insert dummy data into `wallets`
INSERT INTO `wallets` (welfareId, balance) VALUES
(1, 1000.00),
(2, 1500.00);

-- Insert dummy data into `transactions`
INSERT INTO `transactions` (walletId, amount, transactionType, dateTransaction) VALUES
(1, 100.00, 'Donation', '2024-05-05'),
(2, 200.00, 'Donation', '2024-05-06');

-- Insert dummy data into `transactiontypes`
INSERT INTO `transactiontypes` (name) VALUES
('Donation'),
('Expense');
