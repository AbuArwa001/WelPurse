-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema communitywelfare
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema communitywelfare
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `communitywelfare` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `communitywelfare` ;

-- -----------------------------------------------------
-- Table `communitywelfare`.`members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`members` (
  `memberId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`memberId`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`beneficiaries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`beneficiaries` (
  `beneficiaryId` INT NOT NULL AUTO_INCREMENT,
  `memberId` INT NULL DEFAULT NULL,
  `name` VARCHAR(255) NOT NULL,
  `relationship` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`beneficiaryId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `beneficiaries_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`benefits`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`benefits` (
  `benefitId` INT NOT NULL AUTO_INCREMENT,
  `memberId` INT NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `dateReceived` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`benefitId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `benefits_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`contributions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`contributions` (
  `contributionId` INT NOT NULL AUTO_INCREMENT,
  `memberId` INT NULL DEFAULT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `dateContributed` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`contributionId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `contributions_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`dependents`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`dependents` (
  `dependentId` INT NOT NULL AUTO_INCREMENT,
  `memberId` INT NULL DEFAULT NULL,
  `name` VARCHAR(255) NOT NULL,
  `dateOfBirth` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`dependentId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `dependents_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`welfares`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`welfares` (
  `welfareId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`welfareId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`events` (
  `eventId` INT NOT NULL AUTO_INCREMENT,
  `welfareId` INT NULL DEFAULT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `eventDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`eventId`),
  INDEX `welfareId` (`welfareId` ASC) VISIBLE,
  CONSTRAINT `events_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `communitywelfare`.`welfares` (`welfareId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`roles` (
  `roleId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`roleId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`memberroles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`memberroles` (
  `memberId` INT NOT NULL,
  `roleId` INT NOT NULL,
  PRIMARY KEY (`memberId`, `roleId`),
  INDEX `roleId` (`roleId` ASC) VISIBLE,
  CONSTRAINT `memberroles_ibfk_1`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`),
  CONSTRAINT `memberroles_ibfk_2`
    FOREIGN KEY (`roleId`)
    REFERENCES `communitywelfare`.`roles` (`roleId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`wallets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`wallets` (
  `walletId` INT NOT NULL AUTO_INCREMENT,
  `welfareId` INT NULL DEFAULT NULL,
  `balance` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`walletId`),
  UNIQUE INDEX `welfareId` (`welfareId` ASC) VISIBLE,
  CONSTRAINT `wallets_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `communitywelfare`.`welfares` (`welfareId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`transactions` (
  `transactionId` INT NOT NULL AUTO_INCREMENT,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `transactionType` VARCHAR(255) NULL DEFAULT NULL,
  `dateTransaction` DATE NULL DEFAULT NULL,
  `walletId` INT NULL DEFAULT NULL,
  PRIMARY KEY (`transactionId`),
  INDEX `Transactions_ibfk_1` (`walletId` ASC) VISIBLE,
  CONSTRAINT `Transactions_ibfk_1`
    FOREIGN KEY (`walletId`)
    REFERENCES `communitywelfare`.`wallets` (`walletId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`transactiontypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`transactiontypes` (
  `typeId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`typeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`transactiontransactiontypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`transactiontransactiontypes` (
  `transactionId` INT NOT NULL,
  `typeId` INT NOT NULL,
  PRIMARY KEY (`transactionId`, `typeId`),
  INDEX `typeId` (`typeId` ASC) VISIBLE,
  CONSTRAINT `transactiontransactiontypes_ibfk_1`
    FOREIGN KEY (`transactionId`)
    REFERENCES `communitywelfare`.`transactions` (`transactionId`),
  CONSTRAINT `transactiontransactiontypes_ibfk_2`
    FOREIGN KEY (`typeId`)
    REFERENCES `communitywelfare`.`transactiontypes` (`typeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`welfarecontributions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`welfarecontributions` (
  `welfareId` INT NOT NULL,
  `contributionId` INT NOT NULL,
  PRIMARY KEY (`welfareId`, `contributionId`),
  INDEX `contributionId` (`contributionId` ASC) VISIBLE,
  CONSTRAINT `WelfareContributions_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `communitywelfare`.`wallets` (`welfareId`),
  CONSTRAINT `welfarecontributions_ibfk_2`
    FOREIGN KEY (`contributionId`)
    REFERENCES `communitywelfare`.`contributions` (`contributionId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `communitywelfare`.`welfaremembers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `communitywelfare`.`welfaremembers` (
  `welfareId` INT NOT NULL,
  `memberId` INT NOT NULL,
  PRIMARY KEY (`welfareId`, `memberId`),
  INDEX `memberId` (`memberId` ASC) VISIBLE,
  CONSTRAINT `welfaremembers_ibfk_1`
    FOREIGN KEY (`welfareId`)
    REFERENCES `communitywelfare`.`welfares` (`welfareId`),
  CONSTRAINT `welfaremembers_ibfk_2`
    FOREIGN KEY (`memberId`)
    REFERENCES `communitywelfare`.`members` (`memberId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
