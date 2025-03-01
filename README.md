# Watchlist Randomizer

A simple GUI application that helps you randomly select something to watch from your watchlist based on various filters.

## Features

- Filter by Type of Media (Movie, TV Show, etc.)
- Filter by Medium (Animated, Live Action, etc.)
- Filter by Watched status
- Filter by Tags (multiple selection)
- Randomly select an item from your filtered watchlist

## Requirements

- Python 3.6+
- pandas
- numpy
- Tkinter (Python's GUI toolkit)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Tkinter (if not already installed):
   - **macOS** (using Homebrew):
     ```
     brew install python-tk@3.12  # Replace 3.12 with your Python version
     ```
   - **Ubuntu/Debian**:
     ```
     sudo apt-get install python3-tk
     ```
   - **Windows**:
     Tkinter is included with the standard Python installation on Windows.

## Usage

1. Ensure your watchlist is in CSV format and placed at `data/input/watchlist.csv`
2. The CSV file should have the following columns:
   - Name
   - Type of Media
   - Total Time Commitment
   - Medium
   - Watched?
   - Tags (comma-separated values)
3. Run the application:
   ```
   python src/main.py
   ```
4. Use the dropdown menus to filter your watchlist
5. Select one or more tags from the Tags list (hold Ctrl/Cmd to select multiple)
6. Click "Generate Random Selection" to get a random item from your filtered watchlist

## Example CSV Format

```
Name,Type of Media,Total Time Commitment,Medium,Watched?,Tags
Movie Title,Movie,1.75,Animated,TRUE,"Feel good, Whimsy, Romance"
TV Show Title,Short TV,6.5,Live Action,FALSE,"Sad, Action"
Another Show,Long TV,35,Live Action,TRUE,"Feel good, Action"
```

## Customization

You can customize your watchlist by adding more entries to the CSV file. Make sure to follow the same format as the example above.

## Troubleshooting

If you encounter an error about missing `_tkinter` module, it means Tkinter is not installed properly. Follow the installation instructions above to install Tkinter for your operating system. 


## Shoutout Cecilia
