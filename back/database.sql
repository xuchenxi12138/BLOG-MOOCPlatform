create table student
(
    username varchar(20) primary key,
    password varchar(20) not null
);
create table teacher
(
    username varchar(20) primary key,
    password varchar(20) not null
);
create table admin
(
    username    varchar(20) primary key,
    password    varchar(20) not null,
    super_admin boolean default false
);

create table student_info
(
    username      varchar(10) not null primary key,
    nickname      varchar(20),
    name          varchar(30),
    avatar        varchar(45),
    email         varchar(30),
    gender        enum ('male','female','未知'),
    birthday      varchar(20),
    phone_number  varchar(20),
    college       varchar(20),
    major         varchar(20),
    grade         varchar(20),
    entrance_date varchar(20),
    degree        enum ('bachelor','master','doctor','','null'),
    birth_place   varchar(50)
);

create table teacher_info
(
    username      varchar(20) not null primary key,
    avatar        varchar(45),
    name          varchar(30),
    email         varchar(30),
    gender        enum ('male','female','未知'),
    birthday      date,
    phone_number  varchar(20),
    college       varchar(20),
    major         varchar(20),
    degree        enum ('bachelor','master','doctor','','null'),
    entrance_date varchar(20),
    nickname      varchar(20),
    description   longtext
);

create table admin_info
(
    username     varchar(20) not null primary key,
    name         varchar(30),
    avatar       varchar(45),
    email        varchar(30),
    college      varchar(30),
    gender       enum ('男','女','未知'),
    birthday     date,
    phone_number varchar(20)
);
create table lesson
(
    lesson_id     varchar(36) primary key not null,
    teacher_id    varchar(20)             not null,
    teacher_name  varchar(20),
    lesson_name   varchar(20)             not null,
    lesson_code   varchar(20),
    create_time   timestamp,
    description   longtext,
    cover_id varchar(50) default  "",
    college       varchar(30)
);
create table class
(
    class_id     varchar(36) not null primary key,
    class_name   varchar(20),
    college      varchar(20),
    teacher_id   varchar(36),
    teacher_name varchar(36),
    lesson_id    varchar(20),
    class_code   varchar(20)
);

create table student_list
(
    constraint id primary key (class_id, student_id),
    student_id varchar(20) not null,
    class_id   varchar(36) not null
);

create table lesson_chapter
(
    chapter_id    varchar(36) primary key,
    title         varchar(20),
    lesson_id     varchar(36),
    chapter_index int not null,
    file_id varchar(50),
    video_id varchar(50)
);
create table lesson_subchapter
(
    subchapter_id varchar(36) primary key,
    chapter_id    varchar(36) not null,
    title         varchar(20),
    lesson_id     varchar(36),
    subchapter_index int         not null,
    file_id varchar(50),
    video_id varchar(50)
);

create table blog
(
    title           varchar(50),
    blog_id         varchar(36) primary key,
    blog_owner_id   varchar(36) not null,
    blog_type       varchar(20),
    post_time       datetime,
    blog_owner_name varchar(20),
    content_text    longtext,
    content_html    longtext,
    liked_number    bigint default 0,
    cover           longtext,
    reject boolean default false
);
create table home_recommend_work
(
    id         varchar(36) primary key,
    title      varchar(40),
    url        varchar(50),
    cover_url  varchar(50),
    type       varchar(20),
    author     varchar(30),
    author_url varchar(100),
    time       datetime not null
);

create table like_table
(
    username  varchar(30),
    work_id   varchar(36),
    type      varchar(20),
    post_time datetime,
    constraint id primary key (username, work_id),
    state     boolean
);
create table assignment_q
(
    post_time   datetime,
    id          varchar(36) primary key,
    class_id    varchar(36) not null,
    teacher_id  varchar(36),
    title       varchar(20),
    file_id     varchar(50),
    description longtext,
    deadline    datetime
);
create table assignment_a
(
    hand_on_time  datetime,
    class_id      varchar(36),
    assignment_id varchar(36),
    student_id    varchar(36),
    constraint id primary key (assignment_id, student_id),
    file_id       varchar(50),
    score         float   default 0,
    finished      boolean default false,
    comment       longtext,

);
create table report(
    blog_id varchar(36),
    reporter_id varchar(20),
    identification varchar(20),
    constraint id primary key (blog_id,reporter_id,identification),
    reason varchar(100),
    finish boolean default false,
    comment varchar(100)
);