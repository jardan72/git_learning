import re
from collections import Counter
import csv
import json
import yaml

"""
Parse file and save valid input
"""
host_name = []
num_sw =  []
with open('ksv.txt') as fp:
    for line in fp:
        if re.match(r'^\s*$', line):        # Skip empty !
            continue
        line = line.strip()                 # remove white space
        if line.startswith("ksv"):          # Add hostname to host_name list if it start with 'ksv'
            tmp = line.split('#')
            host_name.append(tmp[0])
        
        if re.match(r'^\*|^[0-9]', line):
            if re.match(r'^\*', line):
                line = line.replace('*','',1)   # remove line that start with * typical Active lines start with *
            if "Provisioned" in line:           # skip provisioned switches as they are not installed
                continue
            num_sw.append(int(line[:1]))        # save switch stack number
            

"""
Find highest number of switches 
"""
highest_values = []
current_max = num_sw[0]

for num in num_sw[1:]:
    if num == 1:
        highest_values.append(current_max)
        current_max = num
    else:
        current_max = max(current_max, num)

highest_values.append(current_max)  # Append the last max value


number_of_switches = highest_values.copy()


"""
Merge lists for output
"""

if len(host_name) == len(number_of_switches):
    merged_host_num = list(map(list, zip(host_name, number_of_switches)))
else:
    print("Somethings wrong!  Number of hosts and switches doesn't match up")

"""
Print output to screen
"""
# total nr stacks print
tot_s = len(merged_host_num)
print("Total number of stacks: ", tot_s )
for host, num in merged_host_num:
    print(host,"\t", num)

# Find number of switches with status Ready = total installed switches
with open("ksv.txt", "r") as logfile:
    word_counts = Counter(logfile.read().split())
    wc = word_counts.get('Ready')
    print("Total switches: ", wc )


"""
Save data to file in semi CSV format
"""

with open('ksv-massaged.txt', 'w') as file: 
    first_line = "Hostname, number of switches in stack" + "\n"
    file.write(first_line)
    
    for host, num in merged_host_num:
        new_line = str(host) + "," + str(num) + "\n"
        file.write(new_line)
    file.write("\n")

    last_line = "Total stacks: " + str(tot_s) + "\n" + "total # switches: " + str(wc) +"\n"
    file.write(last_line)
    print("File saved..." )

