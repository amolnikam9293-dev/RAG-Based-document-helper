[Skip to content](https://developers.llamaindex.ai/python/cloud/llamacloud/multi_environment/#_top)
# Multi-Environments
## Single Project Approach
[Section titled “Single Project Approach”](https://developers.llamaindex.ai/python/cloud/llamacloud/multi_environment/#single-project-approach)
Keep all three environments (dev, UAT, production) in the same project.
**Benefits:**
  * **Easy management** - Everything in one place
  * **Quick setup** - Use “Duplicate” button to copy between environments
  * **Streamlined workflow** - Promote changes from dev → UAT → prod seamlessly


**How to set up:**
  1. Create one project for your application
  2. Name your indexes with environment prefixes: `dev-products`, `uat-products`, `prod-products`
  3. Use the duplicate feature to copy indexes configuration (“Duplicate” button can be found in the index page).


## Alternative: Separate Projects
[Section titled “Alternative: Separate Projects”](https://developers.llamaindex.ai/python/cloud/llamacloud/multi_environment/#alternative-separate-projects)
Create individual projects for each environment (3 projects total).
**Consider this only if:**
  * You have specific organizational requirements for complete separation


**Important considerations:**
  * **Manual synchronization** - No easy way to copy configurations between projects


## Our Recommendation
[Section titled “Our Recommendation”](https://developers.llamaindex.ai/python/cloud/llamacloud/multi_environment/#our-recommendation)
Start with the single project approach. It’s simpler, more cost-effective, and easier to manage. You can always separate later if your needs change.
## Need Help?
[Section titled “Need Help?”](https://developers.llamaindex.ai/python/cloud/llamacloud/multi_environment/#need-help)
Contact us if you have questions about setting up your environments.
