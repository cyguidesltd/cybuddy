#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Speed mode
MODE=${1:-normal}
case $MODE in
    fast)
        TYPING_SPEED=60
        WAIT_BEFORE=0.5
        WAIT_AFTER=1.5
        SECTION_WAIT=1
        NARRATE_WAIT=0.5
        ;;
    slow)
        TYPING_SPEED=30
        WAIT_BEFORE=2
        WAIT_AFTER=3.5
        SECTION_WAIT=2.5
        NARRATE_WAIT=1.5
        ;;
    *)
        TYPING_SPEED=45
        WAIT_BEFORE=1
        WAIT_AFTER=2
        SECTION_WAIT=1.5
        NARRATE_WAIT=1
        ;;
esac

# Function to simulate typing
type_text() {
    local text="$1"
    local speed=${2:-$TYPING_SPEED}
    local delay=$(awk "BEGIN {print 1/$speed}")

    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
    echo
}

# Function to show command being typed and executed
run_command() {
    local cmd="$1"
    local desc="$2"

    sleep $WAIT_BEFORE
    echo -e "\n${GRAY}# ${desc}${NC}"
    sleep 0.3
    echo -ne "${GREEN}\$ ${NC}"
    type_text "$cmd" $TYPING_SPEED
    sleep 0.3
    echo -e "${CYAN}"
    eval "$cmd"
    echo -e "${NC}"
    sleep $WAIT_AFTER
}

# Function to show section header
show_section() {
    local title="$1"

    sleep $SECTION_WAIT
    echo -e "\n${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${YELLOW}  $title${NC}"
    echo -e "${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════════${NC}\n"
    sleep 0.8
}

# Function to simulate user narration
narrate() {
    local text="$1"

    echo -e "\n${BOLD}${BLUE}💬 $text${NC}\n"
    sleep $NARRATE_WAIT
}

# Clear screen and start
clear

# Title screen
echo -e "${BOLD}${CYAN}"
cat << "EOF"
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║        ███████╗███████╗ ██████╗██████╗ ██╗   ██╗██████╗         ║
   ║        ██╔════╝██╔════╝██╔════╝██╔══██╗██║   ██║██╔══██╗        ║
   ║        ███████╗█████╗  ██║     ██████╔╝██║   ██║██║  ██║        ║
   ║        ╚════██║██╔══╝  ██║     ██╔══██╗██║   ██║██║  ██║        ║
   ║        ███████║███████╗╚██████╗██████╔╝╚██████╔╝██████╔╝        ║
   ║        ╚══════╝╚══════╝ ╚═════╝╚═════╝  ╚═════╝ ╚═════╝         ║
   ║                                                                  ║
   ║              🛡️  Your Cybersecurity Learning Companion           ║
   ║                                                                  ║
   ║                      ✨ LIVE VC DEMO ✨                          ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

sleep 2

narrate "Welcome! I'm a security student working on a CTF challenge..."

# Scenario 1: Learn Tools
show_section "1️⃣  EXPLAIN - Learn Security Tools"

narrate "Let me understand nmap flags..."

run_command \
    "python3 -m cybuddy explain 'nmap -sV -Pn target'" \
    "Explain nmap command"

# Scenario 2: Get Guidance
show_section "2️⃣  TIP - Security Guidance & Techniques"

narrate "Found a login form. How do I test for SQL injection?"

run_command \
    "python3 -m cybuddy tip 'sql injection'" \
    "Learn SQLi techniques"

# Scenario 3: Plan Next Steps
show_section "3️⃣  PLAN - What to Do Next"

narrate "I got a shell! What's my next move?"

run_command \
    "python3 -m cybuddy plan 'got user shell'" \
    "Plan privilege escalation"

# Scenario 4: Troubleshoot Errors
show_section "4️⃣  ASSIST - Fix Common Errors"

narrate "Getting 'connection refused' error..."

run_command \
    "python3 -m cybuddy assist 'connection refused'" \
    "Troubleshoot connection error"

# Scenario 5: Write Reports
show_section "5️⃣  REPORT - Document Vulnerabilities"

narrate "Need to document my findings professionally..."

run_command \
    "python3 -m cybuddy report 'xss in comment field'" \
    "Generate vulnerability report"

# Scenario 6: Test Knowledge
show_section "6️⃣  QUIZ - Test Your Knowledge"

narrate "Let me test what I learned about web security..."

run_command \
    "python3 -m cybuddy quiz 'jwt'" \
    "Test JWT knowledge"

# Final Statistics
show_section "✨ Demo Complete - Key Highlights"

echo -e "${BOLD}${GREEN}📊 Knowledge Base:${NC} 197 entries covering:\n"
sleep 0.3

echo -e "  ${CYAN}•${NC} 52 security tools (nmap, burp, sqlmap, metasploit...)"
echo -e "  ${CYAN}•${NC} 38 attack techniques (SQLi, XSS, privesc, AD...)"
echo -e "  ${CYAN}•${NC} 25 troubleshooting scenarios"
echo -e "  ${CYAN}•${NC} 22 vulnerability report templates"
echo -e "  ${CYAN}•${NC} 25 learning quizzes"
echo -e "  ${CYAN}•${NC} 35 contextual action plans"

sleep 1.5

echo -e "\n${BOLD}${YELLOW}💡 Key Features:${NC}\n"
sleep 0.3

echo -e "${GREEN}✅${NC} ${BOLD}Zero API Costs${NC} - All responses from local data"
sleep 0.2
echo -e "${GREEN}✅${NC} ${BOLD}Instant Speed${NC} - No network latency"
sleep 0.2
echo -e "${GREEN}✅${NC} ${BOLD}Privacy-First${NC} - Data never leaves machine"
sleep 0.2
echo -e "${GREEN}✅${NC} ${BOLD}Freemium Model${NC} - Mockup (free) + AI (premium)"
sleep 0.5

echo -e "\n${BOLD}${MAGENTA}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}          🎯 Perfect for CTF • Students • Bug Bounty 🎯      ${NC}"
echo -e "${BOLD}${MAGENTA}════════════════════════════════════════════════════════════${NC}\n"

sleep 1

if [ "$MODE" == "fast" ]; then
    DURATION="90 seconds"
elif [ "$MODE" == "slow" ]; then
    DURATION="3 minutes"
else
    DURATION="2 minutes"
fi

echo -e "${GRAY}Demo completed in ~$DURATION${NC}"
echo -e "${GRAY}Zero API calls made - 100% local mockup data${NC}\n"
