
DROP TABLE IF EXISTS `DB_FS`.`Locations`;
CREATE TABLE `DB_FS`.`Locations` (
  `inodeSN` INT NOT NULL,
  `parentinode` INT NULL,
  `filepath` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`inodeSN`));

DROP TABLE IF EXISTS `DB_FS`.`Metadata`;
CREATE TABLE `DB_FS`.`Metadata` (
  `inodeSN` INT NOT NULL,
  `mode` INT NOT NULL,
  `deviceID` INT NOT NULL,
  `size` INT NOT NULL,
  `ctime` INT NULL,
  `mtime` INT NULL,
  `atime` INT NULL,
  PRIMARY KEY (`inodeSN`));


DROP TABLE IF EXISTS `DB_FS`.`Content`;
CREATE TABLE `DB_FS`.`Content` (
  `inodeSN` INT NOT NULL,
  `sequence` VARCHAR(45) NOT NULL,
  `data` LONGBLOB NOT NULL,
  PRIMARY KEY (`inodeSN`, `sequence`));



ALTER TABLE `DB_FS`.`Metadata` 
ADD INDEX `SIZE` (`size` ASC) VISIBLE,
ADD INDEX `CREATION DATE` (`ctime` ASC) VISIBLE;

ALTER TABLE `DB_FS`.`Metadata` 
ADD CONSTRAINT `fk_Metadata_1`
  FOREIGN KEY (`inodeSN`)
  REFERENCES `DB_FS`.`Locations` (`inodeSN`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `DB_FS`.`Content` 
ADD CONSTRAINT `fk_Content_1`
  FOREIGN KEY (`inodeSN`)
  REFERENCES `DB_FS`.`Locations` (`inodeSN`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
