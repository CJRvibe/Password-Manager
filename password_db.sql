-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema password_manager
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema password_manager
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `password_manager` DEFAULT CHARACTER SET utf8mb3 ;
USE `password_manager` ;

-- -----------------------------------------------------
-- Table `password_manager`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `password_manager`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `root_password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `password_manager`.`credentials`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `password_manager`.`credentials` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `site` VARCHAR(50) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `encrypted_password` TEXT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_credentials_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_credentials_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `password_manager`.`users` (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = utf8mb3;

USE `password_manager` ;

-- -----------------------------------------------------
-- procedure create_credentials
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_credentials`(
	user_id INT,
    site VARCHAR(50),
    username VARCHAR(50),
    encrypted_password TEXT
)
BEGIN
	INSERT INTO credentials (
    user_id,
    site,
    username,
    encrypted_password
    )
    VALUES (
    user_id,
    site,
    username,
    encrypted_password
    );
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure create_user
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
	name VARCHAR(50),
    email VARCHAR(255),
    root_password VARCHAR(255)
)
BEGIN
INSERT INTO users (name, email, root_password)
VALUES (name, email, root_password);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_credentials
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_credentials`(
	user_id INT
)
BEGIN
	 SELECT c.id, c.user_id, c.site, c.username, c.encrypted_password
     FROM credentials c
     WHERE c.user_id = user_id;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_user
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_user`(
	username VARCHAR(50)
)
BEGIN
	SELECT user_id, name, email, root_password
    FROM users
    WHERE name = username;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure update_credentials
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_credentials`(
	credential_id INT,
    site VARCHAR(50),
    username VARCHAR(50),
    encrypted_password TEXT
)
BEGIN
	UPDATE credentials c
    SET site = IFNULL(site, c.site),
		username = IFNULL(username, c.username),
        encrypted_password = IFNULL(password, c.password)
    WHERE c.id = credential_id;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure update_user
-- -----------------------------------------------------

DELIMITER $$
USE `password_manager`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_user`(
	user_id INT,
    name VARCHAR(50),
    email VARCHAR(255),
    root_password VARCHAR(255)
)
BEGIN
	UPDATE users u
    SET u.name = IFNULL(name, u.name),
		u.email = IFNULL(email, u.email),
        u.root_password = IFNULL(root_password, u.root_password)
	WHERE u.user_id = user_id;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
