
def to_header_latex(headers):
    return '''
    \\begin{table}[!h]
        \\centering
        \\def\\arraystretch{1}
	    \\setlength\\tabcolsep{6pt}
        \\rowcolors{2}{white}{gray!25}
        \\begin{tabular}{''' + ('l' * len(headers)) + '''}
            \\toprule
''' + to_row_latex(headers) + \
    '''            
            \\midrule'''

def to_footer_latex():
    return '''
            \\bottomrule
        \\end{tabular}
        \\caption{\\TODO{MUST BE DONE}}
        \\label{tab:}
    \\end{table}
    '''
def midrule():
    return  '''
    \midrule
    '''

def to_row_latex(array):
    return '''             ''' + '\t&\t'.join(array) + '\\\\'