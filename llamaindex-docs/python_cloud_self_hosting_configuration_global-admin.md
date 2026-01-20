[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#_top)
# Global Admin Setup
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
Global administrators have platform-wide access and can manage all organizations, users, and system-level configurations in your self-hosted LlamaCloud deployment. This guide covers how to set up and manage global admin access.
## Overview
[Section titled “Overview”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#overview)
The global admin feature provides:
  * **Cross-organization visibility** : Inspect all user-organization memberships across the platform
  * **Admin user management** : Add and remove global admin privileges
  * **System-wide access** : Bypass organization-level restrictions for troubleshooting and support
  * **User support capabilities** : Help users with organization access and membership issues


## Bootstrap Initial Global Admins
[Section titled “Bootstrap Initial Global Admins”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#bootstrap-initial-global-admins)
Choose the appropriate approach based on your deployment needs:
### Approach 1: Grant Global Admin to First User (Simplest)
[Section titled “Approach 1: Grant Global Admin to First User (Simplest)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#approach-1-grant-global-admin-to-first-user-simplest)
Use this approach when you want to automatically grant admin access to the very first user in your deployment without configuring any email lists.
#### When to Use
[Section titled “When to Use”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#when-to-use)
  * Fresh deployment with no existing admins
  * You want the earliest user (by creation time) to become the first admin
  * Simplest setup - no environment variables needed


#### Setup Steps
[Section titled “Setup Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#setup-steps)
  1. **Deploy LlamaCloud** without any special global admin configuration
  2. **Ensure at least one user has logged in** (this creates the user_organization record)
  3. **Bootstrap the first admin** by calling the sync endpoint:


Terminal window```


curl-XPOST"https://your-llamacloud-domain/api/internal/permissions/sync-global-admins?earliest_email=true"


```

### Approach 2: Specify Admin Users via Environment Variable
[Section titled “Approach 2: Specify Admin Users via Environment Variable”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#approach-2-specify-admin-users-via-environment-variable)
Use this approach when you want to explicitly control which users become global admins (e.g. if first user is not the desired initial global admin).
#### When to Use
[Section titled “When to Use”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#when-to-use-1)
  * You want to grant admin access to specific users by email address
  * More controlled admin assignment
  * Adding additional admins after initial setup


#### Setup Steps
[Section titled “Setup Steps”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#setup-steps-1)
  1. **Configure admin emails** in your `values.yaml` file:


```


backend:




extraEnvVariables:




- name: GLOBAL_ADMIN_EMAILS




value: "admin1@yourcompany.com,admin2@yourcompany.com,admin3@yourcompany.com"


```

  1. **Deploy the updated configuration** to your cluster
  2. **Sync the permissions** by calling the API endpoint:


Terminal window```


curl-XPOST"https://your-llamacloud-domain/api/internal/permissions/sync-global-admins"


```

  * **Email requirements** : Use comma-separated email addresses with no spaces
  * **User prerequisite** : Listed users must have logged into the platform at least once
  * **Idempotent** : Safe to run multiple times - won’t create duplicate permissions


## Manage Additional Global Admins via UI
[Section titled “Manage Additional Global Admins via UI”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#manage-additional-global-admins-via-ui)
Once you have at least one global admin, you can manage additional admins through the web interface.
#### Access the Global Admin UI
[Section titled “Access the Global Admin UI”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#access-the-global-admin-ui)
  1. Log in to your LlamaCloud instance with a global admin account
  2. Navigate to `/global-admin` in your browser
  3. You’ll see tabs for **Users** and **Admin Management**


#### Add New Global Admins
[Section titled “Add New Global Admins”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#add-new-global-admins)
  1. Go to the **Admin Management** tab
  2. Click **Add Admin**
  3. Enter the **User ID** (not email) of the user you want to promote
  4. Click **Add Admin**


The manual method requires the User ID (UUID), not the email address. You can find User IDs by searching in the Users tab first.
## Global Admin Permission Levels
[Section titled “Global Admin Permission Levels”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#global-admin-permission-levels)
  * **Global admin UI access** : Can view and manage all user-organization relationships
  * **Admin user management** : Can add and remove other global admin users
  * **RBAC permissions** : Can create and delete RBAC permissions via API
  * **Cross-organization API access** : Can call all existing APIs across all organizations when using user-scoped API keys
  * **Bypasses organization restrictions** : Full platform access via API


For cross-organization API access, you **must use user-scoped API keys** , not project-scoped keys.
## API Reference
[Section titled “API Reference”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#api-reference)
### Sync Global Admins
[Section titled “Sync Global Admins”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#sync-global-admins)
```


POST /api/internal/permissions/sync-global-admins




POST /api/internal/permissions/sync-global-admins?earliest_email=true


```

Synchronizes global admin permissions from the `GLOBAL_ADMIN_EMAILS` environment variable. Optionally includes the earliest user (by creation time) for bootstrap scenarios.
**Parameters:**
  * `earliest_email` (boolean, optional): If `true`, automatically grants admin privileges to the earliest user by created_at timestamp in the user_organization table. Useful for initial deployment setup.


**Response:**
```



"added": ["admin1@company.com", "earliest-user@company.com"],




"skipped": ["admin2@company.com"],




"errors": ["nonexistent@company.com"]



```

**Notes:**
  * Rate limited to 2 requests per 30 seconds
  * Idempotent - safe to run multiple times
  * Creates `admin` permissions for all processed users
  * Both email list and earliest user receive the same permission level


### Manage RBAC Permissions
[Section titled “Manage RBAC Permissions”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/global-admin/#manage-rbac-permissions)
```


GET    /api/permissions?target_type=global&relationship=admin




POST   /api/permissions




DELETE /api/permissions/{permission_id}


```

Create, read, and delete global admin permissions.
