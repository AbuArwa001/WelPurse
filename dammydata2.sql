-- Insert dummy data into the `members` table
INSERT INTO `welpurse`.`members` (`id`, `name`, `email`, `password`, `created_at`, `updated_at`) VALUES
('m1', 'John Doe', 'john@example.com', 'password123', NOW(), NOW()),
('m2', 'Jane Smith', 'jane@example.com', 'password456', NOW(), NOW());

-- Insert dummy data into the `beneficiaries` table
INSERT INTO `welpurse`.`beneficiaries` (`id`, `memberId`, `name`, `relationship`, `created_at`, `updated_at`) VALUES
('b1', 'm1', 'Emma Doe', 'Daughter', NOW(), NOW()),
('b2', 'm2', 'Michael Smith', 'Son', NOW(), NOW());

-- Insert dummy data into the `benefits` table
INSERT INTO `welpurse`.`benefits` (`id`, `memberId`, `description`, `amount`, `dateReceived`, `created_at`, `updated_at`) VALUES
('ben1', 'm1', 'Health Benefit', 500.00, '2023-05-01', NOW(), NOW()),
('ben2', 'm2', 'Education Benefit', 1000.00, '2023-06-01', NOW(), NOW());

-- Insert dummy data into the `contributions` table
INSERT INTO `welpurse`.`contributions` (`id`, `memberId`, `amount`, `dateContributed`, `created_at`, `updated_at`) VALUES
('c1', 'm1', 100.00, '2023-01-15', NOW(), NOW()),
('c2', 'm2', 150.00, '2023-02-15', NOW(), NOW());

-- Insert dummy data into the `dependents` table
INSERT INTO `welpurse`.`dependents` (`id`, `memberId`, `name`, `dateOfBirth`, `created_at`, `updated_at`) VALUES
('d1', 'm1', 'Emma Doe', '2010-04-10', NOW(), NOW()),
('d2', 'm2', 'Michael Smith', '2012-09-20', NOW(), NOW());

-- Insert dummy data into the `welfares` table
INSERT INTO `welpurse`.`welfares` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES
('w1', 'Health Welfare', 'Provides health-related benefits', NOW(), NOW()),
('w2', 'Education Welfare', 'Supports education expenses', NOW(), NOW());

-- Insert dummy data into the `events` table
INSERT INTO `welpurse`.`events` (`id`, `welfareId`, `title`, `description`, `eventDate`, `created_at`, `updated_at`) VALUES
('e1', 'w1', 'Health Checkup Camp', 'Free health checkups for members', '2023-07-10', NOW(), NOW()),
('e2', 'w2', 'Education Fair', 'Educational resources and scholarships', '2023-08-20', NOW(), NOW());

-- Insert dummy data into the `roles` table
INSERT INTO `welpurse`.`roles` (`id`, `name`, `created_at`, `updated_at`) VALUES
('r1', 'Admin', NOW(), NOW()),
('r2', 'Member', NOW(), NOW());

-- Insert dummy data into the `memberroles` table
INSERT INTO `welpurse`.`memberroles` (`memberId`, `roleId`, `created_at`, `updated_at`) VALUES
('m1', 'r1', NOW(), NOW()),
('m2', 'r2', NOW(), NOW());

-- Insert dummy data into the `wallets` table
INSERT INTO `welpurse`.`wallets` (`id`, `welfareId`, `balance`, `created_at`, `updated_at`) VALUES
('wlt1', 'w1', 5000.00, NOW(), NOW()),
('wlt2', 'w2', 8000.00, NOW(), NOW());

-- Insert dummy data into the `transactions` table
INSERT INTO `welpurse`.`transactions` (`id`, `amount`, `transactionType`, `dateTransaction`, `walletId`, `created_at`, `updated_at`) VALUES
('t1', 500.00, 'Deposit', '2023-03-10', 'wlt1', NOW(), NOW()),
('t2', 300.00, 'Withdrawal', '2023-04-15', 'wlt2', NOW(), NOW());
