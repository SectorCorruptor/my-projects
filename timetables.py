import camelot
import pandas as pd
import re
import numpy as np
import shutil
import os
import time # for benchmarking this shitty program
import sys

succount=0
faicount=0

start = time.perf_counter()

if not os.path.exists("datax"):
    os.mkdir("datax")
# update every time
teachers_set = set(['Sydney Atkins', 'John Gomes', 'Toshiko Malhotra', 'Sharada Kenkare', 'Malini Murali', 'Ritesh Dhanak', 'Sreekala Kumar', 'Vinaya Jayadev', 'Sheldon Dias', 'Priya Prakash', 'Rajesh Mehrotra', 'Aarti', 'Trafford Gregory', 'Rajkumar G', 'Avinash Surve', 'Juliana Li', 'Mohammed Inkishaf', 'Rajesh Sinha', 'Troy James', 'Ritu Sharma', 'Sindu Joseph', 'Julia Robertson', 'Divya Rajgarhiya', 'Padma Rajawat', 'Sumaiya', 'Rumana Firdose Rumana', 'Michelle Thomas', 'Muniza Khan Bose', 'Carolyn Reynolds', 'Ryan Wright', 'Deeksha Handa', 'Christina', 'Xena Marian Massey', 'Brandon', 'UURMI GHOSH', 'Anvita', 'Ruchi', 'Latisha', 'Sheroline Fernandes', 'MFS', 'Shehla Abbasi', 'Shiba Juneja', 'Shely Das', 'Seema Khatri', 'Mahek Ajwani', 'Monica Chauhan', 'Maria Albert', 'Thresa Michael', 'Parag Damania', 'Padma shanker', 'Sonia Titus', 'Harkamal Sehdev', 'Isaac', 'NARESH', 'Girish', 'Shauna', 'Hafsa Faisal', 'Sheeba Nair', 'Chinniah', 'Aneesh VV', 'Shaikh Saidu Babu', 'Shruti Talwar', 'Merlene Coutino', 'Deepak', 'Anjana Ninan', 'Anju Shajan', 'Vimaldeep', 'Fanny Thomas', 'Kanchan Sharma', 'Simi S', 'Pillai Leena', 'ANILA M', 'Srividya J.', 'Srinivas Shastri', 'Preetha Vijay', 'Prashansa Raizada', 'Rasheim Sachdeva', 'Jamshi', 'Madhumita Chatterjee', 'Moumita Chakraborty', 'Amita Amita', 'Vinita Joshi', 'Antony Correia', 'Hawabibi', 'Maria Rozario', 'Charles', 'Fagun Balchandani', 'Ayoti Ghosh', 'Agarwal Sangeeta', 'Payal Jagda', 'Suchitra Gummadi', 'Nazneen', 'Vandana Mathur', 'Andrew', "Tina D'Lima", 'Farooq Nawaz', 'Abdullah Sukri', 'Eman Gadalla', 'NORHAN', 'Heba Baghdadi', 'Ishraga', 'AMNA', 'S Marwa', 'Mohammed Adul Aziz', 'Samira', 'Ahmed', 'Ossama', 'Preeti Shekhawat', 'Sandeepa Mehta', 'Seema Kalawatia', 'Preeti Pandey', 'Hemlata', 'Malini Sreekumar', 'Priya', 'Fatima Poonawala', 'Satam Aarti', 'Ait M. Abdellah', 'Mounia', 'Sushmita Mukherjee', 'Sangeeta', 'Sahana', 'Ankita', 'Divya Bhola', 'Shivani Maheshwari', 'Baqiya', 'Kah Charles', 'Sagarika Banerjee', 'Joydeep Chatterjee', 'Srividya S', 'Bhavini', 'Nagarjun Rao', 'Eriyat Lakshmi', 'VNS', 'Rohini Awasthi', 'Rajani Rajani', 'Siby Thomas', 'Aman', 'Swarna Bharathan', 'KamalPreet Kaur', 'Veena Dharmarajan', 'Deepa Balasubramanian', 'Shubhi Tandon', 'Megha Suresh', 'Unni Preetha', 'Shoma', 'Syed Inthekhab Alam', 'Shweta Jain Shweta Jain', 'OSWA', 'Amit', 'Shilpa Kapoor', 'Anika', 'Maria Veena', 'Sindhu', 'Rachel', 'Hannah Shunker', 'Axel Rodericks', 'David', 'Christopher', 'Rajeshwari', 'Jaison Jacob', 'Ramalingam', 'Vasugi Ramalingam', 'Venukumar', 'Bindu', 'Richard', 'Kushal', 'Pageeth', 'Shalin', 'Jignyasa Patel', 'Mithra', 'Eric', 'Myra', 'Raghunath', 'Sreelakshmi', 'Shafiq'])
# this line is important for this to work:
# allahu akbar
def process(data):
    def clean_subject(subject_parts):
        s = " ".join(subject_parts) if isinstance(subject_parts, list) else subject_parts
        return s.replace(" /", "/").replace("/ ", "/")

    def clean_teachers_list(items):
        out = []
        for t in items:
            parts = [p.strip() for p in t.split('/') if p.strip()]
            out.extend(parts)
        return out

    def split_fused(token):
        return re.findall(r'[A-Z][a-z.]*', token) or [token]

    def classify(token):
        """
        Returns: (type, value)
        type = 'teacher' | 'subject' | 'unknown'
        """
        token = token.strip()

        if token in teachers_set:
            return "teacher", token
        else:
            # implement a search of token in substrings of teacher_set's items
            for teacher in teachers_set:
                if token.lower() in teacher.lower():
                    return "teacher", token
        return "subject", token  # default assumption

    def log_fallback(subject, teachers):
        print(end=f"[fallback] ambiguous combo → subject={subject}, teachers={teachers}\t")
        global faicount
        faicount +=1

    if len(data) > 2:
        return [["Multiple subjects", "Multiple teachers"]]

    result = []

    for sub in data:

        subject = None
        teachers_found = []

        # --- STRUCTURE STEP ---
        if len(sub) == 1:
            parts = split_fused(sub[0])
        else:
            parts = sub

        # --- CLASSIFY STEP ---
        classified = []
        for p in parts:
            if '/' in p:
                classified.extend([x for x in p.split('/') if x])
            else:
                classified.append(p)

        classified = [(classify(c)[0], classify(c)[1]) for c in classified]

        # --- SPLIT SUBJECT / TEACHERS ---
        # heuristic: last teacher-like block OR known teachers
        teachers_found = [v for t, v in classified if t == "teacher"]
        subject_parts = [v for t, v in classified if t != "teacher"]

        subject = clean_subject(subject_parts)

        # --- VALIDATION ---
        if not teachers_found:
            # fallback needed
            log_fallback(subject, teachers_found)

            # old heuristic fallback
            if len(sub) == 1:
                teachers_found = []
            else:
                teachers_found = clean_teachers_list(sub[:-1])
                subject = clean_subject([sub[-1]])
        else:
            global succount
            succount+=1

        # --- FINAL RULE ---
        if len(teachers_found) > 2:
            result.append([subject, "Multiple teachers"])
        else:
            result.append([subject] + teachers_found)
    print(result)
    return result

def is_not_na(x):
    return not np.all(pd.isna(x))


def insert(df, row, col, value):
    df = df.copy()

    # Extend the DataFrame by 1 row to prevent losing the last value
    df = pd.concat([df, pd.DataFrame(np.nan, index=[len(df)], columns=df.columns)], ignore_index=True)

    # Shift cells downward manually
    for r in range(len(df)-1, row, -1):
        df.at[r, col] = df.at[r-1, col]

    # Insert the new value
    df.at[row, col] = value

    return df

tables = camelot.read_pdf(sys.argv[1], flavor="lattice", pages=sys.argv[2])#-end later

for j in range(tables.n):
    data = tables[j].df # j later
    # pandas, or my skill with it, sucks.

    # 1. Remove break and lunch time columns. The tables don't handle them
    #    well, so we need to manually adjust per weekday

    rmindexes = []
    for i in range(len(data.loc[0])):
        if "break" in data.loc[0][i].lower() or "lunch" in data.loc[0][i].lower():
            rmindexes.append(i)
    for i in rmindexes:
        data = data.drop(i, axis="columns")

    # 2. Drop the first row. Timings are useless, since I recall someone else
    #    volunteered to manually edit those on their own (universal to the school)

    data = data.drop(0, axis="index")

    # 3. Loop through the cells. If ICE is detected as a substring, replace that cell
    #    with just the text "ICE"

    for r in range(len(data)):
        for c in range(len(data.columns)):
            if "ICE" in data.iloc[r, c]:data.iloc[r, c]="ICE"

    # 4. Get the indexes of the actual day rows

    weekdays = ["Mon", "Tues", "Wed", "Thurs", "Fri"]
    days = []

    for r in range(len(data)):
        if str(data.iloc[r,0]).strip() in weekdays:
            days.append(r)

    days.append(len(data))  # for the final slice

    # 5. Loop through those rows and collapse items into a new dataframe

    # number of columns = original data columns
    num_cols = data.shape[1]
    tt = pd.DataFrame(columns=range(num_cols))

    for x in range(len(days)-1):
        r = days[x]
        row_data = [data.iloc[r,0]]  # first column: day
        for c in range(1, data.shape[1]):
            vals = []
            for until in range(r, days[x+1]):
                cell = data.iloc[until, c]
                if pd.notna(cell) and str(cell).strip():
                    vals.append(str(cell).strip())
            toadd = [l.splitlines()for l in vals]
            # do more preprocessing from here
            for d in toadd:
                if "drama" in [r.lower()for r in d]: # horrible idea. avinash sir is bound to retire someday
                    toadd = [["6th Subject", "Multiple teachers"]]
                    row_data.append(toadd)
                    break
            else:
                #print(toadd, end=" -> ")
                index = next((i for i, s in enumerate(sum(toadd,[]))if "/"in s), None)
                if index is not None:
                    # Multiple teachers, hmm....
                    #print(toadd)
                    toadd = process(toadd)
                elif ["ICE"] in toadd:
                    toadd=[["ICE","Multiple teachers"]]
                elif toadd:  # if not empty but without slashes
                    if len(toadd) == 1:
                        # Single sublist → join subject parts normally
                        toadd = [[ " ".join(toadd[0][:-1]) , toadd[0][-1] ]]
                        print(toadd)
                    else:
                        # Multi-sublists → use our process function to correctly swap teachers/subjects
                        toadd = process(toadd)
                #print(toadd)
                row_data.append(toadd)
        tt.loc[len(tt)] = row_data

    tt = tt.apply(
        lambda row: pd.Series(
            [x for x in row if is_not_na(x)] +
            [np.nan] * (len(row) - sum(is_not_na(x) for x in row))
        ),
        axis=1
    ) # push to left

    tt=tt.T
    tt=tt.drop(0)

    # 6. Revive the break time

    tt=insert(tt, 3, 0, [["Break", "N/A"]])
    tt=insert(tt, 7, 0, [["Lunch", "N/A"]])

    tt=insert(tt, 3, 1, [["Break", "N/A"]])
    tt=insert(tt, 7, 1, [["Lunch", "N/A"]])

    tt=insert(tt, 3, 2, [["Break", "N/A"]])
    tt=insert(tt, 6, 2, [["Lunch", "N/A"]])

    tt=insert(tt, 3, 3, [["Break", "N/A"]])
    tt=insert(tt, 6, 3, [["Lunch", "N/A"]])

    tt=insert(tt, 3, 4, [["Break", "N/A"]])

    # 7. Remove surplus empties

    tt=tt.dropna(how="all")

    # NOTE: The code below should be commented out if we make it - this was a 2022 thingy, because that's what
    # Vihaan gave me. So for some realism...

    tt.iloc[9, 2] = np.nan

    # ... there. Please please comment this out later

    # 8. Compile into teacher and timetable.csv
    teachfile = timefile = "2,3,4,5,6"
    for r in range(len(tt)):
        teachfile += "\n"
        timefile += "\n"
        teachline = timeline = ""
        for c in range(len(tt.columns)):
            if not isinstance(tt.iloc[r, c], float):  # we... probably should do something about this check
                for sublist in tt.iloc[r, c]:
                    timeline += sublist[0] + "/"
                    teachline += "/".join(sublist[1:]) + "/"
                timeline = timeline[:-1] + ","
                teachline = teachline[:-1] + ","
            else:
                timeline = timeline + ","
                teachline = teachline + ","
        timeline = timeline[:-1]
        teachline = teachline[:-1]
        teachfile += teachline
        timefile += timeline

# 9. Export

    try:
        teacher = open(f"datax/{j}-teacher.csv", 'w')
    except FileNotFoundError:
        teacher = open(f"datax/{j}-teacher.csv", 'x')
    try:
        timetab = open(f"datax/{j}-timetable.csv", 'w')
    except FileNotFoundError:
        timetab = open(f"datax/{j}-timetable.csv", 'x')

    teacher.write(teachfile)
    timetab.write(timefile)
    teacher.close()
    timetab.close()

shutil.make_archive('data', 'zip', 'datax')
shutil.rmtree('datax')

print(f"DONE: {time.perf_counter()-start} seconds")
print(f"Match success rate: {succount/(succount+faicount)*100}%")
print("\a")
