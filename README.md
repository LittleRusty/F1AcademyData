F1AcademyData - Historical Formula 1 Academy Data
======
## Repository containing Practice, Qualifying, and Race timing data from past F1 Academy race weekends.

The core purpose of the repository is provide historical practice, qualifying, and race data for the Formual 1 Academy series. This repository contains the scripts used to gather live timing data from the F1 Academy live timing page during sessions. I took a lot of inspiration from the existing FastF1 project (https://docs.fastf1.dev/index.html) and ported some of their examples over for data visualization.

Over time I also hope to grow this repository to contain examples of data visualization and insights that can be generated from the historical data such as the example below.

![FPexample](Montreal_2025/FP_Sector_Time_Graphic.jpg)

![QualifyingExample](Data_visualization/qualifying_deltas.jpg)

![RaceExample](Data_visualization/team_box_and_whisker.jpg)

Getting Started
------
## Gathering Race Data
The F1ALiveTimingDownloader.py is the main driver script. Run it before the session starts. It will open a chromium window and download the live timing data that loads. Period is currently hardcoded to 5 seconds to allow time for the page to load.

## Running Visualizers
The TopSectorsParse.py, QualifyingDeltaViz.py, and RaceTeamSeabornBoxPlot.py all take in a filepath as an argument and generate the appropriate chart.
