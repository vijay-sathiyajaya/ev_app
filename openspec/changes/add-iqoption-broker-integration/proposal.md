## Why

IQOption is one of the most popular binary options and digital options brokers globally. Adding native IQOption integration allows traders to directly connect their IQOption accounts to the platform, enabling seamless binary and digital options trading. This expands the platform's broker support and opens the platform to IQOption's large user base.

## What Changes

- Add IQOption-specific connect/disconnect endpoints that authenticate using IQOption API credentials
- Implement IQOption WebSocket integration for real-time balance updates
- Add option type selector (Binary Options vs Digital Options) in the toolbar to match IQOption's trading modes
- Create IQOption credentials management (email/password or API token)
- Modify broker connection flow to support IQOption-specific authentication
- Update account switching to properly handle IQOption demo and real accounts
- Support IQOption balance fetching and real-time updates

## Capabilities

### New Capabilities
- `iqoption-broker-integration`: Native IQOption broker connection with WebSocket support, real-time balance updates, and option type switching
- `iqoption-credentials-management`: Secure storage and management of IQOption authentication credentials (email/password)
- `option-type-switcher`: UI component to toggle between Binary Options and Digital Options trading modes

### Modified Capabilities
- `broker-connection-management`: Extend to support IQOption-specific authentication flow and WebSocket lifecycle
- `account-type-switching`: Adapt to work with IQOption's demo/real account structure and option type selection

## Impact

### Backend Changes
- Add new IQOption-specific endpoints in Flask backend
- Integrate IQOption Python SDK or REST API library
- Implement WebSocket connection lifecycle management
- Add credential encryption and secure storage

### Frontend Changes
- Add option type toggle buttons (Binary/Digital) to toolbar component
- Create credentials input form for IQOption authentication
- Update Toolbar component to show option type indicator
- Modify API service to call new IQOption endpoints

### Dependencies
- IQOption API Python library (or REST API integration)
- WebSocket support for real-time updates
- Potential credential encryption library

### Breaking Changes
- Broker connection API payload may need to include broker-specific fields (credentials)
