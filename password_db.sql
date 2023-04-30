-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema password_manager
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema password_manager
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `password_manager` DEFAULT CHARACTER SET utf8 ;
USE `password_manager` ;

-- -----------------------------------------------------
-- Table `password_manager`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `password_manager`.`users` (
  `user_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `password_manager`.`passwords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `password_manager`.`passwords` (
  `users_user_id` INT NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `site` VARCHAR(50) NOT NULL,
  INDEX `fk_passwords_users_idx` (`users_user_id` ASC) VISIBLE,
  PRIMARY KEY (`users_user_id`),
  CONSTRAINT `fk_passwords_users`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `password_manager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
