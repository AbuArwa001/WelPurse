USE communitywelfare;

-- Drop foreign key constraints (if any)
ALTER TABLE beneficiaries DROP FOREIGN KEY beneficiaries_ibfk_1;
ALTER TABLE benefits DROP FOREIGN KEY benefits_ibfk_1;
ALTER TABLE contributions DROP FOREIGN KEY contributions_ibfk_1;
ALTER TABLE dependents DROP FOREIGN KEY dependents_ibfk_1;
ALTER TABLE memberroles DROP FOREIGN KEY memberroles_ibfk_1;
ALTER TABLE welfaremembers DROP FOREIGN KEY welfaremembers_ibfk_2;

-- -- Rename columns and change their types to VARCHAR(60)
-- ALTER TABLE members CHANGE COLUMN memberId id VARCHAR(60) NOT NULL;
-- ALTER TABLE beneficiaries CHANGE COLUMN beneficiaryId id VARCHAR(60) NOT NULL;
-- ALTER TABLE benefits CHANGE COLUMN benefitId id VARCHAR(60) NOT NULL;
-- ALTER TABLE contributions CHANGE COLUMN contributionId id VARCHAR(60) NOT NULL;
-- ALTER TABLE dependents CHANGE COLUMN dependentId id VARCHAR(60) NOT NULL;
-- ALTER TABLE welfares CHANGE COLUMN welfareId id VARCHAR(60) NOT NULL;
-- ALTER TABLE events CHANGE COLUMN eventId id VARCHAR(60) NOT NULL;
-- ALTER TABLE roles CHANGE COLUMN roleId id VARCHAR(60) NOT NULL;
-- ALTER TABLE wallets CHANGE COLUMN walletId id VARCHAR(60) NOT NULL;
-- ALTER TABLE transactions CHANGE COLUMN transactionId id VARCHAR(60) NOT NULL;
-- ALTER TABLE transactiontypes CHANGE COLUMN typeId id VARCHAR(60) NOT NULL;
-- ALTER TABLE welfarecontributions CHANGE COLUMN welfareId welfare_id VARCHAR(60) NOT NULL;
-- ALTER TABLE welfarecontributions CHANGE COLUMN contributionId contribution_id VARCHAR(60) NOT NULL;
-- ALTER TABLE welfaremembers CHANGE COLUMN welfareId welfare_id VARCHAR(60) NOT NULL;
-- ALTER TABLE welfaremembers CHANGE COLUMN memberId member_id VARCHAR(60) NOT NULL;

-- Re-add primary key constraints
-- ALTER TABLE members ADD PRIMARY KEY (id);
-- ALTER TABLE beneficiaries ADD PRIMARY KEY (id);
ALTER TABLE benefits ADD PRIMARY KEY (id);
ALTER TABLE contributions ADD PRIMARY KEY (id);
ALTER TABLE dependents ADD PRIMARY KEY (id);
ALTER TABLE welfares ADD PRIMARY KEY (id);
ALTER TABLE events ADD PRIMARY KEY (id);
ALTER TABLE roles ADD PRIMARY KEY (id);
ALTER TABLE wallets ADD PRIMARY KEY (id);
ALTER TABLE transactions ADD PRIMARY KEY (id);
ALTER TABLE transactiontypes ADD PRIMARY KEY (id);

-- Re-add foreign key constraints
ALTER TABLE beneficiaries ADD CONSTRAINT beneficiaries_ibfk_1 FOREIGN KEY (memberId) REFERENCES members(id);
ALTER TABLE benefits ADD CONSTRAINT benefits_ibfk_1 FOREIGN KEY (memberId) REFERENCES members(id);
ALTER TABLE contributions ADD CONSTRAINT contributions_ibfk_1 FOREIGN KEY (memberId) REFERENCES members(id);
ALTER TABLE dependents ADD CONSTRAINT dependents_ibfk_1 FOREIGN KEY (memberId) REFERENCES members(id);
ALTER TABLE memberroles ADD CONSTRAINT memberroles_ibfk_1 FOREIGN KEY (memberId) REFERENCES members(id);
ALTER TABLE memberroles ADD CONSTRAINT memberroles_ibfk_2 FOREIGN KEY (roleId) REFERENCES roles(id);
ALTER TABLE welfaremembers ADD CONSTRAINT welfaremembers_ibfk_2 FOREIGN KEY (member_id) REFERENCES members(id);
ALTER TABLE welfarecontributions ADD CONSTRAINT welfarecontributions_ibfk_1 FOREIGN KEY (welfare_id) REFERENCES wallets(id);
ALTER TABLE welfarecontributions ADD CONSTRAINT welfarecontributions_ibfk_2 FOREIGN KEY (contribution_id) REFERENCES contributions(id);
ALTER TABLE transactions ADD CONSTRAINT transactions_ibfk_1 FOREIGN KEY (walletId) REFERENCES wallets(id);
