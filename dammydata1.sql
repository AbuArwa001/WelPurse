-- Inserting dummy data into `members`
INSERT INTO `welpurse`.`members` (`id`, `name`, `email`, `password`) VALUES
('M001', 'John Doe', 'john.doe@example.com', 'password123'),
('M002', 'Jane Smith', 'jane.smith@example.com', 'password456');

-- Inserting dummy data into `beneficiaries`
INSERT INTO `welpurse`.`beneficiaries` (`id`, `memberId`, `name`, `relationship`) VALUES
('B001', 'M001', 'Alice Doe', 'Daughter'),
('B002', 'M002', 'Bob Smith', 'Son');

-- Inserting dummy data into `benefits`
INSERT INTO `welpurse`.`benefits` (`id`, `memberId`, `description`, `amount`, `dateReceived`) VALUES
('BE001', 'M001', 'Medical Support', '150.00', '2024-05-01'),
('BE002', 'M002', 'Education Grant', '200.00', '2024-06-01');

-- Inserting dummy data into `contributions`
INSERT INTO `welpurse`.`contributions` (`id`, `memberId`, `amount`, `dateContributed`) VALUES
('C001', 'M001', '50.00', '2024-04-15'),
('C002', 'M002', '75.00', '2024-04-20');

-- Inserting dummy data into `dependents`
INSERT INTO `welpurse`.`dependents` (`id`, `memberId`, `name`, `dateOfBirth`) VALUES
('D001', 'M001', 'Charlie Doe', '2010-03-10'),
('D002', 'M002', 'Diana Smith', '2012-07-24');

-- Inserting dummy data into `welfares`
INSERT INTO `welpurse`.`welfares` (`id`, `name`, `description`) VALUES
('W001', 'Healthcare Fund', 'Fund for medical emergencies and health check-ups'),
('W002', 'Education Fund', 'Support fund for educational purposes');

-- Inserting dummy data into `events`
INSERT INTO `welpurse`.`events` (`id`, `welfareId`, `title`, `description`, `eventDate`) VALUES
('E001', 'W001', 'Annual Health Camp', 'Free health check-up for all members', '2024-08-15'),
('E002', 'W002', 'Scholarship Awards', 'Awarding scholarships to eligible students', '2024-09-10');

-- Inserting dummy data into `roles`
INSERT INTO `welpurse`.`roles` (`id`, `name`) VALUES
('R001', 'Treasurer'),
('R002', 'Secretary');

-- Inserting dummy data into `memberroles`
INSERT INTO `welpurse`.`memberroles` (`memberId`, `roleId`) VALUES
('M001', 'R001'),
('M002', 'R002');

-- Inserting dummy data into `wallets`
INSERT INTO `welpurse`.`wallets` (`id`, `welfareId`, `balance`) VALUES
('WLT001', 'W001', '1000.00'),
('WLT002', 'W002', '1500.00');

-- Inserting dummy data into `transactions`
INSERT INTO `welpurse`.`transactions` (`id`, `amount`, `transactionType`, `dateTransaction`, `walletId`) VALUES
('T001', '100.00', 'Donation', '2024-04-25', 'WLT001'),
('T002', '200.00', 'Donation', '2024-04-30', 'WLT002');

-- Inserting dummy data into `transactiontypes`
INSERT INTO `welpurse`.`transactiontypes` (`id`, `name`) VALUES
('TT001', 'Donation'),
('TT002', 'Expense');

-- Inserting dummy data into `transactiontransactiontypes`
INSERT INTO `welpurse`.`transactiontransactiontypes` (`transactionId`, `typeId`) VALUES
('T001', 'TT001'),
('T002', 'TT002');
SET FOREIGN_KEY_CHECKS=1;