
CREATE TABLE pdp (sha varchar(4), pct varchar(3), practice varchar(8), bnf_code varchar(9), bnf_name varchar(40), items integer, nic float, act_cost float, period varchar(6));

CREATE TABLE add (period varchar(6), practice varchar(6), name varchar(41), address varchar(26), street varchar(28), city varchar(26), county varchar(276), postcode varchar(10));

\copy pdp FROM 'T201109PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201109ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201110PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201110ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201111PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201111ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201112PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201112ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201201PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201201ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201202PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201202ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201203PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201203ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201204PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201204ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201205PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201205ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201206PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201206ADD%20REXT.CSV' DELIMITERS ',' CSV;

\copy pdp FROM 'T201207PDP%20IEXT.CSV' DELIMITERS ',' CSV HEADER;
\copy add FROM 'T201207ADD%20REXT.CSV' DELIMITERS ',' CSV;