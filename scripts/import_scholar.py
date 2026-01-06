import os
import re
from datetime import datetime
import time

try:
    from scholarly import scholarly
except ImportError:
    print("Please install the scholarly library first: pip install scholarly")
    exit(1)

# Configuration
AUTHOR_ID = 'TXjlCH4AAAAJ'  # Ganapathy Krishnamurthi
# Determine the project root relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'src', 'content', 'publications')
# LAB_AUTHORS structure: name in scholar -> id in website
# You should update this mapping with your team members
LAB_AUTHORS_MAP = {
    'G Krishnamurthi': 'ganapathy-krishnamurthi',
    'Ganapathy Krishnamurthi': 'ganapathy-krishnamurthi',
    # Add other students/faculty here
}

def clean_filename(title):
    # Convert title to a valid filename: lowercase, remove special chars, dash separated
    clean = re.sub(r'[^\w\s-]', '', title.lower())
    clean = re.sub(r'[-\s]+', '-', clean).strip('-')
    return clean

def guess_type(venue):
    if not venue:
        return 'journal' # Default
    venue_lower = venue.lower()
    if 'conference' in venue_lower or 'proc' in venue_lower or 'symposium' in venue_lower or 'workshop' in venue_lower or 'miccai' in venue_lower or 'isbi' in venue_lower or 'icassp' in venue_lower:
        return 'conference'
    elif 'arxiv' in venue_lower or 'rxiv' in venue_lower:
        return 'preprint'
    elif 'thesis' in venue_lower:
        return 'thesis'
    elif 'book' in venue_lower or 'chapter' in venue_lower:
        return 'book-chapter'
    else:
        return 'journal'

def format_authors(author_str):
    if not author_str:
        return []
    # Split by ' and ' or ', '
    parts = re.split(r', | and ', author_str)
    return [p.strip() for p in parts if p.strip()]

def get_lab_authors(author_list):
    lab_authors = []
    for auth in author_list:
        # Simple fuzzy matching or direct lookup
        for scholar_name, internal_id in LAB_AUTHORS_MAP.items():
            if scholar_name.lower() in auth.lower():
                if internal_id not in lab_authors:
                    lab_authors.append(internal_id)
    return lab_authors

def get_existing_publications():
    existing_ids = set()
    if not os.path.exists(OUTPUT_DIR):
        return existing_ids
        
    for filename in os.listdir(OUTPUT_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for scholarId in frontmatter
                match = re.search(r'scholarId:\s*["\']?([^"\']+)["\']?', content)
                if match:
                    existing_ids.add(match.group(1).strip())
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return existing_ids

def create_markdown(pub, existing_ids):
    pub_id = pub.get('author_pub_id')
    if pub_id and pub_id in existing_ids:
        print(f"Skipping existing (by ID): {pub['bib'].get('title')[:30]}...")
        return

    bib = pub['bib']
    title = bib.get('title', 'Untitled')
    pub_year = bib.get('pub_year')
    if not pub_year:
        # Try to guess or default
        pub_year = datetime.now().year 
    
    clean_title = clean_filename(title)
    filename = f"{pub_year}-{clean_title}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"Skipping existing (by filename): {filename}")
        return

    citation = bib.get('citation', '')
    venue = bib.get('journal') or bib.get('conference') or bib.get('eprint') or "Unknown Venue"
    
    # authors in scholar is sometimes a list or string depending on 'fill' level
    authors_list = pub['bib'].get('author', '').split(' and ') # Basic split for BibTeX standard
    if isinstance(authors_list, str):
         authors_list = [authors_list]
         
    # Clean up authors
    authors_list = [a.strip() for a in authors_list]
    
    lab_authors = get_lab_authors(authors_list)
    pub_type = guess_type(venue)
    
    # Construct frontmatter
    content = "---\n"
    content += f'title: "{title.replace('"', '\\"')}"\n'
    if pub_id:
        content += f'scholarId: "{pub_id}"\n'
    
    content += "authors:\n"
    for auth in authors_list:
        content += f'  - {auth}\n'
        
    content += f'venue: "{venue}"\n'
    # content += f'venueShort: "{venue}"\n' # Optional, hard to guess
    
    content += f'year: {pub_year}\n'
    
    # Optional fields
    if 'pages' in bib:
        content += f'pages: "{bib["pages"]}"\n'
    if 'volume' in bib:
        content += f'volume: "{bib["volume"]}"\n'
    
    content += f'type: {pub_type}\n'
    
    # Add default topic if none (Schema requires topics array)
    content += "topics:\n  - Medical Imaging\n"
    
    if lab_authors:
        content += "labAuthors:\n"
        for la in lab_authors:
            content += f'  - {la}\n'
            
    content += "---\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Created: {filename}")
    # Add to set to prevent duplicate in same run if any
    if pub_id:
        existing_ids.add(pub_id)

def main():
    print(f"Fetching publications for Author ID: {AUTHOR_ID}")
    print("Note: This process sends requests to Google Scholar and may be rate-limited.")
    
    # Create directory if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    existing_ids = get_existing_publications()
    print(f"Found {len(existing_ids)} existing publications with scholar IDs.")

    search_query = scholarly.search_author_id(AUTHOR_ID)
    author = scholarly.fill(search_query)
    
    print(f"Found author: {author.get('name')}")
    pubs = author.get('publications', [])
    print(f"Found {len(pubs)} publications. Processing...")
    
    for i, pub in enumerate(pubs):
        try:
            # Check ID before filling to save requests
            if pub.get('author_pub_id') in existing_ids:
                # print(f"Skipping known ID: {pub.get('author_pub_id')}")
                continue

            # We need to fill the publication to get bibtex details
            # This causes a request per publication. 
            # To be safe against rate limits, we might want to sleep.
            filled_pub = scholarly.fill(pub)
            create_markdown(filled_pub, existing_ids)
            
            # Sleep to be nice to Google's servers
            time.sleep(2) 
            
            if (i+1) % 10 == 0:
                print(f"Processed {i+1}/{len(pubs)}")
                
        except Exception as e:
            print(f"Error processing publication {i}: {e}")
            continue

if __name__ == "__main__":
    main()
