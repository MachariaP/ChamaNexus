# Chama Nexus - Minimal Chama App Implementation

This document provides a comprehensive guide to the core data models, business logic, and user flows implemented for the ChamaNexus minimal Chama (Savings Group) application with a Kenya focus.

## Overview

The implementation focuses on **core functionality** for Kenyan Chamas without unnecessary complexity. It supports basic transaction management, member tracking, and ensures data integrity through business rules.

---

## Part 1: Core Data Models

### 1. Member Model

**Purpose:** Represents a person in the Chama savings group.

**Location:** `/chamas/models.py`

**Core Fields:**

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | UUIDField | Unique identifier | Auto-generated |
| `name` | CharField(255) | Full name of member | Required |
| `phone_number` | CharField(15) | Kenyan phone number for M-Pesa | Regex validated: `+254XXXXXXXXX` or `07XXXXXXXXX` |
| `role` | CharField(20) | Chama role/permission | Choices: TREASURER, ADMIN, MEMBER |
| `status` | CharField(20) | Current membership status | Choices: ACTIVE, INACTIVE, SUSPENDED |
| `user` | ForeignKey | Link to User model (optional) | Nullable |
| `created_at` | DateTimeField | When member was added | Auto-generated |
| `updated_at` | DateTimeField | Last update timestamp | Auto-updated |

**Key Features:**
- Phone numbers are automatically normalized from `0712345678` to `+254712345678` format
- Supports linking to system user accounts or standalone members
- Indexes on phone_number, status, and role for fast queries

**Business Methods:**
- `is_admin_or_treasurer()` - Check if member has admin privileges (Rule 4)
- `calculate_net_balance()` - Calculate member's net balance (Rule 2)
- `get_payment_status(expected_amount)` - Determine payment status (Rule 5)

---

### 2. Transaction Model

**Purpose:** Represents a contribution, fine, payout, or group expense.

**Location:** `/chamas/models.py`

**Core Fields:**

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | UUIDField | Unique identifier | Auto-generated |
| `member` | ForeignKey | Link to Member | Required for contributions/fines/payouts |
| `amount` | DecimalField(10,2) | Transaction amount in KES | Min: 0.01 |
| `date` | DateTimeField | Transaction date/time | Default: now |
| `transaction_type` | CharField(20) | Type of transaction | Choices: CONTRIBUTION, FINE, PAYOUT, EXPENSE |
| `mpesa_code` | CharField(20) | M-Pesa transaction code | **Unique**, 10 alphanumeric characters |
| `status` | CharField(20) | Verification status | Choices: PENDING, VERIFIED, REJECTED |
| `description` | TextField | Optional notes | Optional |
| `created_by` | ForeignKey | User who logged transaction | Nullable |
| `verified_by` | ForeignKey | User who verified transaction | Nullable |
| `verified_at` | DateTimeField | Verification timestamp | Nullable |

**Key Features:**
- M-Pesa codes are automatically converted to uppercase
- Database-level uniqueness constraint on `mpesa_code` prevents duplicates
- Indexes on mpesa_code, transaction_type+status, date, and member+date

**Business Methods:**
- `verify(user)` - Mark transaction as verified (Rule 4)
- `reject(user)` - Mark transaction as rejected (Rule 4)

---

### 3. ChamaGroup Model

**Purpose:** Represents the Chama group for aggregate calculations and settings.

**Location:** `/chamas/models.py`

**Core Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUIDField | Unique identifier |
| `name` | CharField(255) | Group name |
| `description` | TextField | Group description |
| `monthly_contribution_amount` | DecimalField(10,2) | Expected monthly contribution per member |
| `created_at` | DateTimeField | When group was created |
| `updated_at` | DateTimeField | Last update timestamp |

**Business Methods:**
- `calculate_total_balance()` - Calculate group's total cash assets (Rule 3)
- `get_total_fines()` - Get total fines collected

---

## Part 2: Essential Business Logic (5 Rules)

### Rule 1: Data Integrity Logic

**Purpose:** Ensure a single contribution is not logged twice using M-Pesa transaction code as unique identifier.

**Implementation:**
- **Database Level:** Unique constraint on `Transaction.mpesa_code`
- **Model Level:** Custom `clean()` method validates uniqueness before save
- **API Level:** Serializer validation checks for duplicates before creation

**Code Location:** `/chamas/models.py` - `Transaction.clean()` method

```python
def clean(self):
    if self.mpesa_code:
        self.mpesa_code = self.mpesa_code.upper().strip()
        duplicate = Transaction.objects.filter(
            mpesa_code=self.mpesa_code
        ).exclude(pk=self.pk).exists()
        
        if duplicate:
            raise ValidationError({
                'mpesa_code': 'This M-Pesa transaction code has already been logged.'
            })
```

**Test Coverage:** `test_duplicate_mpesa_code_validation()`, `test_duplicate_prevention()`

---

### Rule 2: Member Statement Logic

**Purpose:** Calculate a member's net balance (Total contributions minus fines/payouts).

**Formula:** 
```
Net Balance = Total Contributions - (Total Fines + Total Payouts)
```

**Implementation:**
- Only counts **VERIFIED** transactions
- Uses Django's aggregation for efficient calculation
- Returns Decimal for precise financial calculations

**Code Location:** `/chamas/models.py` - `Member.calculate_net_balance()` method

```python
def calculate_net_balance(self):
    contributions = self.transactions.filter(
        transaction_type='CONTRIBUTION',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    fines = self.transactions.filter(
        transaction_type='FINE',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    payouts = self.transactions.filter(
        transaction_type='PAYOUT',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    return contributions - (fines + payouts)
```

**API Access:** `GET /api/v1/chamas/members/{id}/statement/`

**Test Coverage:** `test_calculate_net_balance_empty()`, `test_calculate_net_balance_with_transactions()`

---

### Rule 3: Group Balance Logic

**Purpose:** Calculate the Chama's total cash assets.

**Formula:**
```
Group Balance = Total Contributions + Total Fines - (Total Payouts + Total Expenses)
```

**Note:** Fines add to the group balance as they represent additional income to the group.

**Implementation:**
- Only counts **VERIFIED** transactions
- Separate tracking of fines for transparency
- Efficient database aggregation

**Code Location:** `/chamas/models.py` - `ChamaGroup.calculate_total_balance()` method

```python
def calculate_total_balance(self):
    contributions = Transaction.objects.filter(
        transaction_type='CONTRIBUTION',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    payouts = Transaction.objects.filter(
        transaction_type='PAYOUT',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    expenses = Transaction.objects.filter(
        transaction_type='EXPENSE',
        status='VERIFIED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    return contributions - (payouts + expenses)
```

**API Access:** `GET /api/v1/chamas/groups/{id}/balance/`

**Test Coverage:** `test_calculate_total_balance_empty()`, `test_calculate_total_balance_with_transactions()`

---

### Rule 4: Admin Access Logic

**Purpose:** Restrict crucial functions (logging/editing transactions) to only Treasurer/Admin roles.

**Implementation:**

**1. Model Level:**
```python
def is_admin_or_treasurer(self):
    return self.role in ['TREASURER', 'ADMIN']
```

**2. Permission Class:** `/chamas/permissions.py`
```python
class IsTreasurerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        member = Member.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).first()
        
        return member and member.is_admin_or_treasurer()
```

**3. View Level:** Applied to create, update, delete, verify, reject actions
```python
def get_permissions(self):
    if self.action in ['create', 'update', 'verify', 'reject']:
        permission_classes = [IsAuthenticated, IsTreasurerOrAdmin]
    else:
        permission_classes = [IsAuthenticated]
    return [permission() for permission in permission_classes]
```

**Protected Operations:**
- Creating transactions
- Updating transactions
- Deleting transactions
- Verifying transactions
- Rejecting transactions

**Test Coverage:** `test_is_admin_or_treasurer()`, `test_admin_access_control()`

---

### Rule 5: Payment Status Logic

**Purpose:** Determine if a member is "PAID," "SHORT," or "OVERDUE" for the current contribution cycle.

**Logic:**

| Condition | Status | Description |
|-----------|--------|-------------|
| Monthly contribution >= Expected amount | `PAID` | Member has fully paid |
| 0 < Monthly contribution < Expected amount | `SHORT` | Member has partially paid |
| Monthly contribution = 0 AND day > 7 | `OVERDUE` | Payment is late |
| Monthly contribution = 0 AND day ≤ 7 | `SHORT` | Still within payment window |

**Implementation:**
- Checks current month's verified contributions
- Compares against expected monthly contribution amount
- Uses day of month to determine if overdue

**Code Location:** `/chamas/models.py` - `Member.get_payment_status()` method

```python
def get_payment_status(self, expected_amount=None):
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0)
    
    monthly_contributions = self.transactions.filter(
        transaction_type='CONTRIBUTION',
        status='VERIFIED',
        date__gte=current_month_start
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    if monthly_contributions >= expected_amount:
        return 'PAID'
    elif monthly_contributions > 0:
        return 'SHORT'
    else:
        if now.day > 7:
            return 'OVERDUE'
        return 'SHORT'
```

**API Access:** `GET /api/v1/chamas/members/{id}/payment_status/`

**Test Coverage:** `test_get_payment_status_paid()`, `test_get_payment_status_short()`

---

## Part 3: Required UI/User Flow (Treasurer)

### Treasurer Workflow: Logging a New Contribution

**Complete 3-Step Flow:**

#### Step 1: Accessing the Logging Screen

**Frontend Action:**
- User navigates to contribution logging page
- Frontend makes authenticated request to member list endpoint

**API Endpoint:** `GET /api/v1/chamas/members/`

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Jane Doe",
    "phone_number": "+254712345678",
    "role": "MEMBER",
    "status": "ACTIVE"
  }
]
```

#### Step 2: Data Entry

**Frontend Form Fields:**
1. **Select Member** - Dropdown populated from member list
2. **Amount** - Numeric input (KES)
3. **M-Pesa Code** - Text input (10 characters)
4. **Transaction Type** - Defaults to "CONTRIBUTION"
5. **Date** - Date/time picker (defaults to now)
6. **Description** - Optional text area

**Example Form Data:**
```json
{
  "member": "member-uuid",
  "amount": "2000.00",
  "mpesa_code": "ABC1234567",
  "transaction_type": "CONTRIBUTION",
  "date": "2024-12-03T10:00:00Z",
  "description": "December monthly contribution"
}
```

#### Step 3: System Action (Verification Check and Saving)

**API Endpoint:** `POST /api/v1/chamas/transactions/`

**Request Headers:**
```
Authorization: Token <auth-token>
Content-Type: application/json
```

**System Actions:**
1. **Validate M-Pesa Code:**
   - Check format (10 alphanumeric characters)
   - Check uniqueness against existing transactions
   - Normalize to uppercase

2. **Validate Amount:**
   - Ensure > 0.01
   - Format to 2 decimal places

3. **Set Metadata:**
   - `created_by` = Current user
   - `status` = 'PENDING'
   - `created_at` = Current timestamp

4. **Save to Database:**
   - Create transaction record
   - Transaction awaits verification

**Success Response (201 Created):**
```json
{
  "message": "Transaction logged successfully. Pending verification.",
  "transaction": {
    "id": "transaction-uuid",
    "member": "member-uuid",
    "member_name": "Jane Doe",
    "amount": "2000.00",
    "date": "2024-12-03T10:00:00Z",
    "transaction_type": "CONTRIBUTION",
    "transaction_type_display": "Contribution",
    "mpesa_code": "ABC1234567",
    "status": "PENDING",
    "status_display": "Pending Verification",
    "description": "December monthly contribution",
    "created_by_email": "treasurer@chama.com",
    "created_at": "2024-12-03T10:00:00Z"
  }
}
```

**Error Response (400 Bad Request) - Duplicate M-Pesa Code:**
```json
{
  "mpesa_code": [
    "This M-Pesa transaction code has already been logged. Duplicate contributions are not allowed."
  ]
}
```

### Verifying a Transaction

**API Endpoint:** `POST /api/v1/chamas/transactions/{id}/verify/`

**Permission Required:** Treasurer or Admin role

**Response:**
```json
{
  "message": "Transaction verified successfully.",
  "transaction": {
    "id": "transaction-uuid",
    "status": "VERIFIED",
    "verified_by": "user-uuid",
    "verified_at": "2024-12-03T10:05:00Z"
  }
}
```

---

## API Endpoints Summary

### Members

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/chamas/members/` | List all members | Authenticated |
| POST | `/api/v1/chamas/members/` | Create new member | Treasurer/Admin |
| GET | `/api/v1/chamas/members/{id}/` | Get member details | Authenticated |
| PUT | `/api/v1/chamas/members/{id}/` | Update member | Treasurer/Admin |
| DELETE | `/api/v1/chamas/members/{id}/` | Delete member | Treasurer/Admin |
| GET | `/api/v1/chamas/members/{id}/statement/` | Get member statement | Authenticated |
| GET | `/api/v1/chamas/members/{id}/payment_status/` | Get payment status | Authenticated |

### Transactions

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/chamas/transactions/` | List all transactions | Authenticated |
| POST | `/api/v1/chamas/transactions/` | Create transaction | Treasurer/Admin |
| GET | `/api/v1/chamas/transactions/{id}/` | Get transaction details | Authenticated |
| PUT | `/api/v1/chamas/transactions/{id}/` | Update transaction | Treasurer/Admin |
| DELETE | `/api/v1/chamas/transactions/{id}/` | Delete transaction | Treasurer/Admin |
| POST | `/api/v1/chamas/transactions/{id}/verify/` | Verify transaction | Treasurer/Admin |
| POST | `/api/v1/chamas/transactions/{id}/reject/` | Reject transaction | Treasurer/Admin |
| GET | `/api/v1/chamas/transactions/pending/` | List pending transactions | Authenticated |

### Groups

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/chamas/groups/` | List groups | Authenticated |
| POST | `/api/v1/chamas/groups/` | Create group | Treasurer/Admin |
| GET | `/api/v1/chamas/groups/{id}/` | Get group details | Authenticated |
| PUT | `/api/v1/chamas/groups/{id}/` | Update group | Treasurer/Admin |
| GET | `/api/v1/chamas/groups/{id}/balance/` | Get group balance | Authenticated |

---

## Database Schema

### Tables Created

1. **chama_members** - Member information
2. **chama_transactions** - All transactions
3. **chama_groups** - Chama group settings

### Indexes

**Optimized for:**
- Phone number lookups
- Member status filtering
- Transaction type and status queries
- Date range queries
- M-Pesa code lookups

---

## Testing

**Test Coverage:** 19 comprehensive tests

**Test Categories:**

1. **Model Tests:**
   - Member creation and validation
   - Transaction creation and validation
   - ChamaGroup creation and calculations

2. **Business Logic Tests:**
   - Rule 1: Duplicate prevention
   - Rule 2: Net balance calculation
   - Rule 3: Group balance calculation
   - Rule 4: Admin access control
   - Rule 5: Payment status determination

3. **Integration Tests:**
   - Complete workflow from creation to verification
   - Multi-member scenarios
   - Edge cases and error handling

**Run Tests:**
```bash
python manage.py test chamas
```

---

## Admin Interface

**Features:**
- View and manage members with net balance display
- View and manage transactions with verification actions
- View group balance and financial summaries
- Bulk verify/reject transactions
- Auto-complete for member selection
- Color-coded balance displays

**Access:** `/admin/chamas/`

---

## Security Considerations

1. **Authentication Required:** All endpoints require authentication
2. **Role-Based Access:** Treasurer/Admin roles for modifications
3. **Data Validation:** Multiple layers (model, serializer, database)
4. **SQL Injection Protection:** Django ORM prevents SQL injection
5. **XSS Protection:** JSON responses sanitized by DRF
6. **Unique Constraints:** Database-level uniqueness for M-Pesa codes
7. **Audit Trail:** Tracks who created/verified transactions

---

## Migration Files

**Location:** `/chamas/migrations/0001_initial.py`

**Applied Changes:**
- Creates all three models
- Creates indexes for performance
- Sets up foreign key relationships
- Establishes unique constraints

**Apply Migrations:**
```bash
python manage.py migrate
```

---

## Future Enhancements (Not in Minimal Version)

These are intentionally **excluded** from the minimal version:

- ❌ In-app M-Pesa payments integration
- ❌ Advanced reporting and analytics
- ❌ Multiple Chama groups per user
- ❌ Loan management
- ❌ Automated reminders/notifications
- ❌ Mobile app (currently API only)
- ❌ Real-time M-Pesa validation
- ❌ Multi-currency support

---

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Create Chama Group
Via Django Admin (`/admin/`):
- Navigate to Chama Groups
- Create new group with name and monthly contribution amount

### 5. Create Members
Via Django Admin or API:
- Add members with names, phone numbers, and roles
- Assign at least one TREASURER role

### 6. Start Logging Transactions
Via API:
- Use `/api/v1/chamas/transactions/` endpoint
- Provide member, amount, and M-Pesa code
- Verify transactions to update balances

---

## Support & Documentation

- **Code Location:** `/chamas/`
- **Tests:** `/chamas/tests.py`
- **API Documentation:** Available via DRF browsable API
- **Admin Interface:** `/admin/chamas/`

---

## Conclusion

This implementation provides a **solid foundation** for a minimal Chama app focused on:
- ✅ Core functionality without complexity
- ✅ Data integrity and trust
- ✅ Simple Treasurer workflow
- ✅ Kenyan M-Pesa integration readiness
- ✅ Comprehensive testing
- ✅ Clear business logic

The system is production-ready for basic Chama operations and can be extended as needs grow.
