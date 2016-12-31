create table payload (
     id int(11) NOT NULL AUTO_INCREMENT,
     payload varchar(255),
	   created datetime,
	   node varchar(255),
     dataPoints int,
     data1 varchar(255),
     data2 varchar(255),
     PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
