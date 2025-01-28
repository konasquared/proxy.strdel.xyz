# strproxy
A high performance, high security proxy for routing game traffic to third-party game servers.

Written by konakona et al. at apple strudel.
## How it works
strproxy uses HAProxy and automatically configures it to start network connections to remote servers your players then connect to.
For more information you should read the research paper on strproxy.

## Quick start guide
This guide assumes you're starting from scratch, but already have a website and client, have the ability to read English and some common sense.

strproxy requires that you run it on something like Debian Server. For instance, Ubuntu, Linux Mint, whatever you want, if it has `apt`, you'll probably be fine.
If you use Windows to host RCCService (though you *could* use also use Wine on Linux for RCCService, like we do), you'll probably have
to use a Docker container for this. It'll work as well. Maybe I'll make a premade dockerfile in the future.

IMPORTANT: If something fails between steps 1 to 5 - that's on YOU to fix! Don't raise an issue, we will delete it because likely *it's not our fault*.
Once you're on or past step 6, you can make an issue if anything fails.

### 1) Clone the repo
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

### 4) Install Python 3.12+
Ensure it's not the minimal build; it does not contain all the standard libraries needed.
In other words - don't use the Python bundled with your distro. Install your own.

### 5) Install Python dependencies
It's best if you make a new virtual environment for this:
```
python3 -m venv strpxyvenv
source strpxyvenv/scripts/activate
```
(Deactivate the venv with the `deactivate` command once you're done)

Simply run `python3 -m pip install -r requirements.txt` and wait for all dependencies to install.

### ?) Configuring strproxy
Inside `/config/`, you will find `database.toml`, `network.toml`.

Your Redis URI and auth will go inside `database.toml`. Read the comments inside and use some common sense.
