# Roll20 Forum Backup
A Python script to back up Roll20 forum posts. It fetches forum posts and saves
them locally in Markdown format.
## Installation
It is recommended to set up a virtual environment to isolate dependencies for
this project.
### Step 1: Create a Virtual Environment
In your project directory, run the following command to create a virtual
environment using `venv`:
```bash
python3 -m venv .venv
```
### Step 2: Activate the Virtual Environment
- **For macOS/Linux:**
```bash
. .venv/bin/activate
```
- **For Windows:**
```bash
.\.venv\Scripts\activate
```
### Step 3: Install Dependencies
With the virtual environment activated, install the required dependencies from
the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
## Configuration
You need to configure the script using environment variables stored in a `.env`
file.
```ini
CAMPAIGN_ID=XXXXXXX
OUTPUT_FOLDER=<path_to_output_folder>
MIN_POST_ID=XXXXXXXX                    # Minimum post ID to download, optional
```
If `MIN_POST_ID` is omitted, the script downloads all forum posts.
## Usage
Run the script with the following command:
```bash
./roll20_forum_backup.py
```
or:
```bash
python3 roll20_forum_backup.py
```
