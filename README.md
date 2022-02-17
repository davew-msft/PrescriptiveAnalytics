# Prescriptive Analytics Workshop

Dave Wentzel  
[LinkedIn Profile](https://linkedin.com/in/dwentzel)  
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

1. **Prescriptive Analytics requires a simple analytics pattern**.  [`CETAS`](https://docs.microsoft.com/en-us/azure/synapse-analytics/sql/develop-tables-cetas) in Synapse works real well.  I have 2 versions of this demo.  Both do the same thing, one is simply a notebook where I can show better documentation and plots:  
    * [Demo SQL Script](./taxi-eda.sql):  import this to your Synapse workspace.  
    * [SQL Serverless Notebook](./taxi-eda.ipynb)
      * this uses a vscode `devcontainer` to ensure everything is setup perfectly.  If you know how to use these then it should be easy.  
      * I use this devcontainer "pattern" along with the imports and utils files in the `scripts` folder to create a totally reproducible "analytics sandbox" that can be used by anyone without dealing with installing python and configuring environments.  
      * **This works awesome for hands-on, interactive demos**.  I have a version of this that runs in the browser and is launched via ACI that will allow MTC session attendees to play with the code and adjust the parameters WITHOUT needing access to Azure, vscode, python, or Synapse.  Let me know if this is interesting and maybe we can collaborate on it.  
2. **Avoiding Cognitive Mistakes**.  Prescriptive Analytics is primarily about answering the question _what do we do next?_.  This requires collaboration and critical thinking skills.  You don't want to make cognitive mistakes.  [Here's a case where we need to talk through the business problem so we tell management the RIGHT decision to make](./CognitiveMistakes.ipynb)
    * we use Synapse Spark for this example, you will need to import the notebook into your Synapse workspace
3. **Marketing Campaign Analytics**. Let's use some data and critical thinking to recommend _what should we do next?_ 



