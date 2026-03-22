# OpenSpec Quick Start Guide

## What is OpenSpec?
OpenSpec is a lightweight spec-driven framework for building software with clear specifications and requirements.

## Project Setup Complete ✅

Your trading application is now configured with OpenSpec specifications.

## Directory Structure

```
d:\app\ev_app/
├── openspec.config.json          # OpenSpec configuration
├── specs/                         # All specifications
│   ├── api.openapi.yml           # API specification (OpenAPI 3.0)
│   ├── COMPONENTS.md             # UI component specs
│   └── FEATURES.md               # Feature specifications
├── .openspec/                    # OpenSpec internal
│   └── changes/                  # Tracked changes
├── backend/                      # Python Flask backend
├── frontend/                     # Vue 3 frontend
└── README.md                     # Project documentation
```

## Key Files

### 1. `openspec.config.json`
Central configuration file defining:
- Project metadata
- Feature status and endpoints
- Code style rules
- Environment configurations

**Key Features Tracked:**
- ✅ Broker Connection (Connect/Disconnect)
- ✅ Account Management (Demo/Real switching)
- ✅ Balance Display (Toolbar + Card)

### 2. `specs/api.openapi.yml`
Complete API specification following OpenAPI 3.0.0 standard.

**Endpoints:**
- `GET /api/trading/status` - Connection status
- `POST /api/trading/connect` - Connect broker
- `POST /api/trading/disconnect` - Disconnect broker
- `GET /api/trading/account` - Get balance
- `POST /api/trading/account/switch` - Switch account

### 3. `specs/COMPONENTS.md`
Vue component specifications with:
- Component structure
- Props definition
- Event/method specifications
- Responsive breakpoints
- Accessibility requirements

**Components Documented:**
- Toolbar (Navigation & Quick Actions)
- Balance Card (Display)
- Status Information (Details)
- Error Banner (Alerts)

### 4. `specs/FEATURES.md`
Feature requirements with:
- Acceptance criteria (checkboxes)
- Workflows
- Integration points
- Error handling
- Performance/Security requirements

## OpenSpec Commands

```bash
# Check project status
openspec status

# Create a new spec-based change
openspec new change <feature-name>

# View specification
openspec view <spec-file>

# Validate specifications
openspec validate

# Generate documentation
openspec docs
```

## How to Use

### 1. Define Specifications First
Before implementing features:
- Write acceptance criteria in `specs/FEATURES.md`
- Define API in `specs/api.openapi.yml`
- Document components in `specs/COMPONENTS.md`

### 2. Track Changes
```bash
openspec new change "Add two-factor authentication"
```

### 3. Implement According to Specs
- Follow component specifications
- Implement only what's specified
- Test against acceptance criteria

### 4. Validate Implementation
- All acceptance criteria met
- Code follows specified style
- API matches OpenAPI spec

## Continuous Development Workflow

```
1. Request Feature
   ↓
2. Write Specification (FEATURES.md)
   ↓
3. Create Change Tracking (openspec new change)
   ↓
4. Implement Code
   ↓
5. Test Against Spec
   ↓
6. Update API Spec if needed
   ↓
7. Document in Changelog
```

## Current Implementation Status

### Implemented Features
- ✅ Broker Connection (Connect/Disconnect)
- ✅ Account Switching (Demo/Real)
- ✅ Balance Display (Toolbar + Card)
- ✅ Status Indicator (Visual feedback)
- ✅ Top Toolbar (Navigation & Actions)

### Specification Coverage
- ✅ API Endpoints (OpenAPI 3.0)
- ✅ Component Structure
- ✅ Feature Requirements
- ✅ Error Handling
- ✅ Responsive Design

## Next Steps

1. **Review Specifications**
   - Read FEATURES.md for all acceptance criteria
   - Check COMPONENTS.md for UI specifications
   - Review api.openapi.yml for API contracts

2. **Run Tests Against Spec**
   ```bash
   npm test
   ```

3. **Add New Features**
   ```bash
   openspec new change "Feature name"
   ```

4. **Generate API Documentation**
   ```bash
   openspec docs
   ```

## Tips & Best Practices

### ✅ Do
- Write specs before implementation
- Use acceptance criteria as test cases
- Update specs when requirements change
- Reference specs in code comments
- Keep specs version-controlled

### ❌ Don't
- Implement features without specs
- Leave specs outdated
- Deviate from specifications without updating docs
- Skip error scenarios
- Ignore accessibility requirements

## Resources

- **OpenSpec Documentation**: https://openspec.dev
- **OpenAPI Documentation**: https://spec.openapis.org/
- **Vue 3 Guide**: https://vuejs.org/
- **Project README**: See root README.md

## Configuration Details

- **Framework**: OpenSpec 1.0.0
- **API Standard**: OpenAPI 3.0.0
- **Frontend**: Vue 3 with Composition API
- **Backend**: Flask with REST
- **Testing**: Spec-based acceptance testing
- **Styling**: Spec-defined CSS standards

## Support

For issues or clarifications:
1. Check `openspec.config.json` for project settings
2. Review relevant spec file (FEATURES.md, COMPONENTS.md, api.openapi.yml)
3. Check error messages in banners
4. Review console logs for debugging info
