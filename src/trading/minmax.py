import sys, csv, math

# ===================================
# FUNCTION: Perform min/max, write outputs
# ===================================
def minmax_benchmark(opt, path_A, path_B, out_path, init=1000):
    
    # ===================================
    # SETUP
    # ===================================
    
    # Parsing filenames, creating paths
    name_A = path_A.split('/')[-1]
    if ".csv" not in path_A:
        path_A = path_A + ".csv"
    else:
        name_A = name_A[:-4]

    name_B = path_B.split('/')[-1]
    if ".csv" not in path_B:
        path_B = path_B + ".csv"
    else:
        name_B = name_B[:-4]

    path_O = out_path + name_A + "_" + name_B + ".csv"
    name_A = name_A.upper()
    name_B = name_B.upper()

    opt = False if opt.lower() == "min" else True

    # Opening files
    try:
        file_A = open(path_A, 'rb')
        file_B = open(path_B, 'rb')
        file_O = open(path_O, 'wb')
    except IOError:
        print "ERROR: Can't find input stocks!"
        exit(1)
       
    # Creating readers / writer
    reader_A = csv.reader(file_A)
    reader_B = csv.reader(file_B)
    writer_O = csv.writer(file_O)
    headers = ['Date', name_A+' Val', name_A+' Amt', name_B+' Val', name_B+' Amt', 'Cash', 'Total']
    writer_O.writerow(headers)

    # ===================================
    # ITERATION
    # ===================================
    date    = ""    # Date
    amt_A   = 0     # Amt of stock A to buy
    amt_B   = 0     # Amt of stock B to buy
    cash    = 0     # Amt of leftover cash
    total   = init  # Amt of total value

    # Getting current stocks
    (cur_date_A, cur_val_A) = reader_A.next()
    (cur_date_B, cur_val_B) = reader_B.next()
    cur_val_A = float(cur_val_A)
    cur_val_B = float(cur_val_B)

    # Checking dates
    while cur_date_A != cur_date_B:
        # Debug message
        print "ERROR: Mismatching dates, " + \
            cur_date_A + "(" + name_A + ") vs " + \
            cur_date_B + "(" + name_B + ")"
        # Compare days, advance 'slower' date
        day_A = int(cur_date_A.split("-")[-1])
        day_B = int(cur_date_B.split("-")[-1])
        if day_A < day_B:
            (cur_date_A, cur_val_A) = reader_A.next()
        else:
            (cur_date_B, cur_val_B) = reader_B.next()

    while True:
        date = cur_date_A

        try:
            # Getting next stocks
            (nxt_date_A, nxt_val_A) = reader_A.next()
            (nxt_date_B, nxt_val_B) = reader_B.next()
            
            # Checking dates
            while nxt_date_A != nxt_date_B:
                # Debug message
                print "ERROR: Mismatching dates, " + \
                    nxt_date_A + "(" + name_A + ") vs " + \
                    nxt_date_B + "(" + name_B + ")"
                # Compare days, advance 'slower' date
                day_A = int(nxt_date_A.split("-")[-1])
                day_B = int(nxt_date_B.split("-")[-1])
                if day_A < day_B:
                    (nxt_date_A, nxt_val_A) = reader_A.next()
                else:
                    (nxt_date_B, nxt_val_B) = reader_B.next()

            nxt_val_A = float(nxt_val_A)
            nxt_val_B = float(nxt_val_B)
            amt_A = 0
            amt_B = 0

            # Comparing growth
            diff_A = nxt_val_A - cur_val_A
            amt_A  = math.floor(total / cur_val_A)
            amt_A  = int(amt_A)
            diff_A = amt_A * diff_A

            diff_B = nxt_val_B - cur_val_B
            amt_B  = math.floor(total / cur_val_B)
            amt_B  = int(amt_B)
            diff_B = amt_B * diff_B

            if opt != (diff_A < diff_B) :
                amt_B = 0
            else:
                amt_A = 0

            # Writing output
            cash = total - (amt_A*cur_val_A + amt_B*cur_val_B)
            cash = round(cash, 2)
            row = [date, cur_val_A, amt_A, cur_val_B, amt_B, cash, total]
            writer_O.writerow(row)
            
            # Updating values
            (cur_date_A, cur_val_A) = (nxt_date_A, nxt_val_A)
            (cur_date_B, cur_val_B) = (nxt_date_B, nxt_val_B)
            if opt != (diff_A < diff_B) :
                total = total + diff_A
                total = round(total, 2)
            else:
                total = total + diff_B
                total = round(total, 2)
            
        except StopIteration:
            break