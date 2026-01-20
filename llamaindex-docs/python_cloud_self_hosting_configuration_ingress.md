[Skip to content](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#_top)
# Ingress
##  Self-Hosting Documentation Access 
This section requires a password to access. Interested in self-hosting? [Contact sales](https://www.llamaindex.ai/contact) to learn more. 
Self-Hosting Documentation Access Granted  Logout 
After first installing the [LlamaCloud helm chart](https://github.com/run-llama/helm-charts/) into your kubernetes environment, you will be able to test the deployment immediately by port-forwarding the frontend server to your local machine using the following command:
Terminal window```


kubectl--namespace<your-namespace>port-forwardsvc/llamacloud-web3000:80


```

Once that command is running, you will be able to visit the LlamaCloud UI at <http://localhost:3000>.
While this may be sufficient for initial testing of your deployment, you will eventually need to setup the an ingress when taking your deployment to production and leveraging LlamaCloud as an API based service.
## Requirements
[Section titled “Requirements”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#requirements)
  * A `super-cool.domain`
  * An ingress controller deployed in your kubernetes cluster 
    * A popular choice is [`ingress-nginx`](https://github.com/kubernetes/ingress-nginx)


## Helm Chart Configuration
[Section titled “Helm Chart Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#helm-chart-configuration)
As of version `0.1.47`, the LlamaCloud helm chart supports the ability to configure an ingress resource for your deployment. The chart supports the following configuration:
values.yaml```


ingress:




enabled: true




host: "<YOUR-HOSTNAME>"




tlsSecretName: "ingress-nginx-secret"




ingressClassName: "nginx"




annotations: {}


```

We recommend setting up the ingress resource using the helm chart configuration above.
Once your ingress endpoint is setup, you can visit the LlamaCloud UI at `https://<your-domain-name>`. And, you can check the status of your ingress resource:
Terminal window```


kubectl-nllamacloudgetingress




# Example output



NAMECLASSHOSTSADDRESSPORTSAGE




llamacloud-ingressnginxllamacloud.example<ip-or-load-balancer-address>80,44310m


```

### Ingress Route Details
[Section titled “Ingress Route Details”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#ingress-route-details)
  * `/api`: route all incoming requests with a path prefix of `/api` to the **llamacloud** service
  * `/`: route all other requests to the **llamacloud-web** service


### TLS Configuration
[Section titled “TLS Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#tls-configuration)
Depending on your ingress controller, you may need to add a TLS secret to your ingress resource. You can specify that in the `.Values.ingress.tlsSecretName` field. Currently, we only support a single host and a single TLS secret. For more information on TLS Secrets, see the [Kubernetes Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls).
## Self-Managed Ingress
[Section titled “Self-Managed Ingress”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#self-managed-ingress)
To configure ingress for your deployment, apply the following ingress resource to your cluster:
```

apiVersion: networking.k8s.io/v1


kind: Ingress


metadata:



name: llamacloud




namespace: llamacloud



spec:



ingressClassName: <YOUR-INGRESS-CLASS-NAME>




rules:




http:




paths:




- backend:




service:




name: llamacloud




port:




number: 80




path: /api




pathType: Prefix




- backend:




service:




name: llamacloud-web




port:




number: 80




path: /




pathType: Prefix


```

For information about configuring an ingress resource, see the [Kubernetes Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/).
### BACKEND_URL Configuration
[Section titled “BACKEND_URL Configuration”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#backend_url-configuration)
The `BACKEND_URL` environment variable is used by the Frontend service to know where to send `/api` requests to. When you self-manage your ingress resource, it is recommended to explicitly set this environment variable so the Frontend service doesn’t have to rely on the internal NextJS proxy to route requests to the Backend service.
```

# The helm charts will automatically configure the BACKEND_URL environment variable for the Frontend service to point to the ingress host.



ingress:




enabled: true




host: <YOUR-DOMAIN-NAME>




tlsSecretName: "tls-secret-name"




# alternative values.yaml



frontend:




extraEnvVariables:




- name: BACKEND_URL




value: "https://<your-domain-name>"




volumeMounts:




- mountPath: "/mount/path/to/your/certificate-mount-path/cert.pem"




name: ca-certs




readOnly: true




volumes:




- name: ca-certs




secret:




secretName: ca-cert-secret


```

## Common Issues
[Section titled “Common Issues”](https://developers.llamaindex.ai/python/cloud/self_hosting/configuration/ingress/#common-issues)
  * When an ingress resource is created, sometimes the frontend service may not be able to resolve the certificate. Users may experience slowness or failure during the login flow if this happens and may see an `UNABLE_TO_VERIFY_LEAF_SIGNATURE` error in the frontend logs.
    * There are easy and hard ways to resolve this issue.
    * The easy way is to set `NODE_TLS_REJECT_UNAUTHORIZED=0` in the Frontend deployment with `.Values.frontend.extraEnvVariables`. This will tell the Frontend to ignore the certificate error. One drawback of this approach is that it may not be accepted by your organization’s security policies.
    * The harder way is enable the Frontend pod to resolve the certificate you used to sign the ingress host. You can do this by mounting the certificate into the Frontend pod.
    * If you are using a self-signed certificate, you can use the following to generate a certificate and key: 
Terminal window```

# create a configmap with the Certificate Authority



kubectlcreateconfigmapca-cert-config--from-file=<certificate-authority-name>.pem=/local/path/to/your/<certificate-authority-name>.pem


```

    * Then, you can mount the configmap into the Frontend pod and add the NODE_EXTRA_CA_CERTS environment variable: 
```

# In the values.yaml file:



frontend:




extraEnvVariables:




- name: NODE_EXTRA_CA_CERTS




value: "/mount/path/to/your/certificate-mount-path/cert.pem"


```

  * If you do not have an automated DNS setup, you will need to provide the IP address of the ingress resource to your DNS provider.


If you require assistance with setting up an ingress resource, please reach out to us on support at llamaindex.ai and we will be happy to help you!
