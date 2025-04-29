import click
import toml
import os
from pathlib import Path
import re
import shutil
import subprocess

# Configuration file path
CONFIG_DIR = Path.home() / ".config" / "silent-search"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# Allow overriding the config file path for testing
if "SILS_CONFIG" in os.environ:
    CONFIG_FILE = Path(os.environ["SILS_CONFIG"])

# Default configuration if file doesn't exist
DEFAULT_CONFIG = {
    "General": {
        "default_path": "~/dev/Resources",
        "default_recursive": True
    },
    "FileTypes": {
        "custom_types": {}  # Users can add their own file type definitions here
    }
}

# Built-in file extensions
FILE_TYPES = {
    "img": {".png", ".jpg", ".jpeg", ".bmp", ".gif"},
    "text": {".txt", ".md", ".markdown", ".rst", ".log", ".csv", ".json", ".xml", ".html", ".css", ".js", ".py", ".java", ".cpp", ".c", ".h", ".hpp", ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".sh", ".bat", ".ps1", ".yml", ".yaml", ".ini", ".conf", ".cfg", ".toml"},
    "md": {".md", ".markdown"},
    "audio": {".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma", ".aiff", ".alac", ".mid", ".midi"},
    "video": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg", ".3gp", ".h264", ".hevc", ".h265"},
    "code": {".py", ".java", ".cpp", ".c", ".h", ".hpp", ".cs", ".js", ".ts", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".m", ".sql", ".r", ".lua", ".pl", ".sh", ".ps1", ".vb", ".fs"}
}

def load_config():
    """Load configuration from TOML file or create default if missing."""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            toml.dump(DEFAULT_CONFIG, f)
        return DEFAULT_CONFIG
    return toml.load(CONFIG_FILE)

def get_extensions_for_type(config, type_filter):
    """Get file extensions for a given type, including custom types from config."""
    # Check custom types first
    custom_types = config.get("FileTypes", {}).get("custom_types", {})
    if type_filter in custom_types:
        return set(custom_types[type_filter])
    
    # Then check built-in types
    return FILE_TYPES.get(type_filter, {".*"})  # Default to all files if type not found

def search_files(path, name_pattern, type_filter, recursive, config):
    """Search for files matching name pattern and type."""
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise click.ClickException(f"Directory {path} does not exist")

    try:
        pattern = re.compile(name_pattern, re.IGNORECASE)
    except re.error:
        raise click.ClickException(f"Invalid pattern: {name_pattern}")

    matches = []
    glob_method = path.rglob if recursive else path.glob
    extensions = get_extensions_for_type(config, type_filter)

    for ext in extensions:
        for file in glob_method(f"*{ext}"):
            # Only match files that end with the exact extension
            if file.suffix.lower() == ext.lower() and pattern.search(file.name):
                matches.append(file.resolve())

    return sorted(matches)

def open_in_explorer(file_path):
    """Open the directory containing the file in the default file explorer."""
    directory = file_path.parent
    try:
        subprocess.run(["xdg-open", str(directory)], check=True)
    except subprocess.CalledProcessError:
        raise click.ClickException(f"Failed to open {directory} in file explorer")

@click.command()
@click.option("-t", "--type", "type_filter", default="img", show_default=True,
              help="File type to search (img, text, md, audio, video, code, all, or custom type)")
@click.option("-n", "--name", required=True, help="Name pattern (regex, e.g., 'concrete|metal|wood')")
@click.option("-p", "--path", default=None, help="Search directory (overrides config default)")
@click.option("-r", "--recursive/--no-recursive", default=None,
              help="Search recursively (overrides config default)")
@click.option("-c", "--copy-to", type=click.Path(), help="Copy selected files to directory (use '.' for current directory)")
@click.option("-o", "--open", "open_explorer", is_flag=True, help="Open selected file's directory in explorer")
def sils(type_filter, name, path, recursive, copy_to, open_explorer):
    """SilentSearch: Find files by name and type.

    Example: sils -t img -n "concrete|metal|wood" -c ~/game_project/assets
    """
    # Load configuration
    config = load_config()
    general = config.get("General", {})

    # Resolve path (use provided path or config default)
    search_path = path if path else general.get("default_path", "~/dev/Resources")
    # Resolve recursive (use provided flag, config default, or True)
    is_recursive = recursive if recursive is not None else general.get("default_recursive", True)

    # Check if type_filter is a custom type
    custom_types = config.get("FileTypes", {}).get("custom_types", {})
    if type_filter in custom_types:
        click.echo(f"Using custom file type '{type_filter}'")

    # Perform search
    try:
        results = search_files(search_path, name, type_filter, is_recursive, config)
    except click.ClickException as e:
        click.echo(f"Error: {e}", err=True)
        return

    if not results:
        click.echo("No files found matching the criteria.")
        return

    # Display results with indices
    click.echo("Found files:")
    for idx, file in enumerate(results, 1):
        click.echo(f"{idx}. {file}")

    # Interactive selection
    if copy_to or open_explorer:
        click.echo("\nEnter indices (e.g., '1,3-5,7') or 'all' to select files, or press Enter to skip:")
        selection = click.prompt("Selection", default="", show_default=False).strip()

        if not selection:
            return

        selected_indices = []
        if selection.lower() == "all":
            selected_indices = list(range(1, len(results) + 1))
        else:
            try:
                # Parse ranges like "1,3-5,7"
                for part in selection.split(","):
                    if "-" in part:
                        start, end = map(int, part.split("-"))
                        selected_indices.extend(range(start, end + 1))
                    else:
                        selected_indices.append(int(part))
            except ValueError:
                click.echo("Error: Invalid selection format.", err=True)
                return

        # Validate indices
        selected_indices = sorted(set(selected_indices))  # Remove duplicates
        if not all(1 <= idx <= len(results) for idx in selected_indices):
            click.echo("Error: Invalid indices.", err=True)
            return

        selected_files = [results[idx - 1] for idx in selected_indices]

        # Copy files if --copy-to is provided
        if copy_to:
            dest_dir = Path(copy_to).expanduser().resolve()
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # If only one file is selected, prompt for new name
            if len(selected_files) == 1:
                file = selected_files[0]
                default_name = file.name
                click.echo(f"\nEnter new name for {default_name} (or press Enter to keep original name):")
                new_name = click.prompt("New name", default=default_name, show_default=False).strip()
                
                if new_name and new_name != default_name:
                    # Ensure the new name has the same extension
                    if not Path(new_name).suffix and file.suffix:
                        new_name = f"{new_name}{file.suffix}"
                    dest_path = dest_dir / new_name
                else:
                    dest_path = dest_dir / default_name
                
                try:
                    shutil.copy2(file, dest_path)
                    click.echo(f"Copied {file.name} to {dest_path}")
                except (shutil.Error, OSError) as e:
                    click.echo(f"Error copying {file.name}: {e}", err=True)
            else:
                # Multiple files - copy with original names
                for file in selected_files:
                    try:
                        shutil.copy2(file, dest_dir)
                        click.echo(f"Copied {file.name} to {dest_dir}")
                    except (shutil.Error, OSError) as e:
                        click.echo(f"Error copying {file.name}: {e}", err=True)

        # Open explorer for selected files if --open is provided
        if open_explorer:
            # Open directory for the first selected file (or all, adjust as needed)
            for file in selected_files[:1]:  # Limit to first file for simplicity
                try:
                    open_in_explorer(file)
                    click.echo(f"Opened directory for {file.name}")
                except click.ClickException as e:
                    click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    sils()