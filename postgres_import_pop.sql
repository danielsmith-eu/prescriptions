CREATE TABLE population (population integer, practice varchar(8));
\copy population FROM 'GPListSize_June2012.csv' DELIMITERS ',' CSV;

