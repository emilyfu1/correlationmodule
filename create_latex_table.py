import os
import numpy as np

# [GABRIELLE] code with example output -- python to latex
def create_latex_table(regression_objects, rhs_variables, lhs_variable, toggle, filename, filepath=os.getcwd()):
    '''
    create latex table that showcases regression output(s).
    
    Paramaters:
        - regression_objects (list of regression objects): regression output -- the coefficient and standard error associated with each rhs_variable.
        - rhs_variables (list of strings): names of independent variables (rhs variables) in the regression 
        - lhs_variable (string): name of dependent variable (lhs variable) in the regression
        - toggle (boolean): whether the Latex file has opening and closing arguments
        - [EMILY: add filename parameter] filename (string): desired name of saved LaTeX file
        - [EMILY: change filepath parameter to include only path] filepath (string): path name where the resulting LaTeX table (.tex file) will be saved
        
    '''
    inputpath = os.path.abspath(filepath) + '\\' + filename + '.tex'

    column_data = []
    for i in range(len(regression_objects)):
        coefficient = regression_objects[i].params[1:] 
        standard_error = regression_objects[i].bse[1:] 
        t_stat_value = regression_objects[i].tvalues[1:] 
        p_value = regression_objects[i].pvalues[1:] 
        rhs_variables = regression_objects[i].model.exog_names[1:]
        number_of_observations = regression_objects[i].nobs 
        
        column_data.append({"coefficient": coefficient, "standard_error": standard_error, "p_value": p_value, "rhs_variables": rhs_variables, "N" : number_of_observations})
    
        row_data = {}

        for column in column_data:
            rhs_variables = column["rhs_variables"]
            for rhs in rhs_variables:
                if rhs not in row_data.keys():
                    row_data[rhs] = []

        for rhs_variable in row_data.keys():
            for column in column_data:
                if rhs_variable in column["rhs_variables"]:
                    index = column["rhs_variables"].index(rhs_variable)
                    row_data[rhs_variable].append({"coefficient": column["coefficient"][index], "standard_error": column["standard_error"][index], "p_value": column["p_value"][index]})
                else:
                    row_data[rhs_variable].append({"coefficient": None, "standard_error": None, "p_value": None})
       
        row_N = []
        for column in column_data:      
            number_of_observations = column["N"]
            row_N.append(number_of_observations)
                
    
    os.makedirs(os.path.dirname(inputpath), exist_ok=True) 
    with open(inputpath, "w") as file:
        
        if toggle:
            file.write("\documentclass[12pt]{article}")
            file.write("\n")
            file.write(r"\usepackage{arev}")
            file.write("\n")
            file.write(r"\usepackage{longtable}")
            file.write("\n")
            file.write(r"\usepackage{setspace}")
            file.write("\n")
            file.write(r"\usepackage{graphicx}")
            file.write("\n")
            file.write(r"\usepackage{booktabs}")
            file.write("\n")
            file.write(r"\usepackage{mathptmx}")
            file.write("\n")
            file.write(r"\usepackage{multirow}")
            file.write("\n")
            file.write(r"\usepackage{helvet}")
            file.write("\n")
            file.write(r"\usepackage{dsfont}")
            file.write("\n")
            file.write(r"\usepackage{soul}")
            file.write("\n")
            file.write(r"\usepackage[utf8]{inputenc}")
            file.write("\n")
            file.write(r"\usepackage{hyperref}")
            file.write("\n")
            file.write(r"\usepackage{epstopdf}")
            file.write("\n")
            file.write(r"\usepackage{subfig}")
            file.write("\n")
            file.write(r"\usepackage[T1]{fontenc}")
            file.write("\n")
            file.write(r"\usepackage[margin=0.2in]{geometry}")
            file.write("\n")
            file.write(r"\usepackage{pdflscape}")
            file.write("\n")
            file.write(r"\usepackage{tablefootnote}")
            file.write("\n")

            file.write(r"\begin{document}")
            file.write("\n")
            
            file.write(r"\begin{landscape}")
            file.write("\n")
            file.write("\n")
            file.write("\n")
            file.write("\n")
            file.write("\n")

        file.write(r"\begin{table}[]")
        file.write("\n")
        file.write("\t\\caption{Regression}")
        file.write("\n")
        file.write("\t\\label{tab:mainEmpirical}")
        file.write("\n")
        file.write("\t\\begin{center}")
        file.write("\n")
        file.write("\t\\scalebox{0.65}{")
        file.write("\n")
        file.write("\n")

        c = ""
        for i in range(len(column_data)):
            c = c + "c"
            
        file.write("\t\\begin{tabular}{l" + c + "}")
        file.write("\n")
        
        file.write("\t\t\\toprule")
        file.write("\n")
        lhs_variable_string = "\t&&\multicolumn{" + str(int(len(column_data)//1.2)) + "}{c}{\emph{" + lhs_variable + "}}\\\\"
        file.write(lhs_variable_string)
        file.write("\n")
        
        cols = "\t"
        for i in range(len(column_data)):
            cols = cols + "&(" + str(i+1) + ")"
        cols = cols + "\\\\\n"
        file.write(cols)
        
        file.write("\midrule")
        file.write("\n")
        
        for key, value in row_data.items():
            start1 = "\t\multirow{2}{*}{\detokenize{" + key + "}}"
            mid1 = ""
            for val in value:
                if val["coefficient"] is not None:
                    mid1 = mid1 + "&" + str(np.round(val["coefficient"], 2))
                    #add asterixis
                    if val["p_value"] < 0.01:
                        mid1 = mid1 + "***"
                    elif val["p_value"] < 0.05:
                        mid1 = mid1 + "**"
                    elif val["p_value"] < 0.1:
                        mid1 = mid1 + "*"
                    
                else:
                    mid1 = mid1 + "&"
            end1 = "\\\\\n"
            
            start2 = "\t"
            mid2 = ""
            for val in value:
                if val["standard_error"] is not None:
                    mid2 = mid2 + "&" + "(" + str(np.round(val["standard_error"], 2)) + ")"
                else:
                    mid2 = mid2 + "&"
            end2 = "\\\\\n"
         
            file.write(start1 + mid1 + end1 + start2 + mid2 + end2)
                    
        file.write("\t\\bottomrule")
        
        start3 = "\t\multirow{2}{*}{\detokenize{" + "N" + "}}"
        mid3 = ""
        for val in row_N:
            if val is not None:
                mid3 = mid3 + "&" + str(val)
            else:
                mid3 = mid3 + "&"  
        end3 = "\\\\\n"
        
        file.write(start3 + mid3 + end3)
        file.write("\n")
        file.write("\t\\bottomrule")

        file.write("\t\end{tabular}}")
        file.write("\n")
        file.write("\t\end{center}")
        file.write("\n")
        file.write("\t\\begin{singlespace}")
        file.write("\n")
        #file.write("\t{\\footnotesize {Robust standard errors are in parenthesis. *, ** and *** denote statistical significance at the 10 percent, 5 percent and 1 percent level respectively.}}")
        file.write("\n")
        file.write("\t\end{singlespace}")
        file.write("\n")
        file.write("\end{table}")
        file.write("\n")
        file.write("\n")
        
        file.write(r"\end{landscape}")
        file.write("\n")
        
        if toggle:
            file.write("\end{document}")  
