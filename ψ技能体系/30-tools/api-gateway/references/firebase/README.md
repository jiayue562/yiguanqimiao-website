# Firebase Routing Reference

**App name:** `firebase`
**Base URL proxied:** `firebase.googleapis.com`

## API Path Pattern

```
/firebase/v1beta1/{resource}
```

## Common Endpoints

### List Projects
```bash
GET /firebase/v1beta1/projects
```

### Get Project
```bash
GET /firebase/v1beta1/projects/{projectId}
```

### Update Project
```bash
PATCH /firebase/v1beta1/projects/{projectId}
Content-Type: application/json

{
  "displayName": "Updated Project Name"
}
```

### List Available Projects
```bash
GET /firebase/v1beta1/availableProjects
```

### Add Firebase to Project
```bash
POST /firebase/v1beta1/projects/{projectId}:addFirebase
Content-Type: application/json

{}
```

### Get Admin SDK Config
```bash
GET /firebase/v1beta1/projects/{projectId}/adminSdkConfig
```

### List Web Apps
```bash
GET /firebase/v1beta1/projects/{projectId}/webApps
```

### Get Web App
```bash
GET /firebase/v1beta1/projects/{projectId}/webApps/{appId}
```

### Create Web App
```bash
POST /firebase/v1beta1/projects/{projectId}/webApps
Content-Type: application/json

{
  "displayName": "My Web App"
}
```

### Get Web App Config
```bash
GET /firebase/v1beta1/projects/{projectId}/webApps/{appId}/config
```

### List Android Apps
```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps
```

### Create Android App
```bash
POST /firebase/v1beta1/projects/{projectId}/androidApps
Content-Type: application/json

{
  "displayName": "My Android App",
  "packageName": "com.example.myapp"
}
```

### Get Android App Config
```bash
GET /firebase/v1beta1/projects/{projectId}/androidApps/{appId}/config
```

### List iOS Apps
```bash
GET /firebase/v1beta1/projects/{projectId}/iosApps
```

### Create iOS App
```bash
POST /firebase/v1beta1/projects/{projectId}/iosApps
Content-Type: application/json

{
  "displayName": "My iOS App",
  "bundleId": "com.example.myapp"
}
```

### Get iOS App Config
```bash
GET /firebase/v1beta1/projects/{projectId}/iosApps/{appId}/config
```

### Check Operation Status
```bash
GET /firebase/v1beta1/operations/{operationId}
```

## Notes

- Project IDs are globally unique identifiers for Firebase projects
- App IDs follow the format `1:PROJECT_NUMBER:PLATFORM:HASH`
- Create operations are asynchronous and return an Operation object
- Deleted apps can be restored within 30 days using the undelete endpoint
- Use `availableProjects` to list GCP projects that can have Firebase added

## Resources

- [Firebase Management API Overview](https://firebase.google.com/docs/projects/api/workflow_set-up-and-manage-project)
- [Firebase Management REST API Reference](https://firebase.google.com/docs/reference/firebase-management/rest)
- [Projects Resource](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects)
- [Web Apps Resource](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.webApps)
- [Android Apps Resource](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.androidApps)
- [iOS Apps Resource](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.iosApps)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/acuity-scheduling/README]] — Acuity Scheduling Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/calendly/README]] — Calendly Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clockify/README]] — Clockify Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/companycam/README]] — CompanyCam Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/google-analytics-admin/README]] — Google Analytics Admin Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/google-apps-script/README]] — Google Apps Script Routing Reference

<!-- AI-LINKS-END -->
