import math
import os
import time
import urllib.request
import pandas as pd
import plotly.express as px
import folium
import webbrowser

from datetime import date, datetime
from branca.element import Template, MacroElement


def print_menu():
    """
    Function that prints the first menu
    don't :return:
    """
    print("\n"+32 * "-", "M E N U", 32 * "-")
    try:
        national_data = pd.read_json("data" + os.sep + "national.json")
        last_date = str(datetime.fromisoformat(national_data.iloc[-1]["data"]).date())
        print("1. Update files (last update: %s)" %(last_date))
    except ValueError:
        print("1. Download")
    print("2. National Submenu")
    print("3. Regional Submenu")
    print("4. CdC MarkDown")
    print("Type 'exit' to stop")
    print(73 * "-")


def try_download_file():
    """
    Function that try to download required files from github (pcm-dpc/COVID-19)
    If some errors happen during download, like "connection lost", it waits for 5 seconds.
    Print info about error in case no internet connection
    don't :return:
    """
    connection = True
    while connection:
        try:
            download_file(
                "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita"
                "-andamento-nazionale.json",
                "national.json", "data")
            download_file(
                "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni"
                ".json",
                "regional.json", "data")
            connection = False
        except urllib.error.URLError:
            print("[i] No connection with Host... retry in 5 seconds")
            connection = True
            time.sleep(5)


def print_submenu2():
    """
    Function to print the sub menu corresponding to national file analysis
    don't :return:
    """
    print("\n"+28 * "-", "N A T I O N A L", 28 * "-")
    print("1. Graph 7 days")
    print("2. Time Series")
    print("3. Max & Min")
    print("4. Quotient 2 variables")
    print("5. Go back to Main Menu")
    print(73 * "-")


def print_submenu3():
    """
    Function to print the sub menu corresponding to national file analysis
    don't :return:
    """
    print("\n"+28 * "-", "R E G I O N A L", 28 * "-")
    print("1. Time Chart Graph")
    print("2. Geographic Graph")
    print("3. Go back to Main Menu")
    print(73 * "-")


def download_file(url, filename, directory):
    """
    Function used to download or update a file from internet
    print info about download state
    :param url: URL of the .json file to download
    :param filename: filename with extension to save in local
    :param directory: name of directory in which file will be saved
    don't :return:
    """
    if not os.path.isdir(directory):
        print('[i] ' + directory + ' folder not found... creating it')
        os.mkdir(directory)
        os.chdir(directory)
        urllib.request.urlretrieve(url, filename)
        os.chdir("..")
        print('[i] ' + filename + ' downloaded in ' + directory + " folder")
    else:
        os.chdir(directory)
        urllib.request.urlretrieve(url, filename)
        os.chdir("..")
        print('[i] ' + filename + ' downloaded in existing folder: ' + directory)


def handle_choice_menu(numberOfChoiches=5):
    """
    function to handle n menu choices
    :return: the choice made by user
    """
    fatto = False 
    while not fatto:
        choice = input("Enter your choice [1-%d]: " %numberOfChoiches)
        try:
            choice = int(choice)
            fatto = choice >= 1 or choice <= numberOfChoiches
        except ValueError:
            fatto = choice[0].lower() == 'e'
    return choice


def national_mean_7_days(filename):
    """
    function that plots the 7 days mean of a variable related to a file
    :param filename: the name of file that function will use to plot 7 days mean
    show a plot of 7 days mean of variable related to filename
    don't :return:
    """
    national_data = pd.read_json(filename)
    variable = national_data.columns[::]
    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
    variable = variables_pool(variable)
    national_data[variable] = national_data[variable].rolling(window=7).mean()
    nat = national_data[national_data[variable] >= 0]
    plot_title = variable.replace("_", " ").capitalize()
    fig = px.line(x=nat["data"].str[0:10], y=nat[variable],
                  labels={'x': 'Day', 'y': "Number " + variable.replace("_", " ")})
    fig.update_layout(title=plot_title + " national")
    fig.show()


def time_series(filename):
    """
    function that plots the time series related to a variable of your file
    :param filename: the name of file function will use to plot time series
    show a plot of time series of variable associated to your file
    don't :return:
    """
    national_data = pd.read_json(filename)
    variable = national_data.columns[::]
    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
    variable = variables_pool(variable)
    nat = national_data[national_data[variable] >= 0]
    plot_title = variable.replace("_", " ").capitalize()
    fig = px.line(x=nat["data"].str[0:10], y=nat[variable],
                  labels={'x': 'Day', 'y': "Number " + variable.replace("_", " ")})
    fig.update_layout(title=plot_title + " national")
    fig.show()


def max_min(filename):
    """
    function that calculated the maximum and minimum related to a variable of your file
    :param filename: the name of file function will use to calculate max and min
    print maximum and minimum value
    don't :return:
    """
    national_data = pd.read_json(filename)
    variable = national_data.columns[::]
    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
    variable = variables_pool(variable)
    column = national_data[variable]
    max_value = column.max()
    min_value = column.min()
    print("Max: ", max_value, "\nMin: ", min_value)


def quotient_variable(dataframe, var1=None, var2=None):
    """
    Function that calculate the quotient of two variables in a specific date
    :param var1: variable chosen from pool (as numerator)
    :param var2: variable chosen from pool (as denominator)
    :param dataframe: the .json file function will handle
    print the quotient between var1 and var2
    don't :return: 
    """
    variable = dataframe.columns[::]
    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
    if var1==None or var2==None:
        var1 = variables_pool(variable, "pick one variable as numerator")
        var2 = variables_pool(variable, "pick one variable as denominator")
    my_date = verify_date(dataframe)
    entries = dataframe["data"] == str(my_date)
    numerator = dataframe[entries][var1]
    numerator = numerator.tolist()[0]
    denominator = dataframe[entries][var2]
    denominator = denominator.tolist()[0]
    quotient = numerator / denominator
    if not math.isnan(quotient):
        print("Ratio between %s and %s is: %s\n" % (var1, var2, round(quotient, 2)))
    else:
        var_not_null = dataframe[var1].notnull() & dataframe[var2].notnull()
        not_null_subset = dataframe[var_not_null]
        new_entries = (not_null_subset[var1] > 0) & (not_null_subset[var2] > 0)
        fixed_subset = not_null_subset[new_entries]
        print("[!] Values not defined in your date\n")
        quotient_variable(fixed_subset,var1,var2)


def temporary_graph(regional):
    """
    function that plots a variable of a region in a specific interval of time
    show a plot graph of your variable associated on a region in a specific period of time
    don't :return:
    """
    variables = regional.columns[::]
    variables = variables.delete([0, 1, 2, 3, 4, 5, 20, 22, 23])
    from_date = verify_date(regional,'starting')
    to_date = verify_date(regional,'ending',from_date)
    if to_date <= from_date:
        correct = False
        if from_date == to_date:
            print("[!] Cannot show temporary graph in only one day\n\n[i] Insert a valid period of time")
        while not correct:
            to_date = verify_date(regional,'ending')
            correct = to_date > from_date

    from_date = str(from_date)
    to_date = str(to_date)

    from_date = from_date[8:10] + from_date[4:8] + from_date[0:4]
    to_date = to_date[8:10] + to_date[4:8] + to_date[0:4]

    region_list = regional["denominazione_regione"].unique()
    region = variables_pool(region_list, "Insert a region")
    obs = variables_pool(variables, "Insert variable to analyze")
    regional["data"] = regional["data"].str[8:10] + regional["data"].str[4:8] + regional["data"].str[0:4]

    start = regional[regional['data'] == from_date].index.values.astype(int)[0]
    stop = regional[regional['data'] == to_date].index.values.astype(int)[0]
    subset = regional.index.to_series().between(start, stop)
    regional_dated = regional[subset]

    region_chosen = regional_dated["denominazione_regione"] == region
    plot_title = obs.replace("_", " ").capitalize()
    fig = px.line(x=regional_dated[region_chosen]["data"], y=regional_dated[region_chosen][obs],
                  labels={'x': 'Day', 'y': "Number " + obs.replace("_", " ")})
    fig.update_layout(title=plot_title + ": " + str(region))
    fig.show()
    

def variables_pool(variable, question='Variable to analyze'):
    """
    :param variable: the variable chosen from variable pool in your dataframe
    :param question: default parameter ("Variable to analyze")
    don't :return:
    """

    def guide(diz):
        """
        function that guides user to chose the right variable
        :param diz: dictionary with key a int number and for value the associate variable
        don't :return:
        """
        print("[i] Chose one from this list:")
        for a_key in diz:
            print("\t%s\t→ %s" % (str(a_key), str(diz[a_key])))

    dictionary = {}

    try:
        variable = variable.tolist()
    except AttributeError:
        if type(variable) == type(list()):
            pass
        elif type(variable) == type(str()):
            variable = variable.strip().split()
            for i in range(0,len(variable)):
                variable[i] = variable[i].strip()
        else:
            raise AttributeError("I can't handle "+str(type(variable))+" object")
    for i in range(1, len(variable)+1):
        dictionary[i] = variable[i-1]

    done = False
    while not done:
        print("\n"+73 * "-")
        guide(dictionary)
        key = input("%s [1-%d]: " % (question,len(variable)))
        try:
            key = int(key)
            if key in dictionary.keys():
                done = True
                return dictionary[key]
            else:
                print("Unknown variable...")
        except ValueError:
            if key in dictionary.values() and key != 0:
                return key
            else:
                print("Unknown variable...")


def verify_date(pd_dataframe,question='\b',s_date=None):
    """
    function that verify if the insert date is in an allowed interval for your dataframe
    :param pd_dataframe: the panda's dataframe take as pd.read_json(path_to_file.json).
    :param question: default parameter is a backspace for cancel a space between 'insert' and 'date'
    :return: the date insert if correct
    """
    min_date = datetime.fromisoformat(pd_dataframe.iloc[0]["data"]).date()
    max_date = datetime.fromisoformat(pd_dataframe.iloc[-1]["data"]).date()
    if s_date != None:
        try:
            s_date = date.fromisoformat(s_date)
        except TypeError:
            pass
        if s_date > min_date:
            min_date = s_date
    

    print("Insert a date between %s and %s" % (str(min_date), str(max_date)))
    done = False
    while not done:
        my_date = input("Insert %s date (e.g format YYYY-MM-DD): " %question)
        try:
            my_date = date.fromisoformat(my_date)
            if min_date <= my_date <= max_date:
                done = True
            else:
                print("[!] Date not in range between %s and %s\n" % (str(min_date), str(max_date)))
        except ValueError:
            print("[!] Format not corresponding to requested\n")
    return my_date


def geographic_graph(regional):
    """
    function that plots the geographic_graph of a variable in a specific date of all the regions in your regional dataframe
    open a browser's tab for showing the map requested
    don't :return:
    """
    variables = regional.columns[::]
    variables = variables.delete([0, 1, 2, 3, 4, 5, 20, 22, 23])
    my_date = verify_date(regional)
    obs = variables_pool(variables, "Insert variable to analyze")
    regional["data"] = regional["data"].str[0:10]
    entries = regional["data"] == str(my_date)
    list_value = regional[entries][obs].tolist()
    longitudini = regional["long"].tolist()[:21]
    latitudini = regional["lat"].tolist()[:21]
    nomi = regional["denominazione_regione"].tolist()[:21]

    color = []
    for k in range(0, len(list_value)):
        if math.isnan(list_value[k]) or list_value[k] == 0:
            list_value[k] = 0
            color.append("green")
        else:
            color.append("crimson")
    try:
        alfa = max(list_value)
        omega = 50000
        scaled_value_list = []
        for i in range(0, len(list_value)):
            equation = (list_value[i] * omega) / alfa
            scaled_value_list.append(equation)
    except ZeroDivisionError:
        scaled_value_list = [0] * len(list_value)
    
        print("[!] Value not defined in this date")
    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)
    for i in range(0, len(list_value)):
        list_value[i] = int(list_value[i])
        folium.Circle(
            location=(latitudini[i], longitudini[i]),
            popup=nomi[i] + "\n" + obs.replace("_", " ").capitalize() + ": " + str(list_value[i]),
            radius=scaled_value_list[i],
            color=color[i],
            fill=True,
            fill_color='crimson'
        ).add_to(m)
    template1 = "    {% macro html(this, kwargs) %}    <!doctype html>    <html lang=\"en\">    <head>      <meta charset=\"utf-8\">      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">      <title>ITALY COVID-19</title>   </head>    <body>    <div id='maplegend' class='maplegend'         style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>    <div class='legend-title'>"
    template = "Data: %s</div>" % str(my_date)
    template = template1+template
    template = template + "    <div class='legend-scale'>      <ul class='legend-labels'>        <li><span style='background:red;opacity:0.7;'></span>Valore presente</li>        <li><span style='background:green;opacity:0.7;'></span>Valore non presente</li>      </ul>    </div>    </div>    </body>    </html>    <style type='text/css'>      .maplegend .legend-title {        text-align: left;        margin-bottom: 5px;        font-weight: bold;        font-size: 90%;        }      .maplegend .legend-scale ul {        margin: 0;        margin-bottom: 5px;        padding: 0;        float: left;        list-style: none;        }      .maplegend .legend-scale ul li {        font-size: 80%;        list-style: none;        margin-left: 0;        line-height: 18px;        margin-bottom: 2px;        }      .maplegend ul.legend-labels li span {        display: block;        float: left;        height: 16px;        width: 30px;        margin-right: 5px;        margin-left: 0;        border: 1px solid #999;        }      .maplegend .legend-source {        font-size: 80%;        color: #777;        clear: both;        }      .maplegend a {        color: #777;        }    </style>    {"""+"""%"""+" endmacro %}"
    macro = MacroElement()
    macro._template = Template(template)
    m.add_child(macro)
    m.save("data" + os.sep + "%s_italy_%s.html" %(str(my_date),obs))
    webbrowser.open_new_tab("data" + os.sep + "%s_italy_%s.html" %(str(my_date),obs))

def show_credits():
    webbrowser.open_new_tab("data" + os.sep + "CdC_MarkDown.html")
