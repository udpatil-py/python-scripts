import pandas
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(process)d - %(message)s"

logging.basicConfig(filename="4_Bangalore_Rainfall_data.log",
                    #filemode='w',
                    level=logging.DEBUG,
                    format=LOG_FORMAT)

try:
    logger = logging.getLogger()
    with pandas.ExcelFile("4_Bangalore_Rainfall_data.xlsx") as rain:
        data = pandas.read_excel(rain)
        df = pandas.DataFrame(data)
    logger.info("Read 100 years Bangalore Rainfall data successfully")
except Exception as e:
    logger.error("Error occurred while accessing the input file",e)
    print("Error occurred while accessing the input file",e)


try:
    logger.info("Setting index as Year")
    data.set_index(data["Year"],inplace=True)
    logger.info("munging/adding zero to empty cells")
    data.fillna(0,inplace=True)
    lines = 100*"-"
    logger.info("\n{0}\nFrom last 100 years (1900 to 2000) data.Average rainfall occurred in each month is:\n{1}".format(lines,lines))
    highest_rainfall = {}
    average_rainfall = {}
    for i in data:
        if data[i] is not data["Year"]:
            highest_rainfall[i]=data[i].max()
            average_rainfall[i]=float('%.3f'%(data[i].mean()))
            logger.info("With 100 years data, average rainfall in the month of {0}\t=\t{1} mm".format(i,'%.3f'%(data[i].mean())))
            print("With 100 years data, average rainfall in the month of {0}\t=\t{1} mm".format(i,'%.3f'%(data[i].mean())))

    highest_rainfall_month_and_value_in_100_years = [(k,v) for k,v in highest_rainfall.items() if highest_rainfall[k] == max(highest_rainfall.values())]
    highest_rainfall_month,highest_rainfall_value = highest_rainfall_month_and_value_in_100_years[0][0],highest_rainfall_month_and_value_in_100_years[0][1]
    highest_rainfall_year = list(df['Year'][df[highest_rainfall_month]==highest_rainfall_value])
    highest_rainfall_year = highest_rainfall_year[0]

    highest_rainfall_month_and_values_every_year = [(k,v) for k,v in average_rainfall.items() if average_rainfall[k] == max(average_rainfall.values())]
    highest_rainfall_month_every_year,highest_rainfall_value_every_year = highest_rainfall_month_and_values_every_year[0][0],highest_rainfall_month_and_values_every_year[0][1]
    
    avg_rainfall_per_year = 0
    for k in average_rainfall:
        avg_rainfall_per_year += average_rainfall[k]

    avg_rainfall_per_month = avg_rainfall_per_year/12


    logger.info("""\n{0}\nWith last 100 years of rainfall data from 1900 to 2000, in Bangalore city.
    Highest rainfall was {1} mm occurred in the month of {2}-{3}. 
    However every year highest rainfall is happening in the month of {4} with approximate rainfall of {5} mm.
    \n But average rainfall in every month in Bangalore is {6} mm. \n Average rainfall every year in Bangalore is {7} mm...!\n{8}.""".format(lines,
                                                                                                          highest_rainfall_value,
                                                                                                          highest_rainfall_month,
                                                                                                          highest_rainfall_year,
                                                                                                          highest_rainfall_month_every_year,
                                                                                                          highest_rainfall_value_every_year,
                                                                                                          avg_rainfall_per_month,
                                                                                                            avg_rainfall_per_year,
                                                                                                            lines))

    print("""\n{0}\nWith last 100 years of rainfall data from 1900 to 2000, in Bangalore city.
    Highest rainfall was {1} mm occurred in the month of {2}-{3}. 
    However every year highest rainfall is happening in the month of {4} with approximate rainfall of {5} mm.
    \n But average rainfall in every month in Bangalore is {6} mm. \n Average rainfall every year in Bangalore is {7} mm...!\n{8}.""".format(lines,
                                                                                                          highest_rainfall_value,
                                                                                                          highest_rainfall_month,
                                                                                                          highest_rainfall_year,
                                                                                                          highest_rainfall_month_every_year,
                                                                                                          highest_rainfall_value_every_year,
                                                                                                          avg_rainfall_per_month,
                                                                                                            avg_rainfall_per_year,
                                                                                                            lines))
except Exception as e:
    print("Unexpected exception occurred while manupulating/calculating rainfall data",e)
    logger.error("Unexpected exception occurred while manupulating/calculating rainfall data",e)
