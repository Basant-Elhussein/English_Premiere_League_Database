CREATE SCHEMA IF NOT EXISTS `PremierLeague`;

CREATE TABLE IF NOT EXISTS Stadium(
	stadiumName VARCHAR(60) NOT NULL PRIMARY KEY,
    recordLeagueAttendance INT,
    capacity INT,
    addressArea VARCHAR(60),
    city VARCHAR(30),
	zipCode VARCHAR(15),
    lengthMeter INT,
    WidthMeter INT,
    buildingDate CHAR(4)
);

CREATE TABLE IF NOT EXISTS Club(
	clubName VARCHAR(60) NOT NULL PRIMARY KEY, 
    website VARCHAR(200) NOT NULL,
    homeStadium VARCHAR(60),
    FOREIGN KEY(homeStadium) REFERENCES Stadium (StadiumName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Player(
	playerID VARCHAR(10) NOT NULL PRIMARY KEY,
	playerName VARCHAR(100) NOT NULL,
    nationality VARCHAR(30) NOT NULL,
    birthDate DATE,
    height INT,
    weight INT,
    `position` VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS ClubPlayers(
	clubName VARCHAR(60) NOT NULL,
    playerID VARCHAR(10) NOT NULL,
    season VARCHAR(10) NOT NULL,
    PRIMARY KEY(clubName, playerID, season),
    FOREIGN KEY(clubName) REFERENCES Club (clubName)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY(playerID) REFERENCES Player (playerID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Match`(
	season VARCHAR(10) NOT NULL,
    homeClub VARCHAR(60) NOT NULL,
    awayClub VARCHAR(60) NOT NULL,
    stadium VARCHAR(60) NOT NULL,
    `date` VARCHAR(20) NOT NULL,
    homePossessions DECIMAL(3, 1) NOT NULL,
    homeRCards INT NOT NULL,
    awayRCards INT NOT NULL,
    homeYCards INT NOT NULL,
    awayYCards INT NOT NULL,
    homeGoals INT NOT NULL,
    awayGoals INT NOT NULL,
    homeFouls INT NOT NULL,
    awayFouls INT NOT NULL,
    homeShots INT NOT NULL,
    awayShots INT NOT NULL,
    PRIMARY KEY (season, homeClub, awayClub),
    FOREIGN KEY(homeClub) REFERENCES Club (clubName)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY(awayClub) REFERENCES Club (clubName)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY(stadium) REFERENCES Stadium (stadiumName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `User`(
	email VARCHAR(60) NOT NULL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    `password` VARCHAR(30) NOT NULL,
    birthDate DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    favoriteClub VARCHAR(60) NOT NULL,
    FOREIGN KEY(favoriteClub) REFERENCES Club (clubName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS MatchReviews(
	userEmail VARCHAR(60) NOT NULL,
	season VARCHAR(10) NOT NULL,
    homeClub VARCHAR(60) NOT NULL,
    awayClub VARCHAR(60) NOT NULL,
    textReview VARCHAR(1200) NOT NULL,
    rate DECIMAL(2, 1) NOT NULL,
    PRIMARY KEY(userEmail, season, homeClub, awayClub),
    FOREIGN KEY(userEmail) REFERENCES `User` (email)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(season, homeClub, awayClub) REFERENCES `Match` (season, homeClub, awayClub)
    ON UPDATE CASCADE ON DELETE CASCADE
);

COMMIT;