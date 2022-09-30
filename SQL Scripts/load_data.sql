LOAD DATA INFILE "D:\\College\\Junior\\Spring\\Database Systems\\project 1\\milestone 3\\final_data\\StadiumsTable2.csv" INTO TABLE stadium
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(stadiumName,@recordLeagueAttendance,@capacity,@addressArea,@city,@zipCode,@lengthMeter,@WidthMeter,@buildingDate)
SET
recordLeagueAttendance = NULLIF(@recordLeagueAttendance, ''),
capacity = NULLIF(@capacitystadiumName, ''),
addressArea = NULLIF(@addressArea, ''),
city = NULLIF(@city, ''),
zipcode = NULLIF(@zipcode, ''),
lengthMeter = NULLIF(@lengthMeter, ''),
WidthMeter = NULLIF(@WidthMeter, ''),
buildingDate = NULLIF(@buildingDate, '')
;

LOAD DATA INFILE "D:\\College\\Junior\\Spring\\Database Systems\\project 1\\milestone 3\\final_data\\ClubsTable2.csv" INTO TABLE club
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE "D:\\College\\Junior\\Spring\\Database Systems\\project 1\\milestone 3\\final_data\\PlayersTable2.csv" INTO TABLE player
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(playerID,playerName,nationality,@birthDate,@height,@weight,`position`)
SET
birthDate = STR_TO_DATE(@birthDate,'%d/%m/%Y'),
height = NULLIF(@height, ''),
weight = NULLIF(@weight, '')
;

LOAD DATA INFILE "D:\\College\\Junior\\Spring\\Database Systems\\project 1\\milestone 3\\final_data\\ClubPlayersTable2.csv" INTO TABLE ClubPlayers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE "D:\\College\\Junior\\Spring\\Database Systems\\project 1\\milestone 3\\final_data\\MatchesTable2.csv" INTO TABLE `Match`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

INSERT INTO `User`
VALUES ("basantelhussein@gmail.com", "Basant", "123456", "2001-06-17", "F", "Arsenal");

SELECT username, rate, textReviewFROM matchreviews INNER JOIN `user` ON userEmail = emailWHERE season = '2021/22' AND homeClub = 'Arsenal' AND awayClub = 'Liverpool';






