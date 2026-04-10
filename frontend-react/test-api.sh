#!/bin/bash

# API Smoke Test Script
# Tests all backend endpoints to verify they're working before E2E UI testing

API_BASE="http://127.0.0.1:8000"
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BOLD}=== Pocket Heist API Smoke Test ===${NC}\n"

# Test counter
PASSED=0
FAILED=0

# Helper function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local expected_status=$5
    local token=$6

    echo -n "Testing: $description ... "

    if [ -n "$token" ]; then
        HEADERS=(-H "Authorization: Bearer $token" -H "Content-Type: application/json")
    else
        HEADERS=(-H "Content-Type: application/json")
    fi

    if [ -n "$data" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X $method "$API_BASE$endpoint" "${HEADERS[@]}" -d "$data")
    else
        RESPONSE=$(curl -s -w "\n%{http_code}" -X $method "$API_BASE$endpoint" "${HEADERS[@]}")
    fi

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)

    if [ "$HTTP_CODE" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $HTTP_CODE)"
        ((PASSED++))
        if [ -n "$7" ]; then
            eval $7="'$BODY'"
        fi
    else
        echo -e "${RED}✗ FAILED${NC} (Expected HTTP $expected_status, got HTTP $HTTP_CODE)"
        echo -e "  Response: $BODY"
        ((FAILED++))
    fi
}

# 1. Test root endpoint
test_endpoint GET "/" "Root endpoint" "" 200

# 2. Test API docs
echo -n "Testing: API documentation endpoint ... "
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/docs")
if [ "$DOCS_RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✓ PASSED${NC} (HTTP $DOCS_RESPONSE)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (HTTP $DOCS_RESPONSE)"
    ((FAILED++))
fi

# 3. Register new user
TIMESTAMP=$(date +%s)
USERNAME="test_e2e_$TIMESTAMP"
PASSWORD="TestPass123"
REGISTER_DATA="{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"

test_endpoint POST "/auth/register" "User registration" "$REGISTER_DATA" 201 REGISTER_RESPONSE

# 4. Login with new user
LOGIN_DATA="{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
test_endpoint POST "/auth/login" "User login" "$LOGIN_DATA" 200 LOGIN_RESPONSE

# Extract JWT token from login response
JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')

if [ -z "$JWT_TOKEN" ]; then
    echo -e "${RED}✗ FAILED to extract JWT token${NC}"
    ((FAILED++))
    echo "Login response: $LOGIN_RESPONSE"
    exit 1
fi

echo -e "${YELLOW}JWT Token acquired: ${JWT_TOKEN:0:20}...${NC}\n"

# 5. Test protected endpoint
test_endpoint GET "/protected-test" "Protected route (with auth)" "" 200 "$JWT_TOKEN"

# 6. Test getting active heists (should be empty for new user)
test_endpoint GET "/heists" "List active heists" "" 200 "$JWT_TOKEN"

# 7. Create a new heist
HEIST_DEADLINE=$(date -u -d "+3 hours" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v+3H +"%Y-%m-%dT%H:%M:%SZ")
CREATE_HEIST_DATA="{
  \"title\":\"Test Heist $TIMESTAMP\",
  \"target\":\"Test Target\",
  \"difficulty\":\"Medium\",
  \"assignee_username\":\"$USERNAME\",
  \"deadline\":\"$HEIST_DEADLINE\",
  \"description\":\"Automated test heist\"
}"

test_endpoint POST "/heists" "Create heist" "$CREATE_HEIST_DATA" 201 "$JWT_TOKEN" CREATE_RESPONSE

# Extract heist ID
HEIST_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | sed 's/"id"://')

if [ -n "$HEIST_ID" ]; then
    echo -e "${YELLOW}Created heist with ID: $HEIST_ID${NC}\n"

    # 8. Get heist by ID
    test_endpoint GET "/heists/$HEIST_ID" "Get heist by ID" "" 200 "$JWT_TOKEN"

    # 9. Get user's heists
    test_endpoint GET "/heists/mine" "List my heists" "" 200 "$JWT_TOKEN"

    # 10. Abort heist
    test_endpoint PATCH "/heists/$HEIST_ID/abort" "Abort heist" "" 200 "$JWT_TOKEN"

    # 11. Get archive (should include aborted heist)
    test_endpoint GET "/heists/archive" "List archived heists" "" 200 "$JWT_TOKEN"
else
    echo -e "${RED}✗ Could not extract heist ID from create response${NC}"
    ((FAILED++))
fi

# 12. Test unauthorized access (no token)
test_endpoint GET "/heists" "Protected route (no auth)" "" 401

# 13. Test invalid token
test_endpoint GET "/heists" "Protected route (invalid token)" "" 401 "invalid.token.here"

# Summary
echo ""
echo -e "${BOLD}=== Test Summary ===${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo -e "Total:  $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✓ All API tests passed! Backend is ready for E2E testing.${NC}"
    exit 0
else
    echo -e "\n${RED}${BOLD}✗ Some tests failed. Fix backend issues before E2E testing.${NC}"
    exit 1
fi
