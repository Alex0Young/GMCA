drop table if exists entries;
create table ca_info(
  id integer primary key autoincrement,
  password string not null
)