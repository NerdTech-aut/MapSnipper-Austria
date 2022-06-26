from pyproj import Transformer
import re
import folium
import csv
import argparse
import sqlite3
from datetime import datetime

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
    "<tr>"
    "<td>Google Maps:</td>"
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">Open on Google Maps</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Mobilfunknetz/Alle\" target=\"_blank\">Open on Breitbandatlas</a></td>"
    "</tr>"
    "</table>").format(sender_id, lat, lon, system1, leistung1, leistung2, max_dl, system3, leistung3, lat, lon, lat, lon)
    return text

# This function fils the popup of mobile coverage tiles with information.
def mobile_popup_text_function(raster_id, provider, band, tech, agv_dl, avg_ul, max_dl, max_ul, date, lat, lon, mnc):
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
    "<tr>"
    "<td>Google Maps:</td>"
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Mobilfunknetz/{}\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
    "</tr>"
    "<tr>"
    "<td>Cellmapper:</td>"
    "<td><a href=\"https://www.cellmapper.net/map?MCC=232&MNC={}&type=LTE&latitude={}&longitude={}&zoom=15.3\" target=\"_blank\">auf Cellmapper ansehen</a></td>"
    "</tr>"
    "</table>").format(raster_id, provider, band, tech, agv_dl, avg_ul, max_dl, max_ul, date, lat, lon, lat, lon, provider, mnc, lat, lon)
    return text

# This function fils the popup of the fixed broadband tiles with information.
def fixed_popup_text_function(raster_id, provider, tech, dl, ul, ratio, date, lat, lon):
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
    "<td>Download-Upload Verhältnis:</td>"
    "<td>{}:1</td>"
    "</tr>"
    "<tr>"
    "<td>Datum:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Google Maps:</td>"
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">Open on Google Maps</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Festnetz/\" target=\"_blank\">Open on Breitbandatlas</a></td>"
    "</tr>"
    "</table>").format(raster_id, provider, tech, dl, ul, ratio, date, lat, lon, lat, lon)
    return text

# This function fils the popup of the government supported broadband rollout tiles with information.
def grant_popup_text_function(raster_id, antrangsnummer, ausschreibung, fördernehmer, projekttitel, projektkosten, förderbetrag, fördersatz, förderbetrag_land, tag_gewährung, tag_vertragsabschluss, tag_projektende, förderbar_nach_prüfung, förderung_nach_prüfung, projektstatus, tag_bearbeitung, lat, lon):
    text = ("<table class=\"tbl\">"
    "<tr>"
    "<td class=\"lls\">Raster ID:</td>"
    "<td class=\"rls\">{}</td>"
    "</tr>"
    "<tr>"
    "<td>Antragsnummer:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Ausschreibung:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Fördernehmer:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Projekttitel:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Projektkosten:</td>"
    "<td>{} €</td>"
    "</tr>"
    "<tr>"
    "<td>Förderbetrag:</td>"
    "<td>{} €</td>"
    "</tr>"
    "<tr>"
    "<td>Fördersatz:</td>"
    "<td>{} %</td>"
    "</tr>"
    "<tr>"
    "<td>Förderbetrag Land Anschlussförderung:</td>"
    "<td>{} €</td>"
    "</tr>"
    "<tr>"
    "<td>Tag der Genehmigung:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Tag des Vertragsabschluss:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Projektende:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Förderbar nach Prüfung:</td>"
    "<td>{} €</td>"
    "</tr>"
    "<tr>"
    "<td>Förderung nach Prüfung:</td>"
    "<td>{} €</td>"
    "</tr>"
    "<tr>"
    "<td>Projektstatus:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Zuletzt bearbeitet:</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Google Maps:</td>"
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">Open on Google Maps</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Geförderter%20Ausbau/\" target=\"_blank\">Open on Breitbandatlas</a></td>"
    "</tr>"
    "</table>").format(raster_id, antrangsnummer, ausschreibung, fördernehmer, projekttitel, projektkosten, förderbetrag, fördersatz, förderbetrag_land, tag_gewährung, tag_vertragsabschluss, tag_projektende, förderbar_nach_prüfung, förderung_nach_prüfung, projektstatus, tag_bearbeitung, lat, lon, lat, lon)
    return text

start = datetime.now()

con = sqlite3.connect('map_data.db')
cur = con.cursor()

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
parser.add_argument("-grant", "--BroadbandGrant", action="store_true", help="adds government supported broadband rollout to the map")

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
print(args.A1TelekomAustria)
if args.A1TelekomAustria == True:
    operator_restriction = "A1"
elif args.MagentaTelekom == True:
    operator_restriction = "Magenta"
elif args.HutchisonDreiAustria == True:
    operator_restriction = "Drei"

# Setting the fixed broadband enabled boolean. 
fixed_enable = args.FixedBroadband

# Setting the financially supported broadband enabled Boolean.
grant_enable = args.BroadbandGrant

# Splitting the positional center argument into three parts:
# the scale
# the northern coordinate
# the eastern coordinate
center_split = re.split('mN|E',args.center)

# Setting uo the transformer from EPSG89:3035 to EPSG89:4326 (WSG84)
transformer = Transformer.from_crs(3035, 4326)

# Transforming the positional data of the center localtion to set the initial view of the map.
transformation_result = transformer.transform((int(center_split[1]) * int(center_split[0])), (int(center_split[2]) * int(center_split[0])))

# Setting up the folium map with a center location and a zoom level of 12.
m = folium.Map(location=[float(transformation_result[0]), float(transformation_result[1])], zoom_start=12)

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
for station in cur.execute('SELECT * FROM Cell_Sites WHERE LAT <= ? AND LAT >= ? AND LON <= ? AND LON >= ?', [transformation_result_TL[0], transformation_result_LR[0], transformation_result_TR[1], transformation_result_LL[1]]):
    # Create a tuple with the location data of a cell site marker.
    station_location = (float(station[2]), float(station[3]))
    # Setup the tooltip and the popup for a cell site marker.
    tooltip_text = station[1]
    marker_popup_text_string = marker_popup_text_function(station[1], station[2], station[3], station[4], round(float(station[5]),2), station[6], round(float(station[7]),2), station[8], round(float(station[9]),2))
    popup_text = folium.Popup(marker_popup_text_string, max_width=len(str(station[2])) * 25)
    # Creating a cell site marker and adding it to the cell site layer.
    folium.Marker(station_location, popup=popup_text, tooltip=tooltip_text).add_to(marker_layer)

# Adding the layer with the cell site markers to the map.
marker_layer.add_to(m)

#region Mobile
# Go through each operator in the network operators list.
for network_operator in cur.execute('SELECT * FROM Mobile_Operators').fetchall():
    # Continue if the current network operator meets the operator restriction and tech restriction, otherwise skip.
    if operator_restriction in network_operator[0] and tech_restriction in network_operator[7]:
        print("Analyzing " + network_operator[0] + " " + network_operator[1] + " MHz")

        # Create the folium map layer for the current operator.
        map_layer = folium.FeatureGroup(name = (network_operator[0] + " " + network_operator[1] + " MHz"), show=False)

        # The first bandwidth bracket is the lowest number to the lowest number + 10%.
        avg_dl_low = 0
        for row in cur.execute('SELECT DL_NORMAL FROM ' + network_operator[2] + ' ORDER BY DL_NORMAL ASC LIMIT 1'):
            avg_dl_low = row[0] * 1.1
        # The second bandwidth bracket is the lowest number + 10% to the average bandwidth out of all the average bandwidth numbers.
        avg_dl_avg = 0
        for row in cur.execute('SELECT AVG(DL_NORMAL) FROM ' + network_operator[2]):
            avg_dl_avg = row[0]
        # The thrid bandwidth bracket is the average bandwidth out of all the average bandwidth numbers to the highest number - 15%.
        avg_dl_high = 0
        for row in cur.execute('SELECT DL_NORMAL FROM ' + network_operator[2] + ' ORDER BY DL_NORMAL DESC LIMIT 1'):
            avg_dl_high = row[0] * 0.85
        # The fourth bandwidth bracket is the highest number - 15% to the highest number.

        i = 0

        # Go through each entry of the list imported from the csv file.
        for WSG84 in cur.execute('SELECT * FROM ' + network_operator[2] + ' WHERE DL_NORMAL > 0 AND UL_NORMAL > 0 AND DL_MAX > 0 AND UL_MAX > 0 AND NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', [int(center_split[1]) + radius, int(center_split[1]) - (radius + 1), int(center_split[2]) + radius, int(center_split[2]) - (radius + 1)]):
                    
            # The four transformations for the four corners of the tile.
            transformation_result_LL = transformer.transform((WSG84[5] * WSG84[4]), (WSG84[6] * WSG84[4]))
            transformation_result_LR = transformer.transform((WSG84[5] * WSG84[4]), ((WSG84[6] + 1) * WSG84[4]))
            transformation_result_TR = transformer.transform(((WSG84[5] + 1) * WSG84[4]), ((WSG84[6] + 1) * WSG84[4]))
            transformation_result_TL = transformer.transform(((WSG84[5] + 1) * WSG84[4]), (WSG84[6] * WSG84[4]))
            
            transformation_result_CE = transformer.transform(((WSG84[5] + 0.5) * WSG84[4]), ((WSG84[6] + 0.5) * WSG84[4]))

            col = ''
            col_data = WSG84[7]

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
            tooltip_text = network_operator[0] + " " + network_operator[1] + " MHz AVG Download: " + str(round(col_data / 1000000, 2)) + " Mbit/s"

            # Configure the popup of the tile.
            popup_text_string = mobile_popup_text_function(str(int(WSG84[4]))+'mN'+str(int(WSG84[5]))+'E'+str(int(WSG84[6])), network_operator[0], network_operator[1] + " MHz", network_operator[7],round(WSG84[7] / 1000000, 2), round(WSG84[8] / 1000000, 2), round(WSG84[9] / 1000000, 2), round(WSG84[10] / 1000000, 2), WSG84[3], transformation_result_CE[0], transformation_result_CE[1], network_operator[8])
            popup_text = folium.Popup(popup_text_string, max_width= (len(str(WSG84[4])) + len(str(WSG84[5])) + len(str(WSG84[6]))) * 25)
            
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
    
    
    for provider in cur.execute('SELECT DISTINCT INFRASTRUKTURANBIETER FROM Festnetz WHERE NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', [int(center_split[1]) + radius, int(center_split[1]) - (radius + 1), int(center_split[2]) + radius, int(center_split[2]) - (radius + 1)]).fetchall():
        map_layer = folium.FeatureGroup(name = provider, show = False)

        n = 0
        
        for entry in cur.execute('SELECT * FROM Festnetz WHERE INFRASTRUKTURANBIETER = ? AND NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', [provider[0], int(center_split[1]) + radius, int(center_split[1]) - (radius + 1), int(center_split[2]) + radius, int(center_split[2]) - (radius + 1)]):
                    
            # The four transformations for the four corners of the tile.
            transformation_result_LL = transformer.transform((entry[1] * entry[0]), (entry[2] * entry[0]))
            transformation_result_LR = transformer.transform((entry[1] * entry[0]), ((entry[2] + 1) * entry[0]))
            transformation_result_TR = transformer.transform(((entry[1] + 1) * entry[0]), ((entry[2] + 1) * entry[0]))
            transformation_result_TL = transformer.transform(((entry[1] + 1) * entry[0]), (entry[2] * entry[0]))
            
            transformation_result_CE = transformer.transform(((entry[1] + 0.5) * entry[0]), ((entry[2] + 0.5) * entry[0]))

            col = "#1b2433"

            tooltip_text = entry[3] + " " + entry[4] + " Download: " + str(round(float(entry[5])*0.5, 2)) if (entry[3] == "A1" and entry[4] == "xDSL") else str(entry[5]) + " Mbit/s"

            popup_text_string = fixed_popup_text_function(str(int(entry[0]))+'mN'+str(int(entry[1]))+'E'+str(int(entry[2])), entry[3], entry[4], str(round(float(entry[5])*0.5, 2)) if (entry[3] == "A1" and entry[4] == "xDSL") else entry[5], str(round(float(entry[6])*0.5, 2)) if (entry[3] == "A1" and entry[4] == "xDSL") else entry[6], str(round((round(float(entry[5])*0.5, 2) if (entry[3] == "A1" and entry[4] == "xDSL") else entry[5])/(round(float(entry[6])*0.5, 2) if (entry[3] == "A1" and entry[4] == "xDSL") else entry[6]), 2)), entry[7], transformation_result_CE[0], transformation_result_CE[1])
            popup_text = folium.Popup(popup_text_string, max_width=len(entry[7]) * 25)
                    
            folium.Polygon((transformation_result_LL,transformation_result_LR,transformation_result_TR,transformation_result_TL), popup_text, tooltip_text, color=col, fill=True).add_to(map_layer)

            n = n + 1
        
        print(provider[0] + ": " + str(n) + " tiles with coverage found\n")
        if(n > 0):
            map_layer.add_to(m)

#endregion

#region Grant
if grant_enable == True:

    map_layer = folium.FeatureGroup(name = "Geförderter Ausbau", show=False)
    n = 0

    for entry in cur.execute('SELECT * FROM Gefoerderter_Ausbau WHERE NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', [int(center_split[1]) + radius, int(center_split[1]) - (radius + 1), int(center_split[2]) + radius, int(center_split[2]) - (radius + 1)]):
        # The four transformations for the four corners of the tile.
        transformation_result_LL = transformer.transform((entry[1] * entry[0]), (entry[2] * entry[0]))
        transformation_result_LR = transformer.transform((entry[1] * entry[0]), ((entry[2] + 1) * entry[0]))
        transformation_result_TR = transformer.transform(((entry[1] + 1) * entry[0]), ((entry[2] + 1) * entry[0]))
        transformation_result_TL = transformer.transform(((entry[1] + 1) * entry[0]), (entry[2] * entry[0]))
        
        transformation_result_CE = transformer.transform(((entry[1] + 0.5) * entry[0]), ((entry[2] + 0.5) * entry[0]))

        col = "#6b798f"

        tooltip_text = entry[5] + " sollte das Projekt " + entry[6] + " bis " + entry[13] + " abschließen"

        popup_text_string = grant_popup_text_function(str(int(entry[0]))+'mN'+str(int(entry[1]))+'E'+str(int(entry[2])), entry[3], entry[4], entry[5], entry[6], str("{:,}".format(int(entry[7]))).replace(',', '.'), str("{:,}".format(int(entry[8]))).replace(',', '.'), entry[9], str("{:,}".format(int(entry[10]))).replace(',', '.'), entry[11], entry[12], entry[13], str("{:,}".format(int(entry[14]))).replace(',', '.'), str("{:,}".format(int(entry[15]))).replace(',', '.'), entry[16], entry[17], transformation_result_CE[0], transformation_result_CE[1])
        popup_text = folium.Popup(popup_text_string, max_width=len(entry[6]) * 25)
                
        folium.Polygon((transformation_result_LL,transformation_result_LR,transformation_result_TR,transformation_result_TL), popup_text, tooltip_text, color=col, fill=True).add_to(map_layer)

        n = n + 1
                
    print(str(n) + " tiles with government funded broadband rollout found\n")
    if(n > 0):
        map_layer.add_to(m)

#endregion

print("Write to File (this may take several seconds)")

folium.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(m)

m.save("index.html")

print("export of index.html is done")

end = datetime.now()

difference = end - start

print(difference)