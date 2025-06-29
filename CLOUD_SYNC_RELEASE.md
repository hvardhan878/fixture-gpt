# FixtureGPT v0.1.1 - Cloud Sync Release 🚀

## 🎉 What's New

FixtureGPT now supports **cloud sync** with the FixtureGPT SaaS dashboard! Share fixtures across your team and never lose expensive API call results again.

## ✨ New Features

### ☁️ Cloud Sync
- **Team Collaboration**: Share fixtures across team members instantly
- **Multi-Mode Sync**: Choose local-only, cloud-only, or hybrid sync
- **Automatic Fallback**: Works offline and falls back gracefully
- **Smart Configuration**: Environment variables or programmatic setup

### 🔧 New API
```python
from fixturegpt import configure_cloud_sync

# Configure cloud sync programmatically
configure_cloud_sync(
    api_key="your-api-key-here",
    sync_mode="both"  # local, cloud, or both
)
```

### 🖥️ Enhanced CLI
- `fixturegpt config` - Show current configuration
- Enhanced `fixturegpt stats` - Shows cloud sync status
- Cloud sync status indicators throughout

### 🎛️ Environment Variables
```bash
# Cloud sync configuration
export FIXTUREGPT_API_KEY="your-api-key"
export FIXTUREGPT_SYNC_MODE="both"        # local, cloud, both
export FIXTUREGPT_API_URL="https://app.fixturegpt.com"
```

## 🚀 How It Works

### 1. Local-Only (Default)
```python
# Works exactly as before - no changes needed
result = snapshot("test", expensive_function, "arg")
```

### 2. Cloud Sync Enabled
```python
from fixturegpt import configure_cloud_sync

# Enable cloud sync
configure_cloud_sync("your-api-key", "both")

# Now fixtures sync to cloud dashboard automatically!
result = snapshot("test", expensive_function, "arg")
```

### 3. Team Collaboration
```python
# Team member A records fixtures
configure_cloud_sync("team-api-key", "both")
os.environ["FIXTUREGPT_MODE"] = "record"
result = snapshot("onboarding", generate_email, user_data)

# Team member B replays instantly
configure_cloud_sync("team-api-key", "both")
os.environ["FIXTUREGPT_MODE"] = "replay"
same_result = snapshot("onboarding", generate_email, user_data)
```

## 🔄 Sync Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `local` | Local fixtures only (default) | Individual development |
| `cloud` | Cloud fixtures only | Serverless/stateless environments |
| `both` | Hybrid: local + cloud | Team collaboration (recommended) |

## 📊 Benefits

### For Individual Developers
- ✅ **Backup**: Never lose expensive API results
- ✅ **Sync**: Access fixtures from any device
- ✅ **Analytics**: Track costs in web dashboard

### For Teams
- 🤝 **Collaboration**: Share fixtures instantly
- 📈 **Analytics**: Team usage and cost tracking
- 🎯 **Consistency**: Same test data across environments
- 🔐 **Access Control**: Team permissions and API keys

## 🛡️ Reliability Features

### Graceful Fallbacks
- **Cloud unavailable?** → Falls back to local cache
- **No local cache?** → Falls back to live API calls
- **Network issues?** → Continues working offline

### Error Handling
- Non-blocking cloud sync errors
- Informative warning messages
- Automatic retry logic (built into requests library)

## 📦 Installation & Setup

### 1. Install/Upgrade
```bash
pip install --upgrade fixturegpt
```

### 2. Get API Key
Visit [https://app.fixturegpt.com/dashboard/api-keys](https://app.fixturegpt.com/dashboard/api-keys)

### 3. Configure
```python
from fixturegpt import configure_cloud_sync
configure_cloud_sync("your-api-key", "both")
```

Or use environment variables:
```bash
export FIXTUREGPT_API_KEY="your-api-key"
export FIXTUREGPT_SYNC_MODE="both"
```

## 🧪 Testing

Run the integration tests:
```bash
python test_cloud_sync.py
```

All tests pass with:
- ✅ Local fixtures work perfectly
- ✅ Cloud sync configuration works
- ✅ Fallback behavior is correct
- ✅ CLI integration is functional

## 🔮 What's Next

### SaaS Dashboard Features
- 📊 **Usage Analytics**: Detailed cost and performance metrics
- 🏷️ **Smart Tagging**: Automatic categorization of fixtures
- 👥 **Team Management**: User roles and permissions
- 🔔 **Notifications**: Usage alerts and budget tracking
- 📱 **Mobile App**: Manage fixtures on the go

### Package Improvements
- 🔄 **Auto-sync**: Background sync without blocking
- 🗜️ **Compression**: Reduce fixture storage size
- 🔍 **Search**: Advanced fixture search and filtering
- 📝 **Annotations**: Add comments and metadata to fixtures

## 💰 Pricing

### Open Source Package
- ✅ **Free forever** - Local fixtures
- ✅ All core features included

### Cloud Sync Plans
- 🆓 **Free**: 100 fixtures/month
- 💼 **Pro**: $19/month - Unlimited fixtures
- 🏢 **Team**: $49/month - Advanced analytics
- 🏭 **Enterprise**: Custom pricing

## 🤝 Feedback

We'd love to hear from you! 

- 🐛 [Report Issues](https://github.com/fixturegpt/fixturegpt/issues)
- 💬 [Join Discord](https://discord.gg/fixturegpt)
- 📧 [Email Us](mailto:support@fixturegpt.com)

---

**Happy caching with cloud sync! ☁️🚀** 