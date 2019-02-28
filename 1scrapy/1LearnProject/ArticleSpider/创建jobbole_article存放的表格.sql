CREATE TABLE `NewTable` (
`title`  varchar(200) NOT NULL ,
`create_date`  date NULL ,
`url`  varchar(300) NOT NULL ,
`url_object_id`  varchar(50) NOT NULL ,
`front_image_url`  varchar(300) NULL ,
`front_image_path`  varchar(200) NULL DEFAULT 0 ,
`comment_nums`  int(11) NOT NULL ,
`fav_nums`  int(11) NOT NULL DEFAULT 0 ,
`praise_nums`  int(11) NOT NULL DEFAULT 0 ,
`tags`  varchar(100) NULL ,
`content`  longtext NOT NULL ,
PRIMARY KEY (`url_object_id`)
);