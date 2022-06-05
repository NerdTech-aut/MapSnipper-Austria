from pyproj import Transformer
import re
import folium
import csv
import argparse

# This function fils the popup of the cell site markers with information.
def marker_popup_text_function(sender_id, lat, lon, system1, leistung1, leistung2, max_dl, system3, leistung3):
    text = ("<table class=\"tbl\">"
    "<tr>"
    "<td class=\"lls\">Sender ID:</td>"
    "<td class=\"rls\">{}</td>"
    "</tr>"
    "<tr>"
    "<td>Breitengrad (lat):</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Längengrad (lon):</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 1 Technologien:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 1 Leistung:</td>"
    "<td>{} Watt</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 2 Technologien:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 2 Leistung:</td>"
    "<td>{} Watt</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 3 Technologien:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Sender 3 Leistung:</td>"
    "<td>{} Watt</td>"
    "</tr>"
    "</table>").format(sender_id, lat, lon, system1, leistung1, leistung2, max_dl, system3, leistung3)
    return text

# This function fils the popup of mobile coverage tiles with information.
def mobile_popup_text_function(raster_id, provider, band, tech, agv_dl, avg_ul, max_dl, max_ul, date):
    text = ("<table class=\"tbl\">"
    "<tr>"
    "<td class=\"lls\">Raster ID:</td>"
    "<td class=\"rls\">{}</td>"
    "</tr>"
    "<tr>"
    "<td>Anbieter:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Frequenz:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Technologie:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>AVG Download:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>AVG Upload:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>Max Download:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>Max Upload:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>Datum:</td>"
    "<td>{}</td>"
    "</tr>"
    "</table>").format(raster_id, provider, band, tech, agv_dl, avg_ul, max_dl, max_ul, date)
    return text

# This function fils the popup of the fixed broadband tiles with information.
def fixed_popup_text_function(raster_id, provider, tech, dl, ul, date):
    text = ("<table class=\"tbl\">"
    "<tr>"
    "<td class=\"lls\">Raster ID:</td>"
    "<td class=\"rls\">{}</td>"
    "</tr>"
    "<tr>"
    "<td>Anbieter:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Technologie:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Download:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>Upload:</td>"
    "<td>{} Mbit/s</td>"
    "</tr>"
    "<tr>"
    "<td>Datum:</td>"
    "<td>{}</td>"
    "</tr>"
    "</table>").format(raster_id, provider, tech, dl, ul, date)
    return text

# This is the list with information on all the mobile operator layers. An entry contains:
# the name of the operator
# the frequency band
# the cvs file name
# the color for the tiles with an average bandwidth that is lower then the lowest average bandwidth out of all the tiles in this layer + 10%
# the color for the tiles with an average bandwidth that is lower then the average bandwidth out of all the tiles in this layer
# the color for the tiles with an average bandwidth that is lower then the highest average bandwidth out of all the tiles in this layer - 15%
# the color for the tiles with an average bandwidth that is higher then the highest average bandwidth out of all the tiles in this layer - 15%
# the technology
network_operators = []
network_operators.append(["A1", "800", "A1_0800_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "4G/LTE"])
network_operators.append(["A1", "900", "A1_0900_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "2G/GSM & 3G/UMTS"])
network_operators.append(["A1", "1.800", "A1_1800_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "4G/LTE"])
network_operators.append(["A1", "2.100", "A1_2100_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "3G/UMTS & 5G/NR NSA"])
network_operators.append(["A1", "2.600", "A1_2600_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "4G/LTE"])
network_operators.append(["A1", "3.500", "A1_5GNR3500_Final_20220331.csv", "#ee8ea7", "#e66686", "#ff2f2b", "#940a03", "5G/NR NSA"])
network_operators.append(["Magenta", "3.500", "SPEED_5G_22Q1.csv", "#ffc1e1", "#ff79be", "#e20075", "#9d0054", "5G/NR NSA"])
network_operators.append(["Drei", "3.500", "h3a-versorgung-rohdaten.csv", "#ffba8c", "#ff7d27", "#ea5e00", "#953c00", "5G/NR NSA"])
network_operators.append(["Spusu", "3.500", "OpenDataRasterdatenMASS.csv", "#8eeaaa", "#95d600", "#22b14d", "#00605b", "5G/NR SA"])
network_operators.append(["Liwest", "3.500", "rtr_f716_20220426.csv", "#99d8ea", "#8f92be", "#00a2e8", "#3f48cc", "5G/NR Fixed Wireless"])
network_operators.append(["Graz Holding Citycom", "3.500", "GrazNewRadio_Versorgungskarte.csv", "#99d8ea", "#8f92be", "#00a2e8", "#3f48cc", "5G/NR Fixed Wireless"])
network_operators.append(["Salzburg AG CableLink Air", "3.500", "RohdatenSalzburgAG3_5GHz.csv", "#c8c2cf", "#a69cb1", "#7b6d8b", "#484051", "5G/NR Fixed Wireless"])

# Adding all the arguments to the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument("center", help="enter the center point for this map. Like: 100mN28087E47942")
parser.add_argument("-r", "--radius", type=float, required=False, help="enter a radius in km (default: 5 km)", default= 5)
parser.add_argument("-2G", "--twoG", action="store_true", help="only process layers with 2G; some layers might include multiple technologies")
parser.add_argument("-3G", "--threeG", action="store_true", help="only process layers with 3G; some layers might include multiple technologies")
parser.add_argument("-4G", "--fourG", action="store_true", help="only process layers with 4G; some layers might include multiple technologies")
parser.add_argument("-5G", "--fiveG", action="store_true", help="only process layers with 5G; some layers might include multiple technologies")
parser.add_argument("-FWA", "--FixedWirelessAccess", action="store_true", help="only process layers with fixed wireless access")
parser.add_argument("-A1", "--A1TelekomAustria", action="store_true", help="only process layers from A1 Telekom Austria")
parser.add_argument("-Magenta", "--MagentaTelekom", action="store_true", help="only process layers with Magenta Telekom")
parser.add_argument("-Drei", "--HutchisonDreiAustria", action="store_true", help="only process layers from Hutchison Drei Austria")
parser.add_argument("-fixed", "--FixedBroadband", action="store_true", help="adds fixed broadband providers to the map")

# Settings the args variablewith the argument data from the argument parser.
args = parser.parse_args()

# Setting the radius variable with the data from the argument. It needs to be converted into hectometres for further use (*10).
radius = args.radius * 10

# Configuration of the tech restriction string.
tech_restriction = ""
if args.twoG == True:
    tech_restriction = "2G"
elif args.threeG == True:
    tech_restriction = "3G"
elif args.fourG == True:
    tech_restriction = "4G"
elif args.fiveG == True:
    tech_restriction = "5G"
elif args.FixedWirelessAccess == True:
    tech_restriction = "Fixed Wireless"

# Configuration of the operator restriction string.
operator_restriction = ""
if args.A1TelekomAustria == True:
    operator_restriction = "A1"
elif args.MagentaTelekom == True:
    operator_restriction = "Magenta"
elif args.HutchisonDreiAustria == True:
    operator_restriction = "Drei"

# Setting the fixed broadband enabled boolean. 
fixed_enable = args.FixedBroadband

# Splitting the positional center argument into three parts:
# the scale
# the northern coordinate
# the eastern coordinate
center_split = re.split('mN|E',args.center)

# Setting uo the transformer from EPSG89:3035 to EPSG89:4326 (WSG84)
transformer = Transformer.from_crs(3035, 4326)

# Transforming the positional data of the center localtion to set the initial view of the map.
transformation_result = transformer.transform((int(center_split[1]) * int(center_split[0])), (int(center_split[2]) * int(center_split[0])))

# Converting the positional data from a tuple into a string, remove the brackets and split the string into the two coordinate parts.
transformation_result_str = str(transformation_result).replace('(', '').replace(')', '')
transformation_result_split = re.split(', ', transformation_result_str)

# Setting up the folium map with a center location and a zoom level of 12.
m = folium.Map(location=[float(transformation_result_split[0]), float(transformation_result_split[1])], zoom_start=12)

# The four transformations for the four corners of a square with a radius around the center tile.
transformation_result_LL = transformer.transform(((int(center_split[1]) - radius) * int(center_split[0])), ((int(center_split[2]) - radius) * int(center_split[0])))
transformation_result_LR = transformer.transform(((int(center_split[1]) - radius) * int(center_split[0])), ((int(center_split[2]) + radius) * int(center_split[0])))
transformation_result_TR = transformer.transform(((int(center_split[1]) + radius) * int(center_split[0])), ((int(center_split[2]) + radius) * int(center_split[0])))
transformation_result_TL = transformer.transform(((int(center_split[1]) + radius) * int(center_split[0])), ((int(center_split[2]) - radius) * int(center_split[0])))

# Creating a polygon border around the center tile and adding it to the map.
folium.Polygon((transformation_result_LL,transformation_result_LR,transformation_result_TR,transformation_result_TL), "tiles border", "tiles border", color='#ff7800').add_to(m)

# Creating the cell site marker layer.
marker_layer = folium.FeatureGroup("Sendemasten")

# Open the csv file with the cell site data. 
with open("stations.csv") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=';')
        line_count = 0
        # Cycle through each line in the csv file
        for station in csv_reader:
            # Skip the first line since it is the header
            if line_count == 0:
                line_count += 1
            else:
                # Create a tuple with the location data of a cell site marker.
                station_location = (float(station[2]), float(station[3]))
                # Only if the location of the cell site is within the square it can be added to the map. This square is slightly different then the square of the tiles. 
                if(station_location[0] >= transformation_result_LR[0] and station_location[0] <= transformation_result_TL[0] and station_location[1] >= transformation_result_LL[1] and station_location[1] <= transformation_result_TR[1]):
                    # Setup the tooltip and the popup for a cell site marker.
                    tooltip_text = station[1]
                    marker_popup_text_string = marker_popup_text_function(station[1], station[2], station[3], station[4], round(float(station[5]),2), station[6], round(float(station[7]),2), station[8], round(float(station[9]),2))
                    popup_text = folium.Popup(marker_popup_text_string, max_width=len(station[2]) * 25)
                    # Creating a cell site marker and adding it to the cell site layer.
                    folium.Marker(station_location, popup=popup_text, tooltip=tooltip_text).add_to(marker_layer)

# Adding the layer with the cell site markers to the map.
marker_layer.add_to(m)

#region Mobile
# Go through each operator in the network operators list.
for network_operator in network_operators:
    # Continue if the current network operator meets the operator restriction and tech restriction, otherwise skip.
    if operator_restriction in network_operator[0] and tech_restriction in network_operator[7]:
        print("Analyzing " + network_operator[0] + " " + network_operator[1] + " MHz")

        csv_lines = []
        avg_dl = []

        # Create the folium map layer for the current operator.
        map_layer = folium.FeatureGroup(name = (network_operator[0] + " " + network_operator[1] + " MHz"), show=False)

        # Open the csv file of the current operator defined in the network operators list.
        with open(network_operator[2]) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=';')
            line_count = 0
            # Go through each line of the csv file
            for row in csv_reader:
                # Skip the first line since it is the header
                if line_count == 0:
                    line_count += 1
                else:
                    # Add the list of the current row to a list.
                    csv_lines.append(row)

                    # If the average bandwidth of the current row isn't 0 add it to the list. 
                    if float(row[5]) != 0:
                        avg_dl.append(float(row[5]))

        # Sort the list of all the average downlink numbers for this operator in an ascending order.
        avg_dl.sort()
        # The first bandwidth bracket is the lowest number to the lowest number + 10%.
        avg_dl_low = avg_dl[0]*1.1
        # The second bandwidth bracket is the lowest number + 10% to the average bandwidth out of all the average bandwidth numbers.
        avg_dl_avg = sum(avg_dl)/len(avg_dl)
        # The thrid bandwidth bracket is the average bandwidth out of all the average bandwidth numbers to the highest number - 15%.
        avg_dl_high = avg_dl[len(avg_dl)-1]*0.85
        # The fourth bandwidth bracket is the highest number - 15% to the highest number.


        i = 0

        # Go through each entry of the list imported from the csv file.
        for WSG84 in csv_lines:

            # Check if the average and max bandwidth numbers aren't 0.
            if(int(WSG84[5]) != 0 and int(WSG84[6]) != 0 and int(WSG84[7]) != 0 and int(WSG84[8]) != 0):
            
                # Split the positional center argument into three parts:
                # the scale
                # the northern coordinate
                # the eastern coordinate
                WSG84_split = re.split('mN|E',WSG84[4])

                # Check if the current entry is within the borders of the square.
                if(int(WSG84_split[1]) < int(center_split[1]) + radius and int(WSG84_split[1]) > int(center_split[1]) - (radius + 1)  and int(WSG84_split[2]) < int(center_split[2]) + radius and int(WSG84_split[2]) > int(center_split[2]) - (radius + 1)):

                    # The four transformations for the four corners of the tile.
                    transformation_result_LL = transformer.transform((int(WSG84_split[1]) * int(WSG84_split[0])), (int(WSG84_split[2]) * int(WSG84_split[0])))
                    transformation_result_LR = transformer.transform((int(WSG84_split[1]) * int(WSG84_split[0])), ((int(WSG84_split[2]) + 1) * int(WSG84_split[0])))
                    transformation_result_TR = transformer.transform(((int(WSG84_split[1]) + 1) * int(WSG84_split[0])), ((int(WSG84_split[2]) + 1) * int(WSG84_split[0])))
                    transformation_result_TL = transformer.transform(((int(WSG84_split[1]) + 1) * int(WSG84_split[0])), (int(WSG84_split[2]) * int(WSG84_split[0])))

                    col = ''
                    col_data = int(WSG84[5])

                    # Select the color of the tile based on the average bandwidth.
                    if (col_data < avg_dl_low):
                        col = network_operator[3]
                    elif (col_data < avg_dl_avg):
                        col = network_operator[4]
                    elif (col_data < avg_dl_high):
                        col = network_operator[5]
                    else:
                        col = network_operator[6]

                    # Configure the text for the tooltip of the tile.
                    tooltip_text = network_operator[0] + " " + network_operator[1] + " MHz AVG Download: " + str(col_data / 1000000) + " Mbit/s"

                    # Configure the popup of the tile.
                    popup_text_string = mobile_popup_text_function(WSG84[4], network_operator[0], network_operator[1] + " MHz", network_operator[7],round(float(WSG84[5]) / 1000000, 2), round(float(WSG84[6]) / 1000000, 2), round(float(WSG84[7]) / 1000000, 2), round(float(WSG84[8]) / 1000000, 2), WSG84[3])
                    popup_text = folium.Popup(popup_text_string, max_width=len(WSG84[4]) * 25)
                    
                    # Create the tile as a folum polygon and add it to the current operators layer. 
                    folium.Polygon((transformation_result_LL,transformation_result_LR,transformation_result_TR,transformation_result_TL), popup_text, tooltip_text, color=col, fill=True).add_to(map_layer)

                    i = i + 1
                else:
                    o = 0

        # Print how many tiles were found from this operator in the square.
        print (network_operator[0] + " " + network_operator[1] + " MHz: " + str(i) + " tiles with coverage found\n")
        # If there are tiles in the map layer add the layer to the foium map.
        if(i>0):
            map_layer.add_to(m)
#endregion

#region Fixed
if fixed_enable == True:
    line_count = 0
    provider_list = []
    entry_list = []

    with open("festnetz_2021q3_20220203.csv") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            for entry in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    entry_list.append(entry)
                    if(len(provider_list) == 0):
                        provider_list.append(entry[1])
                    elif entry[1] not in provider_list:
                        provider_list.append(entry[1])

    for provider in provider_list:
        map_layer = folium.FeatureGroup(name = (provider), show=False)

        n = 0

        for entry in entry_list:
            if(entry[1] == provider):
                WSG84_split = re.split('mN|E', entry[0])

                if(int(WSG84_split[1]) < int(center_split[1]) + radius and int(WSG84_split[1]) > int(center_split[1]) - (radius + 1)  and int(WSG84_split[2]) < int(center_split[2]) + radius and int(WSG84_split[2]) > int(center_split[2]) - (radius + 1)):
                    
                    transformation_result_LL = transformer.transform((int(WSG84_split[1]) * int(WSG84_split[0])), (int(WSG84_split[2]) * int(WSG84_split[0])))
                    transformation_result_LR = transformer.transform((int(WSG84_split[1]) * int(WSG84_split[0])), ((int(WSG84_split[2]) + 1) * int(WSG84_split[0])))
                    transformation_result_TR = transformer.transform(((int(WSG84_split[1]) + 1) * int(WSG84_split[0])), ((int(WSG84_split[2]) + 1) * int(WSG84_split[0])))
                    transformation_result_TL = transformer.transform(((int(WSG84_split[1]) + 1) * int(WSG84_split[0])), (int(WSG84_split[2]) * int(WSG84_split[0])))

                    col = "#1b2433"

                    tooltip_text = entry[1] + " " + entry[2] + " Download: " + entry[3] + " Mbit/s"

                    popup_text_string = fixed_popup_text_function(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
                    popup_text = folium.Popup(popup_text_string, max_width=len(WSG84[4]) * 25)
                            
                    folium.Polygon((transformation_result_LL,transformation_result_LR,transformation_result_TR,transformation_result_TL), popup_text, tooltip_text, color=col, fill=True).add_to(map_layer)

                    n = n + 1
                else:
                    o = 0
        
        
        print(provider + ": " + str(n) + " tiles with coverage found\n")
        if(n > 0):
            map_layer.add_to(m)

#endregion

print("Write to File (this may take several seconds)")

folium.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(m)

m.save("index.html")

print("export of index.html is done")