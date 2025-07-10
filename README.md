# USB HawkEye 🦅

A real-time USB cybersecurity monitoring and defense tool with a cyberpunk-themed interface. Monitor USB devices, detect threats, and protect your system with advanced security features.

## 🚀 Features

- **Real-time USB Monitoring**: Track device insertion/removal events
- **Threat Detection**: Malware scanning and suspicious activity detection
- **Access Control**: Whitelist/blacklist USB devices
- **Geolocation Tracking**: IP-based device location tracking
- **Alert System**: Email and SMS notifications for security events
- **Cyberpunk UI**: Modern, animated interface with dark theme
- **User Management**: Multi-user support with role-based access
- **Logging & Analytics**: Comprehensive event logging and reporting

## 📋 Requirements

- Python 3.7+
- Windows 10/11 (primary support)
- PyQt5
- Additional dependencies listed in `requirements.txt`

## 🛠️ Installation

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the main application
python main.py
```

### Building Executable
```bash
# Build standalone executable
pyinstaller main.spec
```

## 🎯 Usage

1. **Launch the Application**: Run `python main.py` or the compiled executable
2. **Login/Register**: Create an account or login with existing credentials
3. **Monitor Devices**: View real-time USB device activity in the dashboard
4. **Configure Settings**: Set up email/SMS alerts, access controls, and preferences
5. **Review Logs**: Check security events and device history

## 🔧 Configuration

### Email Alerts
Configure SMTP settings in the application for email notifications:
- Gmail SMTP support included
- Custom email templates for different alert types

### Access Control
- Whitelist trusted USB devices
- Blacklist suspicious or unauthorized devices
- Automatic blocking of unauthorized devices

### User Management
- Admin and regular user roles
- User registration and authentication
- Session management and timeout settings

## 📁 Project Structure

```
USB/
├── main.py                 # Main application entry point
├── core/                   # Core functionality modules
│   ├── usb_monitor.py     # USB device monitoring
│   ├── malware_scanner.py # Threat detection
│   ├── access_control.py  # Device access control
│   ├── alerts.py          # Alert system
│   ├── geoip.py           # Geolocation services
│   └── logger.py          # Logging functionality
├── ui/                     # User interface components
│   ├── dashboard.ui       # Main dashboard
│   ├── settings.ui        # Settings interface
│   └── *.py              # UI logic files
├── resources/              # Application resources
│   └── icons/             # UI icons and graphics
├── config.json            # Application configuration
├── requirements.txt       # Python dependencies
└── setup.py              # Package setup
```

## 🔒 Security Features

- **Real-time Monitoring**: Instant detection of USB device events
- **Malware Scanning**: Integration with ClamAV for threat detection
- **Access Control**: Granular device permissions
- **Audit Logging**: Comprehensive event tracking
- **Encrypted Storage**: Secure user data storage
- **Session Management**: Secure user authentication

## 🎨 UI Features

- **Cyberpunk Theme**: Dark, futuristic interface design
- **Animated Backgrounds**: Dynamic visual effects
- **Responsive Design**: Adapts to different screen sizes
- **Modern Icons**: Custom SVG icons and graphics
- **Smooth Animations**: Professional UI transitions

## 📧 Alert System

### Email Notifications
- Device insertion/removal events
- Threat detection alerts
- Access control violations
- System status updates

### SMS Alerts (Optional)
- Critical security events
- Emergency notifications
- System downtime alerts

## 🚀 Deployment

### Windows
```bash
# Build executable
pyinstaller main.spec

# Run from dist/main.exe
```

### Microsoft Store
- Package as MSIX using MSIX Packaging Tool
- Sign with appropriate certificates
- Submit to Microsoft Store

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for educational and security monitoring purposes. Users are responsible for complying with local laws and regulations regarding system monitoring and data collection.

## 🆘 Support

For issues, questions, or feature requests:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` folder
- Review the configuration examples

## 🔄 Updates

Stay updated with the latest features and security patches by:
- Following the GitHub repository
- Checking for new releases
- Reviewing the changelog

---

**USB HawkEye** - Your cyberpunk guardian for USB security! 🛡️ 