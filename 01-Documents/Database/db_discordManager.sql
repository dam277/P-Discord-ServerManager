-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Wed Dec 20 21:29:27 2023 
-- * LUN file: E:\Développement\01-Github\www\projects\P-DiscordManager\01-Documents\Database\db_discordManager.lun 
-- * Schema: MLD/2-1-1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database MLD;
use MLD;


-- Tables Section
-- _____________ 

create table noteList (
     id_noteList bigint not null auto_increment,
     name varchar(100) not null,
     fk_server bigint not null,
     constraint ID_noteList_ID primary key (id_noteList));

create table note (
     id_note bigint not null auto_increment,
     title varchar(100) not null,
     text varchar(255) not null,
     fk_noteList bigint not null,
     constraint ID_note_ID primary key (id_note));

create table server (
     id_server bigint not null auto_increment,
     guildID bigint not null,
     name varchar(150) not null,
     constraint ID_server_ID primary key (id_server));

create table file (
     id_file bigint not null auto_increment,
     name varchar(255) not null,
     path varchar(500) not null,
     fk_server bigint not null,
     constraint ID_file_ID primary key (id_file));

create table music (
     id_file bigint not null,
     constraint FKfil_mus_ID primary key (id_file));

create table playlist (
     id_playlist bigint not null auto_increment,
     name varchar(255) not null,
     fk_server bigint not null,
     constraint ID_playlist_ID primary key (id_playlist));

create table music_playlist (
     id_file bigint not null,
     id_playlist bigint not null,
     constraint ID_music_playlist_ID primary key (id_file, id_playlist));


-- Constraints Section
-- ___________________ 

alter table noteList add constraint FKcontains_FK
     foreign key (fk_server)
     references server (id_server);

alter table note add constraint FKpossess_FK
     foreign key (fk_noteList)
     references noteList (id_noteList);

alter table file add constraint FKhas_FK
     foreign key (fk_server)
     references server (id_server);

alter table music add constraint FKfil_mus_FK
     foreign key (id_file)
     references file (id_file);

-- Not implemented
-- alter table playlist add constraint ID_playlist_CHK
--     check(exists(select * from music_playlist
--                  where music_playlist.id_playlist = id_playlist)); 

alter table playlist add constraint FKis_in_FK
     foreign key (fk_server)
     references server (id_server);

alter table music_playlist add constraint FKmus_pla_FK
     foreign key (id_playlist)
     references playlist (id_playlist);

alter table music_playlist add constraint FKmus_mus
     foreign key (id_file)
     references music (id_file);


-- Index Section
-- _____________ 

create unique index ID_noteList_IND
     on noteList (id_noteList);

create index FKcontains_IND
     on noteList (fk_server);

create unique index ID_note_IND
     on note (id_note);

create index FKpossess_IND
     on note (fk_noteList);

create unique index ID_server_IND
     on server (id_server);

create unique index ID_file_IND
     on file (id_file);

create index FKhas_IND
     on file (fk_server);

create unique index FKfil_mus_IND
     on music (id_file);

create unique index ID_playlist_IND
     on playlist (id_playlist);

create index FKis_in_IND
     on playlist (fk_server);

create unique index ID_music_playlist_IND
     on music_playlist (id_file, id_playlist);

create index FKmus_pla_IND
     on music_playlist (id_playlist);

