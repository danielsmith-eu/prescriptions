create table latlon (postcode varchar(10), lat float, lng float);
\copy latlon FROM 'postcode_lat_long.csv' DELIMITERS ',' CSV;

