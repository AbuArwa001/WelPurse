-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema welpurse
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema welpurse
-- DROP DATABASE  `welpures`;

CREATE SCHEMA IF NOT EXISTS `welpurse` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `welpurse` ;

-- -----------------------------------------------------
-- Table `welpurse`.`members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`members` (
  `id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`beneficiaries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`beneficiaries` (
  `id` VARCHAR(60) NOT NULL,
  `memberId` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `relationship` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `beneficiaries_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`benefits`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`benefits` (
  `id` VARCHAR(60) NOT NULL,
  `memberId` VARCHAR(60) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `dateReceived` DATE NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `benefits_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`contributions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`contributions` (
  `id` VARCHAR(60) NOT NULL,
  `memberId` VARCHAR(60) NOT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `dateContributed` DATE NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `contributions_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`dependents`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`dependents` (
  `id` VARCHAR(60) NOT NULL,
  `memberId` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `dateOfBirth` DATE NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `dependents_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`welfares`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`welfares` (
  `id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`events` (
  `id` VARCHAR(60) NOT NULL,
  `welfareId` VARCHAR(60) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `eventDate` DATE NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `welfareId` (`welfareId` ASC) VISIBLE,
  CONSTRAINT `events_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `welpurse`.`welfares` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`roles` (
  `id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`memberroles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`memberroles` (
  `memberId` VARCHAR(60) NOT NULL,
  `roleId` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`memberId`, `roleId`),
  INDEX `roleId` (`roleId` ASC) VISIBLE,
  CONSTRAINT `memberroles_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`),
  CONSTRAINT `memberroles_ibfk_2`
    FOREIGN KEY (`roleId`)
    REFERENCES `welpurse`.`roles` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`wallets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`wallets` (
  `id` VARCHAR(60) NOT NULL,
  `welfareId` VARCHAR(60) NOT NULL,
  `balance` DECIMAL(10,2) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `welfareId` (`welfareId` ASC) VISIBLE,
  CONSTRAINT `wallets_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `welpurse`.`welfares` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.  `wallet_transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.  `wallet_transactions` (
  `id` VARCHAR(60) NOT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `transactionType` VARCHAR(255) NULL DEFAULT NULL,
  `dateTransaction` DATE NULL DEFAULT NULL,
  `walletId` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `Transactions_ibfk_1` (`walletId` ASC) VISIBLE,
  CONSTRAINT `Transactions_ibfk_1`
    FOREIGN KEY (`walletId`)
    REFERENCES `welpurse`.`wallets` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`transactiontypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`transactiontypes` (
  `id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`transactiontransactiontypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`transactiontransactiontypes` (
  `transactionId` VARCHAR(60) NOT NULL,
  `typeId` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`transactionId`, `typeId`),
  INDEX `typeId` (`typeId` ASC) VISIBLE,
  CONSTRAINT `transactiontransactiontypes_ibfk_1`
    FOREIGN KEY (`transactionId`)
    REFERENCES `welpurse`.  `wallet_transactions` (`id`),
  CONSTRAINT `transactiontransactiontypes_ibfk_2`
    FOREIGN KEY (`typeId`)
    REFERENCES `welpurse`.`transactiontypes` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`welfarecontributions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`welfarecontributions` (
  `welfareId` VARCHAR(60) NOT NULL,
  `contributionId` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`welfareId`, `contributionId`),
  INDEX `contributionId` (`contributionId` ASC) VISIBLE,
  CONSTRAINT `WelfareContributions_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `welpurse`.`wallets` (`id`),
  CONSTRAINT `welfarecontributions_ibfk_2`
    FOREIGN KEY (`contributionId`)
    REFERENCES `welpurse`.`contributions` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `welpurse`.`welfaremembers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `welpurse`.`welfaremembers` (
  `welfareId` VARCHAR(60) NOT NULL,
  `memberId` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`WelfareId`, `memberId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `welfaremembers_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `welpurse`.`welfares` (`id`),
  CONSTRAINT `welfaremembers_ibfk_2`
    FOREIGN KEY (`memberId`)
    REFERENCES `welpurse`.`members` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
