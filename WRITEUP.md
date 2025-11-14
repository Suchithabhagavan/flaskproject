# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*Analyze costs, scalability, availability, and workflow*
*To deploy my Flask-based CMS application, I compared Azure Virtual Machines and Azure App Service based on cost, scalability, availability, and workflow. A Virtual Machine is more expensive because it charges for the full compute instance 24/7 and requires extra costs for storage, networking, OS patching, and security maintenance. 
Azure App Service is more cost-efficient since it uses a pay-as-you-go model and removes the need for OS-level management. In terms of scalability, a VM requires manually configuring load balancers or scale sets, while App Service provides built-in autoscaling and deployment slots that make scaling much simpler. Availability also favors App Service because it includes high availability and monitoring by default, whereas a VM requires manually configuring redundancy and backups. Workflow is easier on App Service, which integrates with GitHub Actions and Azure SQL, Blob Storage, and Microsoft Entra ID without needing OS setup.
*Choose the appropriate solution (VM or App Service) for deploying the app*

Based on these comparisons, I choose Azure App Service for deploying my CMS app because it is cheaper, easier to scale, more reliable, and simpler to maintain. It fits perfectly with the services my project already uses and removes the overhead of managing a full server. A VM would only be required if the application needed custom system-level configurations, background processes, GPU workloads, or full OS control. For this CMS app, App Service remains the most efficient and cost-effective option.*
* Justify your choice*
*If my application needed custom server configurations such as special system libraries, background services, or high-performance workloads like machine learning tasks or GPU processing, then moving to a Virtual Machine would be necessary. A VM would also be required if I needed full operating-system control for advanced networking or container orchestration. Since my CMS app is lightweight and does not require these advanced capabilities, Azure App Service remains the most suitable, simpler, and cost-efficient choice.*
### Assess app changes that would change your decision.

*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 

To switch from an Azure App Service to a VM, my Flask application would need major changes. I would have to manage the OS, install and configure Python, Flask, and all dependencies manually, and handle updates, security patches, and scaling on my own. I would also need to create and maintain a full Docker setup or custom deployment pipeline, and configure networking, firewalls, and monitoring from scratch. Only if my project required complete control over the environment, custom background services, or very heavy processing tasks would moving to a VM make sense. Otherwise, App Service remains the simplest, most efficient choice for my project.
**Deployed Application URL:**  
 [https://projectweb-h3b3h2gacnfkc2gt.southindia-01.azurewebsites.net](url)
