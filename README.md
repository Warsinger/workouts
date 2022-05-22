# Apple Workouts Data Parser
Parser for Apple Watch workout data generated by an app I found that exports the data as CSV files. 
This only parses the *Workout* portion that the app can download. These files start with *HKWorkoutActivityType*. All these files in the directory will be parsed, but empty files will be ignored, as will files that only contain *User Entered* data.
Combines the data from the separate files into a single file with the field names being the ones that are common across all files with data.

## App
CSV download app for Apple HealthKit data
https://www.ericwolter.com/projects/apple-health-export/

I was considering writing my own app, but then I figured someone has already done this. A brief search and I was right. So now I can focus on parsing and playing with the data.
# Usage
Use the app to download your workout data as a ZIP file and open the zip. The app stores it in your iCloud files, so you can easily get it from there.

The parser script takes only one parameter that is the directory containing the downloaded CSV files.

```/usr/bin/python3 /Users/matthewlee/dev/workouts/workoutparser.py ~/Downloads/HealthAll_2022-05-142_13-46-39_SimpleHealthExportCSV```

Output is a file in the current directory `health_output.csv`. This file can be opened or imported into Excel or any other tool for analysis.

# Analysis
Each file can be imported into Excel (or other tools) separately, but I wanted a single file to do analysis across workout types.
I used Excel to import the data (live query using Power Query so it can be easily refreshed). I created a Pivot Table and Chart that plots the energy, duration, and Metabolic Equivalent of Task (MET). This is a measure of the work required and increases with the intensity.
After generating a new file, you can simply *Refresh All* for the table in Excel and then go to the Pivot Table and *Refresh* there and the new data will show up.

## Pivot Table
Here's a sample Pivot Table in Excel:
<img width="327" alt="ActivityPivotTable" src="https://user-images.githubusercontent.com/5703848/169712083-8d7f433a-a62c-4733-99f6-9c5d9a3a74a8.png">
Here's the configuration:
<img width="335" alt="ActivityPivotTableConfig" src="https://user-images.githubusercontent.com/5703848/169712148-45592a07-faf5-4f01-9374-141d849e8dcd.png">

## Pivot Chart
Here's a sample Pivot Chart
<img width="617" alt="ActivityPivotChart" src="https://user-images.githubusercontent.com/5703848/169712086-f9705303-abec-4c32-abee-e7b8b5bf2345.png">

# Research
Upon looking at the data, a new field showed up that I hadn't seen: Average MET from the HKAverageMET field in the data. The units are kcal/(kg * hour). You can read all about it here:
https://en.wikipedia.org/wiki/Metabolic_equivalent_of_task

I was originally using a metric of kcal/min to determine the intensity. And also kcal/heartrate as a measure of intensity. I still think kcal/min is interesting, but the MET being a standard measure makes the heartrate metric unnecessary. Also heartrate is not available in this data directly and I'm not interested in parsing it out of the other files at this time.
