# Database Planning

+----------------------+     +-------------------------+
|        Bikes         |     |    MaintenanceHistory   |
+----------------------+     +-------------------------+
| * bike_id           |---->| * maintenance_id        |
|   model_name        |     |   bike_id              |
|   purchase_date     |     |   service_date         |
|   last_maintenance  |     |   miles_at_service     |
|   total_miles_driven|     |   service_type         |
|   status            |     |                        |
+----------------------+     +-------------------------+