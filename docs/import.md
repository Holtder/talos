# Importing results
This guide will provide you with *one of the ways* you can import the data provided by Talos. Several applications offer tools to import raw data, such as Microsoft Excel, Microsoft Access, SQL, Castor and so on. Even within Excel there are multiple ways to approach this, so educate yourself on the possibilies out there and choose what works best for your project! That being said, the following steps show how I prefer to import Talos data for my projects.

> **NOTE:** This guide uses Microsoft Excel 365 in English, YMMV as to which version and langauge you use.

## Preparation
Create a new direcory and download all the completed queries in CSV format (as described in [Usage](usage.md)) to this directory. Make sure no other files are present!

![image](https://user-images.githubusercontent.com/1879915/112723368-62830580-8f0e-11eb-85f2-edcb1f31e24d.png)


## Finding the right dialogue (Import from Folder)
In Excel, select the ```Data``` tab on the ribbon, in the far left, look for the section named ```Get & Transform Data```.

![image](https://user-images.githubusercontent.com/1879915/112723707-3a94a180-8f10-11eb-8f6a-e9b6e3c5e4fd.png)

Click on the following: ```Get Data > From File > From Folder```

![image](https://user-images.githubusercontent.com/1879915/112723829-cdcdd700-8f10-11eb-8b4b-cadf6f63e9ef.png)

This will lead to the following dialogue:

![image](https://user-images.githubusercontent.com/1879915/112723865-ea6a0f00-8f10-11eb-8f95-a4d59e01cb83.png)

## Choosing and double checking
Click ```Browse``` and navigate to the directory that houses your CSV files:

![image](https://user-images.githubusercontent.com/1879915/112723943-3ddc5d00-8f11-11eb-8347-ab3ba11f2e8a.png)

> **NOTE:** As you can see the dialogue does not show any of the files you downloaded, this is working as intended. It ensured you select the DIRECTORY, not just one of the files within.

Click ```Open``` and ```OK```, you will be presented with the following dialogue:

![image](https://user-images.githubusercontent.com/1879915/112724137-176af180-8f12-11eb-9eda-2beaa9364e40.png)

## Checking the data
If you used multiple adjecent search terms, you will most certainly have gotten some duplicate results in your data. 
This is especially true as Google likes to pad their results by making popular apps appear multiple times in the same search. 
(This can sometimes get out of hand with one result appearing dozens of times, sadly this works as intended).
If you wish to remove those duplicates choose ```Combine > Combine & Transform Data```. 
If you want to include all data, duplicates included, choose ```Combine > Combine & Load``` and skip the step **Removing duplicates**.

No matter which option you chose, you will be presented with the following:

![image](https://user-images.githubusercontent.com/1879915/112724286-f060ef80-8f12-11eb-99db-9ed427db8099.png)

> **NOTE:** The files generated by Talos are formatted in ```UTF-8 Unicode```, make sure to choose that option in the ```File Origin``` dropdown if it hasn't been chosen yet. Make sure the delimiter is set to ```Semicolon```.

If the examples pulled from your data seem to be correct, press ```OK```.

## Removing duplicates
> **NOTE:** You may skip this step if you chose ```Combine & Load`` in the previous step.

In the top ribbon, under the ```Home``` tab, look for the section named ```Reduce Rows```:

![image](https://user-images.githubusercontent.com/1879915/112724529-1cc93b80-8f14-11eb-94a6-9f07402f2e89.png)

Within that section, click on ```Remove Rows > Remove Duplicates```. Note that the earliest/highest entry of duplicates will be kept, so if two hypothetical sources are very comparable in results, the first source will provide significantly more results to the final list after removing duplicates.

Once you are happy with the results, find the ```Close``` section to the far left of the ```Home``` tab in the ribbon:

![image](https://user-images.githubusercontent.com/1879915/112724686-da542e80-8f14-11eb-919d-e03df6112467.png)

Choose ```Close & Load``` and let Excel import all the data to a table:

![image](https://user-images.githubusercontent.com/1879915/112724766-3028d680-8f15-11eb-94a1-c481b699a3b6.png)

## Each column explained
The table you are now presented with has twelve columns, the following table will provide a short explanation what each of them contain:

| Column Name    | Content                                                                                                                                                            |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Source.Name    | The name of the file from which this entry was taken.                                                                                                              |
| app_title      | The name of the application as presented in the app store                                                                                                          |
| bundleid       | A unique identifier of the application within the appstore.                                                                                                        |
| store          | Either ```android``` or ```apple```, signifying which store this result was pulled from.                                                                           |
| description    | The description of the application, this section is writted by the developers themselves.                                                                          |
| dev_name       | The name of the developer of the app.                                                                                                                              |
| dev_id         | A unique identifier of the developer of the app.                                                                                                                   |
| fullprice      | The full price of an application in dollar cents.                                                                                                                  |
| versionnumber  | The current version number of the application, changes with every update.                                                                                          |
| osreq          | The minimally required operating system (iOS or Android) version to use this app.                                                                                  |
| latest_patch   | The date when the most recent update of this application was published. (tip: use this if you want do filter out apps that have been abandoned by their developer) |
| content_rating | A suggested minimum age or age range for users of this application.                                                                                                |

##