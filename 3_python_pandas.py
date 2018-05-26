#!/usr/bin/python
##############################################################
#  Script     : 3_python_pandas.py
#  Author     : Uday Kumar Patil  (udpatil.py@gmail.com)
#  Date       : 07/25/2016
#  Description: Script to Calculate the shift allowances of individual System Admin
##############################################################

import pandas
import logging


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(process)d - %(message)s"

logging.basicConfig(filename = "3_python_pandas.log",
                    filemode = 'w',
                    level = logging.DEBUG,
                    format=LOG_FORMAT
                    )

try:
    logger = logging.getLogger()
    logger.info("Log Format is :\n asctime \t\t\t- levelname -  process id - message")
    logger.info("Python pandas, reading 3_pandas_input.xlsx file with System Admin's shift data")
    with pandas.ExcelFile("3_pandas_input.xlsx") as excel:
        df1 = pandas.read_excel(excel)    
##    logger.info("Read input file successfully")
    print(80*"-","\n",df1,"\n",80*"-")
    df1.set_index("Month",inplace=True)
    logger.info("index is set to Month")
    df1.fillna(0,inplace=True)
    logger.info("Replaced all NA/Nan/empty cells with zero:")
    logger.info("Below is the input values read from input file:\n{0}\n{1}\n{2}".format(80*'-',df1,80*'-'))
except Exception as e:
    print("Exception occurred while accessing input file",e)
    logger.error("Exception occurred while accessing input file{0}".format(e))
    
##print(type(df1))

##print(df1)

try:
    logger.info("Calculating shift allowances per System Admin now...!")
    Total_Worked_Shifts = df1["Shift A"]+df1["Shift B"]+df1["Shift C"]
    Shift_A_Pay = df1["Shift A"]*125
    Shift_B_Pay = df1["Shift B"]*175
    Shift_C_Pay = df1["Shift C"]*400
    Total_Amount = Shift_A_Pay+Shift_B_Pay+Shift_C_Pay
except Exception as e:
    print("Exception occurred while calculating input values",e)
    logger.error("Exception occurred while calculating input values{0}".format(e))
    
##print(type(Total_Worked_Shifts))

logger.info("Preparing a data frame to write into output excel file")
df2 = pandas.DataFrame({"Shift A":df1["Shift A"],
                        "Shift B":df1["Shift B"],
                        "Shift C":df1["Shift C"], 
                        "Total Worked Shifts":Total_Worked_Shifts,
                        "Shift A Pay":Shift_A_Pay,
                        "Shift B Pay":Shift_B_Pay,
                        "Shift C Pay":Shift_C_Pay,
                        "Total Amount":Total_Amount,
                         })

##print(df2)
engine = 'openpyxl'
try:
    with pandas.ExcelWriter('3_pandas_output.xlsx'.format(engine),engine=engine)as writer:
        df2.to_excel(writer,sheet_name="Shift_Allowances",index=True,startrow=0,startcol=0)
    logger.info("Below data is written to out put excel file successfully:\n{0}\n{1}\n{2}".format(80*'-',df2,80*'-'))
    print(80*"-","\n",df2,"\n",80*"-")
except Exception as e:
    print("Exception occurred while writing data to out put file",e)
    logger.error("Exception occurred while writing data to out put file{0}".format(e))
    
##print(help(pandas.ExcelWriter))
