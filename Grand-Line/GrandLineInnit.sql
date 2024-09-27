-- --------------------------------------------------------
-- Hôte:                         grandlinedb.cpoc8qswkm6u.eu-north-1.rds.amazonaws.com
-- Version du serveur:           8.0.35 - Source distribution
-- SE du serveur:                Linux
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Listage de la structure de la table grandlinedb. chat
CREATE TABLE IF NOT EXISTS `chat` (
  `mess_id` int NOT NULL AUTO_INCREMENT,
  `ID` int NOT NULL,
  `time` timestamp NOT NULL,
  `expediteur` int NOT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`mess_id`) USING BTREE,
  KEY `FK_expe` (`expediteur`),
  KEY `FK_amitie` (`ID`),
  CONSTRAINT `FK_amitie` FOREIGN KEY (`ID`) REFERENCES `friends` (`ID`),
  CONSTRAINT `FK_expe` FOREIGN KEY (`expediteur`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table grandlinedb. friends
CREATE TABLE IF NOT EXISTS `friends` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `mem_1` int NOT NULL,
  `mem_2` int NOT NULL,
  `valid` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `FK_mem11` (`mem_1`),
  KEY `FK_mem22` (`mem_2`),
  CONSTRAINT `FK_mem11` FOREIGN KEY (`mem_1`) REFERENCES `user` (`id`),
  CONSTRAINT `FK_mem22` FOREIGN KEY (`mem_2`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table grandlinedb. user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `ip` varchar(50) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Les données exportées n'étaient pas sélectionnées.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
