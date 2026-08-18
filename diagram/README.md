# Diagrams — Topic Mind Maps

Mermaid `mindmap` diagrams for memorizing vault topics. Each file groups **related topics**; nodes are **topic names only** (no descriptions).

## Files

| Mind map | Vault folders |

| [[OS-and-Linux]] | Linux, Operating System |
| --- | --- |
| [[Networking-and-DNS]] | Networking, DNS, Protocol |
| [[Containers-and-Orchestration]] | Docker, Kubernates, helm |
| [[Cloud-and-IaC]] | AWS, Terraform, Deployment, Netlify |
| [[Data-Stores]] | Database, MongoDB, Redis, Prisma |
| [[Security-and-Access]] | Security, ssh, cookies |
| [[Web-Frontend]] | React, javascript, css, NextJS, TypeScript, vite, Rendering performance |
| [[Backend-Runtimes]] | NodeJS, ExpressJS, npm, php, Python, golang, kotlin, dart, flutter, android |
| [[Messaging-and-Streaming]] | Messaging, Streaming |
| [[System-Design-and-Architecture]] | System Design, Architectures, Design pattern |
| [[DevOps-and-Delivery]] | DevOps, GIT, GitHub, Nginx, apache, pm2 |
| [[Data-Structures-and-Algorithms]] | Data structure, compiler |
| [[Machine-Learning-and-AI]] | ML, MCP |
| [[Editors-and-Terminals]] | vim, nvim, zed, tmux |
| [[Reference-and-Descriptive]] | Descriptive |
| [[Features-and-Projects]] | Feature implementation, LLD, Projects, Payments, Firebase |
| [[Miscellaneous]] | Errors, Proxy, RTQ, Programming paradigm |
| [[Vault-Root]] | Root-level standalone notes |
| [[Vault-Overview]] | All groups at a glance |

## How to use

1. Open a group mind map in Obsidian (enable **Mermaid**).
2. Read outward from the center — root → folder → subfolder → topic.
3. Jump to the note via `[[wikilink]]` from folder hubs or search.

Regenerate: run `python3 scripts/generate_mindmaps.py` after adding notes.
