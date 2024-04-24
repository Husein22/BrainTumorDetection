-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 05, 2024 at 01:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `users`
--

-- --------------------------------------------------------

--
-- Table structure for table `doktor`
--

CREATE TABLE `doktor` (
  `doc_id` int(11) NOT NULL,
  `doc_ime` varchar(20) NOT NULL,
  `doc_sifra` varchar(10) NOT NULL,
  `specijalizacija` varchar(20) NOT NULL,
  `user` text NOT NULL DEFAULT 'doktor'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doktor`
--

INSERT INTO `doktor` (`doc_id`, `doc_ime`, `doc_sifra`, `specijalizacija`, `user`) VALUES
(1, 'HuseinCisic', 'prvi', 'neurolog', 'doktor'),
(2, 'IsmoIsmic', 'doctor', 'neurolog', 'doktor');

-- --------------------------------------------------------

--
-- Table structure for table `korsinici`
--

CREATE TABLE `korsinici` (
  `id` int(11) NOT NULL,
  `ime` varchar(40) DEFAULT NULL,
  `sifra` varchar(10) DEFAULT NULL,
  `slika` varchar(100) DEFAULT NULL,
  `rezultat` varchar(40) NOT NULL,
  `uloga` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `medicinske_sestra`
--

CREATE TABLE `medicinske_sestra` (
  `medses_id` int(11) NOT NULL,
  `med_ime` text NOT NULL,
  `med_sifra` text NOT NULL,
  `user` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medicinske_sestra`
--

INSERT INTO `medicinske_sestra` (`medses_id`, `med_ime`, `med_sifra`, `user`) VALUES
(1, 'PajaPajic', '1234', 'sestra');

-- --------------------------------------------------------

--
-- Table structure for table `pacijent`
--

CREATE TABLE `pacijent` (
  `pac_id` int(11) NOT NULL,
  `pac_ime` varchar(20) NOT NULL,
  `pac_sifra` varchar(20) NOT NULL,
  `slika` varchar(40) NOT NULL,
  `rezultat` varchar(100) NOT NULL,
  `doc_id` int(11) NOT NULL,
  `user` text NOT NULL DEFAULT 'pacijent'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pacijent`
--

INSERT INTO `pacijent` (`pac_id`, `pac_ime`, `pac_sifra`, `slika`, `rezultat`, `doc_id`, `user`) VALUES
(1, 'NikoNikic', 'pacijentt', 'no20.jpg', 'NE.Nije pronaden tumor na mozgu', 1, 'pacijent'),
(2, 'HusoHusic', 'pacije', 'no1.jpg', 'NE.Nije pronaden tumor na mozgu', 1, 'pacijent'),
(5, 'DzemoDzemic', 'dzemooo', 'No18.jpg', 'NE.Nije pronaden tumor na mozguu', 1, 'pacijent'),
(6, 'LamijaLama', 'lama', 'pred59.jpg', 'NE.Nije pronađen tumor na mozgu', 2, 'pacijent'),
(7, 'PetkoPetkic', 'petkic', 'pred17.jpg', 'NE.Nije pronaden tumor na mozguu', 1, 'pacijent'),
(8, 'SubotSubtic', 'subtic', 'pred13.jpg', 'DA.Pronađen je tumor na mozgu', 2, 'pacijent'),
(10, 'KlatoKlatic', 'klatic', 'pred19.jpg', 'NE.Nije pronaden tumor na mozgu', 1, 'pacijent'),
(11, 'NoviNovko', 'novii', 'pred19.jpg', 'NE.Nije pronađen tumor na mozgu', 2, 'pacijent'),
(12, 'NahidNahic', 'nahic', 'pred18.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(13, 'LekaLaka', 'laka', 'pred19.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(14, 'RadiRadio', 'radio', 'pred19.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(15, 'EskEsk', 'esk', 'pred17.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(16, 'OmOm', 'om', 'pred18.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(17, 'LepLep', 'lep', 'pred18.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(18, 'NekINeki', 'neki', 'pred19.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(19, 'NoviNovko', 'Mini321', 'pred18.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(20, 'Prvo', 'TajnasIFRA1!', 'pred18.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent'),
(21, 'Lepww', 'lepww1A\"', 'pred19.jpg', 'NE.Nije pronađen tumor na mozgu', 1, 'pacijent');

-- --------------------------------------------------------

--
-- Table structure for table `pregled`
--

CREATE TABLE `pregled` (
  `pr_id` int(11) NOT NULL,
  `doc_id` int(11) NOT NULL,
  `pac_id` int(11) NOT NULL,
  `datum` datetime NOT NULL,
  `odobreno` text NOT NULL,
  `med_id` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pregled`
--

INSERT INTO `pregled` (`pr_id`, `doc_id`, `pac_id`, `datum`, `odobreno`, `med_id`) VALUES
(1, 1, 1, '2024-01-31 00:00:00', 'DA', 1),
(2, 2, 2, '0000-00-00 00:00:00', 'DA', 1),
(15, 2, 1, '2023-12-21 06:48:00', 'DA', 1),
(16, 2, 6, '2024-02-14 19:05:00', '', 1),
(26, 2, 8, '2023-12-13 01:03:00', '', 1),
(27, 2, 6, '2023-12-28 01:03:00', 'DA', 1),
(28, 2, 8, '2023-12-20 01:19:00', '', 1),
(29, 2, 11, '2023-12-08 01:20:00', '', 1),
(30, 2, 8, '2023-12-30 01:23:00', '', 1),
(31, 2, 11, '2023-12-30 01:24:00', '', 1),
(32, 2, 11, '2023-12-31 01:25:00', 'da', 1),
(33, 2, 8, '2023-12-30 01:26:00', 'da', 1),
(34, 2, 8, '2023-12-01 01:32:00', 'da', 1),
(35, 1, 5, '2023-12-21 02:50:00', 'da', 1),
(36, 1, 12, '2024-01-14 02:51:00', 'da', 1),
(37, 1, 5, '2024-01-24 16:45:00', 'da', 1),
(38, 1, 7, '2024-02-22 16:41:00', 'da', 1),
(39, 1, 15, '2024-02-28 17:09:00', 'da', 1),
(40, 2, 6, '2024-01-12 12:20:00', 'da', 1),
(41, 2, 6, '2024-01-30 12:24:00', 'da', 1),
(42, 2, 6, '2024-01-10 12:27:00', 'da', 1),
(43, 2, 6, '2024-01-26 12:27:00', 'da', 1),
(44, 2, 6, '2024-01-23 12:27:00', 'da', 1),
(45, 2, 6, '2024-01-27 12:27:00', 'da', 1),
(46, 2, 6, '2024-01-29 12:32:00', '', 1),
(47, 1, 1, '2024-01-19 17:49:00', '', 1),
(48, 1, 16, '2024-01-18 12:55:00', 'da', 1),
(49, 1, 1, '2024-01-25 13:00:00', '', 1),
(50, 1, 15, '2024-01-26 13:00:00', 'DA', 1),
(52, 1, 1, '2024-01-03 13:20:00', 'da', 1),
(54, 1, 18, '2024-03-06 13:26:00', '', 1),
(55, 2, 6, '2024-01-30 13:37:00', '', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doktor`
--
ALTER TABLE `doktor`
  ADD PRIMARY KEY (`doc_id`);

--
-- Indexes for table `korsinici`
--
ALTER TABLE `korsinici`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `medicinske_sestra`
--
ALTER TABLE `medicinske_sestra`
  ADD PRIMARY KEY (`medses_id`);

--
-- Indexes for table `pacijent`
--
ALTER TABLE `pacijent`
  ADD PRIMARY KEY (`pac_id`);

--
-- Indexes for table `pregled`
--
ALTER TABLE `pregled`
  ADD PRIMARY KEY (`pr_id`),
  ADD KEY `doktorVezanje` (`doc_id`),
  ADD KEY `pacijentVezanje` (`pac_id`),
  ADD KEY `sestraVezanjew` (`med_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doktor`
--
ALTER TABLE `doktor`
  MODIFY `doc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `korsinici`
--
ALTER TABLE `korsinici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT for table `medicinske_sestra`
--
ALTER TABLE `medicinske_sestra`
  MODIFY `medses_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pacijent`
--
ALTER TABLE `pacijent`
  MODIFY `pac_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `pregled`
--
ALTER TABLE `pregled`
  MODIFY `pr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pregled`
--
ALTER TABLE `pregled`
  ADD CONSTRAINT `doktorVezanje` FOREIGN KEY (`doc_id`) REFERENCES `doktor` (`doc_id`),
  ADD CONSTRAINT `pacijentVezanje` FOREIGN KEY (`pac_id`) REFERENCES `pacijent` (`pac_id`),
  ADD CONSTRAINT `sestraVezanjew` FOREIGN KEY (`med_id`) REFERENCES `medicinske_sestra` (`medses_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
