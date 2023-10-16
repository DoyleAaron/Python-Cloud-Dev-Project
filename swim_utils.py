from statistics import mean
import os
import webbrowser

Folder = r"swimdata/"


def convert2hundreths(timestring):
    """Given a string which represents a time, this function converts the string
    to a number (int) representing the string's hundredths of seconds value, which is
    returned.
    """
    if ":" in timestring:
        mins, rest = timestring.split(":")
        secs, hundredths = rest.split(".")
    else:
        mins = 0
        secs, hundredths = timestring.split(".")

    return int(hundredths) + (int(secs) * 100) + ((int(mins) * 60) * 100) 


def build_time_string(num_time):
    """ """
    secs, hundredths = str(round(num_time / 100, 2)).split(".")
    mins = int(secs) // 60
    seconds = int(secs) - mins*60
    return f"{mins}:{seconds}.{hundredths}"  


def get_swimmers_data(filename):
    """ """
    name, age, distance, stroke = filename.removesuffix(".txt").split("-")
    with open(Folder + filename) as fh:
        data = fh.read()    
    times = data.strip().split(",")
    converts = []  # empty list
    for t in times:
        converts.append(convert2hundreths(t))
    average = build_time_string(mean(converts))

    return name, age, distance, stroke, times, converts, average

def get_first_name(Folder):
    nameList = set()
    for filename in os.listdir(Folder):
        if filename != ".DS_Store":
            allData = get_swimmers_data(filename)
            nameList.add(allData[0])

    return nameList

def second_list_data(Folder, selectedName):
    dataList = set()
    for filename in os.listdir(Folder):
        if filename != ".DS_Store":
            allData = get_swimmers_data(filename)
            if selectedName == allData[0]:
                dataList.add(allData[1] + "-" + allData[2] + "-" + allData[3]) 
    return dataList

def convert2range(v, f_min, f_max, t_min, t_max):
    """Given a value (v) in the range f_min-f_max, convert the value
    to its equivalent value in the range t_min-t_max.

    Based on the technique described here:
        http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
    """
    return round(t_min + (t_max - t_min) * ((v - f_min) / (f_max - f_min)), 2)


def html_charts(fileToGraph):
    data = get_swimmers_data(fileToGraph)
    name, age, distance, stroke, times, values, average = data 
    title = f"{name} (Under {age}) {distance} - {stroke}"
    header = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>
                {title}
            </title>
        </head>
        <body>
            <h3>{title}</h3>
    """
    converts = []
    for n in values:
        converts.append(convert2range(n, 0, max(values)+50, 0, 400))
    times.reverse()
    converts.reverse()
    body = ""
    for t, c in zip(times, converts):
        svg = f""" 
                    <svg height="30" width="400">
                            <rect height="30" width="{c}" style="fill:rgb(0,0,255);" />
                    </svg>{t}<br />
                """
        body = body + svg
    footer = f""" 
            <p>Average: {average}</p>
        </body>
    </html>
    """
    html = header + body + footer
    html_file = "index.html"
    with open(html_file, "w") as f:
        print(html, file = f) 
    webbrowser.open_new_tab("file://" + os.path.realpath(html_file))