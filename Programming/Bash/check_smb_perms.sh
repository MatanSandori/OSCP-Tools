#!/bin/bash

# Colors for terminal output
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
RESET="\033[0m"

# Usage information
usage() {
    echo "Usage:"
    echo "  $0 <target_ip> [-u username] [-p password] [-v]"
    echo ""
    echo "Options:"
    echo "  -u    Specify a username for authentication"
    echo "  -p    Specify a password for authentication"
    echo "  -v    Enable verbose mode"
    echo "  --help    Display this help message"
    exit 1
}

verbose() {
    if $VERBOSE; then
        echo "[VERBOSE] $1"
    fi
}

# Parsing command-line arguments
USERNAME=""
PASSWORD=""
VERBOSE=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u) USERNAME="$2"; shift;;
        -p) PASSWORD="$2"; shift;;
        -v) VERBOSE=true;;
        --help) usage;;
        *) 
            if [[ -z "$TARGET" ]]; then
                TARGET="$1"
            else
                echo "Unknown parameter passed: $1"
                usage
            fi
            ;;
    esac
    shift
done

if [[ -z "$TARGET" ]]; then
    usage
fi

AUTH=""
if [[ ! -z "$USERNAME" ]]; then
    AUTH="-U $USERNAME"
    if [[ ! -z "$PASSWORD" ]]; then
        AUTH="$AUTH%$PASSWORD"
    fi
fi

# Fetch and parse share details
SHARES=$(smbclient -L //$TARGET -N $AUTH 2>&1 | awk 'NR>4 {print $1, $3, $NF}' | sed '/^$/d')
DOMAIN_INFO=$(smbclient -L //$TARGET -N $AUTH 2>&1 | grep "Domain=")

# Display OS/Domain Info
echo -e "${YELLOW}Domain Info: $DOMAIN_INFO${RESET}"
echo "----------------------------------"

# Check for errors
if [[ "$SHARES" =~ NT_STATUS_(LOGON_FAILURE|ACCESS_DENIED) ]]; then
    echo -e "${RED}Authentication failure. Check username and password.${RESET}"
    exit 1
fi

if [[ "$SHARES" =~ NT_STATUS_IO_TIMEOUT ]]; then
    echo -e "${RED}Connection to $TARGET failed. Check the address and network.${RESET}"
    exit 1
fi

# Enumerate through shares
for SHARE_INFO in $SHARES; do
    SHARE=$(echo $SHARE_INFO | cut -d' ' -f1)
    TYPE=$(echo $SHARE_INFO | cut -d' ' -f2)
    DESCRIPTION=$(echo $SHARE_INFO | cut -d' ' -f3-)
    
    echo -e "\n${YELLOW}Share: $SHARE${RESET}"
    echo -e "${GREEN}Description: $DESCRIPTION${RESET}"

    # Skip IPC$ check
    if [[ "$SHARE" == "IPC$" ]]; then
        echo -e "    ${GREEN}Type: IPC (No file-based permissions to check)${RESET}"
        echo "----------------------------------"
        continue
    fi

    verbose "Checking read access for $SHARE"
    # Check for read permission
    smbclient //$TARGET/$SHARE -N $AUTH -c "ls" 2>/dev/null >/dev/null 
    if [[ $? -eq 0 ]]; then
        echo -e "    ${GREEN}Read access: Yes${RESET}"
        
        # Disk space
        DISK_INFO=$(smbclient //$TARGET/$SHARE -N $AUTH -c "du" 2>/dev/null)
        TOTAL_SPACE=$(echo "$DISK_INFO" | grep "Total bytes listed" | awk '{print $4}')
        if [[ -z "$TOTAL_SPACE" ]]; then
            TOTAL_SPACE="Unknown"
        fi
        echo -e "    ${GREEN}Total space: $TOTAL_SPACE bytes${RESET}"

        # Share size
        SHARE_SIZE=$(echo "$DISK_INFO" | awk 'NF{a=$1} END{print a}')
        if [[ -z "$SHARE_SIZE" ]]; then
            SHARE_SIZE="Unknown"
        fi
        echo -e "    ${GREEN}Share size: $SHARE_SIZE bytes${RESET}"
        
        verbose "Checking write access for $SHARE"
        # Check for write permission by trying to put a temporary file
        smbclient //$TARGET/$SHARE -N $AUTH -c "put /dev/null test_write_access.tmp" 2>/dev/null >/dev/null 
        if [[ $? -eq 0 ]]; then
            echo -e "    ${GREEN}Write access: Yes${RESET}"
            
            verbose "Cleaning up test file on $SHARE"
            # Clean up by removing the temporary file
            smbclient //$TARGET/$SHARE -N $AUTH -c "del test_write_access.tmp" 2>/dev/null >/dev/null 
        else
            echo -e "    ${RED}Write access: No${RESET}"
        fi
    else
        echo -e "    ${RED}Read access: No${RESET}"
    fi
    echo "----------------------------------"
done
