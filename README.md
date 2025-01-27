# A modern proxying system for conveniently playing legacy games
apple strudel, konakona et al., 2025. 
## Synopsis
This paper describes strproxy, a system for routing game traffic to third-party game servers, ensuring convenience, security, and performance, for the legacy Roblox revival apple strudel.

## Overview
Legacy/old Roblox revivals are a fairly recent and interesting phenomenon on the internet, where people write their own websites and host legacy versions of roblox game servers and clients, usually for fun, the challenge involved, or nostalgia purposes.
This is typically done by having all the servers be first-party, i.e. hosted by the website hosts, too. There were some revivals where third parties hosted, too; but they were done in very poor ways and were unpopular as they were inconvenient compared to first-party servers.

As apple strudel is a community-focused revival, where everyone can host their own third-party server to host on the website, this raises questions about the potential security concerns and troubles regarding domain names and patching the client and server. Obviously, if anyone could connect to a bad actor's server, they could just log everyone's IP address and cause another IP leak incident, like with the goodblox revival. also, with the way Roblox works, you can't really connect directly to an IP address - it's possible, sure, but it's inconvenient for both us and the user to do, and technically we'd need control over that server too, which defeats the point of community hosted servers.

In order to solve this problem, we propose strproxy - routing everyone's game traffic through secure, high performance proxy servers, stopping leaks and removing the hassle of leaking both player and server ip addresses.

## Architecture
strproxy consists of three main elements:
- The proxy - main part of the system
- The router - sets up proxy connections automatically
- The matchmaker - for automatically deciding which server to connect users to

### The proxy
As proxy servers that are fast, stable, reliable, and secure already exist, and we already had little experience in routing network traffic, we chose not to write our own and use one of the many existing ones.

We looked at the current options that exist, and came down to these options:
- HAProxy - a fast, lower-level proxy server for TCP packets, and load balancer
- nginx (with streaming) - a well known proxy server with the streaming module to route TCP/UDP packets
- Traefik - another option similar to HAProxy, however also supports UDP traffic, but also is commercial as opposed to HAProxy

The best choice for us was HAProxy, as it was fully free and open source, and TCP was all we needed anyway. 
It also has a fairly simple yet powerful config system, and runtime API to allow adding volatile routing rules during runtime. 
Traefik could have also worked, but it's commercial model was not very attractive to us, and community support was more limited as opposed to HAProxy. therefore, HAProxy was chosen as our proxy software.

However, on it's own, the proxy server will be useless - it won't know were to route what by itself, which is why we need the router to do this job.

### The router
The router is another fundamental part of the entire proxy system - it receives requests to open and close connections, from a user to a server,
and automatically sets up the proxy server via it's runtime API to do as the request says.

The router is designed with safeguards, in the event that the proxy does fail, or needs to be restarted for system maintenance. 

It stores live connection information in a database (we use Redis for high performance, but any database could be used) - if the proxy ever fails, or needs to be restarted, the data is kept and the router restarts all the previous connections, reconnecting users without reaching timeout. We also use this for notifying users who are connected to a proxy when this happens via a Discord bot.

The database is also used for keeping analytics data on live concurrent players, server performance, server stats, and network traffic/conditions.

### The matchmaker
By default, on apple strudel, users connect to games by selecting a game in a list, and clicking a "play" button - and they will automatically join the best server for them, based on network conditions, friends already playing, and avoiding players who are blocked.

(There is also an advanced view, where users can connect to servers directly - but this is not related to the subject right now.)

For this to work, a matchmaking service is used. Using the live database from the router, it uses a simple weighted decision-making system to decide which server is best, with these variables:
| Variable                   | Weight |
|----------------------------|--------|
| Network latency            | 1      |
| Latency consistency        | 1.5    |
| Server performance         | 1      |
| Server stability           | 1      |
| Official server status     | 2      |
| # of friends playing       | 3      |
| # of blocked users playing | -10    |
| Blocked server operator    | -10    |
| Remaining player slots     | 1.5    |
| Server age                 | 1.2    |

apple strudel uses a few more factors, which we won't cover because ummm secret :3.

Some notes on a few of the variables:
- Server performance is measured by taking the server's heartbeat deltatime and dividing it by a target deltatime (in this case 60). Servers with a faster heartbeat than 60 will have a higher weight, pushing the server out on the sort. This does require unlocking the server physics FPS on behalf of the user, though.
- Network latency is only measured between the proxy and the server. User-proxy latency is handled by the global proxy router, which this paper covers soon.
- The latency and stability factors are done by measuring the minimum and maximum of the aforementioned factores over the last 1, 5 and 10 minutes, then taking the mean of those.
- Official server status is either 1 or 0.

The final weight is the sum of all the variables multiplied by the weight. The server with the largest weight is then the server that the user will connect to.

The matchmaker actually has one more task it does - which is decide which proxy server to make users connect to. As apple strudel anticipates users from around the world, we have the ability to add more proxy servers in different countries<sup>[note 1]</sup>.

For simplicity, the matchmaker is a centralised system, with only one instance running on our central server alongside the website. While this does mean that if it goes down, automatic server selection will go down too, but we can fallback to manual server selection by the users if this does occur.

## Comparison
strproxy has many benefits over other "traditional" methods of hosting. This paper compares VPN-based third party hosting, server sharing-based hosting and first-party hosting, as well as strproxy.

### VPN-based third-party hosting
| Benefits                                            | Downsides                                                                 |
|-----------------------------------------------------|---------------------------------------------------------------------------|
| VPN prevents real IP addresses from being leaked    | Inconvenient to connect to VPN every time to play                         |
| VPN encrypts data traveling throughout the  network | Latency is much higher due to VPN server and overhead from the connection |
| Simpler for server owners and players to connect    | First time setup of VPN software can be complicated for everyone          |
| Decentralized hosting                               | If VPN goes down, no one can host or play                                 |

### Direct IP connection
| Benefits                                  | Downsides                                               |
|-------------------------------------------|---------------------------------------------------------|
| Lowest latency to the server, no overhead | Player and server IP addresses are revealed to everyone |
| Minimal cost for website owners           | No IP protection - DDoS attacks can be possible         |
| Simplest setup for players                | Complex to setup networking for server operators        |
| Fully decentralized                       | High barrier to entry                                   |

### First-party hosting
| Benefits                                                                       | Downsides                                                                            |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Full control of servers by website owners                                      | High cost to website owners to also host all game servers                            |
| Consistent experience for all players                                          | Limited scalability - cost grows with more players                                   |
| Best security, as no malicious server operators exist                          | Powerful servers are required to host games, which can be expensive in other regions |
| Best matchmaking integration, as server data can be shared in internal network | Fully centralized - if a service goes down then no one at all can play               |

### strproxy (Ours)
| Benefits                                                               | Downsides                                                               |
|------------------------------------------------------------------------|-------------------------------------------------------------------------|
| IP address protection for all as all traffic is through a proxy        | Some cost to keep worldwide server infrastructure                       |
| Centralized management, allowing for IP bans, better matchmaking, etc. | Performance overhead of proxy can impact gameplay                       |
| Scaling infrastructure is much cheaper than with first-party hosting   | Complex implementation leads to more points of failure in the codebase  |
| Much easier for users and server hosts alike to network and use        | Proxy servers can be a point of failure, leading to region-wide outages |

## Conclusion
Of course, strproxy is not a perfect solution. It's very complex for us, and the additional latency overhead will likely impact gameplay. But now, we can have a balance between security, performance, and ease of use, where before, there was no choice that offered all three, but only two at a time, for example security, performance, but hard to use, or easy to use and secure, but slow.

As this is such a complex system, we do not expect that everyone will make their own implementation of this system. Therefore, we have made strproxy free and open source to use under the MIT license, available at https://github.com/konasquared/proxy.strdel.xyz. We invite you to contribute, make pull requests, improve our code, and suggest general improvements, too.

## Footnotes
[1] As of writing, apple strudel only operates one proxy server in Europe, as traffic is low enough that we do not need any more. We are planning to add another proxy server in the US as a lot of users in the revival community are based in the US (from basic observations) and this would be best for them.
