import os
from bs4 import BeautifulSoup

def find_escaping_images():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    found_issues = False
    
    # Sort for consistent output
    html_files.sort()

    for file_name in html_files:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                # Use html.parser which is built-in
                soup = BeautifulSoup(content, 'html.parser')
            
            images = soup.find_all('img')
            for img in images:
                # Check if has class 'image'
                classes = img.get('class', [])
                if classes is None: classes = [] # Handle case where class attribute exists but is empty/None? bs4 usually gives list or None.
                has_image_class = 'image' in classes
                
                # Check if descendant of .image
                is_descendant = False
                for parent in img.parents:
                    if parent is None: break
                    if parent.name == '[document]': break 
                    
                    parent_classes = parent.get('class', [])
                    if parent_classes and 'image' in parent_classes:
                        is_descendant = True
                        break
                
                if not is_descendant:
                    found_issues = True
                    # sourceline might be None if parser didn't track it, generally works with html.parser
                    line = img.sourceline if img.sourceline else "?"
                    print(f"File: {file_name}, Line: {line}")
                    print(f"  Tag: {img}")
                    
                    if has_image_class:
                         print("  Info: Tag DOES have class 'image', but is not inside a container with class 'image'.")
                    else:
                         print("  Issue: Tag is NOT inside .image and does NOT have class 'image'.")
                    print("-" * 20)

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    if not found_issues:
        print("All images are covered")

if __name__ == "__main__":
    find_escaping_images()
