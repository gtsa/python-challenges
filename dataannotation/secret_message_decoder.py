import requests
from bs4 import BeautifulSoup


def fetch_doc_content(url):
    """Fetch content from the Google Doc URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an error for bad status codes
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching document: {e}")
        return None


def parse_table_from_doc(doc_content):
    """Parse the table from the Google Doc content."""
    soup = BeautifulSoup(doc_content, 'html.parser')
    table = soup.find('table')

    if not table:
        print("No table found in the document.")
        return {}

    grid = {}

    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')

        if len(cells) == 3:
            x = int(cells[0].get_text(strip=True))  # x-coordinate
            y = int(cells[2].get_text(strip=True))  # y-coordinate
            char = cells[1].get_text(strip=True)

            if x not in grid:
                grid[x] = {}
            grid[x][y] = char

    return grid


def print_grid(grid):
    """Print the grid of characters."""
    if not grid:
        print("No grid data available.")
        return

    max_x = max(grid.keys())
    max_y = max(y for x in grid.values() for y in x.keys())

    for y in range(max_y, -1, -1): # Start from max_y down to 0
        for x in range(max_x + 1):
            # Print the character at (x, y), or a space if it doesn't exist
            print(grid.get(x, {}).get(y, ' '), end='')
        print()  # Move to the next line after each row


def print_grid_from_doc(url):
    """Fetch, parse, and print grid from a Google Doc URL."""
    doc_content = fetch_doc_content(url)
    if doc_content:
        grid = parse_table_from_doc(doc_content)
        print_grid(grid)


# Example usage
url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
print_grid_from_doc(url)
