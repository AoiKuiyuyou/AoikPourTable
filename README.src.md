[:var_set('', """
# Compile command
aoikpourtable -s README.src.md -n aoikpourtable.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikPourTable
Pour data in out of table.

The data pouring process is divided into four steps:
- Input
- Count
- Convert
- Output

Each step uses a plugin to process the data.

Use SQLAlchemy to support a variety of databases.

Tested working with:
- Linux, Windows
- Python 2.7+, 3.5+

![Image](https://raw.githubusercontent.com/AoiKuiyuyou/AoikPourTable/0.1.0/screenshot/screenshot.gif)

## Table of Contents
[:hd_to_key('toc')]\
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikPourTable
```

### Setup via git
Clone this repository to local:
```
git clone https://github.com/AoiKuiyuyou/AoikPourTable
```

In the local repository, run:
```
pip install .
```
Or:
```
python setup.py install
```

### Run program
Run:
```
aoikpourtable
```
Or:
```
python -m aoikpourtable
```
Or:
```
python src/aoikpourtable/aoikpourtable.py
```

## Usage
[:tod()]

### Show help
Run:
```
aoikpourtable --help
```

### Pretend to be busy
Run:
```
aoikpourtable --limit-rows=10000000 --batch-size=10000
```

### Prepare Data and Databases
[:tod()]

#### CSV
Run:
```
for i in {1..10000}; do echo '"0","0","CC","Province","City"' >> ipcity.csv; done
```

#### MySQL
Run:
```
CREATE DATABASE IF NOT EXISTS aoikpourtable;

DROP TABLE IF EXISTS aoikpourtable.ipcity;

CREATE TABLE aoikpourtable.ipcity (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    ip_bgn INT UNSIGNED NOT NULL,
    ip_end INT UNSIGNED NOT NULL,
    country CHAR(2) NOT NULL,
    prov VARCHAR(80) NOT NULL,
    city VARCHAR(80) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET='utf8mb4';

CREATE USER aoik@'%' IDENTIFIED BY 'passwd';

GRANT ALL ON aoikpourtable.* TO aoik@'%';
```

#### PostgreSQL
Run:
```
CREATE DATABASE aoikpourtable;

CREATE SCHEMA IF NOT EXISTS aoikpourtable;

DROP TABLE IF EXISTS aoikpourtable.ipcity;

CREATE TABLE aoikpourtable.ipcity (
    id SERIAL NOT NULL,
    ip_bgn BIGINT NOT NULL,
    ip_end BIGINT NOT NULL,
    country CHAR(2) NOT NULL,
    prov VARCHAR(80) NOT NULL,
    city VARCHAR(80) NOT NULL,
    PRIMARY KEY (id)
);

CREATE USER aoik WITH password 'passwd';

GRANT ALL ON ALL TABLES IN SCHEMA aoikpourtable TO aoik;
GRANT ALL ON ALL SEQUENCES IN SCHEMA aoikpourtable TO aoik;
```

### Stdin to Stdout
Run:
```
cat ipcity.csv | aoikpourtable --input-factory="aoikpourtable.std_io::stdin_factory" --output-factory="aoikpourtable.std_io::stdout_factory" --limit-rows=10
```

### CSV to Stdout
Run:
```
aoikpourtable --input=ipcity.csv --input-factory="aoikpourtable.csv_io::csv_input_factory" --input-args="encoding=utf-8&lineterminator=%0A&delimiter=,&quotechar=%22&quoting=QUOTE_ALL" --output-factory="aoikpourtable.std_io::stdout_factory" --count-factory="aoikpourtable.count_io::count_lines" --count-args="encoding=utf-8" --limit-rows=10
```

### CSV to CSV
Run:
```
aoikpourtable --input=ipcity.csv --input-factory="aoikpourtable.csv_io::csv_input_factory" --input-args="encoding=utf-8&lineterminator=%0A&delimiter=,&quotechar=%22&quoting=QUOTE_ALL" --output="aoikpourtable_output.csv" --output-factory="aoikpourtable.csv_io::csv_output_factory" --output-args="encoding=utf-8&lineterminator=%0A&delimiter=|&quotechar=%22&quoting=QUOTE_MINIMAL" --count-factory="aoikpourtable.count_io::count_lines" --count-args="encoding=utf-8" --limit-rows=5000 --batch-size=1000
```

### CSV to MySQL
Run:
```
aoikpourtable --input=ipcity.csv --input-factory="aoikpourtable.csv_io::csv_input_factory" --input-args="encoding=utf-8&lineterminator=%0A&delimiter=,&quotechar=%22&quoting=QUOTE_ALL" --output="mysql+mysqldb://aoik:passwd@192.168.56.1:3306/aoikpourtable" --output-factory="aoikpourtable.db_io::insert_factory" --output-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --count-factory="aoikpourtable.count_io::count_lines" --count-args="encoding=utf-8" --convert-args="i,i,s,utf-8,utf-8" --limit-rows=5000 --batch-size=1000
```

### MySQL to CSV
Run:
```
aoikpourtable --input="mysql+mysqldb://aoik:passwd@192.168.56.1:3306/aoikpourtable" --input-factory="aoikpourtable.db_io::select_factory" --input-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --output="aoikpourtable_output.csv" --output-factory="aoikpourtable.csv_io::csv_output_factory" --output-args="encoding=utf-8&lineterminator=%0A&delimiter=,&quotechar=%22&quoting=QUOTE_ALL" --limit-rows=5000 --batch-size=1000
```

### MySQL to MySQL
Run:
```
aoikpourtable --input="mysql+mysqldb://aoik:passwd@192.168.56.1:3306/aoikpourtable" --input-factory="aoikpourtable.db_io::select_factory" --input-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --output="mysql+mysqldb://aoik:passwd@192.168.56.1:3306/aoikpourtable" --output-factory="aoikpourtable.db_io::insert_factory" --output-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --convert-args="i,i,s,s,s" --limit-rows=5000 --batch-size=1000
```

### MySQL to PostgreSQL
Run:
```
aoikpourtable --input="mysql+mysqldb://aoik:passwd@192.168.56.1:3306/aoikpourtable" --input-factory="aoikpourtable.db_io::select_factory" --input-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --output="postgresql+psycopg2://aoik:passwd@192.168.56.1:5432/aoikpourtable" --output-factory="aoikpourtable.db_io::insert_factory" --output-args="schema=aoikpourtable&table=ipcity&columns=ip_bgn,ip_end,country,prov,city" --convert-args="i,i,s,s,s" --limit-rows=5000 --batch-size=1000
```
