-- MySQL Script generated by MySQL Workbench
-- Sat Jan  2 21:48:52 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE DATABASE [IF NOT EXISTS] BrainGenix;

-- -----------------------------------------------------
-- Schema bgdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bgdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bgdb` DEFAULT CHARACTER SET utf8 ;
USE `bgdb` ;

-- -----------------------------------------------------
-- Table `bgdb`.`Neurons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bgdb`.`Neurons` (
  `Neurons_id` BIGINT NOT NULL AUTO_INCREMENT,
  `BrainRegion` VARCHAR(45) NOT NULL,
  `X_coord` INT NULL,
  `Y_coord` INT NULL,
  `Z_coord` INT NULL,
  PRIMARY KEY (`Neurons_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bgdb`.`Synapses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bgdb`.`Synapses` (
  `Synapses_id` BIGINT NOT NULL AUTO_INCREMENT,
  `Neurons_id` BIGINT NOT NULL,
  PRIMARY KEY (`Synapses_id`),
  INDEX `Neuron_fk_idx` (`Neurons_id` ASC) VISIBLE,
  CONSTRAINT `Neuron_fk`
    FOREIGN KEY (`Neurons_id`)
    REFERENCES `bgdb`.`Neurons` (`Neurons_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bgdb`.`SynapseConnections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bgdb`.`SynapseConnections` (
  `SynapseConnections_id` BIGINT NOT NULL AUTO_INCREMENT,
  `Synapses_id` BIGINT NOT NULL,
  `ConnectedToSynapses_id` BIGINT NOT NULL,
  `Strength` INT NULL,
  PRIMARY KEY (`SynapseConnections_id`),
  INDEX `Synapses_fk_idx` (`Synapses_id` ASC) VISIBLE,
  CONSTRAINT `Synapses_fk`
    FOREIGN KEY (`Synapses_id`)
    REFERENCES `bgdb`.`Synapses` (`Synapses_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SynapsesConnection_fk`
    FOREIGN KEY (`Synapses_id`)
    REFERENCES `bgdb`.`Synapses` (`Synapses_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


--insert data into the newly created tables
insert into bgdb.Neurons values (1, 'Cerebellum', 0, 0, 0);
insert into bgdb.Neurons (brainregion, x_coord, y_coord, z_coord) values ('Cerebellum', 1, 0, 0);

insert into bgdb.Synapses (Neurons_id) values (1);
insert into bgdb.Synapses (Neurons_id) values (2);

insert into bgdb.SynapseConnections (synapses_id, connectedtosynapses_id, strength) values (1, 2, 10);
insert into bgdb.SynapseConnections (synapses_id, connectedtosynapses_id, strength) values (1, 3, 9);

--create a user for working on the local database if necessary; swap out real values for 'userName' and 'password'
    CREATE USER 'userName'@'localhost' IDENTIFIED BY 'password';
    GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'userName'@'localhost' WITH GRANT OPTION;

    --user table for application login
    CREATE TABLE IF NOT EXISTS `bgdb`.`User` (
      `User_id` BIGINT NOT NULL AUTO_INCREMENT,
      `User_Name` VARCHAR(45) NOT NULL unique,
      `User_Password` blob not null,
      `First_Name` VARCHAR(45) NOT NULL,
      `Last_Name` VARCHAR(45) NOT NULL,
      PRIMARY KEY (`User_id`))
    ENGINE = InnoDB;

    --sample for encrypting/dectrypting passwords
    insert into bgdb.User (user_name, user_password, first_name, last_name) values ('bleu', aes_encrypt('password_text', 'secret'), 'Brad', 'Leu');

    select user_name, aes_decrypt(`User_Password`, 'secret') as password, first_name, last_name as password from bgdb.User;