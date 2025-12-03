#!/usr/bin/env python3
"""
Load TPC-H data into SQLite database
"""

import sqlite3
import csv
import os
import sys

def load_table(conn, table_name, csv_file, columns):
    """Load a table from CSV file"""
    print(f"Loading {table_name}...", end=" ")
    
    cursor = conn.cursor()
    
    # Read CSV file
    filepath = os.path.join("tpch_data", csv_file)
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return False
    
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            # Skip empty rows
            if not row or all(not cell.strip() for cell in row):
                continue
            # Skip header row if it matches column names
            if row[0] == columns[0]:
                continue
            # Clean and convert data
            cleaned_row = []
            for i, cell in enumerate(row[:len(columns)]):
                cell = cell.strip()
                # Handle empty strings
                if not cell:
                    cleaned_row.append(None)
                else:
                    cleaned_row.append(cell)
            rows.append(cleaned_row)
    
    if not rows:
        print(f"WARNING: No data found in {csv_file}")
        return False
    
    # Prepare insert statement
    placeholders = ','.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
    
    # Insert data
    try:
        cursor.executemany(insert_sql, rows)
        conn.commit()
        count = len(rows)
        print(f"✓ {count} rows loaded")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(f"  First row: {rows[0] if rows else 'None'}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python load_tpch_data.py <database_file>")
        print("Example: python load_tpch_data.py tpch_default.db")
        sys.exit(1)
    
    db_file = sys.argv[1]
    
    print("="*60)
    print(f"Loading TPC-H Data into SQLite: {db_file}")
    print("="*60)
    print()
    
    # Remove existing database
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing {db_file}")
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    
    # Create schema
    print("Creating schema...")
    with open("create_tpch_schema.sql", 'r') as f:
        schema_sql = f.read()
        conn.executescript(schema_sql)
    print("✓ Schema created")
    print()
    
    # Load data in order (respecting foreign keys)
    print("Loading data...")
    print()
    
    # Load in dependency order
    load_table(conn, "region", "region.tbl", 
               ["r_regionkey", "r_name", "r_comment"])
    
    load_table(conn, "nation", "nation.tbl",
               ["n_nationkey", "n_name", "n_regionkey", "n_comment"])
    
    load_table(conn, "customer", "customer.tbl",
               ["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", 
                "c_acctbal", "c_mktsegment", "c_comment"])
    
    load_table(conn, "supplier", "supplier.tbl",
               ["s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone",
                "s_acctbal", "s_comment"])
    
    load_table(conn, "part", "part.tbl",
               ["p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size",
                "p_container", "p_retailprice", "p_comment"])
    
    load_table(conn, "partsupp", "partsupp.tbl",
               ["ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost", "ps_comment"])
    
    load_table(conn, "orders", "orders.tbl",
               ["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate",
                "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"])
    
    load_table(conn, "lineitem", "lineitem.tbl",
               ["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity",
                "l_extendedprice", "l_discount", "l_tax", "l_returnflag", "l_linestatus",
                "l_shipdate", "l_commitdate", "l_receiptdate", "l_shipinstruct",
                "l_shipmode", "l_comment"])
    
    # Analyze tables for query optimizer
    print()
    print("Analyzing tables for query optimizer...")
    conn.execute("ANALYZE")
    print("✓ Analysis complete")
    
    # Get table statistics
    print()
    print("Table Statistics:")
    cursor = conn.cursor()
    tables = ["region", "nation", "customer", "supplier", "part", "partsupp", "orders", "lineitem"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table:12s}: {count:>10,} rows")
    
    conn.close()
    
    print()
    print("="*60)
    print("✓ Data loading complete!")
    print("="*60)
    print()
    print(f"Database: {db_file}")
    print("Ready for TPC-H benchmark queries")

if __name__ == "__main__":
    main()

