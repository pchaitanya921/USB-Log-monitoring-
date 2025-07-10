import os
import subprocess
import json
from datetime import datetime

class AccessControl:
    """
    Enhanced USB device access control system with:
    - Threat-based automatic blocking
    - Read-only mode for new/unknown devices
    - Manual access control by users
    - Device status tracking and history
    """
    def __init__(self):
        self.permissions = {}  # device_id -> permission ('read-only', 'block', 'full')
        self.whitelist = set()
        self.blacklist = set()
        self.device_history = {}  # device_id -> history of access changes
        self.threat_devices = set()  # devices with detected threats
        self.new_devices = set()  # newly connected devices
        self.clean_devices = set()  # devices that passed security scan
        self.config_file = 'access_control_config.json'
        self.load_config()

    def load_config(self):
        """Load access control configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.permissions = data.get('permissions', {})
                    self.whitelist = set(data.get('whitelist', []))
                    self.blacklist = set(data.get('blacklist', []))
                    self.threat_devices = set(data.get('threat_devices', []))
                    self.clean_devices = set(data.get('clean_devices', []))
                    self.device_history = data.get('device_history', {})
        except Exception as e:
            print(f"Error loading access control config: {e}")

    def save_config(self):
        """Save access control configuration to file."""
        try:
            data = {
                'permissions': self.permissions,
                'whitelist': list(self.whitelist),
                'blacklist': list(self.blacklist),
                'threat_devices': list(self.threat_devices),
                'clean_devices': list(self.clean_devices),
                'device_history': self.device_history,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving access control config: {e}")

    def set_permission(self, device_id, permission):
        """Set access permission for a device (read-only, block, full)."""
        old_permission = self.permissions.get(device_id, 'read-only')
        self.permissions[device_id] = permission
        
        # Log the permission change
        self.log_device_change(device_id, f"Permission changed from {old_permission} to {permission}")
        
        # Apply the permission at system level
        self.apply_permission(device_id, permission)
        
        # Save configuration
        self.save_config()

    def get_permission(self, device_id):
        """Get current permission for a device."""
        # Check if device is blacklisted
        if device_id in self.blacklist:
            return 'block'
        
        # Check if device has threats
        if device_id in self.threat_devices:
            return 'block'
        
        # Check if device is whitelisted
        if device_id in self.whitelist:
            return self.permissions.get(device_id, 'full')
        
        # Check if device is clean and has been scanned
        if device_id in self.clean_devices:
            return self.permissions.get(device_id, 'full')
        
        # Default to read-only for new/unknown devices
        return self.permissions.get(device_id, 'read-only')

    def is_whitelisted(self, device_id):
        """Check if a device is whitelisted."""
        return device_id in self.whitelist

    def is_blacklisted(self, device_id):
        """Check if a device is blacklisted."""
        return device_id in self.blacklist

    def add_to_whitelist(self, device_id):
        """Add device to whitelist and grant full access."""
        self.whitelist.add(device_id)
        self.blacklist.discard(device_id)
        self.threat_devices.discard(device_id)
        self.set_permission(device_id, 'full')
        self.log_device_change(device_id, "Added to whitelist")
        self.save_config()

    def add_to_blacklist(self, device_id):
        """Add device to blacklist and block access."""
        self.blacklist.add(device_id)
        self.whitelist.discard(device_id)
        self.set_permission(device_id, 'block')
        self.log_device_change(device_id, "Added to blacklist")
        self.save_config()

    def mark_device_threat(self, device_id):
        """Mark device as having threats and block it."""
        self.threat_devices.add(device_id)
        self.set_permission(device_id, 'block')
        self.log_device_change(device_id, "Marked as threat - blocked")
        self.save_config()

    def mark_device_clean(self, device_id):
        """Mark device as clean after security scan."""
        self.clean_devices.add(device_id)
        self.threat_devices.discard(device_id)
        # Keep current permission or set to read-only if new
        if device_id not in self.permissions:
            self.set_permission(device_id, 'read-only')
        self.log_device_change(device_id, "Marked as clean")
        self.save_config()

    def add_new_device(self, device_id):
        """Add newly connected device with read-only access."""
        self.new_devices.add(device_id)
        self.set_permission(device_id, 'read-only')
        self.log_device_change(device_id, "New device connected - read-only access")
        self.save_config()

    def log_device_change(self, device_id, change_description):
        """Log changes to device access permissions."""
        if device_id not in self.device_history:
            self.device_history[device_id] = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'change': change_description,
            'permission': self.permissions.get(device_id, 'read-only')
        }
        self.device_history[device_id].append(log_entry)

    def apply_permission(self, device_id, permission):
        """Apply permission at system level using Windows commands."""
        try:
            if permission == 'block':
                # Block device access
                self.block_device_access(device_id)
            elif permission == 'read-only':
                # Set read-only access
                self.set_readonly_access(device_id)
            elif permission == 'full':
                # Grant full access
                self.set_full_access(device_id)
        except Exception as e:
            print(f"Error applying permission {permission} to {device_id}: {e}")

    def block_device_access(self, device_id):
        """Block device access using Windows commands."""
        try:
            # Use diskpart to set device offline
            diskpart_script = f"""
select disk {self.get_disk_number(device_id)}
offline disk
exit
"""
            with open('temp_diskpart.txt', 'w') as f:
                f.write(diskpart_script)
            
            subprocess.run(['diskpart', '/s', 'temp_diskpart.txt'], 
                         capture_output=True, text=True)
            
            if os.path.exists('temp_diskpart.txt'):
                os.remove('temp_diskpart.txt')
        except Exception as e:
            print(f"Error blocking device {device_id}: {e}")

    def set_readonly_access(self, device_id):
        """Set read-only access for device."""
        try:
            # Use diskpart to set read-only
            diskpart_script = f"""
select disk {self.get_disk_number(device_id)}
attributes disk set readonly
exit
"""
            with open('temp_diskpart.txt', 'w') as f:
                f.write(diskpart_script)
            
            subprocess.run(['diskpart', '/s', 'temp_diskpart.txt'], 
                         capture_output=True, text=True)
            
            if os.path.exists('temp_diskpart.txt'):
                os.remove('temp_diskpart.txt')
        except Exception as e:
            print(f"Error setting read-only for {device_id}: {e}")

    def set_full_access(self, device_id):
        """Set full access for device."""
        try:
            # Use diskpart to remove read-only and online disk
            diskpart_script = f"""
select disk {self.get_disk_number(device_id)}
attributes disk clear readonly
online disk
exit
"""
            with open('temp_diskpart.txt', 'w') as f:
                f.write(diskpart_script)
            
            subprocess.run(['diskpart', '/s', 'temp_diskpart.txt'], 
                         capture_output=True, text=True)
            
            if os.path.exists('temp_diskpart.txt'):
                os.remove('temp_diskpart.txt')
        except Exception as e:
            print(f"Error setting full access for {device_id}: {e}")

    def get_disk_number(self, device_id):
        """Get disk number from device ID."""
        try:
            # Extract disk number from device path
            # This is a simplified approach - in real implementation,
            # you'd need to map device IDs to disk numbers
            if '\\\\.\\PhysicalDrive' in device_id:
                return device_id.split('PhysicalDrive')[-1]
            return '0'  # Default fallback
        except:
            return '0'

    def get_device_status(self, device_id):
        """Get comprehensive device status."""
        return {
            'permission': self.get_permission(device_id),
            'is_whitelisted': device_id in self.whitelist,
            'is_blacklisted': device_id in self.blacklist,
            'has_threats': device_id in self.threat_devices,
            'is_clean': device_id in self.clean_devices,
            'is_new': device_id in self.new_devices,
            'history': self.device_history.get(device_id, [])
        }

    def get_all_devices_status(self):
        """Get status of all known devices."""
        all_devices = set(self.permissions.keys()) | self.whitelist | self.blacklist | self.threat_devices | self.clean_devices | self.new_devices
        return {device_id: self.get_device_status(device_id) for device_id in all_devices}
