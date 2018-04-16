CREATE TABLE `deviceinfo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `equipid` varchar(30) NOT NULL,
  `ipaddress` varchar(30) NOT NULL,
  `status` tinyint DEFAULT 0,
  `delay` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
