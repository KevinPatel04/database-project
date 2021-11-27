drop table if exists Appears_for cascade;
drop table if exists Enroll_in cascade;
drop table if exists Attempts cascade;
drop table if exists Questions cascade;
drop table if exists Exam cascade;
drop table if exists Course cascade;
drop type if exists answers cascade;
drop table if exists Users cascade;
drop type if exists roles cascade;

-- enum for roles
create type  roles as enum ('instructor', 'student');

create table Users(
	uid serial primary key,
	firstname varchar(150) not null,
	lastname varchar(150),
	email varchar(150) unique,
	role roles not null,
	username varchar(250) unique not null,
	password varchar(200) not null
);

create table Course(
	cid varchar(10),
	term varchar(11),
	course_title varchar(250) not null,
	primary key (cid,term),
	-- `instructs` relationship
	instructor integer not null,
	foreign key (instructor) references Users(uid)
);

create table Exam(
	eid serial primary key,
	due_date date not null,
	due_time time not null,
	is_released boolean not null default FALSE,
	-- `manages` relationship
	managed_by integer not null,
	-- `conducted for` relationship
	cid varchar(10) not null,
	term varchar(11) not null,
	foreign key (managed_by) references Users(uid),
	foreign key (cid,term) references Course(cid,term)
);

-- enum for answer option
create type  answers as enum ('A', 'B', 'C', 'D');

create table Questions(
	qid serial primary key,
	description text not null,
	opt_answer answers not null,
	opt_a varchar(250) not null,
	opt_b varchar(250) not null,
	opt_c varchar(250) not null,
	opt_d varchar(250) not null,
	points integer not null default 0,
	-- `consists of` relationship
	eid integer not null,
	foreign key (eid) references Exam(eid)
);

create table Attempts(
	adate date,
	atime time,
	primary key(adate,atime)
);

create table Enroll_in(
	cid varchar(10),
	term varchar(11),
	suid integer,
	primary key(cid,term,suid),
	foreign key (suid) references Users(uid),
	foreign key (cid,term) references Course(cid,term)
);

create table Appears_for(
	suid integer,
	eid integer,
	adate date,
	atime time,
	points integer not null,
	primary key(suid,eid,adate,atime),
	foreign key (adate,atime) references Attempts(adate,atime),
	foreign key (suid) references Users(uid)
);