from openpyxl import load_workbook
from models import Results

def formatResults(searchID):

    wb = load_workbook('/Users/williamostler/Desktop/University/Stage 2/CSC2033 - Software Engineering Team Project/PriceComparisonStockChecker/BOMOutputTemplate/BOMOutput.xlsx')
    results_data = Results.query.filter(Results.searchnumber == searchID).all()
    write = wb.active

    i=0
    for result in results_data:

        write[f'C{str(8+i)}'] = result.partnumber
        write[f'D{str(8+i)}'] = result.supplier
        write[f'E{str(8+i)}'] = result.stock
        write[f'F{str(8+i)}'] = result.stockrequired
        write[f'G{str(8+i)}'] = result.priceperunit
        write[f'H{str(8+i)}'] = result.totalprice
        write[f'I{str(8+i)}'] = result.link

        i+=1

    wb.save("results.xlsx")

formatResults(1)