# strproxy
A high performance, high security proxy for routing game traffic to third-party game servers.

Written by konakona et al. at apple strudel.
## How it works
strproxy uses HAProxy and automatically configures it to start network connections to remote servers your players then connect to.
For more information you should read the research paper on strproxy.

## Quick start guide
This guide assumes you're starting from scratch, but already have a website and client.

### 1) Clone the repo
Simple enough.
```
git clone https://github.com/konasquared/strproxy
```

### 2) Get Redis working
If you're entirely self-hosting strproxy, follow [these instructions](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) to get Redis running and get your URI and auth details.

If you opt to use a Redis instance on the cloud, simply have the URI and auth details ready to use.

### 3) Install HAProxy
Admittedly, the documentation on this is sparse. But it is pretty simple.
If you're running Debian or Ubuntu, you can find the commands to run [here](https://haproxy.debian.net/).
Just put in the details of your OS and put any HAProxy version above 3.0 (I'd advise an LTS release).

### 4) Configuring strproxy
Inside `/config/`, you will find `database.toml`, `network.toml`.

Your Redis URI and auth will go inside `database.toml`. Read the comments inside and use some common sense.
