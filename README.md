# Prescriptive Analytics Workshop

Dave Wentzel  
linkedin.com/in/dwentzel  
Spark - 20220218

## Abstract 

As analytics practitioners we tend to be enamored with "the tech".  We love to talk about data lakes, MPPs, ETL, and ML algorithms.  But none of this is particularly interesting to a project sponsor or executive.  They are interested in business outcomes.  

We build dashboards that forecast sales, but is that adding value?  

we build ML algos to predict which customers will likely churn...but is that adding value?  

Initially, most executives will _say_ dashboards and predictive algorithms add value, but if you probe you'll likely hear something like this:  

> "The dashboard gives me a bunch of facts but doesn't tell me a story and more importantly _what do I do next?_"
> "Thanks for telling me which customers will churn, _what do I do about it?_"

Now imagine if we didn't talk about the tech at all, but just demo'd how to solve a really thorny analytics problem using simple tech that mere mortals can understand, with a repeatble set of patterns (People Process Technology). Suddenly data projects are viewed as less risky.  

In this session we'll look at a few interesting use cases to understand how Prescriptive Analytics can help you compellingly demonstrate how an organization can be more _data literate_ and _insights-driven_.  

## Demos

1. Prescriptive Analytics requires a simple analytics pattern implementation.  [`CETAS`](https://docs.microsoft.com/en-us/azure/synapse-analytics/sql/develop-tables-cetas) in Synapse works real well.  [Demo Notebook]()

2. Prescriptive Analytics is primarily about asking interesting questions in a collaborative environment.  You don't want to make cognitive mistakes.  [Here's a case where we need to talk through the business problem so we tell management the RIGHT decision to make](CognitiveMistakes.ipynb)

lakepath:lake/gold/drill-data/drill-trials.csv

https://davewdemodata.blob.core.windows.net/lake/gold/drill-data/drill-trials.csv?sv=2020-04-08&st=2021-02-10T14%3A58%3A00Z&se=2030-02-11T14%3A58%3A00Z&sr=b&sp=r&sig=muqHLi735zBkT8lxqpcMixzKJwk5mfaLILkysbY5FpU%3D