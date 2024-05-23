-- Dummy data for `members`
-- INSERT INTO `welpurse`.`members` (`id`, `name`, `email`, `password`)
-- VALUES
-- ('1', 'John Doe', 'john.doe@example.com', 'hashedpassword123'),
-- ('2', 'Jane Smith', 'jane.smith@example.com', 'hashedpassword456');

-- Dummy data for `beneficiaries`
-- INSERT INTO `welpurse`.`beneficiaries` (`id`, `member_id`, `name`, `relation`)
-- VALUES
-- ('1', '1', 'Jane Doe', 'Spouse'),
-- ('2', '2', 'John Smith', 'Son');

-- -- Dummy data for `benefits`
-- INSERT INTO `welpurse`.`benefits` (`id`, `member_id`, `description`, `amount`, `date_received`)
-- VALUES
-- ('1', '1', 'Medical Expense Reimbursement', '120.00', '2024-05-01'),
-- ('2', '2', 'Annual Bonus', '500.00', '2024-05-10');

-- -- Dummy data for `contributions`
-- INSERT INTO `welpurse`.`contributions` (`id`, `member_id`, `amount`, `date_contributed`)
-- VALUES
-- ('1', '1', '150.00', '2024-04-15'),
-- ('2', '2', '200.00', '2024-04-15');

-- -- Dummy data for `dependents`
-- INSERT INTO `welpurse`.`dependents` (`id`, `member_id`, `name`, `date_of_birth`)
-- VALUES
-- ('1', '1', 'Jimmy Doe', '2010-06-15'),
-- ('2', '2', 'Amelia Smith', '2012-08-21');

-- -- Dummy data for `welfares`
-- INSERT INTO `welpurse`.`welfares` (`id`, `name`, `description`)
-- VALUES
-- ('1', 'General Welfare Fund', 'Fund for general welfare activities'),
-- ('2', 'Education Fund', 'Support for educational activities');

-- -- Dummy data for `events`
-- INSERT INTO `welpurse`.`events` (`id`, `welfare_id`, `title`, `description`, `event_date`)
-- VALUES
-- ('1', '1', 'Annual Meetup', 'Annual gathering for all members', '2024-12-01'),
-- ('2', '2', 'Scholarship Awards', 'Awarding scholarships to eligible members', '2024-09-01');

-- -- Dummy data for `roles`
-- INSERT INTO `welpurse`.`roles` (`id`, `name`)
-- VALUES
-- ('1', 'President'),
-- ('2', 'Treasurer');

-- -- Dummy data for `memberroles`
-- INSERT INTO `welpurse`.`memberroles` (`member_id`, `role_id`)
-- VALUES
-- ('1', '1'),
-- ('2', '2');

-- -- Dummy data for `wallets`
-- INSERT INTO `welpurse`.`wallets` (`id`, `welfare_id`, `balance`)
-- VALUES
-- ('1', '1', '1000.00'),
-- ('2', '2', '500.00');

-- -- Dummy data for `transactions`
-- INSERT INTO `welpurse`.`wallet_transactions` (`id`, `amount`, `transaction_type`, `date_transaction`, `wallet_id`)
-- VALUES
-- ('1', '150.00', 'Contribution', '2024-04-15', '1'),
-- ('2', '200.00', 'Contribution', '2024-04-15', '2');

-- -- Dummy data for `transactiontypes`
-- INSERT INTO `welpurse`.`transactiontypes` (`id`, `name`)
-- VALUES
-- ('1', 'Contribution'),
-- ('2', 'Benefit');

-- -- Dummy data for `transactiontransactiontypes`
-- INSERT INTO `welpurse`.`transaction_transaction_types` (`transaction_id`, `type_id`)
-- VALUES
-- ('1', '1'),
-- ('2', '1');

-- Dummy data for `welfarecontributions`
-- INSERT INTO `welpurse`.`welfarecontributions` (`welfare_id`, `contribution_id`)
-- VALUES
-- ('1', '1'),
-- ('2', '2');

-- Dummy data for `welfaremembers`
INSERT INTO `welpurse`.`welfaremembers` (`welfare_id`, `member_id`)
VALUES
('1', '1'),
('2', '2');
