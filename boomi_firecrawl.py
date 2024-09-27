import time
from firecrawl import FirecrawlApp
from urls import urls  # Import the array of URLs

app = FirecrawlApp(api_key="")

# Create a filename for the output
output_filename = "scraped_content.md"
batch_size = 20  # Set batch size for memory efficiency
all_content = []

# Open the output file once at the beginning
with open(output_filename, 'w', encoding='utf-8') as file:
    # Iterate through each URL in the array
    for index, url in enumerate(urls):
        print(f"Scraping: {url}")
        content = app.scrape_url(url, params={'formats': ['markdown'], 'onlyMainContent': True})

        # Store the markdown content along with the URL for reference
        all_content.append({
            'url': url,
            'markdown': content['markdown']
        })

        # Write to the file if the batch size is reached
        if (index + 1) % batch_size == 0:
            for entry in all_content:
                file.write(f"# {entry['url']}\n\n")
                file.write(f"{entry['markdown']}\n\n---\n\n")  # Separator between different URL contents
            
            # Clear the content variable after writing
            all_content.clear()
            print(f"Written {batch_size} entries to {output_filename}. Current batch cleared.")

            # Wait for 6 seconds to comply with the rate limit
            time.sleep(6)

    # Write any remaining content in all_content after the loop
    if all_content:
        for entry in all_content:
            file.write(f"# {entry['url']}\n\n")
            file.write(f"{entry['markdown']}\n\n---\n\n")

print(f"All content saved to {output_filename}")
