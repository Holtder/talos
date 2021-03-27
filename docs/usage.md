# Usage
> NOTE: this page is still work in progress and cannot be used as-is!

## The User Interface
If you complete all the steps in [instalation](installation/md) and open ```http://127.0.0.1:5000``` in your browser of preference, you will find the following page:

![image](https://user-images.githubusercontent.com/1879915/112722091-c950f080-8f07-11eb-9c0e-0a3afeb52ed7.png)

In the top bar, you will find links to the following pages:

| Link         | Content                                                                                                                                                                                          |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Home         | The first page you will see when you open Talos. It contains a message congratulating you on completing the installation successfully.                                                           |
| Submit Query | A form where you can fill in your query.                                                                                                                                                         |
| Jobs         | This page contains a list for all queries that are either ready to be sent, queued up, running or finished. From this page you can download any data that has been gathered from the app stores. |
| Guide        | Leads to the home page of the website you are now on.                                                                                                                                            |
| Github       | The repository that provides the code behind Talos.                                                                                                                                              |

> **WARNING:** The usage guide assumes that the reader has completed the [installation](installation.md) manual and has started a Talos WSL server as explained in the final step. 

## The Job system
Both the Apple and Google app stores limit how many connections a device can send a request to their servers at the same time. 
This means that any device, wether that would be your smart device or the server running Talos, can only send one query at a time. 
If you want to use Talos to gather data with fifty separate search terms, that would require you to wait for each query to complete before submitting a new one.
With this is mind, Talos was designed with a queue system.
Each query, or 'Job', is submitted one after another.
With this method, a user can submit queries one after another without delay!

### Preparing a query
When preparing a query, the user needs to fill in the following data on the ```Submit Query``` page:

| Input        | Meaning                                                                                                                                                                                   |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Search terms | The actual query; this is the same string of characters you enter when looking for an app in a store on your smart device.                                                                |
| Region       | App store results differ per region from which the query is sent. Talos is capable of choosing different regions. Currently US, GB and NL are supported as regions, but more will follow. |
| Job Name     | Each query can be assigned a name. This has no consequence on the results and is mainly intended for the user to easily differentiate between jobs sent to the queue.                     |

![image](https://user-images.githubusercontent.com/1879915/112722517-5006cd00-8f0a-11eb-9ea0-863dc3947282.png)

### Job overview
The page ```Jobs``` provides an overview of all queued or completed queries. From this page it's possible to start or cancel queries by using their respective buttons. You can queue multiple jobs by pressing start on multiple jobs, but only one queue can be ran at the same time. This means that queued jobs will run in the order they were started.

![image](https://user-images.githubusercontent.com/1879915/112722619-f18e1e80-8f0a-11eb-8b9b-adb81dd69269.png)

> **DESCRIPTION:** As seen in the image above, three queries have been prepared named fencing 01-03. Each job has it's own synonym of fencing and they are all targeted at the US region.

### Waiting
Sadly, due to restrictions made by the developers behind both Apple and Google app stores, scraping is not a fast process. Each job may take up to a few minutes, so plan wisely with the job system that Talos offers.

![image](https://user-images.githubusercontent.com/1879915/112722864-15059900-8f0c-11eb-9835-24f358095396.png)

> **DESCRIPTION:** In this image, fencing 01, 02 and 03 were started in order, with 03 being that last as can be seen in the messagebox at the top of the page. Feel free to refresh the page to see if the job has finished yet.

![image](https://user-images.githubusercontent.com/1879915/112722953-89d8d300-8f0c-11eb-934e-653ba4329515.png)

> **DESCRIPTION:** Job fencing 01 has completed, whereas 02 and 03 noow have moved up the queue.

## Results

For more information on how to export and use these results, please consult [exporting](export.md)
