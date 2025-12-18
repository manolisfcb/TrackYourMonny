``` 
mermaid 
flowchart TB
  %% Clients
  A[Android App] -->|HTTPS (JWT)| LB[Cloud Run Service: API (FastAPI)]

  %% Core data
  LB -->|SQLAlchemy async| DB[(Neon Postgres)]
  LB --> LOG[Cloud Logging / Monitoring]

  %% Receipt upload path
  A -->|Upload image (signed URL)| ST[(Cloud Storage Bucket)]
  LB -->|Create receipt record: PENDING| DB

  %% Queue for receipt processing
  LB -->|Enqueue task (receipt_id)| Q[Cloud Tasks Queue]

  %% Worker processing
  Q -->|HTTP POST + OIDC| W[Cloud Run Service: Worker (FastAPI)]
  W -->|Read image| ST
  W -->|Call external API| LLM[External LLM / Receipt Extraction API]
  W -->|Write draft + status DONE/FAILED| DB
  W --> LOG

  %% Dashboard path
  A -->|GET /dashboard?month=...| LB
  LB -->|Aggregations (SUM/GROUP BY)| DB

  %% Alerts (MVP)
  LB -->|On create/update expense: check budget| DB
  LB -->|Create alert record| DB
  A -->|GET /alerts| LB
```