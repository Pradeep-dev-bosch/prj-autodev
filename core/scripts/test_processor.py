#!/usr/bin/env python3
"""
Test script for JIRA Attachment Processor
Creates sample attachments and demonstrates the extraction/organization workflow.
"""

import sys
import zipfile
from pathlib import Path

# Add parent directory to path to import the processor
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.process_jira_attachments import JiraAttachmentProcessor


def create_sample_zip_with_logs() -> bytes:
    """Create a sample zip file containing multiple log files."""
    import io
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add logcat
        logcat_content = """03-25 14:32:15.123  1234  5678 E AndroidRuntime: FATAL EXCEPTION: main
03-25 14:32:15.124  1234  5678 E AndroidRuntime: Process: com.example.app, PID: 1234
03-25 14:32:15.125  1234  5678 E AndroidRuntime: java.lang.NullPointerException: Attempt to invoke virtual method
03-25 14:32:15.126  1234  5678 E AndroidRuntime:     at com.example.app.MainActivity.onCreate(MainActivity.java:42)
"""
        zipf.writestr('logcat.txt', logcat_content)
        
        # Add tombstone
        tombstone_content = """*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'Android/aosp_car/aosp_car:14/UP1A.231005.007/eng:userdebug/dev-keys'
Revision: '0'
ABI: 'arm64'
Timestamp: 2026-03-25 14:30:00.123456789+0000
Process uptime: 5s
Cmdline: /system/bin/vehicle_hal_service
pid: 9876, tid: 9877, name: VehicleHalThre  >>> /system/bin/vehicle_hal_service <<<
uid: 1000
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000000000000000
"""
        zipf.writestr('tombstone_01', tombstone_content)
        
        # Add ANR trace
        anr_content = """ANR in com.example.app (com.example.app/.MainActivity)
PID: 1234
Reason: Input dispatching timed out (Waiting to send key event because the focused window has not finished processing all of the input events that were previously delivered to it)
Load: 1.2 / 1.5 / 1.3
CPU usage from 5000ms to 0ms ago:

"main" prio=5 tid=1 Native
  | group="main" sCount=1 dsCount=0 flags=1 obj=0x71234567 self=0x71234567
  | sysTid=1234 nice=-10 cgrp=default sched=0/0 handle=0x71234567
  | state=S schedstat=( 123456789 98765432 567 ) utm=12 stm=3 core=1 HZ=100
  at android.os.BinderProxy.transactNative(Native method)
"""
        zipf.writestr('traces.txt', anr_content)
        
        # Add system log
        dmesg_content = """[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
[    0.000000] Linux version 5.10.0-android-common (builder@build-host)
[    5.123456] init: Service 'vehicle_hal_service' (pid 9876) exited with status 139
[    5.234567] init: Service 'vehicle_hal_service' (pid 9876) killed by signal 11
"""
        zipf.writestr('dmesg.log', dmesg_content)
    
    zip_buffer.seek(0)
    return zip_buffer.read()


def run_test():
    """Run the test with sample data."""
    print("=" * 70)
    print("Autodev Attachment Processor - Test Mode")
    print("=" * 70)
    print()
    
    # Get workspace path
    workspace_root = Path(__file__).parent.parent / 'workspace'
    issue_key = 'TEST-123'
    
    print(f"Workspace: {workspace_root}")
    print(f"Issue Key: {issue_key}")
    print()
    
    # Initialize processor
    processor = JiraAttachmentProcessor(str(workspace_root), issue_key)
    
    # Create sample attachments
    print("Creating sample attachments...")
    attachments = [
        ('logcat_main.txt', b"03-25 14:30:00.000  1000  2000 I System: Test log\n"),
        ('logs.zip', create_sample_zip_with_logs()),
        ('screenshot.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00'),
    ]
    
    print(f"  - {len(attachments)} attachments prepared")
    print()
    
    # Process attachments
    print("Processing attachments...")
    print("-" * 70)
    summary = processor.process_attachments(attachments)
    print("-" * 70)
    print()
    
    # Display summary
    print("Processing Summary:")
    print(f"  Attachments saved: {summary['attachments_saved']}")
    print(f"  Files extracted:   {summary['files_extracted']}")
    print()
    
    print("Logs organized:")
    for log_type, count in summary['logs'].items():
        print(f"  {log_type:12} : {count} file(s)")
    print()
    
    # Get priority logs
    priority = processor.get_priority_logs()
    print("Priority logs for RCA:")
    for log_type, files in priority.items():
        if files:
            print(f"  {log_type:12} : {len(files)} file(s)")
            for f in files:
                print(f"    - {f.name}")
    print()
    
    # Display paths
    print("Workspace structure created at:")
    print(f"  {processor.issue_dir}")
    print()
    print("To view files:")
    print(f"  ls -la {processor.attachments_dir}")
    print(f"  ls -la {processor.extracted_dir}")
    print(f"  ls -la {processor.logs_dir}")
    print()
    
    # Cleanup option
    print("To cleanup test data:")
    print(f"  python3 -c \"from scripts.process_jira_attachments import JiraAttachmentProcessor; JiraAttachmentProcessor('{workspace_root}', '{issue_key}').cleanup()\"")
    print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(run_test())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
