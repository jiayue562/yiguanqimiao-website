# Zoho Bookings Routing Reference

**App name:** `zoho-bookings`
**Base URL proxied:** `www.zohoapis.com`

## API Path Pattern

```
/zoho-bookings/bookings/v1/json/{endpoint}
```

## Common Endpoints

### Workspaces

```bash
# List workspaces
GET /zoho-bookings/bookings/v1/json/workspaces

# Get specific workspace
GET /zoho-bookings/bookings/v1/json/workspaces?workspace_id={workspace_id}

# Create workspace
POST /zoho-bookings/bookings/v1/json/createworkspace
Content-Type: application/x-www-form-urlencoded

name=New+Workspace
```

### Services

```bash
# List services (workspace_id required)
GET /zoho-bookings/bookings/v1/json/services?workspace_id={workspace_id}

# Create service
POST /zoho-bookings/bookings/v1/json/createservice
Content-Type: application/x-www-form-urlencoded

name=Consultation&workspace_id={workspace_id}&duration=60
```

### Staff

```bash
# List staff (workspace_id required)
GET /zoho-bookings/bookings/v1/json/staffs?workspace_id={workspace_id}
```

### Appointments

```bash
# Book appointment
POST /zoho-bookings/bookings/v1/json/appointment
Content-Type: application/x-www-form-urlencoded

service_id={service_id}&staff_id={staff_id}&from_time=20-Feb-2026+10:00:00&customer_details={"name":"John","email":"john@example.com","phone_number":"+15551234567"}

# Get appointment
GET /zoho-bookings/bookings/v1/json/getappointment?booking_id=%23NU-00001

# Fetch appointments (uses 'data' wrapper)
POST /zoho-bookings/bookings/v1/json/fetchappointment
Content-Type: application/x-www-form-urlencoded

data={"from_time":"17-Feb-2026 00:00:00","to_time":"20-Feb-2026 23:59:59"}

# Update appointment (cancel/complete/noshow)
POST /zoho-bookings/bookings/v1/json/updateappointment
Content-Type: application/x-www-form-urlencoded

booking_id=#NU-00001&action=cancel
```

## Request Format Notes

- **GET endpoints**: Use query parameters
- **POST endpoints**: Use `application/x-www-form-urlencoded`
- **fetchappointment**: Requires parameters wrapped in `data` field as JSON string
- **customer_details**: Must be a JSON string, not an object
- **Date format**: `dd-MMM-yyyy HH:mm:ss` (e.g., `20-Feb-2026 10:00:00`)

## Service Types

- `APPOINTMENT` - One-on-one appointments
- `RESOURCE` - Resource bookings
- `CLASS` - Group classes
- `COLLECTIVE` - Collective bookings with multiple staff

## Appointment Status Values

- `UPCOMING` - Future appointments
- `CANCEL` - Cancelled appointments
- `COMPLETED` - Completed appointments
- `NO_SHOW` - Customer no-shows
- `PENDING` - Pending confirmation
- `ONGOING` - Currently in progress

## Notes

- Booking IDs include `#` prefix (URL-encode as `%23` in GET requests)
- The `workspace_id` is required for services and staff endpoints
- POST endpoints use form-urlencoded, not JSON body
- Daily API limits: Free (250), Basic (1,000), Premium/Zoho One (3,000) per user

## Resources

- [Zoho Bookings API Documentation](https://www.zoho.com/bookings/help/api/v1/oauthauthentication.html)
- [Book Appointment API](https://www.zoho.com/bookings/help/api/v1/book-appointment.html)
- [Fetch Services API](https://www.zoho.com/bookings/help/api/v1/fetch-services.html)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/cal-com/README]] — Cal.com Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/dropbox-business/README]] — Dropbox Business Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/facebook-page/README]] — Facebook Page Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/getresponse/README]] — GetResponse Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/google-calendar/README]] — Google Calendar Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/google-merchant/README]] — Google Merchant Routing Reference

<!-- AI-LINKS-END -->
