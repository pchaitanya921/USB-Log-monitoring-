import threading
import wmi
import time
import os

class USBMonitor:
    """
    Monitors USB device plug-in/out events in real time using WMI (Windows).
    Allows registration of callbacks for device events.
    """
    def __init__(self):
        self._running = False
        self._callbacks = []
        self._thread = None

    def start_monitoring(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()

    def stop_monitoring(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def register_callback(self, callback):
        """Register a callback to be called on device events. Callback signature: (event_type, device_info)"""
        self._callbacks.append(callback)

    def _monitor_loop(self):
        wmi_obj = wmi.WMI()
        watcher_insert = wmi_obj.Win32_DeviceChangeEvent.watch_for(notification_type="Creation")
        watcher_remove = wmi_obj.Win32_DeviceChangeEvent.watch_for(notification_type="Deletion")
        while self._running:
            try:
                inserted = watcher_insert(timeout_ms=500)
                if inserted:
                    for cb in self._callbacks:
                        cb('insert', self.get_connected_devices())
            except wmi.x_wmi_timed_out:
                pass
            try:
                removed = watcher_remove(timeout_ms=500)
                if removed:
                    for cb in self._callbacks:
                        cb('remove', self.get_connected_devices())
            except wmi.x_wmi_timed_out:
                pass
            time.sleep(0.1)

    def get_connected_devices(self):
        """Return a list of currently connected USB flash drives and external USB storage devices only."""
        devices = []
        wmi_obj = wmi.WMI()
        
        # Get only USB flash drives and external USB storage devices
        for disk in wmi_obj.Win32_DiskDrive():
            if 'USB' in disk.InterfaceType:
                # Only include actual USB flash drives and external storage
                if self._is_usb_flash_or_external(disk):
                    device_info = {
                        'DeviceID': disk.DeviceID,
                        'Product': disk.Model,
                        'Vendor': getattr(disk, 'Manufacturer', 'Unknown'),
                        'Serial': getattr(disk, 'SerialNumber', 'Unknown'),
                        'Size': self._format_size(disk.Size) if disk.Size else 'Unknown',
                        'Type': 'USB Storage',
                        'Path': self._get_drive_letter(disk.DeviceID)
                    }
                    devices.append(device_info)
        
        # Remove duplicates based on DeviceID
        unique_devices = []
        seen_ids = set()
        for device in devices:
            if device['DeviceID'] not in seen_ids:
                unique_devices.append(device)
                seen_ids.add(device['DeviceID'])
        
        return unique_devices
    
    def _format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if not size_bytes:
            return 'Unknown'
        try:
            size_bytes = int(size_bytes)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} PB"
        except:
            return 'Unknown'
    
    def _is_usb_flash_or_external(self, disk):
        """Check if a disk device is a USB flash drive or external USB storage"""
        try:
            device_name = disk.Model.lower() if disk.Model else ''
            
            # USB Flash Drive indicators
            flash_keywords = ['flash', 'usb', 'memory stick', 'thumb drive', 'pen drive', 'traveler', 'datatraveler']
            if any(keyword in device_name for keyword in flash_keywords):
                return True
            
            # External USB storage indicators
            external_keywords = ['external', 'portable', 'removable']
            if any(keyword in device_name for keyword in external_keywords):
                return True
            
            # Check media type for flash indicators
            if hasattr(disk, 'MediaType') and disk.MediaType:
                media_type = disk.MediaType.lower()
                flash_media = ['removable', 'flash', 'usb', 'portable']
                if any(indicator in media_type for indicator in flash_media):
                    return True
            
            # Exclude internal drives
            internal_indicators = ['ssd', 'hard disk', 'internal', 'nvme', 'sata', 'hdd']
            if any(indicator in device_name for indicator in internal_indicators):
                return False
            
            # For USB devices, be more restrictive - only include if clearly external
            # Most USB devices that are not clearly internal should be included
            return True
        except:
            return False  # Default to False if we can't determine
    

    
    def _get_drive_letter(self, device_id):
        """Try to get drive letter for USB storage device"""
        try:
            # Get logical disk information to map device IDs to drive letters
            wmi_obj = wmi.WMI()
            for logical_disk in wmi_obj.Win32_LogicalDisk():
                if logical_disk.DriveType == 2:  # Removable drive (USB)
                    drive_path = f"{logical_disk.DeviceID}\\"
                    if os.path.exists(drive_path):
                        return drive_path
            return 'Unknown'
        except:
            return 'Unknown'
