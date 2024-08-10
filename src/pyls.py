import json
import argparse
from datetime import datetime
import os

def format_time(epoch_time):
    return datetime.fromtimestamp(epoch_time).strftime('%b %d %H:%M')

def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T', 'P']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}P"

def find_item_by_path(directory, path_parts):
    if not path_parts:
        return directory

    for item in directory.get('contents', []):
        if item['name'] == path_parts[0]:
            if len(path_parts) == 1:
                return item
            if 'contents' in item:
                return find_item_by_path(item, path_parts[1:])
            else:
                return None
    return None

def pyls(directory, path=None, show_all=False, long_format=False, reverse=False, sort_by_time=False, filter_type=None, human_readable=False):
    # Resolve the path
    if path:
        path_parts = path.strip('./').split('/')
        target = find_item_by_path(directory, path_parts)
        if target is None:
            print(f"error: cannot access '{path}': No such file or directory")
            return
    else:
        target = directory

    # If target is a file, just print it
    if 'contents' not in target:
        if long_format:
            permissions = target['permissions']
            size = human_readable_size(target['size']) if human_readable else target['size']
            time_modified = format_time(target['time_modified'])
            name = os.path.join('.', path) if path else target['name']
            print(f"{permissions} {size:>5} {time_modified} {name}")
        else:
            print(target['name'])
        return
    
    # Filter and sort items based on arguments
    items = target['contents']
    
    if filter_type == 'file':
        items = [item for item in items if 'contents' not in item]
    elif filter_type == 'dir':
        items = [item for item in items if 'contents' in item]
    
    if sort_by_time:
        items = sorted(items, key=lambda x: x['time_modified'], reverse=reverse)
    else:
        items = sorted(items, key=lambda x: x['name'], reverse=reverse)
    
    # Print the contents
    for item in items:
        if not show_all and item['name'].startswith('.'):
            continue
        
        if long_format:
            permissions = item['permissions']
            size = human_readable_size(item['size']) if human_readable else item['size']
            time_modified = format_time(item['time_modified'])
            name = item['name']
            print(f"{permissions} {size:>5} {time_modified} {name}")
        else:
            print(item['name'], end=' ')
    
    if not long_format:
        print()  # To end the line after listing all items

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(
        description="pyls: A Python implementation of the ls command for navigating JSON-based directory structures.",
        usage="python -m pyls [options] [path]",
        epilog="For more information, visit the documentation."
    )
    parser.add_argument('-A', action='store_true', help="Include hidden files")
    parser.add_argument('-l', action='store_true', help="Use a long listing format")
    parser.add_argument('-r', action='store_true', help="Reverse order while sorting")
    parser.add_argument('-t', action='store_true', help="Sort by time modified (oldest first)")
    parser.add_argument('--filter', type=str, choices=['file', 'dir'], help="Filter output by type (file or dir)")
    parser.add_argument('-H', '--human-readable', action='store_true', help="Show human-readable sizes")
    parser.add_argument('path', nargs='?', default='.', help="Path to directory or file")
    
    args = parser.parse_args()
    
    # Load JSON file containing the directory structure
    json_file_path = 'structure.json'
    
    with open(json_file_path, 'r') as file:
        directory_structure = json.load(file)
    
    # Execute the pyls command with provided arguments
    pyls(
        directory_structure, 
        path=args.path,
        show_all=args.A, 
        long_format=args.l, 
        reverse=args.r, 
        sort_by_time=args.t, 
        filter_type=args.filter,
        human_readable=args.human_readable
    )

if __name__ == '__main__':
    main()
