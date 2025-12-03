-- TPC-H Schema for SQLite
-- Based on TPC-H specification, adapted for SQLite

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS lineitem;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS partsupp;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS nation;
DROP TABLE IF EXISTS region;

-- Region table (smallest, 5 rows)
CREATE TABLE region (
    r_regionkey INTEGER PRIMARY KEY,
    r_name      TEXT,
    r_comment   TEXT
);

-- Nation table (25 rows)
CREATE TABLE nation (
    n_nationkey INTEGER PRIMARY KEY,
    n_name      TEXT,
    n_regionkey INTEGER,
    n_comment   TEXT,
    FOREIGN KEY (n_regionkey) REFERENCES region(r_regionkey)
);

-- Supplier table
CREATE TABLE supplier (
    s_suppkey   INTEGER PRIMARY KEY,
    s_name      TEXT,
    s_address   TEXT,
    s_nationkey INTEGER,
    s_phone     TEXT,
    s_acctbal   REAL,
    s_comment   TEXT,
    FOREIGN KEY (s_nationkey) REFERENCES nation(n_nationkey)
);

-- Customer table
CREATE TABLE customer (
    c_custkey    INTEGER PRIMARY KEY,
    c_name       TEXT,
    c_address    TEXT,
    c_nationkey  INTEGER,
    c_phone      TEXT,
    c_acctbal    REAL,
    c_mktsegment TEXT,
    c_comment    TEXT,
    FOREIGN KEY (c_nationkey) REFERENCES nation(n_nationkey)
);

-- Part table
CREATE TABLE part (
    p_partkey     INTEGER PRIMARY KEY,
    p_name        TEXT,
    p_mfgr        TEXT,
    p_brand       TEXT,
    p_type        TEXT,
    p_size        INTEGER,
    p_container   TEXT,
    p_retailprice REAL,
    p_comment     TEXT
);

-- Partsupp table (part-supplier relationship)
CREATE TABLE partsupp (
    ps_partkey    INTEGER,
    ps_suppkey    INTEGER,
    ps_availqty   INTEGER,
    ps_supplycost REAL,
    ps_comment    TEXT,
    PRIMARY KEY (ps_partkey, ps_suppkey),
    FOREIGN KEY (ps_partkey) REFERENCES part(p_partkey),
    FOREIGN KEY (ps_suppkey) REFERENCES supplier(s_suppkey)
);

-- Orders table
CREATE TABLE orders (
    o_orderkey      INTEGER PRIMARY KEY,
    o_custkey       INTEGER,
    o_orderstatus   TEXT,
    o_totalprice    REAL,
    o_orderdate     TEXT,
    o_orderpriority TEXT,
    o_clerk         TEXT,
    o_shippriority  INTEGER,
    o_comment       TEXT,
    FOREIGN KEY (o_custkey) REFERENCES customer(c_custkey)
);

-- Lineitem table (largest table)
CREATE TABLE lineitem (
    l_orderkey      INTEGER,
    l_partkey       INTEGER,
    l_suppkey       INTEGER,
    l_linenumber    INTEGER,
    l_quantity      REAL,
    l_extendedprice REAL,
    l_discount      REAL,
    l_tax           REAL,
    l_returnflag    TEXT,
    l_linestatus    TEXT,
    l_shipdate      TEXT,
    l_commitdate    TEXT,
    l_receiptdate   TEXT,
    l_shipinstruct  TEXT,
    l_shipmode      TEXT,
    l_comment       TEXT,
    PRIMARY KEY (l_orderkey, l_linenumber),
    FOREIGN KEY (l_orderkey) REFERENCES orders(o_orderkey),
    FOREIGN KEY (l_partkey) REFERENCES part(p_partkey),
    FOREIGN KEY (l_suppkey) REFERENCES supplier(s_suppkey)
);

-- Create indexes for better query performance
CREATE INDEX idx_lineitem_orderkey ON lineitem(l_orderkey);
CREATE INDEX idx_lineitem_partkey ON lineitem(l_partkey);
CREATE INDEX idx_lineitem_suppkey ON lineitem(l_suppkey);
CREATE INDEX idx_lineitem_shipdate ON lineitem(l_shipdate);
CREATE INDEX idx_orders_custkey ON orders(o_custkey);
CREATE INDEX idx_orders_orderdate ON orders(o_orderdate);
CREATE INDEX idx_customer_nationkey ON customer(c_nationkey);
CREATE INDEX idx_supplier_nationkey ON supplier(s_nationkey);
CREATE INDEX idx_partsupp_partkey ON partsupp(ps_partkey);
CREATE INDEX idx_partsupp_suppkey ON partsupp(ps_suppkey);

