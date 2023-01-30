from pyproj import Transformer
import re
import folium
import argparse
import sqlite3
from datetime import datetime

# This function fils the popup of the cell site markers with information.
def border_popup_text_function(center, center_lat_lon, lower_left_lat_lon, lower_right_lat_lon, top_right_lat_lon, top_left_lat_lon):
    text = ("<table class=\"tbl\">"
    "<tr>"
    "<td class=\"lls\">Zentrum:</td>"
    "<td class=\"rls\">{}</td>"
    "</tr>"
    "<tr>"
    "<td>Zentrum (lat & lon):</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Unten Links (lat & lon):</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Unten Rechts (lat & lon):</td>"
    "<td>{}</td>"
    "</tr>"
    "<tr>"
    "<td>Oben Rechts (lat & lon):</td>"
    "<td>{} Watt</td>"
    "</tr>"
    "<tr>"
    "<td>Oben Links (lat & lon):</td>"
    "<td>{}</td>"
    "</tr>"
    "</table>").format(center, str(center_lat_lon[0]) + "," + str(center_lat_lon[1]), str(lower_left_lat_lon[0]) + "," + str(lower_left_lat_lon[1]), str(lower_right_lat_lon[0]) + "," + str(lower_right_lat_lon[1]), str(top_right_lat_lon[0]) + "," + str(top_right_lat_lon[1]), str(top_left_lat_lon[0]) + "," + str(top_left_lat_lon[1]))
    return text

# This function fils the popup of the cell site markers with information.
def marker_popup_text_function(sender_id, lat, lon, system1, leistung1, system2, leistung2, system3, leistung3):
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
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Mobilfunknetz/Alle\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
    "</tr>"
    "</table>").format(sender_id, lat, lon, system1, leistung1, system2, leistung2, system3, leistung3, lat, lon, lat, lon)
    return text

# This function fills the popup of mobile coverage squares with information.
def mobile_popup_text_function(raster_id, provider, frequency_band, technology, average_download, average_upload, maximum_download, maximum_upload, date, lat, lon, mnc, cellmapper_network_technology):
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
    "<td><a href=\"https://www.cellmapper.net/map?MCC=232&MNC={}&type={}&latitude={}&longitude={}&zoom=15.3\" target=\"_blank\">auf Cellmapper ansehen</a></td>"
    "</tr>"
    "</table>").format(raster_id, provider, frequency_band, technology, average_download, average_upload, maximum_download, maximum_upload, date, lat, lon, lat, lon, provider, mnc, cellmapper_network_technology, lat, lon)
    return text

# This function fils the popup of the fixed broadband squares with information.
def fixed_popup_text_function(raster_id, provider, technology, download_speed, upload_speed, download_upload_ratio, date, lat, lon):
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
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Festnetz/\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
    "</tr>"
    "</table>").format(raster_id, provider, technology, download_speed, upload_speed, download_upload_ratio, date, lat, lon, lat, lon)
    return text

# This function fils the popup of the government supported broadband rollout squares with information.
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
    "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
    "</tr>"
    "<tr>"
    "<td>Breitbandatlas:</td>"
    "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Geförderter%20Ausbau/\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
    "</tr>"
    "</table>").format(raster_id, antrangsnummer, ausschreibung, fördernehmer, projekttitel, projektkosten, förderbetrag, fördersatz, förderbetrag_land, tag_gewährung, tag_vertragsabschluss, tag_projektende, förderbar_nach_prüfung, förderung_nach_prüfung, projektstatus, tag_bearbeitung, lat, lon, lat, lon)
    return text

# Save the starttime of this programs execution.
program_execution_start_timestamp = datetime.now()

# Create a new SQLite connection
sqlite3_database_connection = sqlite3.connect('map_data.db')

# Create a new SQLite cursor
sqlite3_database_cursor = sqlite3_database_connection.cursor()

# Add all the arguments to the argument parser.
CLI_argument_parser = argparse.ArgumentParser()
CLI_argument_parser.add_argument("center", help="enter the center point for this map. Like: 100mN28087E47942")
CLI_argument_parser.add_argument("-r", "--radius", type=float, required=False, help="enter a radius in km (default: 5 km)", default= 5)
CLI_argument_parser.add_argument("-2G", "--twoG", action="store_true", help="only process layers with 2G; some layers might include multiple technologies")
CLI_argument_parser.add_argument("-3G", "--threeG", action="store_true", help="only process layers with 3G; some layers might include multiple technologies")
CLI_argument_parser.add_argument("-4G", "--fourG", action="store_true", help="only process layers with 4G; some layers might include multiple technologies")
CLI_argument_parser.add_argument("-5G", "--fiveG", action="store_true", help="only process layers with 5G; some layers might include multiple technologies")
CLI_argument_parser.add_argument("-FWA", "--FixedWirelessAccess", action="store_true", help="only process layers with fixed wireless access")
CLI_argument_parser.add_argument("-A1", "--A1TelekomAustria", action="store_true", help="only process layers from A1 Telekom Austria")
CLI_argument_parser.add_argument("-Magenta", "--MagentaTelekom", action="store_true", help="only process layers with Magenta Telekom")
CLI_argument_parser.add_argument("-Drei", "--HutchisonDreiAustria", action="store_true", help="only process layers from Hutchison Drei Austria")
CLI_argument_parser.add_argument("-fixed", "--FixedBroadband", action="store_true", help="adds fixed broadband providers to the map")
CLI_argument_parser.add_argument("-grant", "--BroadbandGrant", action="store_true", help="adds government supported broadband rollout to the map")

# Settings the args variablewith the argument data from the argument parser.
CLI_arguments = CLI_argument_parser.parse_args()

# Setting the radius variable with the data from the argument. It needs to be converted into hectometres for further use (*10).
radius_from_center_point = CLI_arguments.radius * 10

# Configuration of the tech restriction string.
technology_filter = ""
if CLI_arguments.twoG == True:
    technology_filter = "2G"
elif CLI_arguments.threeG == True:
    technology_filter = "3G"
elif CLI_arguments.fourG == True:
    technology_filter = "4G"
elif CLI_arguments.fiveG == True:
    technology_filter = "5G"
elif CLI_arguments.FixedWirelessAccess == True:
    technology_filter = "Fixed Wireless"

# Configuration of the operator restriction string.
operator_filter = ""
if CLI_arguments.A1TelekomAustria == True:
    operator_filter = "A1"
elif CLI_arguments.MagentaTelekom == True:
    operator_filter = "Magenta"
elif CLI_arguments.HutchisonDreiAustria == True:
    operator_filter = "Drei"

# Set the fixed broadband enabled boolean. 
fixed_broadband_enabled = CLI_arguments.FixedBroadband

# Set the financially supported broadband enabled Boolean.
grant_enable = CLI_arguments.BroadbandGrant

# Split the positional center argument into three parts:
# the scale
# the northern coordinate
# the eastern coordinate
center_point_split = re.split('mN|E',CLI_arguments.center)

center_point_scale = int(center_point_split[0])
center_point_latitude_LAEA_Europe = int(center_point_split[1])
center_point_longitude_LAEA_Europe = int(center_point_split[2])

# Set uo the transformer from EPSG:3035 (ETRS89) aka LAEA Europe to EPSG:4326 (WSG84) aka GPS coordinates
transform_from_LAEA_Europe_to_GPS = Transformer.from_crs(3035, 4326)

# Transform the positional data of the center localtion to set the initial view of the map.
coordinates_of_map_center = transform_from_LAEA_Europe_to_GPS.transform((center_point_latitude_LAEA_Europe * center_point_scale), (center_point_longitude_LAEA_Europe * center_point_scale))

# Setting up the folium map with a center location and a zoom level of 12.
folium_map = folium.Map(location=[float(coordinates_of_map_center[0]), float(coordinates_of_map_center[1])], zoom_start=12)

# The four transformations for the four corners of a square with a radius around the center square.
coordinates_of_radius_border_lower_left_corner = transform_from_LAEA_Europe_to_GPS.transform(((center_point_latitude_LAEA_Europe - radius_from_center_point) * center_point_scale), ((center_point_longitude_LAEA_Europe - radius_from_center_point) * center_point_scale))
coordinates_of_radius_border_lower_right_corner = transform_from_LAEA_Europe_to_GPS.transform(((center_point_latitude_LAEA_Europe - radius_from_center_point) * center_point_scale), ((center_point_longitude_LAEA_Europe + radius_from_center_point) * center_point_scale))
coordinates_of_radius_border_top_right_corner = transform_from_LAEA_Europe_to_GPS.transform(((center_point_latitude_LAEA_Europe + radius_from_center_point) * center_point_scale), ((center_point_longitude_LAEA_Europe + radius_from_center_point) * center_point_scale))
coordinates_of_radius_border_top_left_corner = transform_from_LAEA_Europe_to_GPS.transform(((center_point_latitude_LAEA_Europe + radius_from_center_point) * center_point_scale), ((center_point_longitude_LAEA_Europe - radius_from_center_point) * center_point_scale))

# Configure the text for the tooltip of the square.
radius_border_tooltip_text = "Rahmen für Zentrum " + CLI_arguments.center + ": " + str(coordinates_of_map_center[0]) + " " + str(coordinates_of_map_center[1])

# Configure the popup of the square.
radius_border_popup_text_string = border_popup_text_function(CLI_arguments.center, coordinates_of_map_center, coordinates_of_radius_border_lower_left_corner, coordinates_of_radius_border_lower_right_corner, coordinates_of_radius_border_top_right_corner, coordinates_of_radius_border_top_left_corner)
radius_border_popup_text = folium.Popup(radius_border_popup_text_string, max_width=  len(str(coordinates_of_map_center[0]) + "," + str(coordinates_of_map_center[1])) * 25)

# Create a polygon border around the center square and add it to the map.
folium.Polygon((coordinates_of_radius_border_lower_left_corner,coordinates_of_radius_border_lower_right_corner,coordinates_of_radius_border_top_right_corner,coordinates_of_radius_border_top_left_corner), radius_border_popup_text, radius_border_tooltip_text, color='#ff7800').add_to(folium_map)

# Create the cell site marker layer.
cell_sites_layer = folium.FeatureGroup("Sendemasten")

# Add all the cell sites in the area from the Cell_Sites table to the map layer
for cell_site in sqlite3_database_cursor.execute(
    'SELECT * FROM Cell_Sites WHERE LAT <= ? AND LAT >= ? AND LON <= ? AND LON >= ?', 
    [coordinates_of_radius_border_top_left_corner[0], coordinates_of_radius_border_lower_right_corner[0], coordinates_of_radius_border_top_right_corner[1], coordinates_of_radius_border_lower_left_corner[1]]
    ):
    
    # Create a tuple with the location data of a cell site marker.
    cell_site_GPS_location = (float(cell_site[2]), float(cell_site[3]))
    # Set up the tooltip and the popup for a cell site marker.
    cell_site_tooltip_text = cell_site[1]
    cell_site_popup_text_string = marker_popup_text_function(cell_site[1], cell_site[2], cell_site[3], cell_site[4], round(float(cell_site[5]),2), cell_site[6], round(float(cell_site[7]),2), cell_site[8], round(float(cell_site[9]),2))
    cell_site_popup_text = folium.Popup(cell_site_popup_text_string, max_width=len(str(cell_site[2])) * 25)
    # Create a cell site marker and add it to the cell site layer.
    folium.Marker(cell_site_GPS_location, popup=cell_site_popup_text, tooltip=cell_site_tooltip_text).add_to(cell_sites_layer)

# Add the layer with the cell site markers to the map.
cell_sites_layer.add_to(folium_map)

#region Mobile
# Go through each current_square in the Mobile_Operators table.
for network_operator in sqlite3_database_cursor.execute('SELECT * FROM Mobile_Operators').fetchall():
    # Continue if the current network operator meets the operator restriction and tech restriction, otherwise skip.
    if operator_filter in network_operator[0] and technology_filter in network_operator[7]:
        print("Analyzing " + network_operator[0] + " " + network_operator[1] + " MHz")

        # Create the folium map layer for the current operator.
        map_layer = folium.FeatureGroup(name = (network_operator[0] + " " + network_operator[1] + " MHz"), show=False)

        # The first bandwidth bracket is the lowest number to the lowest number + 10%.
        speed_bracket_lowest_speed_plus_ten_percent = 0
        for lowest_speed in sqlite3_database_cursor.execute('SELECT DL_NORMAL FROM {} ORDER BY DL_NORMAL ASC LIMIT 1'.format(network_operator[2])):
            speed_bracket_lowest_speed_plus_ten_percent = lowest_speed[0] * 1.1
       
        # The second bandwidth bracket is the lowest number + 10% to the average bandwidth out of all the average bandwidth numbers.
        speed_bracket_average_speed = 0
        for average_speed in sqlite3_database_cursor.execute('SELECT AVG(DL_NORMAL) FROM {}'.format(network_operator[2])):
            speed_bracket_average_speed = average_speed[0]
        
        # The thrid bandwidth bracket is the average bandwidth out of all the average bandwidth numbers to the highest number - 15%.
        speed_bracket_highest_speed_negative_fifteen_percent = 0
        for highest_speed in sqlite3_database_cursor.execute('SELECT DL_NORMAL FROM {} ORDER BY DL_NORMAL DESC LIMIT 1'.format(network_operator[2])):
            speed_bracket_highest_speed_negative_fifteen_percent = highest_speed[0] * 0.85
        # The fourth bandwidth bracket is the highest number - 15% to the highest number.

        square_counter = 0

        # Get a list of all the squares in the area and go through each current_square.
        for current_square in sqlite3_database_cursor.execute(
            'SELECT * FROM {} WHERE DL_NORMAL > 0 AND UL_NORMAL > 0 AND DL_MAX > 0 AND UL_MAX > 0 AND NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?'.format(network_operator[2]),
            [center_point_latitude_LAEA_Europe + radius_from_center_point, center_point_latitude_LAEA_Europe - (radius_from_center_point + 1), center_point_longitude_LAEA_Europe + radius_from_center_point, center_point_longitude_LAEA_Europe - (radius_from_center_point + 1)]
            ):
                    
            # The four transformations for the four corners of the square.
            coordinates_of_square_lower_left_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[5] * current_square[4]), (current_square[6] * current_square[4]))
            coordinates_of_square_lower_right_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[5] * current_square[4]), ((current_square[6] + 1) * current_square[4]))
            coordinates_of_square_top_right_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[5] + 1) * current_square[4]), ((current_square[6] + 1) * current_square[4]))
            coordinates_of_square_top_left_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[5] + 1) * current_square[4]), (current_square[6] * current_square[4]))
            
            # The transformation for the center of the square.
            coordinates_of_square_center = transform_from_LAEA_Europe_to_GPS.transform(((current_square[5] + 0.5) * current_square[4]), ((current_square[6] + 0.5) * current_square[4]))

            # Set up the color variable
            color_in_hex = ''

            # Select the color of the square based on the average bandwidth.
            if (current_square[7] < speed_bracket_lowest_speed_plus_ten_percent):
                color_in_hex = network_operator[3]
            elif (current_square[7] < speed_bracket_average_speed):
                color_in_hex = network_operator[4]
            elif (current_square[7] < speed_bracket_highest_speed_negative_fifteen_percent):
                color_in_hex = network_operator[5]
            else:
                color_in_hex = network_operator[6]

            # Configure the text for the tooltip of the square.
            current_square_tooltip_text = network_operator[0] + " " + network_operator[1] + " MHz AVG Download: " + str(round(current_square[7] / 1000000, 2)) + " Mbit/s"

            # Configure the popup of the square.
            current_square_popup_text_string = mobile_popup_text_function(str(int(current_square[4]))+'mN'+str(int(current_square[5]))+'E'+str(int(current_square[6])), network_operator[0], network_operator[1] + " MHz", network_operator[7],round(current_square[7] / 1000000, 2), round(current_square[8] / 1000000, 2), round(current_square[9] / 1000000, 2), round(current_square[10] / 1000000, 2), current_square[3], coordinates_of_square_center[0], coordinates_of_square_center[1], network_operator[8], network_operator[9])
            current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width= (len(str(current_square[4])) + len(str(current_square[5])) + len(str(current_square[6]))) * 25)
            
            # Create the square as a folum polygon and add it to the current operators layer. 
            folium.Polygon((coordinates_of_square_lower_left_corner, coordinates_of_square_lower_right_corner, coordinates_of_square_top_right_corner, coordinates_of_square_top_left_corner), current_square_popup_text, current_square_tooltip_text, color=color_in_hex, fill=True).add_to(map_layer)

            square_counter = square_counter + 1

        print (network_operator[0] + " " + network_operator[1] + " MHz: " + str(square_counter) + " squares with coverage found\n")
        # If there are squares in the map layer add the layer to the foium map.
        if(square_counter > 0):
            map_layer.add_to(folium_map)
#endregion

#region Fixed
if fixed_broadband_enabled == True:
    
    # Get a list of all fixed braodband operators and go through each provider table.
    for provider in sqlite3_database_cursor.execute('SELECT DISTINCT INFRASTRUKTURANBIETER FROM Festnetz WHERE NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', [center_point_latitude_LAEA_Europe + radius_from_center_point, center_point_latitude_LAEA_Europe - (radius_from_center_point + 1), center_point_longitude_LAEA_Europe + radius_from_center_point, center_point_longitude_LAEA_Europe - (radius_from_center_point + 1)]).fetchall():
        
        # Create the folium map layer for the current broadband provider.
        map_layer = folium.FeatureGroup(name = provider, show = False)

        square_counter = 0
        
        # Get a list of all the squares in the area and go through each entry.
        for current_square in sqlite3_database_cursor.execute('SELECT * FROM Festnetz WHERE INFRASTRUKTURANBIETER = ? AND NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', 
            [provider[0], center_point_latitude_LAEA_Europe + radius_from_center_point, center_point_latitude_LAEA_Europe - (radius_from_center_point + 1), center_point_longitude_LAEA_Europe + radius_from_center_point, center_point_longitude_LAEA_Europe - (radius_from_center_point + 1)]
            ):
                    
            # The four transformations for the four corners of the square.
            coordinates_of_square_lower_left_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[1] * current_square[0]), (current_square[2] * current_square[0]))
            coordinates_of_square_lower_right_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[1] * current_square[0]), ((current_square[2] + 1) * current_square[0]))
            coordinates_of_square_top_right_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 1) * current_square[0]), ((current_square[2] + 1) * current_square[0]))
            coordinates_of_square_top_left_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 1) * current_square[0]), (current_square[2] * current_square[0]))
            
            # The transformation for the center of the square.
            coordinates_of_square_center = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 0.5) * current_square[0]), ((current_square[2] + 0.5) * current_square[0]))

            color_in_hex = ''
            
            # Select the color of the square based on the bandwidth.
            if ((current_square[5]*0.5 if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5]) < 15):
                color_in_hex = "#73ffef"
            elif ((current_square[5]*0.5 if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5]) < 50):
                color_in_hex = "#33c4b3"
            elif ((current_square[5]*0.5 if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5]) < 200):
                color_in_hex = "#3e9c91"
            elif ((current_square[5]*0.5 if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5]) < 999):
                color_in_hex = "#1f6e64"
            else:
                color_in_hex = "#143834"


            # Configure the text for the tooltip of the square.
            current_square_tooltip_text = current_square[3] + " " + current_square[4] + " Download: " + (str(round(float(current_square[5])*0.5, 2)) if (current_square[3] == "A1" and current_square[4] == "xDSL") else str(current_square[5])) + " Mbit/s"

            # Configure the popup of the square.
            current_square_popup_text_string = fixed_popup_text_function(str(int(current_square[0]))+'mN'+str(int(current_square[1]))+'E'+str(int(current_square[2])), current_square[3], current_square[4], str(round(float(current_square[5])*0.5, 2)) if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5], str(round(float(current_square[6])*0.5, 2)) if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[6], str(round((round(float(current_square[5])*0.5, 2) if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[5])/(round(float(current_square[6])*0.5, 2) if (current_square[3] == "A1" and current_square[4] == "xDSL") else current_square[6]), 2)), current_square[7], coordinates_of_square_center[0], coordinates_of_square_center[1])
            current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width=len(current_square[7]) * 25)
            
            # Create the square as a folum polygon and add it to the current operators layer. 
            folium.Polygon((coordinates_of_square_lower_left_corner, coordinates_of_square_lower_right_corner, coordinates_of_square_top_right_corner, coordinates_of_square_top_left_corner), current_square_popup_text, current_square_tooltip_text, color=color_in_hex, fill=True).add_to(map_layer)

            square_counter = square_counter + 1
        
        # Print how many squares were found from this broadband provider in the square.
        print(provider[0] + ": " + str(square_counter) + " squares with coverage found\n")
        
        # If there are squares in the map layer add the layer to the foium map.
        if(square_counter > 0):
            map_layer.add_to(folium_map)

#endregion

#region Grant
if grant_enable == True:

    # Create the folium map layer for the government supported braodband rollout.
    map_layer = folium.FeatureGroup(name = "Geförderter Ausbau", show=False)

    square_counter = 0

    # Get a list of all the squares in the area and go through each entry.
    for current_square in sqlite3_database_cursor.execute('SELECT * FROM Gefoerderter_Ausbau WHERE NORTH < ? AND NORTH > ? AND EAST < ? AND EAST > ?', 
        [center_point_latitude_LAEA_Europe + radius_from_center_point, center_point_latitude_LAEA_Europe - (radius_from_center_point + 1), center_point_longitude_LAEA_Europe + radius_from_center_point, center_point_longitude_LAEA_Europe - (radius_from_center_point + 1)]
        ):
        
        # The four transformations for the four corners of the square.
        coordinates_of_square_lower_left_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[1] * current_square[0]), (current_square[2] * current_square[0]))
        coordinates_of_square_lower_right_corner = transform_from_LAEA_Europe_to_GPS.transform((current_square[1] * current_square[0]), ((current_square[2] + 1) * current_square[0]))
        coordinates_of_square_top_right_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 1) * current_square[0]), ((current_square[2] + 1) * current_square[0]))
        coordinates_of_square_top_left_corner = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 1) * current_square[0]), (current_square[2] * current_square[0]))
        
        # The transformation for the center of the square.
        coordinates_of_square_center = transform_from_LAEA_Europe_to_GPS.transform(((current_square[1] + 0.5) * current_square[0]), ((current_square[2] + 0.5) * current_square[0]))

        color_in_hex = "#6b798f"

        # Configure the text for the tooltip of the square.
        current_square_tooltip_text = current_square[5] + " sollte das Projekt " + current_square[6] + " bis " + current_square[13] + " abschließen"

        # Configure the popup of the square.
        current_square_popup_text_string = grant_popup_text_function(str(int(current_square[0]))+'mN'+str(int(current_square[1]))+'E'+str(int(current_square[2])), current_square[3], current_square[4], current_square[5], current_square[6], str("{:,}".format(int(current_square[7]))).replace(',', '.'), str("{:,}".format(int(current_square[8]))).replace(',', '.'), current_square[9], str("{:,}".format(int(current_square[10]))).replace(',', '.'), current_square[11], current_square[12], current_square[13], str("{:,}".format(int(current_square[14]))).replace(',', '.'), str("{:,}".format(int(current_square[15]))).replace(',', '.'), current_square[16], current_square[17], coordinates_of_square_center[0], coordinates_of_square_center[1])
        current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width=len(current_square[6]) * 25)
        
        # Create the square as a folum polygon and add it to the current operators layer. 
        folium.Polygon((coordinates_of_square_lower_left_corner, coordinates_of_square_lower_right_corner, coordinates_of_square_top_right_corner, coordinates_of_square_top_left_corner), current_square_popup_text, current_square_tooltip_text, color=color_in_hex, fill=True).add_to(map_layer)

        square_counter = square_counter + 1
    
    # Print how many squares of government supported braodband rollout were found in the square.
    print(str(square_counter) + " squares with government supported broadband rollout found\n")
        
    # If there are squares in the map layer add the layer to the foium map.
    if(square_counter > 0):
        map_layer.add_to(folium_map)

#endregion

print("Write to File (this may take some time)\nwe will let you know when it is done\n")

# Add a folium LayerControl to the map.
folium.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(folium_map)

# Save the map as an html file
folium_map.save("index.html")

print("export of index.html is done\n")
print("runtime was:")
print(program_execution_start_timestamp - datetime.now())