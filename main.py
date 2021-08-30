from ot_get import pu_ot


if __name__ == "__main__":

    file_html = 'PU_oliveira.html'
    file_xls = 'PU_oliveira.xlsx'

    df = pu_ot(file_html, file_xls)

    print('Finalizado')
