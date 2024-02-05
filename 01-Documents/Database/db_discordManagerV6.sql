-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Mon Feb  5 16:43:40 2024 
-- * LUN file: E:\Development\01-Github\www\projects\P-DiscordManager\01-Documents\Database\db_discordManager.lun 
-- * Schema: MLD/6-1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database DiscordManagerV6;
use DiscordManagerV6;


-- Tables Section
-- _____________ 

create table server (
     id_server bigint not null auto_increment,
     guildID bigint not null,
     name varchar(150) not null,
     constraint ID_erver_ID primary key (id_server));

create table file (
     id_file bigint not null auto_increment,
     name varchar(255) not null,
     path varchar(500) not null,
     fk_server bigint not null,
     constraint ID_file_ID primary key (id_file));

create table image (
     id_file bigint not null,
     constraint FKfil_ima_ID primary key (id_file));

create table music (
     id_file bigint not null,
     constraint FKfil_mus_ID primary key (id_file));

create table note (
     id_note bigint not null auto_increment,
     title varchar(100) not null,
     text varchar(255) not null,
     fk_noteList bigint not null,
     constraint ID_note_ID primary key (id_note));

create table noteList (
     id_noteList bigint not null auto_increment,
     name varchar(100) not null,
     fk_file bigint,
     fk_server bigint not null,
     constraint ID_noteList_ID primary key (id_noteList));

create table playlist (
     id_playlist bigint not null auto_increment,
     name varchar(255) not null,
     description varchar(500) not null,
     fk_file bigint,
     fk_server bigint not null,
     constraint ID_playlist_ID primary key (id_playlist));

create table channel (
     id_channel bigint not null auto_increment,
     channelID bigint not null,
     fk_channelType bigint not null,
     fk_server bigint not null,
     constraint ID_channel_ID primary key (id_channel));

create table channelType (
     id_channelType bigint not null auto_increment,
     name varchar(100) not null,
     constraint ID_channelType_ID primary key (id_channelType));

create table distantServer (
     id_distantServer bigint not null auto_increment,
     adress varchar(255) not null,
     port bigint not null,
     fk_server bigint not null,
     constraint ID_distantServer_ID primary key (id_distantServer));

create table music_playlist (
     id_file bigint not null,
     id_playlist bigint not null,
     constraint ID_music_playlist_ID primary key (id_file, id_playlist));


-- Constraints Section
-- ___________________ 

alter table file add constraint FKhave_FK
     foreign key (fk_server)
     references server (id_server);

alter table image add constraint FKfil_ima_FK
     foreign key (id_file)
     references file (id_file);

alter table music add constraint FKfil_mus_FK
     foreign key (id_file)
     references file (id_file);

alter table note add constraint FKpossess_FK
     foreign key (fk_noteList)
     references noteList (id_noteList);

alter table noteList add constraint FKmaybe_contains_FK
     foreign key (fk_file)
     references image (id_file);

alter table noteList add constraint FKcontains_FK
     foreign key (fk_server)
     references server (id_server);

-- Not implemented
-- alter table playlist add constraint ID_playlist_CHK
--     check(exists(select * from music_playlist
--                  where music_playlist.id_playlist = id_playlist)); 

alter table playlist add constraint FKmaybe_include_FK
     foreign key (fk_file)
     references image (id_file);

alter table playlist add constraint FKbe_in_FK
     foreign key (fk_server)
     references server (id_server);

alter table channel add constraint FKis_FK
     foreign key (fk_channelType)
     references channelType (id_channelType);

alter table channel add constraint FKget_FK
     foreign key (fk_server)
     references server (id_server);

alter table distantServer add constraint FKposess_FK
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

create unique index ID_erver_IND
     on server (id_server);

create unique index ID_file_IND
     on file (id_file);

create index FKhave_IND
     on file (fk_server);

create unique index FKfil_ima_IND
     on image (id_file);

create unique index FKfil_mus_IND
     on music (id_file);

create unique index ID_note_IND
     on note (id_note);

create index FKpossess_IND
     on note (fk_noteList);

create unique index ID_noteList_IND
     on noteList (id_noteList);

create index FKmaybe_contains_IND
     on noteList (fk_file);

create index FKcontains_IND
     on noteList (fk_server);

create unique index ID_playlist_IND
     on playlist (id_playlist);

create index FKmaybe_include_IND
     on playlist (fk_file);

create index FKbe_in_IND
     on playlist (fk_server);

create unique index ID_channel_IND
     on channel (id_channel);

create index FKis_IND
     on channel (fk_channelType);

create index FKget_IND
     on channel (fk_server);

create unique index ID_channelType_IND
     on channelType (id_channelType);

create unique index ID_distantServer_IND
     on distantServer (id_distantServer);

create index FKposess_IND
     on distantServer (fk_server);

create unique index ID_music_playlist_IND
     on music_playlist (id_file, id_playlist);

create index FKmus_pla_IND
     on music_playlist (id_playlist);

