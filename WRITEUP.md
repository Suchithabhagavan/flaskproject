# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For my Flask application flaskproject, I compared deploying on an Azure Virtual Machine (VM) versus Azure App Service. A VM provides full control over the operating system, allowing custom installations and complete configuration. However, it requires significant setup and maintenance, including managing security patches, web servers, updates, and deployments. This makes it more suitable for complex applications that need OS-level customization.
Azure App Service, on the other hand, is a fully managed hosting platform designed specifically for web applications. It supports Python and Flask out of the box, automatically installs dependencies using Oryx, and integrates easily with GitHub Actions for CI/CD. App Service also removes the need to manage infrastructure, making deployments faster and more reliable.
I chose Azure App Service because my project does not require deep system-level control. App Service provides a simpler, cleaner, and more efficient deployment experience, especially for lightweight Flask applications. It handles scaling, environment variables, and server management automatically, allowing me to focus entirely on the application rather than infrastructure.*

### Assess app changes that would change your decision.

*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 

*For my Flask application flaskproject, I chose Azure App Service over a Virtual Machine because it is easier to deploy, requires no server management, and has built-in support for Python and Flask. App Service automatically handles dependency installation, scaling, and updates, and integrates smoothly with GitHub Actions for CI/CD. Since my app is lightweight and does not need custom system configurations, App Service is the simplest and most efficient option.
When My Decision Would Change?
I would switch to a VM only if the application needed full OS control—such as installing custom system packages, running background services, handling GPU or heavy ML workloads, or hosting multiple services on one machine. In those cases, a VM’s flexibility would be necessary. For the current scope of flaskproject, App Service is the best fit.*
