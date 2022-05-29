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

### Where is the data coming from?
MapSnipper uses the publicly available data which is provided by the cellular companies.  
All the data can be found through the links on this [site of the RTR](https://www.rtr.at/TKP/was_wir_tun/telekommunikation/spectrum/bands/3400-3800MHz/Spectrum3400MHz.de.html).  
The cell site data was provided by Jonas12 aka. JonasGhost and stems from [senderkataster.at](senderkataster.at).

### Why use this tool?
All of the companies who publish the data used by this tool also provide a graphical representation of the data.  
But these graphical representations can lack depth and therefore aren't useful.    
This tool makes all of the data visible in a way that is easy to understand.  
Furthermore, it makes comparing theoretical coverage across operators easier than ever before.

### What does MapSnipper do:
MapSnipper generates an HTML file with a detailed map.  
This HTML file can be viewed in a web browser.  
By default, this tool generates a 10 by 10 kilometer map with as much data as it can find.

### Limitations:
- Performance: More data means a more resource intensive map. The default radius is a compromise between performance/resource consumption and usefulness.  
- Not all frequencies: Magenta does currently not provide data for 700, 800, 900, 1800, 2100 and 2600 MHz and Drei does currently not provide data for 900, 1800, 2100 and 2600 MHz
- Cell sites: The cell site data lacks operator information. This means you can't see which cell site is operated by which operator. 

## Get started:
### Python:
Make sure you have python installed on your machine.  
If you are not sure if python is already installed on your computer run this command in a terminal window:
```
python -V
```
If python isn’t installed, please download the lasted version.  
[python download page](https://www.python.org/downloads/)  
[python on the Microsoft store for windows 10 & 11](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5)

### Python packages:   
After python was successfully installed, please install the following packages:
- pyproj
- 
I have prepared a file to make the installation of these packages easier.  
All you need to do is run this command:
```
pip install -r requirements.txt
```
### Additional software:
If you use Windows please download and install the [Microsoft Visual C++ Redistributable packages for Visual Studio 2015, 2017, 2019, and 2022](https://aka.ms/vs/17/release/vc_redist.x64.exe).

### Download additional data:
To be able to use this project you need additional data. You can download this data from my OneDrive. [MapSnipper_Data.zip](https://1drv.ms/u/s!Ajecn6-yGfx0iHryUTPootTeHdSS?e=IdwTYy)

## How to use:


## Acknowledgements:
Thanks to [styxer](https://www.lteforum.at/user/styxer.7288/) aka. [styx3r](https://github.com/styx3r) for providing the fundamentals for this project! His project can be found [here](https://github.com/styx3r/breitbandatlas_analysis).  
Thanks to [Jonas12](https://www.lteforum.at/user/jonas12.1666/) aka. [JonasGhost](https://github.com/JonasGhost) for providing the cell site data and contributing to the code!  

## ToDo:
- refine color scheme for operators
- perimeter Popup and Tooltip
