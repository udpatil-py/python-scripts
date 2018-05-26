#generate fibonacci series and write to csv file, and produce logs as well

import csv
import logging
from functools import lru_cache
import re
from builtins import int

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='2_csv_log.log',
#                    filemode='w',
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    )

logger = logging.getLogger()

@lru_cache(maxsize=1024)
def fibonacci(n):
    """calculate fibonacci series of given number and store in the csv file
    the fibonacci calculation should be fast, like use cache to calculate the series"""
    global logger
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return (fibonacci(n-1)+fibonacci(n-2))
    elif n < 0:
        logger.error("fibonacci series input %s is negative/zero"%n)

check_input = re.compile(r"[^0-9]")
number = input("Please enter number to find fibonacci values:")

while check_input.search(number) or number == '':
    print("Invalid input...!,%s, please re-enter correct positive number, like 1 and above"%number)
    logger.error("Invalid input...!,%s, please re-enter correct positive number, like 1 and above"%number)
    number = input("Please re-enter number to find fibonacci values:")
    
if int(number) != 0:
    number = int(number)+1
elif int(number) == 0:
    logger.error("Invalid input...!,0, please re-enter correct positive number, like 1 and above")
    raise ValueError("Invalid input...!,0, please re-enter correct positive number, like 1 and above")

logger.info("Program started to find the fibonacci series for the given number %s"%(number-1))

try:
    file = open('2_csv_file.csv','w',newline='')
    writer = csv.writer(file)
    writer.writerow(["fibonacci_number","fibonacci_value"])
except PermissionError:
    logger.error("unable to create or open the csv file")
    logger.error("[Errno 13] Permission denied: csv file is in open state or you do not have permission to access it")
    print("Permission denied: csv file is in open state or you do not have permission to access it")
except Exception as e:
    logger.error("unexpected error occurred while opening the csv file %s",e)
    print("unexpected error occurred while opening the csv file %s",e)

try:
    for n in range(1,number):
        value = fibonacci(n)
        writer.writerow([n,value])
        logger.info("fibonacci value for number %s \t= %s"%(n,value))
        print(n,"=",value)
    file.close()
except Exception as e:
    logger.error("unexpected error occurred while calculating fibonacci value")
    print("unexpected error occurred while calculating fibonacci value")