# SilentSearch (sils)

A powerful command-line tool for searching and managing files by name and type. Perfect for game developers, content creators, and anyone who needs to quickly find specific files across directories.

## Features

- Search for files by name using regex patterns
- Filter by file type (images, text, markdown, audio, video, code, or all files)
- Custom file type definitions in config
- Recursive directory searching
- Copy selected files to a destination directory
- Open file locations in your default file explorer
- Configurable default settings

## Installation

### Option 1: From GitHub Release (Recommended)

#### For Arch Linux users:
```bash
# Download the .pkg.tar.zst file from the latest release
# Install using pacman
sudo pacman -U silent-search-0.1.0-1-any.pkg.tar.zst
```

#### For other Linux users:
```bash
# Download the .tar.gz file from the latest release
# Extract it
tar xzf silent-search-0.1.0.tar.gz
cd silent-search-0.1.0
# Install using pip
pip install .
```

### Option 2: From Source

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/silent-search.git
   cd silent-search
   ```

2. Install the required dependencies:
   ```
   pip install click toml
   ```

3. Make the script executable:
   ```
   chmod +x sils.py
   ```

4. Create a symbolic link to make the command available system-wide:
   ```
   ln -s $(pwd)/sils.py /usr/local/bin/sils
   ```

## Configuration

SilentSearch creates a configuration file at `~/.config/silentsearch/config.toml` with default settings:

```toml
[General]
default_path = "~/dev/Resources"
default_recursive = true

[FileTypes]
custom_types = { }  # Add your custom file type definitions here
```

You can modify these settings to:
1. Change the default search path
2. Change recursive search behavior
3. Add custom file type definitions

### Custom File Types

You can define your own file types in the config file. For example:

```toml
[General]
default_path = "~/dev/Resources"
default_recursive = true

[FileTypes.custom_types]
web = [".html", ".css", ".js", ".php"]
docs = [".pdf", ".doc", ".docx", ".odt"]
scripts = [".py", ".sh", ".bash"]
```

Then use your custom types just like built-in types:
```bash
sils -t web -n "index"      # Search for web files
sils -t docs -n "report"    # Search for document files
sils -t scripts -n "backup" # Search for script files
```

The type parameter is flexible and accepts any string, so you can use any custom type you define in the config file without modifying the code.

## Usage

### Basic Search

Search for files by name pattern:

```
sils -n "pattern"
```

This will search for files containing "pattern" in their name, using the default settings from your config file.

### File Type Filtering

Search for specific file types:

```
sils -t img -n "texture"     # Search for image files
sils -t text -n "readme"     # Search for text files
sils -t md -n "documentation" # Search for markdown files
sils -t audio -n "music"     # Search for audio files
sils -t video -n "tutorial"  # Search for video files
sils -t code -n "main"       # Search for code files
sils -t all -n "pattern"     # Search all file types
```

### Advanced Options

Specify a custom search path:

```
sils -p ~/Projects -n "pattern"
```

Control recursive search:

```
sils -r -n "pattern"         # Search recursively (default)
sils --no-recursive -n "pattern" # Search only in the specified directory
```

### File Management

Copy selected files to a destination directory:

```
sils -n "pattern" -c ~/destination_folder
```

Open the directory containing a file in your default file explorer:

```
sils -n "pattern" -o
```

### Interactive Selection

When using the `-c` (copy) or `-o` (open) options, you'll be prompted to select files from the search results:

```
Found files:
1. /path/to/file1.png
2. /path/to/file2.jpg
3. /path/to/file3.png

Enter indices (e.g., '1,3-5,7') or 'all' to select files, or press Enter to skip:
```

You can select files by:
- Entering individual indices: `1,3,5`
- Using ranges: `1-3,5-7`
- Combining both: `1,3-5,7`
- Selecting all files: `all`

## Examples

Search for texture files containing "wood" or "metal":

```
sils -t img -n "wood|metal"
```

Find all markdown documentation files:

```
sils -t md -n "readme|documentation"
```

Search for audio files in a specific directory and copy them to another location:

```
sils -t audio -n "background" -p ~/Music -c ~/GameAssets/Audio
```

Find video tutorials and open their directories:

```
sils -t video -n "tutorial" -o
```

## Supported File Types

- **Images**: .png, .jpg, .jpeg, .bmp, .gif
- **Text**: .txt, .md, .markdown, .rst, .log, .csv, .json, .xml, .html, .css, .js, and many programming language files
- **Markdown**: .md, .markdown
- **Audio**: .mp3, .wav, .ogg, .flac, .aac, .m4a, .wma, .aiff, .alac, .mid, .midi
- **Video**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpeg, .mpg, .3gp, .h264, .hevc, .h265
- **Code**: .py, .java, .cpp, .c, .h, .hpp, .cs, .js, .ts, .php, .rb, .go, .rs, .swift, .kt, .scala, .m, .sql, .r, .lua, .pl, .sh, .ps1, .vb, .fs
- **Custom Types**: Define your own in the config file

## License

[MIT License](LICENSE) 