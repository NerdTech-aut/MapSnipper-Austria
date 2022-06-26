# MapSnipper-Austria
```
This document is under construction!
```
### What is MapSnipper?
MapSnipper is a tool which lets you create detailed coverage maps for all cellular operators in Austria.  
The tool currently supports the following operators:
- A1 Telekom Austria | Technologies: 2G, 3G, 4G & 5G NSA | Frequencies: 800, 900, 1800, 2100, 2600 & 3500 MHz
- Magenta Telekom | Technologies: 5G NSA | Frequencies: 3500 MHz
- Hutchison Drei Austria | Technologies: 5G NSA | Frequencies: 3500 MHz
- Mass Response aka. Spusu | Technologies: 5G SA | Frequencies: 3500 MHz
- LIWEST | Technologies: 5G FWA | Frequencies: 3500 MHz
- Graz Holding Citycom | Technologies: 5G FWA | Frequencies: 3500 MHz
- Salzburg AG Cable Link Air | Technologies: 5G FWA | Frequencies: 3500 MHz  

Additionally, you can see all cell sites from A1, Magenta and Drei.
Furthermore, viewing fixed broadband coverage and government supported broadband rollout is supported too.

### Where is the data coming from?
MapSnipper uses the publicly available data which is provided by the cellular companies.  
All the data can be found through the links on this ~~[site of the RTR](https://www.rtr.at/TKP/was_wir_tun/telekommunikation/spectrum/bands/3400-3800MHz/Spectrum3400MHz.de.html)~~ (list was removed since development began).  
Since development started A1 has pulled the data for 800, 900, 1800, 2100 and 2600 MHz and replaced it with a simple speedmap for all frequencies (800-3500 MHz).  
The cell site data was provided by Jonas12 aka. JonasGhost and stems from [senderkataster.at](senderkataster.at).
The fixed broadband and government supported broadband rollout data is from [data.gv.at](https://www.data.gv.at/katalog/dataset/588b9fdc-d2dd-4628-b186-f7b974065d40) and [info.bmlrt.gv.at](https://info.bmlrt.gv.at/themen/telekommunikation-post/breitband/breitbandfoerderung/breitbandaustria2020/projekte.html)

### Why use this tool?
All of the companies who publish the data used by this tool also provide a graphical representation of the data.  
But these graphical representations can lack depth and therefore aren't useful.    
This tool makes all of the data visible in a way that is easy to understand.  
Furthermore, it makes comparing theoretical coverage across operators easier than ever before.

### What does MapSnipper do:
MapSnipper generates an HTML file with a detailed map.  
This HTML file can be viewed in a web browser.  
By default, this tool generates a 10 by 10 kilometer map with as much data as it can find for mobile coverage.

### Limitations:
- Performance: More data means a more resource intensive map. The default radius is a compromise between performance/resource consumption and usefulness.  
- Not all frequencies: Magenta does currently not provide data for 700, 800, 900, 1800, 2100 and 2600 MHz and Drei does currently not provide data for 900, 1800, 2100 and 2600 MHz
- Cell sites: The cell site data lacks operator information. This means you can't see which cell site is operated by which operator. 

### Why does this tool only report half of the A1 xDSL bandwidth compared to breitbandatlas.gv.at?
On [breitbandatlas.gv.at](https://breitbandatlas.gv.at/) the xDSL bandwidth is the bandwidth achievable through VDSL2LR bonding, VDSL2 bonding or VPlus bonding.  
Bonding means two DSL lines are used as one, through which twice as much data can be transmitted.  
But most companies who offer xDSL don't offer the bonding of two lines. And the companies who do offer bonding charge a 300€ fee.  
Therefore, most people will never get bonding.  
This is why the decision was made to alter the xDSL bandwidth reported by this tool.  
But there are other shenanigans in the A1 data I can't do anything about.

## Get started:
### Download this repository:
You can download this repository either as a zip archive or through git.  
If you want to go through git I reckon, you know what you are doing.  
Otherwise just download this repository as a zip archive. You can do this by clicking on the green "Code" button and then choose "Download ZIP". After the download is complete extract the zip archive.

### Useful software for Windows Users:
If you use Windows 10 or 11 you can make your life a lot easier if you download the [Windows Terminal App from the Microsoft Store](https://www.microsoft.com/store/productId/9N0DX20HK701)
 
### Python:
Make sure you have python installed on your machine.  
If you are not sure if python is already installed on your computer run this command in a terminal window:
```
python -V
```
If python isn’t installed, please download the lasted version.  
[python download page](https://www.python.org/downloads/)  
[python on the Microsoft store for Windows 10 & 11](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5)

### Python packages:   
After python was successfully installed, please install the following packages:
- pyproj
- folium  

I have prepared a file to make the installation of these packages easier.  
If you use Windows and have Windows Terminal installed in a file explorer window, right click in the MapSnipper folder which contains the four files above and select "Open in Terminal". This opens a new Windows Terminal window at the right location.  
Everyone else just open a Terminal and navigate to the folder with the four files above.  
All you need to do now is run this command:
```
pip install -r requirements.txt
```
### Additional software:
If you use Windows please download and install the [Microsoft Visual C++ Redistributable packages for Visual Studio 2015, 2017, 2019, and 2022](https://aka.ms/vs/17/release/vc_redist.x64.exe).

### Download coverage and cell site data:
To be able to use this project you need additional data which is not included in this repository. You can download this data from my OneDrive.  [MapSnipper_Data.zip](https://1drv.ms/u/s!Ajecn6-yGfx0iH2XMce7W3Ue9CXv?e=koQkmj)  
After the download is completed unzip the folder and move the datebase file into the same folder as the four files above. At the end you should have one folder with 5 files.

## How to use:
### Basic operation:
First you need a center location based on which the MapSnipper tool can create a 10 x 10 kilometer map.  
After you have made your decision where this center point is go to [breitbandatlas.gv.at](breitbandatlas.gv.at) and find the square at this location. Click on the square to reveal a popup with information about the fixed broadband at this location. If there is no square at this location switch to the "Mobilfunknetz" tab. Then copy the tile id at the bottom right of the popup into the clipboard. The tile id looks like this: 100mN28000E47000


Open a terminal and navigate to the folder with the 5 files. If you use Windows Terminal just right click in a file explorer window in the MapSnipper folder like before. If you have the terminal open from the installation you can reuse it.
Once a terminal window is open and at the correct location use a command like this one but replace the tile id with the tile id you want:
```
python mapsnipper.py 100mN28000E47000
```
After you entered the command a 10 x 10 kilometer map will be generated. This may take several minutes depending on your computer.  
When the html file is done you can open it in your default web browser by double clicking on it.  

By default, only the layer with the cell sites is shown. To view additional layers, move your mouse over of tap the layer control icon in the top right of the webpage and activate the layers you want to see. You can view all layers at once if you want to but expect degraded performance when you do so.

### Advanced operation:
Additional options are available to customize the maps:
```
  -r RADIUS, --radius RADIUS     enter a radius in km (default: 5 km)
  -2G, --twoG                    only process layers with 2G; some layers might include multiple technologies
  -3G, --threeG                  only process layers with 3G; some layers might include multiple technologies
  -4G, --fourG                   only process layers with 4G; some layers might include multiple technologies
  -5G, --fiveG                   only process layers with 5G; some layers might include multiple technologies
  -FWA, --FixedWirelessAccess    only process layers with fixed wireless access
  -A1, --A1TelekomAustria        only process layers from A1 Telekom Austria
  -Magenta, --MagentaTelekom     only process layers with Magenta Telekom
  -Drei, --HutchisonDreiAustria  only process layers from Hutchison Drei Austria
  -fixed, --FixedBroadband       adds fixed broadband providers to the map
  -grant, --BroadbandGrant       adds government supported broadband rollout to the map
```
## Acknowledgements:
Thanks to [styxer](https://www.lteforum.at/user/styxer.7288/) aka. [styx3r](https://github.com/styx3r) for providing the fundamentals for this project! His project can be found [here](https://github.com/styx3r/breitbandatlas_analysis).  
Thanks to [Jonas12](https://www.lteforum.at/user/jonas12.1666/) aka. [JonasGhost](https://github.com/JonasGhost) for providing the cell site data and contributing to the code!  

## How is it posible to create a map from this data?
[styxer](https://www.lteforum.at/user/styxer.7288/) aka. [styx3r](https://github.com/styx3r) explained to me the fundamentals.  
The position for each square needs to be converted into regular coordinates using [pyproj](https://pyproj4.github.io/pyproj/stable/) (Python library).  
In addition, I used [re](https://www.w3schools.com/python/python_regex.asp) (Python RegEx) to split the position information into the three parts (scale, north & east).  
The scale of this data is 100 meters.  
To get a square you need to do a transformation for each corner (lower-left, lower-right, top-right & top-left).


```
from pyproj import Transformer
import re

WSG84_split = re.split('mN|E','100mN28000E47000')
scale = int(WSG84_split[0])
north = int(WSG84_split[1])
east = int(WSG84_split[2])

transformer = Transformer.from_crs(3035, 4326)

transformation_result_LL = transformer.transform((north * scale), (east * scale))
transformation_result_LR = transformer.transform((north * scale), ((east + 1) * scale))
transformation_result_TR = transformer.transform(((north + 1) * scale), ((east + 1) * scale))
transformation_result_TL = transformer.transform(((north + 1) * scale), (east * scale))
```

## ToDo:
- more work on fixed broadband
- refine color scheme for operators
- perimeter Popup and Tooltip
