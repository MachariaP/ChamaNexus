# ChamaNexus Render Deployment Guide

This guide will walk you through deploying ChamaNexus (Django backend + React frontend) to Render.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Deploy with Blueprint](#quick-deploy-with-blueprint)
3. [Manual Deployment](#manual-deployment)
4. [Environment Variables](#environment-variables)
5. [Render Settings Reference](#render-settings-reference)
6. [Post-Deployment Steps](#post-deployment-steps)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:
- A [Render](https://render.com) account
- Your GitHub repository connected to Render
- The following changes committed to your repository:
  - PostgreSQL database configuration in `config/settings.py`
  - Production dependencies in `requirements.txt`
  - Build script (`build.sh`)
  - Render Blueprint (`render.yaml`)

---

## Quick Deploy with Blueprint

The easiest way to deploy is using the Render Blueprint (`render.yaml`) included in this repository.

### Steps:

1. **Connect your GitHub repository to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **New** → **Blueprint**
   - Select your GitHub repository containing ChamaNexus
   - Render will automatically detect the `render.yaml` file

2. **Review and Deploy**
   - Review the services that will be created:
     - `chamanexus-db` - PostgreSQL database (free plan)
     - `chamanexus-backend` - Django API server
     - `chamanexus-frontend` - React frontend
   - Click **Apply** to start the deployment

3. **Wait for Deployment**
   - Render will automatically:
     - Create the PostgreSQL database
     - Build and deploy the Django backend
     - Build and deploy the React frontend
   - This typically takes 5-10 minutes

---

## Manual Deployment

If you prefer to set up services manually, follow these steps:

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure the database:
   - **Name**: `chamanexus-db`
   - **Database**: `chamanexus`
   - **User**: `chamanexus`
   - **Plan**: Free
4. Click **Create Database**
5. Copy the **Internal Database URL** (you'll need this for the backend)

### Step 2: Deploy Django Backend

1. Click **New** → **Web Service**
2. Connect your GitHub repository
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `chamanexus-backend` |
| **Root Directory** | _(leave empty - uses repo root)_ |
| **Runtime** | Python |
| **Build Command** | `chmod +x build.sh && ./build.sh` |
| **Start Command** | `gunicorn config.wsgi:application` |
| **Plan** | Free |

4. Add Environment Variables (see [Environment Variables](#environment-variables) section)
5. Click **Create Web Service**

### Step 3: Deploy React Frontend

1. Click **New** → **Web Service**
2. Connect the same GitHub repository
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `chamanexus-frontend` |
| **Root Directory** | `FE` |
| **Runtime** | Node |
| **Build Command** | `npm install && npm run build` |
| **Start Command** | `npm start` |
| **Plan** | Free |

4. Add Environment Variables:
   - `NODE_ENV`: `production`
   - `VITE_API_URL`: `https://chamanexus-backend.onrender.com`
5. Click **Create Web Service**

---

## Environment Variables

### Backend (Django) Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | _(from database)_ | PostgreSQL connection string |
| `SECRET_KEY` | _(auto-generate)_ | Django secret key |
| `DEBUG` | `False` | Disable debug mode |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed hosts |
| `PYTHON_VERSION` | `3.11.4` | Python version |
| `CORS_ALLOWED_ORIGINS` | `https://chamanexus-frontend.onrender.com` | CORS allowed origins |

### Frontend (React) Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_ENV` | `production` | Node environment |
| `VITE_API_URL` | `https://chamanexus-backend.onrender.com` | Backend API URL |

---

## Render Settings Reference

### Backend Service Settings

```yaml
Type: Web Service
Name: chamanexus-backend
Runtime: Python
Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn config.wsgi:application
Plan: Free
```

### Frontend Service Settings

```yaml
Type: Web Service
Name: chamanexus-frontend
Root Directory: FE
Runtime: Node
Build Command: npm install && npm run build
Start Command: npm start
Plan: Free
```

### Database Settings

```yaml
Type: PostgreSQL
Name: chamanexus-db
Database Name: chamanexus
User: chamanexus
Plan: Free
```

---

## Post-Deployment Steps

### 1. Create Django Superuser

After deployment, you may need to create a superuser for the Django admin:

1. Go to your backend service in Render Dashboard
2. Click the **Shell** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts to create an admin user

### 2. Verify Database Connection

Check that migrations ran successfully:
```bash
python manage.py showmigrations
```

### 3. Update Frontend API URL

Ensure your frontend is pointing to the correct backend URL:
- Check the `VITE_API_URL` environment variable
- Should be: `https://chamanexus-backend.onrender.com`

### 4. Configure Custom Domain (Optional)

1. Go to your service settings
2. Click **Custom Domains**
3. Add your domain and follow DNS instructions

---

## Troubleshooting

### Common Issues

#### 1. "Application failed to respond" error

**Cause**: The application might be starting too slowly or failing to bind to the port.

**Solution**: 
- Check the logs in Render Dashboard
- Ensure gunicorn is binding to `0.0.0.0:$PORT`
- The default gunicorn configuration should work automatically

#### 2. Database connection failed

**Cause**: DATABASE_URL might not be set correctly.

**Solution**:
- Verify the `DATABASE_URL` environment variable is set
- Ensure the database service is running
- Check that the internal database URL is used (starts with `postgres://`)

#### 3. Static files not loading

**Cause**: Static files might not be collected properly.

**Solution**:
- Check that `python manage.py collectstatic` ran in the build command
- Verify `whitenoise` is in `INSTALLED_APPS` middleware
- Check `STATIC_ROOT` is set correctly

#### 4. CORS errors

**Cause**: Frontend and backend are on different domains.

**Solution**:
- Add `django-cors-headers` to requirements
- Configure `CORS_ALLOWED_ORIGINS` with the frontend URL
- Ensure the frontend URL includes the protocol (https://)

#### 5. Migrations not running

**Cause**: Build script might not have execute permissions.

**Solution**:
- Ensure `chmod +x build.sh` is in the build command
- Or use: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`

### Checking Logs

1. Go to Render Dashboard
2. Select your service
3. Click the **Logs** tab
4. Look for error messages

### Useful Commands (via Shell)

```bash
# Check database connection
python manage.py dbshell

# Check migrations status
python manage.py showmigrations

# Run migrations manually
python manage.py migrate

# Check static files
python manage.py findstatic admin/css/base.css
```

---

## Local Development with PostgreSQL

To test PostgreSQL locally before deploying:

1. Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgres://user:password@localhost:5432/chamanexus
   SECRET_KEY=your-development-secret-key
   DEBUG=True
   ```

2. Install PostgreSQL locally or use Docker:
   ```bash
   docker run --name postgres-chamanexus -e POSTGRES_PASSWORD=password -e POSTGRES_DB=chamanexus -p 5432:5432 -d postgres
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## Cost Considerations

Render's free tier includes:
- **Web Services**: 750 free hours/month
- **PostgreSQL**: Free tier available with limited storage
- **Note**: Free services spin down after 15 minutes of inactivity

For production use, consider upgrading to paid plans for:
- Always-on services
- More database storage
- Custom domains with SSL
- Better performance

---

## Support

If you encounter issues:
1. Check Render's [documentation](https://render.com/docs)
2. Review the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
3. Open an issue in the GitHub repository
