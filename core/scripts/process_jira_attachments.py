#!/usr/bin/env python3
"""
JIRA Attachment Processor for Autodev
Downloads, extracts, and organizes log files from JIRA attachments.
"""

import sys
import zipfile
import tarfile
import shutil
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Log file patterns for Android IVI debugging
LOG_PATTERNS = {
    'logcat': [
        r'.*logcat.*\.txt$',
        r'.*main\.log$',
        r'.*system\.log$',
        r'.*radio\.log$',
        r'.*events\.log$',
        r'.*crash\.log$'
    ],
    'tombstones': [
        r'.*tombstone.*',
        r'.*crash_dump.*',
        r'.*native_crash.*'
    ],
    'anr': [
        r'.*anr.*\.txt$',
        r'.*traces.*\.txt$',
        r'.*ANR.*'
    ],
    'system': [
        r'.*dmesg.*',
        r'.*kernel.*\.log$',
        r'.*bugreport.*\.txt$',
        r'.*dumpsys.*\.txt$'
    ]
}

class JiraAttachmentProcessor:
    def __init__(self, workspace_root: str, issue_key: str):
        """
        Initialize processor for a specific JIRA issue.
        
        Args:
            workspace_root: Path to Autodev/workspace/
            issue_key: JIRA issue key (e.g., PROJ-1234)
        """
        self.workspace_root = Path(workspace_root)
        self.issue_key = issue_key
        
        # Create issue-specific directories
        self.issue_dir = self.workspace_root / issue_key
        self.attachments_dir = self.issue_dir / 'attachments'
        self.extracted_dir = self.issue_dir / 'extracted'
        self.logs_dir = self.issue_dir / 'logs'
        
        # Create subdirectories for each log type
        for log_type in LOG_PATTERNS.keys():
            (self.logs_dir / log_type).mkdir(parents=True, exist_ok=True)
        
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_dir.mkdir(parents=True, exist_ok=True)
    
    def save_attachment(self, filename: str, content: bytes) -> Path:
        """Save raw attachment from JIRA."""
        filepath = self.attachments_dir / filename
        with open(filepath, 'wb') as f:
            f.write(content)
        print(f"✓ Saved: {filename}")
        return filepath
    
    def is_archive(self, filepath: Path) -> bool:
        """Check if file is a supported archive."""
        return filepath.suffix.lower() in ['.zip', '.tar', '.gz', '.tgz', '.bz2']
    
    def extract_archive(self, filepath: Path) -> List[Path]:
        """Extract archive file and return list of extracted files."""
        extracted_files = []
        extract_to = self.extracted_dir / filepath.stem
        extract_to.mkdir(parents=True, exist_ok=True)
        
        try:
            if filepath.suffix == '.zip':
                with zipfile.ZipFile(filepath, 'r') as zf:
                    zf.extractall(extract_to)
                    extracted_files = [extract_to / name for name in zf.namelist()]
                    print(f"✓ Extracted zip: {len(zf.namelist())} files from {filepath.name}")
            
            elif filepath.suffix in ['.tar', '.gz', '.tgz', '.bz2']:
                mode = 'r'
                if filepath.suffix == '.gz' or filepath.suffix == '.tgz':
                    mode = 'r:gz'
                elif filepath.suffix == '.bz2':
                    mode = 'r:bz2'
                
                with tarfile.open(filepath, mode) as tf:
                    tf.extractall(extract_to)
                    extracted_files = [extract_to / name for name in tf.getnames()]
                    print(f"✓ Extracted tar: {len(tf.getnames())} files from {filepath.name}")
        
        except Exception as e:
            print(f"✗ Failed to extract {filepath.name}: {e}", file=sys.stderr)
            return []
        
        return extracted_files
    
    def classify_log(self, filepath: Path) -> str:
        """Classify log file by type based on filename patterns."""
        filename = filepath.name.lower()
        
        for log_type, patterns in LOG_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, filename, re.IGNORECASE):
                    return log_type
        
        # Check file content for logcat-like patterns
        if filepath.is_file() and filepath.stat().st_size < 100_000_000:  # < 100MB
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    first_lines = f.read(2048)
                    if re.search(r'\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3}\s+\d+\s+\d+\s+[VDIWEF]', first_lines):
                        return 'logcat'
            except:
                pass
        
        return None
    
    def organize_logs(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Organize files into categorized log directories."""
        organized = {log_type: [] for log_type in LOG_PATTERNS.keys()}
        organized['other'] = []
        
        for filepath in files:
            if not filepath.is_file():
                continue
            
            log_type = self.classify_log(filepath)
            
            if log_type:
                # Copy to appropriate log directory
                dest = self.logs_dir / log_type / filepath.name
                shutil.copy2(filepath, dest)
                organized[log_type].append(dest)
                print(f"✓ Classified as {log_type}: {filepath.name}")
            else:
                organized['other'].append(filepath)
        
        return organized
    
    def process_attachments(self, attachment_files: List[Tuple[str, bytes]]) -> Dict[str, any]:
        """
        Main processing pipeline: save, extract, organize.
        
        Args:
            attachment_files: List of (filename, content) tuples from JIRA
        
        Returns:
            dict with organized log paths and summary
        """
        all_files = []
        
        # Step 1: Save all attachments
        for filename, content in attachment_files:
            filepath = self.save_attachment(filename, content)
            all_files.append(filepath)
        
        # Step 2: Extract archives
        extracted_files = []
        for filepath in all_files:
            if self.is_archive(filepath):
                extracted = self.extract_archive(filepath)
                extracted_files.extend(extracted)
            else:
                extracted_files.append(filepath)
        
        # Step 3: Organize all files (original + extracted)
        organized = self.organize_logs(extracted_files)
        
        # Summary
        summary = {
            'issue_key': self.issue_key,
            'attachments_saved': len(all_files),
            'files_extracted': len(extracted_files),
            'logs': {k: len(v) for k, v in organized.items() if v},
            'paths': {
                'attachments': str(self.attachments_dir),
                'extracted': str(self.extracted_dir),
                'logs': str(self.logs_dir)
            },
            'organized_files': organized
        }
        
        return summary
    
    def get_priority_logs(self) -> Dict[str, List[Path]]:
        """Return most relevant logs for analysis (logcat, tombstones, ANR)."""
        priority = {}
        for log_type in ['logcat', 'tombstones', 'anr']:
            log_dir = self.logs_dir / log_type
            if log_dir.exists():
                priority[log_type] = list(log_dir.glob('*'))
        return priority
    
    def cleanup(self):
        """Remove all workspace files for this issue."""
        if self.issue_dir.exists():
            shutil.rmtree(self.issue_dir)
            print(f"✓ Cleaned up workspace for {self.issue_key}")


def main():
    """
    CLI interface for standalone execution.
    Usage: python3 process_jira_attachments.py <workspace_root> <issue_key>
    """
    import argparse
    import glob
    
    parser = argparse.ArgumentParser(
        description='Process JIRA attachments for Autodev root cause analysis'
    )
    parser.add_argument(
        'workspace_root',
        help='Path to Autodev workspace directory (e.g., /home/user/Autodev/core/workspace)'
    )
    parser.add_argument(
        'issue_key',
        help='JIRA issue key (e.g., PROJ-1234)'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Remove all workspace files for this issue and exit'
    )
    
    args = parser.parse_args()
    
    processor = JiraAttachmentProcessor(
        workspace_root=args.workspace_root,
        issue_key=args.issue_key
    )
    
    if args.cleanup:
        processor.cleanup()
        return 0
    
    # Load all raw attachments from raw/ directory
    raw_dir = Path(args.workspace_root) / args.issue_key / 'raw'
    
    if not raw_dir.exists():
        print(f"✗ Raw directory not found: {raw_dir}", file=sys.stderr)
        print(f"  Did you download attachments first?", file=sys.stderr)
        return 1
    
    raw_files = []
    for filepath in sorted(raw_dir.glob('*')):
        if filepath.is_file():
            filename = filepath.name
            with open(filepath, 'rb') as f:
                content = f.read()
            raw_files.append((filename, content))
            print(f"✓ Loaded: {filename} ({len(content):,} bytes)")
    
    if not raw_files:
        print(f"✗ No files found in {raw_dir}", file=sys.stderr)
        return 1
    
    print(f"\nProcessing {len(raw_files)} attachment(s)...")
    print("=" * 70)
    
    # Process: extract archives, classify, organize logs
    summary = processor.process_attachments(raw_files)
    
    # Print summary
    print("\n" + "=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Attachments saved:  {summary['attachments_saved']}")
    print(f"Files extracted:    {summary['files_extracted']}")
    print(f"\nLogs organized:")
    for log_type, count in summary['logs'].items():
        if count > 0:
            print(f"  {log_type:14} : {count} file(s)")
    
    # Show priority log paths
    priority = processor.get_priority_logs()
    if priority:
        print(f"\n{'=' * 70}")
        print("PRIORITY LOGS FOR ANALYSIS")
        print("=" * 70)
        for category, paths in priority.items():
            if paths:
                print(f"\n{category.upper()}:")
                for p in paths:
                    size = p.stat().st_size if p.exists() else 0
                    print(f"  • {p.relative_to(processor.issue_dir)} ({size:,} bytes)")
    
    print(f"\n✓ Processing complete for {args.issue_key}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
