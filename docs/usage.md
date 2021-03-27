> NOTE: this page is still work in progress and cannot be used as-is!

# The User Interface
If you complete all the steps in [instalation](installation/md) and open ```http://127.0.0.1:5000``` in your browser of preference, you will find the following page:

> placeholder

In the top bar, you will find links to the following pages:

| Link         | Content                                                                                                                                                                                          |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Home         | The first page you will see when you open Talos. It contains a message congratulating you on completing the installation successfully.                                                           |
| Submit Query | A form where you can fill in your query.                                                                                                                                                         |
| Jobs         | This page contains a list for all queries that are either ready to be sent, queued up, running or finished. From this page you can download any data that has been gathered from the app stores. |
| Guide        | Leads to the home page of the website you are now on.                                                                                                                                            |
| Github       | The repository that provides the code behind Talos.                                                                                                                                              |

# The Job system
Both the Apple and Google app stores limit how many connections a device can send a request to their servers at the same time. 
This means that any device, wether that would be your smart device or the server running Talos, can only send one query at a time. 
If you want to use Talos to gather data with fifty separate search terms, that would require you to wait for each query to complete before submitting a new one.
With this is mind, Talos was designed with a queue system.
Each query, or 'Job', is submitted one after another.
With this method, a user can submit queries one after another without delay!

> **WARNING:** The usage guide assumes that the reader has completed the [installation](installation.md) manual and has started a Talos WSL server as explained in the final step. 

## Preparing a query


## Queueing a query 

## Results and exporting

# Troubleshooting
