import xlsxwriter
class XlsFactory():
    @staticmethod
    def create_csv(file_name, sheet_name, data, row_is_lst = False):
        wb = xlsxwriter.Workbook(file_name)
        ws = wb.add_worksheet(sheet_name)
        row_count = 0
        for row in range(0, len(data)):
            col_count = 0
            if row_is_lst:
                for value in data[row]:
                    #(row, col, value, style/expression)
                    ws.write(row_count, col_count, value)
                    col_count += 1
            else:
                #(row, col, value, style/expression)
                ws.write(row_count, col_count, str(data[row]))
            row_count += 1
        wb.close()
