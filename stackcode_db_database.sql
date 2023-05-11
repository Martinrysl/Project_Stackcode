CREATE DATABASE  IF NOT EXISTS `stackcode_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `stackcode_db`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: stackcode_db
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `database`
--

DROP TABLE IF EXISTS `database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(250) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database`
--

LOCK TABLES `database` WRITE;
/*!40000 ALTER TABLE `database` DISABLE KEYS */;
INSERT INTO `database` VALUES (1,'Martinis','martinis@outlook.com','pbkdf2:sha256:600000$gc4IdjBh$e61430bcf1ebc75a48096da807b6d09ca197619b52a2e07d977feb488a01c1bf','2023-05-10 12:54:42','2023-05-10 17:17:55'),(2,'Daniel','daniel@gmail.com','pbkdf2:sha256:600000$uqI0tPse$ad3a4ca13fc582e668ec8a9b5ebcad21b07204c8a65971a31109e570b2f88ef3','2023-05-10 12:56:39','2023-05-10 12:56:39'),(3,'Frank','frank@publisher.com','pbkdf2:sha256:600000$A46NvoHo$33c30b54fdcdf44f370e719b5c6fb51faaa11d3f02d82ca6475b26c16f574ad5','2023-05-10 12:57:18','2023-05-10 12:57:18'),(5,'Juan','juanzo@outlook.com','pbkdf2:sha256:600000$8Ee95C3x$7c746e47884487bda6bd457aeb99d390f05e35467110b5eac85030e44d4e25bc','2023-05-10 18:50:49','2023-05-10 18:50:49'),(6,'Juancho','juanzho@outlook.com','pbkdf2:sha256:600000$go3oT7A3$758526b1773d59bef50d685e2e4a5610bef87852b56101191a699630f0aa0d34','2023-05-10 18:51:33','2023-05-10 18:51:33'),(7,'Juanis','juanzio@outlook.com','pbkdf2:sha256:600000$igEGM5fH$cecc44fb19f70992a20e129a234a92918982e865852fa5a2baba9c3e2c082c80','2023-05-10 18:51:37','2023-05-10 18:51:37'),(8,'Christian','chrisio@outlook.com','pbkdf2:sha256:600000$5epSJ72D$8970dd410a0f6e281670959cbfa02d24abd79841bd0312586bce266b3557c807','2023-05-10 18:52:12','2023-05-10 18:52:12'),(9,'Denis','denis@outlook.com','pbkdf2:sha256:600000$EXpflgCo$d56d5fe8d52986c8499d247eb9cc7feb1e6d52d64e1ad89952d798340eca7984','2023-05-10 18:52:20','2023-05-10 18:52:20'),(10,'Waldo','Waldo@outlook.com','pbkdf2:sha256:600000$EoIZg4J0$aed78ad1c41c751830f16dfcafa21ef20dcd158134c37a6e01a02ae017c6b1ff','2023-05-10 18:52:50','2023-05-10 18:52:50'),(11,'Zack','Zack@outlook.com','pbkdf2:sha256:600000$tpZl8vLg$dd51ebcc974737f0625636a6597aa13dbe1d675104ab6512583e3879c2757143','2023-05-10 18:52:54','2023-05-10 18:52:54'),(12,'Pascual','Pask@outlook.com','pbkdf2:sha256:600000$nONK5VND$c20034bee05d56e383361c4d32862bbf336fbf329c9e81f55e746ba32db939e9','2023-05-10 18:53:29','2023-05-10 18:53:29');
/*!40000 ALTER TABLE `database` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-10 21:35:32
