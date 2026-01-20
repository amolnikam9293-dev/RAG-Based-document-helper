[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#_top)
# Auth
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
For self-hosted deployments, LlamaCloud supports authenticating users via **OIDC** and **Basic Auth (email/password)**.
## Basic Auth (Email/Password)
[Section titled “Basic Auth (Email/Password)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#basic-auth-emailpassword)
Basic auth is a simple authentication mode that allows you to authenticate users via email and password. This is useful for self-hosted deployments where you may not have an existing identity provider and is perfect for staging deployments. For production deployments, we recommend configuring OIDC.
### Configuration
[Section titled “Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#configuration)
In your `values.yaml` file, you can configure the following:
```


config:




authentication:




basicAuth:




enabled: true




validEmailDomain: "runllama.ai"# this is optional, but a way to restrict access to only users with a specific email domain




jwtSecret: <YOUR-JWT-SECRET># default is a random string




# secret: <BASIC-AUTH-SECRET> # if you want to use an existing secret for the JWT secret


```

After you’ve configured the above, you should see the following in the UI:
To get started, administrators can click `Create Account` to get set up and then proceed to inviting other users to the organization you’ve created.
#### Notes
[Section titled “Notes”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#notes)
  * In basic auth mode, users can update their settings under `Settings > Personal`.


## OIDC (OpenID Connect)
[Section titled “OIDC (OpenID Connect)”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#oidc-openid-connect)
### Requirements
[Section titled “Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#requirements)
  1. Your IdP supports using a discovery URL or issuer URL.
  2. The required scopes are `openid`, `profile`, and `email`.
  3. Please make sure the redirect URL is set to `<your-host>/api/v1/auth/callback`.


In your `values.yaml` file, you can configure the following:
```


config:




authentication:




oidc:




enabled: true




# Example with Microsoft Entra ID




discoveryUrl: "https://login.microsoftonline.com/<TENANT-ID>/v2.0/.well-known/openid-configuration"




clientId: <CLIENT-ID>




clientSecret: <CLIENT-SECRET>


```

After you’ve configured the above, you should see the following in the UI:
## Possible Gotchas
[Section titled “Possible Gotchas”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#possible-gotchas)
  * A valid OIDC discovery URL must end in `.well-known/openid-configuration`.
  * In test environments, you may need to disable SSL verification if your OIDC provider does not have a valid SSL certificate. This is not recommended for production environments. To bypass SSL verification, you can add the following to your `values.yaml` file: 
    * ```


backend:




extraEnvVariables:




- name: OIDC_VERIFY_SSL




value: false


```



## Popular IdPs that support OIDC
[Section titled “Popular IdPs that support OIDC”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/auth-modes/#popular-idps-that-support-oidc)
  * [Microsoft Entra (Azure AD)](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)


