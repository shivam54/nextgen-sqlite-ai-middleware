#!/usr/bin/env python3
"""
Generate sample TPC-H data for SQLite testing
This creates a small-scale dataset for cache performance testing
"""

import random
import csv
import os

# Scale factor (SF-0.1 = ~100MB, SF-1 = ~1GB)
# For SQLite testing, we'll use SF-0.1 (small scale)
SCALE_FACTOR = 0.1

def generate_region_data():
    """Generate region data (5 rows)"""
    regions = [
        (0, "AFRICA", "lar deposits. blithely final packages cajole."),
        (1, "AMERICA", "hs use ironic, even requests. s"),
        (2, "ASIA", "ges. thinly even pinto beans ca"),
        (3, "EUROPE", "ly final courts cajole furiously final excuse"),
        (4, "MIDDLE EAST", "uickly special accounts cajole carefully blithely close requests. carefully final asymptotes haggle furiousl")
    ]
    return regions

def generate_nation_data():
    """Generate nation data (25 rows)"""
    nations = [
        (0, "ALGERIA", 0, " final accounts. regular deposits wake slyly. "),
        (1, "ARGENTINA", 1, "al foxes promise slyly according to the regular accounts. bold requests alon"),
        (2, "BRAZIL", 1, "y alongside of the pending deposits. carefully special packages are about the ironic forges. slyly special "),
        (3, "CANADA", 1, "eas hang ironic, silent packages. slyly regular packages are furiously over the tithes. fluffily bold"),
        (4, "EGYPT", 4, "y above the carefully unusual theodolites. final dugouts are quickly across the furiously regular d"),
        (5, "ETHIOPIA", 0, "ven packages wake quickly. regu"),
        (6, "FRANCE", 3, "refully final requests. regular, ironi"),
        (7, "GERMANY", 3, "l platelets. regular accounts x-ray: unusual, regular acco"),
        (8, "INDIA", 2, "ss excuses cajole slyly across the packages. deposits print about the packages. furious"),
        (9, "INDONESIA", 2, " slyly express asymptotes. regular deposits haggle slyly. carefully ironic hockey players sleep blithely. carefull"),
        (10, "IRAN", 4, "efully alongside of the slyly final dependencies. "),
        (11, "IRAQ", 4, "nic deposits boost atop the quickly final requests? quickly regula"),
        (12, "JAPAN", 2, "ously. final, express gifts cajole a"),
        (13, "JORDAN", 4, "ic deposits are blithely about the carefully regular pa"),
        (14, "KENYA", 0, " pending excuses haggle furiously deposits. pending, express pinto beans wake fluffily past t"),
        (15, "MOROCCO", 0, "rns. blithely bold courts among the closely regular packages are furiously slyly"),
        (16, "MOZAMBIQUE", 0, "s. ironic, unusual asymptotes wake blithely r"),
        (17, "PERU", 1, "platelets. blithely pending dependencies use fluffily across the even pinto beans. carefully silent accoun"),
        (18, "CHINA", 2, "c dependencies. furiously express notornis sleep slyly regular accounts. ideas sleep. depos"),
        (19, "ROMANIA", 3, "ular asymptotes are about the furious multipliers. express dependencies nag above the ironically ironic account"),
        (20, "SAUDI ARABIA", 4, "ts. silent, brazen instructions eat ironically with ironically ironic"),
        (21, "VIETNAM", 2, "hely enticingly express accounts. even, final "),
        (22, "RUSSIA", 3, " requests against the platelets use never according to the quickly regular pint"),
        (23, "UNITED KINGDOM", 3, "eans boost carefully special requests. accounts are. carefull"),
        (24, "UNITED STATES", 1, "y final packages. slow foxes cajole quickly. quickly silent platelets breach ironic accounts. unusual pinto be")
    ]
    return nations

def generate_customer_data(num_customers):
    """Generate customer data"""
    customers = []
    segments = ["AUTOMOBILE", "BUILDING", "FURNITURE", "MACHINERY", "HOUSEHOLD"]
    
    for i in range(num_customers):
        custkey = i + 1
        name = f"Customer#{custkey:09d}"
        address = f"Address {random.randint(1, 1000)}"
        nationkey = random.randint(0, 24)
        phone = f"{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        acctbal = round(random.uniform(-999.99, 9999.99), 2)
        mktsegment = random.choice(segments)
        comment = f"Comment {i}"
        
        customers.append((custkey, name, address, nationkey, phone, acctbal, mktsegment, comment))
    
    return customers

def generate_supplier_data(num_suppliers):
    """Generate supplier data"""
    suppliers = []
    
    for i in range(num_suppliers):
        suppkey = i + 1
        name = f"Supplier#{suppkey:09d}"
        address = f"Address {random.randint(1, 1000)}"
        nationkey = random.randint(0, 24)
        phone = f"{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        acctbal = round(random.uniform(-999.99, 9999.99), 2)
        comment = f"Comment {i}"
        
        suppliers.append((suppkey, name, address, nationkey, phone, acctbal, comment))
    
    return suppliers

def generate_part_data(num_parts):
    """Generate part data"""
    parts = []
    containers = ["SM CASE", "SM BOX", "SM PACK", "SM PKG", "MED CASE", "MED BOX", "MED PACK", "MED PKG", "LG CASE", "LG BOX", "LG PACK", "LG PKG"]
    types = ["STANDARD", "ECONOMY", "PROMO", "SMALL", "MEDIUM", "LARGE"]
    brands = [f"Brand#{i}" for i in range(1, 6)]
    mfgrs = [f"Manufacturer#{i}" for i in range(1, 6)]
    
    for i in range(num_parts):
        partkey = i + 1
        name = f"Part {partkey}"
        mfgr = random.choice(mfgrs)
        brand = random.choice(brands)
        ptype = random.choice(types)
        size = random.randint(1, 50)
        container = random.choice(containers)
        retailprice = round(random.uniform(901.00, 2098.99), 2)
        comment = f"Comment {i}"
        
        parts.append((partkey, name, mfgr, brand, ptype, size, container, retailprice, comment))
    
    return parts

def save_to_csv(data, filename, headers=None):
    """Save data to CSV file"""
    filepath = os.path.join("tpch_data", filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        if headers:
            writer.writerow(headers)
        writer.writerows(data)
    print(f"  Generated {filename}: {len(data)} rows")

def main():
    print("="*60)
    print("Generating TPC-H Sample Data for SQLite")
    print("="*60)
    print()
    print(f"Scale Factor: {SCALE_FACTOR}")
    print()
    
    # Create directory
    os.makedirs("tpch_data", exist_ok=True)
    
    # Calculate row counts based on scale factor
    # TPC-H standard: SF-1 has ~150K customers, 1.5M orders, 6M lineitems
    num_customers = int(150000 * SCALE_FACTOR)  # ~15K for SF-0.1
    num_suppliers = int(10000 * SCALE_FACTOR)   # ~1K for SF-0.1
    num_parts = int(200000 * SCALE_FACTOR)      # ~20K for SF-0.1
    num_orders = int(1500000 * SCALE_FACTOR)    # ~150K for SF-0.1
    num_lineitems = int(6000000 * SCALE_FACTOR) # ~600K for SF-0.1
    
    print("Generating data...")
    print(f"  Customers: {num_customers}")
    print(f"  Suppliers: {num_suppliers}")
    print(f"  Parts: {num_parts}")
    print(f"  Orders: {num_orders}")
    print(f"  Lineitems: {num_lineitems}")
    print()
    
    # Generate and save data
    print("Generating region data...")
    regions = generate_region_data()
    save_to_csv(regions, "region.tbl", ["r_regionkey", "r_name", "r_comment"])
    
    print("Generating nation data...")
    nations = generate_nation_data()
    save_to_csv(nations, "nation.tbl", ["n_nationkey", "n_name", "n_regionkey", "n_comment"])
    
    print("Generating customer data...")
    customers = generate_customer_data(num_customers)
    save_to_csv(customers, "customer.tbl", ["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"])
    
    print("Generating supplier data...")
    suppliers = generate_supplier_data(num_suppliers)
    save_to_csv(suppliers, "supplier.tbl", ["s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone", "s_acctbal", "s_comment"])
    
    print("Generating part data...")
    parts = generate_part_data(num_parts)
    save_to_csv(parts, "part.tbl", ["p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size", "p_container", "p_retailprice", "p_comment"])
    
    print("Generating partsupp data...")
    partsupps = []
    seen_pairs = set()  # Track (partkey, suppkey) pairs to avoid duplicates
    for i in range(num_parts):
        partkey = i + 1
        num_suppliers_per_part = random.randint(1, 4)
        suppliers_used = set()
        for j in range(num_suppliers_per_part):
            # Try to find a unique supplier for this part
            attempts = 0
            while attempts < 10:  # Limit attempts to avoid infinite loop
                suppkey = random.randint(1, num_suppliers)
                if (partkey, suppkey) not in seen_pairs:
                    seen_pairs.add((partkey, suppkey))
                    suppliers_used.add(suppkey)
                    availqty = random.randint(1, 9999)
                    supplycost = round(random.uniform(1.00, 1000.00), 2)
                    comment = f"Comment {i}-{j}"
                    partsupps.append((partkey, suppkey, availqty, supplycost, comment))
                    break
                attempts += 1
    save_to_csv(partsupps, "partsupp.tbl", ["ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost", "ps_comment"])
    
    print("Generating orders data...")
    orders = []
    order_statuses = ["O", "F", "P"]
    priorities = ["1-URGENT", "2-HIGH", "3-MEDIUM", "4-NOT SPECIFIED", "5-LOW"]
    for i in range(num_orders):
        orderkey = i + 1
        custkey = random.randint(1, num_customers)
        orderstatus = random.choice(order_statuses)
        totalprice = round(random.uniform(800.00, 500000.00), 2)
        # Random date in 1990s
        year = random.randint(1992, 1998)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        orderdate = f"{year}-{month:02d}-{day:02d}"
        orderpriority = random.choice(priorities)
        clerk = f"Clerk#{random.randint(1, 1000):09d}"
        shippriority = random.randint(0, 1)
        comment = f"Comment {i}"
        orders.append((orderkey, custkey, orderstatus, totalprice, orderdate, orderpriority, clerk, shippriority, comment))
    save_to_csv(orders, "orders.tbl", ["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"])
    
    print("Generating lineitem data...")
    lineitems = []
    return_flags = ["R", "A", "N"]
    line_statuses = ["O", "F"]
    ship_modes = ["REG AIR", "AIR", "RAIL", "SHIP", "TRUCK", "MAIL", "FOB"]
    ship_instructs = ["DELIVER IN PERSON", "COLLECT COD", "NONE", "TAKE BACK RETURN"]
    
    for orderkey in range(1, num_orders + 1):
        num_lineitems = random.randint(1, 7)
        for linenumber in range(1, num_lineitems + 1):
            partkey = random.randint(1, num_parts)
            suppkey = random.randint(1, num_suppliers)
            quantity = random.randint(1, 50)
            extendedprice = round(quantity * random.uniform(900.00, 2100.00), 2)
            discount = round(random.uniform(0.00, 0.10), 2)
            tax = round(random.uniform(0.00, 0.08), 2)
            returnflag = random.choice(return_flags)
            linestatus = random.choice(line_statuses)
            
            # Dates
            year = random.randint(1992, 1998)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            shipdate = f"{year}-{month:02d}-{day:02d}"
            commitdate = f"{year}-{month:02d}-{day:02d}"
            receiptdate = f"{year}-{month:02d}-{day:02d}"
            
            shipmode = random.choice(ship_modes)
            shipinstruct = random.choice(ship_instructs)
            comment = f"Comment {orderkey}-{linenumber}"
            
            lineitems.append((orderkey, partkey, suppkey, linenumber, quantity, extendedprice,
                            discount, tax, returnflag, linestatus, shipdate, commitdate,
                            receiptdate, shipinstruct, shipmode, comment))
    
    save_to_csv(lineitems, "lineitem.tbl", 
                ["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity",
                 "l_extendedprice", "l_discount", "l_tax", "l_returnflag", "l_linestatus",
                 "l_shipdate", "l_commitdate", "l_receiptdate", "l_shipinstruct",
                 "l_shipmode", "l_comment"])
    
    print()
    print("="*60)
    print("Data generation complete!")
    print("="*60)
    print()
    print("Note: For full TPC-H data, use official dbgen tool")
    print("This sample data is sufficient for cache performance testing")
    print()
    print("Next steps:")
    print("1. Load data into SQLite: python load_tpch_data.py")
    print("2. Run benchmark: python benchmark_tpch.py")

if __name__ == "__main__":
    main()

