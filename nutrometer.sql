-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nutrometer
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `meal_record`
--

DROP TABLE IF EXISTS `meal_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meal_record` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `account_number` int DEFAULT NULL,
  `meal_category` set('Breakfast','Lunch','Dinner','Snack') DEFAULT NULL,
  `meal_date` date DEFAULT NULL,
  `meal_time` time DEFAULT NULL,
  `meal_item` set('carrot','egg','apple') DEFAULT NULL,
  `meal_item_code` int DEFAULT NULL,
  `amount` float(5,1) DEFAULT NULL,
  `measure_unit` set('ml','oz','g') DEFAULT NULL,
  `measure_unit_id` char(10) DEFAULT NULL,
  `magnesium` float(5,1) DEFAULT NULL,
  `calcium` float(5,1) DEFAULT NULL,
  `potassium` float(5,1) DEFAULT NULL,
  `sodium` float(5,1) DEFAULT NULL,
  `phosphorus` float(5,1) DEFAULT NULL,
  `chloride` float(5,1) DEFAULT NULL,
  `choline` float(5,1) DEFAULT NULL,
  `chromium` float(5,1) DEFAULT NULL,
  `copper` float(5,1) DEFAULT NULL,
  `fluoride` float(5,1) DEFAULT NULL,
  `iodine` float(5,1) DEFAULT NULL,
  `iron` float(5,1) DEFAULT NULL,
  `manganese` float(5,1) DEFAULT NULL,
  `molybdenum` float(5,1) DEFAULT NULL,
  `selenium` float(5,1) DEFAULT NULL,
  `zinc` float(5,1) DEFAULT NULL,
  `vitamin_c` float(5,1) DEFAULT NULL,
  `cobalamin` float(5,1) DEFAULT NULL,
  `vitamin_vb12` float(5,1) DEFAULT NULL,
  `thiamine_vb1` float(5,1) DEFAULT NULL,
  `riboflavin_vb2` float(5,1) DEFAULT NULL,
  `niacin_vb3` float(5,1) DEFAULT NULL,
  `pantothenic_acid_vb5` float(5,1) DEFAULT NULL,
  `pyridoxine_vb6` float(5,1) DEFAULT NULL,
  `biotin_vb7` float(5,1) DEFAULT NULL,
  `folate_vb9` float(5,1) DEFAULT NULL,
  `vitamin_d` float(5,1) DEFAULT NULL,
  `vitamin_k` float(5,1) DEFAULT NULL,
  `vitamin_e` float(5,1) DEFAULT NULL,
  `vitamin_a` float(5,1) DEFAULT NULL,
  `proteins` float(5,1) DEFAULT NULL,
  `carbohydrates` float(5,1) DEFAULT NULL,
  `fats` float(5,1) DEFAULT NULL,
  `water` float(5,1) DEFAULT NULL,
  `carbohydrate` float(5,1) DEFAULT NULL,
  `fiber` float(5,1) DEFAULT NULL,
  `linoleic_acid` float(5,1) DEFAULT NULL,
  `alpha_linolenic_acid` float(5,1) DEFAULT NULL,
  `protein` float(5,1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meal_record`
--

LOCK TABLES `meal_record` WRITE;
/*!40000 ALTER TABLE `meal_record` DISABLE KEYS */;
INSERT INTO `meal_record` VALUES (1,NULL,'','2020-01-01','01:00:00','',NULL,1.0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,NULL,'','2020-02-02','02:00:00','',NULL,2.0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,NULL,'','2020-03-03','03:00:00','',NULL,3.0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,NULL,'','2020-04-04','04:00:00','',NULL,4.0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,NULL,NULL,'2020-01-01','15:20:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `meal_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_account`
--

DROP TABLE IF EXISTS `user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_account` (
  `account_number` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `height` float(5,1) DEFAULT NULL,
  `weight` float(5,1) DEFAULT NULL,
  `physical_activity_level` set('Sedentary','Lightly active','Moderately active',' Very active','Extra active') DEFAULT NULL,
  PRIMARY KEY (`account_number`),
  UNIQUE KEY `account_number_UNIQUE` (`account_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_account`
--

LOCK TABLES `user_account` WRITE;
/*!40000 ALTER TABLE `user_account` DISABLE KEYS */;
INSERT INTO `user_account` VALUES (1,'user111','111','Tester_1','Rebel_1','F','1970-01-01',160.0,100.0,NULL),(2,'user222','222','Tester_2','Rebel_2','M','1975-02-02',180.0,140.0,NULL),(3,'user333','333','Tester_3','Rebel_3','M','1980-03-03',185.0,150.0,NULL),(4,'user444','444','Tester_4','Rebel_4','F','1985-04-04',170.0,130.0,NULL),(5,'user444','555','Tester_5',NULL,NULL,NULL,NULL,NULL,NULL),(6,'user555','666','Tester6','Rebel_6','M','1990-09-09',188.0,150.0,NULL),(7,'user555','666','Tester6','Rebel_6','M','1990-09-09',188.0,150.0,NULL);
/*!40000 ALTER TABLE `user_account` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-25 22:26:37