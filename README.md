# a modern proxying system for conveniently playing legacy games
konakona et al. 2025
## synopsis
this paper describes a system for routing game traffic to third-party game servers, ensuring convenience, security, and performance, for the legacy roblox revival apple strudel.

## preamble
legacy/old roblox revivals are a fairly new and interesting phenomenon on the internet, where people write their own websites and host legacy versions of roblox game servers and clients for nostalgia purposes.
this is typically done by having all the servers be first-party, i.e. hosted by the website hosts, too. there were some revivals where third parties hosted, too; but they were done in very poor ways and were unpopular as they were inconvenient compared to first-party servers.

as apple strudel is a community-focused revival, where everyone can host their own third-party server to host on the website, this raises questions about the potential security concerns and troubles regarding domain names and patching the client and server. obviously, if anyone could connect to a bad actor's server, they could just log everyone's ip address and cause another ip leak incident, like with the goodblox revival in 2020. also, with the way roblox works, you can't really connect directly to an ip address - it's possible, sure, but it's annoying to do and technically we'd need control over that server anyway, which defeats the point of community hosted servers.

in order to solve this problem, we propose the apple strudel game proxy - routing everyone's game traffic through secure, high performance proxy servers, stopping leaks and removing the hassle of leaking both player and server ip addresses.

---
## architecture
the game proxy consists of three main elements:
- the proxy - main part of the system
- the router - sets up proxy connections automatically
- the matchmaker - decides which server to connect users to

### the proxy
as proxy servers that are fast, stable, reliable, and secure already exist, and we already had little experience in routing network traffic, we chose not to write our own and use one of the many existing ones.

we looked at the current options that exist, and came down to these options:
- HAProxy - a fast, lower-level proxy server for TCP packets, and load balancer
- nginx (with streaming) - a well known proxy server with the streaming module to route TCP/UDP packets
- Traefik - another option similar to HAProxy, however also supports UDP traffic, but also is commercial as opposed to HAProxy

the best choice for us was HAProxy, as it was fully free and open source, and TCP was all we needed anyway. 
it also has a fairly simple yet powerful config system, and runtime API to allow adding volatile routing rules during runtime. 
Traefik could have also worked, but it's commercial model was not very attractive to us, and community support was more limited as opposed to HAProxy.

therefore, HAProxy was chosen as our proxy software.

however, on it's own, the proxy server will be useless - it won't know where to route what by itself, which is why we need the router to do this job.

### the router
