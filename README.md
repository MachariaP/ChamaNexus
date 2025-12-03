# ChamaNexus - Minimal Chama (Savings Group) App

A simple, non-complex Django-based mobile application to help Kenyan Chamas manage their transactions and members, with a focus on core functionality for group Treasurers.

## 🎯 Features

### Core Functionality
- ✅ **Member Management** - Track members with roles (Treasurer, Admin, Member)
- ✅ **Transaction Logging** - Record contributions, fines, and payouts with M-Pesa codes
- ✅ **Data Integrity** - Prevent duplicate transactions using unique M-Pesa codes
- ✅ **Member Statements** - Calculate net balances automatically
- ✅ **Group Balance** - Track total Chama assets
- ✅ **Payment Status** - Monitor who has paid, is short, or overdue
- ✅ **Role-Based Access** - Restrict sensitive operations to Treasurers/Admins

### Business Logic (5 Core Rules)

1. **Data Integrity** - M-Pesa transaction codes are unique identifiers
2. **Member Statement** - Net Balance = Contributions - (Fines + Payouts)
3. **Group Balance** - Total Assets = Contributions + Fines - (Payouts + Expenses)
4. **Admin Access** - Only Treasurer/Admin can log and verify transactions
5. **Payment Status** - Automatic determination of PAID/SHORT/OVERDUE status

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Django 5.2.8
- PostgreSQL (production) or SQLite (development)

### Installation

1. Clone the repository
```bash
git clone https://github.com/MachariaP/ChamaNexus.git
cd ChamaNexus
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run migrations
```bash
python manage.py migrate
```

4. Create a superuser
```bash
python manage.py createsuperuser
```

5. Run the development server
```bash
python manage.py runserver
```

## 📚 Documentation

See [CHAMA_IMPLEMENTATION.md](./CHAMA_IMPLEMENTATION.md) for detailed documentation including:
- Data model specifications
- Business logic implementation
- API endpoints
- User workflows
- Testing guide

## 🔌 API Endpoints

### Members
- `GET/POST /api/v1/chamas/members/` - List/Create members
- `GET /api/v1/chamas/members/{id}/statement/` - Member statement
- `GET /api/v1/chamas/members/{id}/payment_status/` - Payment status

### Transactions
- `GET/POST /api/v1/chamas/transactions/` - List/Create transactions
- `POST /api/v1/chamas/transactions/{id}/verify/` - Verify transaction
- `GET /api/v1/chamas/transactions/pending/` - Pending transactions

### Groups
- `GET /api/v1/chamas/groups/{id}/balance/` - Group balance

## 🧪 Testing

Run the test suite:
```bash
python manage.py test chamas
```

All 19 tests validate:
- Model creation and validation
- Business logic rules
- API serialization
- Permission controls
- Complete workflows

## 🏗️ Project Structure

```
ChamaNexus/
├── accounts/          # User authentication and management
├── chamas/           # Core Chama functionality
│   ├── models.py     # Member, Transaction, ChamaGroup models
│   ├── views.py      # API viewsets
│   ├── serializers.py # DRF serializers
│   ├── permissions.py # Custom permissions
│   ├── admin.py      # Django admin configuration
│   └── tests.py      # Comprehensive test suite
├── config/           # Django settings and configuration
└── manage.py
```

## 🔐 Security

- ✅ Role-based access control
- ✅ Authentication required for all endpoints
- ✅ Unique M-Pesa code validation
- ✅ Audit trail for all transactions
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (DRF sanitization)

## 📱 User Workflow (Treasurer)

### Logging a Contribution (3 Steps)

**Step 1:** Access the logging screen via API endpoint

**Step 2:** Enter data:
- Select member
- Enter amount (KES)
- Enter M-Pesa code
- Add optional description

**Step 3:** System validates and saves:
- Checks M-Pesa code uniqueness
- Validates amount
- Creates transaction with PENDING status
- Awaits verification

## 🛠️ Tech Stack

- **Backend:** Django 5.2.8, Django REST Framework 3.16.1
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Token-based authentication
- **Security:** Argon2 password hashing, CORS headers
- **Deployment:** Gunicorn, WhiteNoise

## 📄 License

This project is part of the ChamaNexus platform.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for Kenyan Chamas**
