## Introduction
A system for automated deployment of a TLS-enabled Redis Stack server on an Azure Container Instance.

## How to use
Works on Windows or Linux (Mac OS not tested yet).

### Installation
#### Step 1: Install Docker
Requires Docker to be installed and running on the system. Follow instructions here:
 - [Windows](https://docs.docker.com/desktop/install/windows-install/)
 - [Linux](https://docs.docker.com/desktop/install/linux-install/)

Additionally, for Windows, you need the Docker WSL2 backend, which also requires installing WSL2 features on Windows. For more detailed instructions, see [WSL2 Docker](https://docs.docker.com/desktop/wsl/)

#### Step 2: Install Azure Command Line Interface (CLI)
Requires Azure CLI to be installed on the system. Follow instructions here:
 - [Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)
 - [Linux](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

#### Step 3: Install Python
Requires python (>=3.9) with packages pyyaml and python-dotenv. The easiest way to install is to use the dedicated conda environment provided in ```environment.yml```:
```
conda env create -f environment.yml
```
This creates a conda environment called ```redis_server``` and installs the package along with dependencies inside it. See [Miniconda install](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html) for instructions on how to install conda if you don't already have it installed and [condas user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) for a more general guide to using conda.

But any python environment with pyyaml and python-dotenv installed should be fine.

### Configuration

#### config.yml

Prior to running, you must create a file called `config.yml` in the repository root directory, in which you set all of the following fields.

```yaml
# Global setting (anything set here will be used for all)
GLOBAL:
  RESOURCE_GROUP: my-resource-group
  LOCATION: eastus
  SLEEP: 300

# Azure Container Registry for redis container
ACR:
  NAME: mycontainerregistry
  CONTAINER:
    NAME: my-container-name
    VERSION: 0.0.1

# Azure Container Instance for running redis server
ACI:
  NAME: my-container-instance
  CPU: 1.0
  MEMGB: 1.5
  # Optional (defaults to ACI.NAME)
  DOMAIN: my-domain-name

# Azure Storage Account for cert
ASA:
  NAME: mystorageaccount
  SHARE: my-file-share
```

Each Azure resource listed here will be created during the process, including resource group, and cannot already exist. The final url of the server will be:

    {ACI.DOMAIN}.{GLOBAL.LOCATION}.azurecontainer.io

Using the example here, that would be:

    my-domain-name.eastus.azurecontainer.io
    
Most names can be any format that you choose, but some cannot contain hyphens or underscores. These are indicated in the above example.

#### .env

In addition to the configuration file, you may also set a single environment variable:

    REDIS_KEY="my-redis-key"

This will be the key that is required to connect to the Redis server once it has been deployed. Choose any string that you want here. You can either set this environment variable manually or create a file called .env in the repository root with this line in it.

Alternately, if you choose not to set this environment variable, or if it is an empty string, a random key will be generated for you. You can find this key afterwards in the generated redis_pass.txt file.

### Run

#### Full process
Once installed and configured, the full deployment process can be run with:

    python ./python/deploy_script.py --full

The process consists of 2 stages:

1. All Azure resources are created and a preliminary container is deployed to the Azure Container Instance. The sole job of this preliminary container is to request a TLS certificate for the domain from https://letsencrypt.org (via certbot). Before requesting the certificate, it waits for a time after launch (given in config.GLOBAL.SLEEP in seconds) to give time for the domain to be registered. Once the certificate has been received, it is saved to the file share and the container's job is finished
2. The preliminary container is deleted and and the final Redis Stack server container is deployed to the same Azure Container Instance. The final container runs the Redis Stack server with the provided TLS certificate and periodically (every month) renews the certificate.

The logic of the process is adapted for Redis from the following guide to deploying Streamlit on Azure Container Instance: [Part 1](https://towardsdatascience.com/beginner-guide-to-streamlit-deployment-on-azure-f6618eee1ba9), [Part 2](https://towardsdatascience.com/beginner-guide-to-streamlit-deployment-on-azure-part-2-cf14bb201b8e)

It is possible that 300 seconds is not long enough to wait for the domain to be registered, in which case certbot will fail and stage 2 deployment will fail also. If there are any issues there, try setting a longer sleep between stages 1 and 2.

#### Separate stages

You can also choose to run the 2 stages separately. To run only the first stage:

    python ./python/deploy_script.py --first

On Azure portal you can navigate to the container instance and view and refresh the running logs to see if the certificate is successfully generated. You can also navigate to and refresh the file share to check for this.

Once happy, you can then run the second stage with:

    python ./python/deploy_script.py --final

#### Delete all resources

If you want to remove all Azure resources created by the process, you can run:

    python ./python/deploy_script.py --clean

This will delete everything in the resource group that you created, taking you back to the very start.

#### Be wary of

With certbot you have a rate limit of 50 certificate requests per week for a given domain. Every time you run stage 1 to successful completion with the same `ACI.DOMAIN` and `GENERAL.LOCATION` settings, this will consume one of those requests. It's unlikely that you will exceed the rate limit but just be aware of this.

### Use

After successfully deploying the Redis Stack server, you can connect to it via any Redis API:

- host: `{ACI.DOMAIN}.{GLOBAL.LOCATION}.azurecontainer.io`
- TCP port: `6379`
- TLS port: `6381`
- password: `{REDIS_KEY}`