# Dashboard Setup Guide

## Overview
The dashboard endpoint has been updated to display real data from the database instead of hardcoded mock data.

## Setup Instructions

### 1. Database Migration
Ensure all migrations are applied:
```bash
python manage.py migrate
```

### 2. Seed Sample Data
To populate the database with sample data for testing:
```bash
python manage.py seed_data
```

To clear existing data and reseed:
```bash
python manage.py seed_data --clear
```

### 3. Test Users
After seeding, you can login with these test accounts (password: `password123`):

**Treasurer Account:**
- Email: `treasurer@chamanexus.com`
- Role: Staff/Treasurer

**Member Accounts:**
- `john@chamanexus.com`
- `mary@chamanexus.com`
- `peter@chamanexus.com`
- `jane@chamanexus.com`
- `david@chamanexus.com`
- `grace@chamanexus.com`

## API Endpoints

### Dashboard Summary
**Endpoint:** `/accounts/dashboard/summary/`
**Method:** GET
**Authentication:** Required (Token)

**Response for Members:**
```json
{
  "personal_balance": 125000.0,
  "group_balance": 2450000.0,
  "next_meeting": {...},
  "loan_status": {...},
  "recent_transactions": [...],
  "contribution_summary": {...}
}
```

**Response for Treasurers:**
```json
{
  "group_summary": {...},
  "defaulters": [...],
  "pending_actions": {...},
  "recent_group_transactions": [...]
}
```

## Data Models

The dashboard queries data from:
- `Member` - Chama members
- `Transaction` - Contributions, fines, payouts, and expenses
- `ChamaGroup` - Group settings and configurations

## Business Logic

### Personal Balance Calculation
```
Personal Balance = Total Contributions - (Fines + Payouts)
```

### Group Balance Calculation
```
Group Balance = (Contributions + Fines) - (Payouts + Expenses)
```

### Defaulters Identification
Members are identified as defaulters if they:
1. Have unpaid fines, OR
2. Haven't made a contribution in the current month

## Production Deployment

On Render or production environments:
1. Set `DATABASE_URL` environment variable for PostgreSQL
2. Run migrations: `python manage.py migrate`
3. Seed initial data: `python manage.py seed_data`
4. Configure environment variables in Render dashboard

## Notes

- The seed command creates realistic test data for development
- Data includes contributions over the last 3 months
- Some members have loans (payouts) to test loan status display
- Pending transactions are included to test approval workflows
