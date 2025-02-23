import os
import shutil
from collections import defaultdict, Counter

# Define existing header categories and their respective subcategories
HEADER_CATEGORIES = {
    "Technology": ["AI", "Programming", "Web", "Cybersecurity", "Cloud Computing", "Data Science", "DevOps", "Blockchain", "IoT", "Game Development", "Mobile Development"],
    "Science": ["Mathematics", "Science", "Physics", "Biology", "Chemistry"],
    "Engineering": ["Mechatronics", "Robotics", "Control", "Embedded", "Electricity"],
    "Humanities": ["Philosophy", "History", "Fiction"],
}

# Define keywords for categorization
CATEGORIES = {
    "AI": {"ai", "artificial intelligence", "machine learning", "deep learning", "neural network"},
    "Programming": {"programming", "python", "java", "c++", "javascript", "coding"},
    "Mathematics": {"mathematics", "math", "calculus", "algebra", "statistics", "probability"},
    "Science": {"science", "physics", "chemistry", "biology", "renewable energy", "fuzzy"},
    "Philosophy": {"philosophy", "ethics", "logic"},
    "History": {"history", "historical"},
    "Fiction": {"fiction", "novel", "story"},
    "Mechatronics": {"mechatronics"},
    "Robotics": {"robotics", "robot", "mobile robots", "autonomous robots"},
    "Solar Panels": {"solar panel", "solar energy"},
    "Control": {"control system", "control engineering"},
    "Electricity": {"electricity", "electrical engineering"},
    "Web": {"web development", "html", "css", "javascript", "frontend", "backend"},
    "Cloud Computing": {"cloud computing", "aws", "azure", "google cloud"},
    "Cybersecurity": {"cybersecurity", "network security", "encryption", "hacking"},
    "Data Science": {"data science", "big data", "data visualization"},
    "DevOps": {"devops", "docker", "kubernetes"},
    "Blockchain": {"blockchain", "bitcoin", "ethereum", "cryptocurrency"},
    "IoT": {"iot", "internet of things", "smart devices"},
    "Game Development": {"game development", "unity", "unreal engine"},
    "Mobile Development": {"mobile development", "android", "ios", "flutter"},
}

def categorize_books(directory):
    categorized_books = defaultdict(list)
    uncategorized_books = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = file.lower()
            
            # Skip non-PDF files
            if not file_name.endswith(".pdf") or file.startswith("."):
                continue

            words = set(file_name.replace("_", " ").replace("-", " ").split())
            category_found = False
            
            for category, keywords in CATEGORIES.items():
                if words & keywords:
                    categorized_books[category].append(file_path)
                    category_found = True
                    break
            
            if not category_found:
                uncategorized_books.append(file_path)
    
    # Create new categories from uncategorized books if at least 2 books share a common word
    if uncategorized_books:
        word_counts = Counter()
        for file_path in uncategorized_books:
            file_name = os.path.basename(file_path).lower()
            words = set(file_name.replace("_", " ").replace("-", " ").split())
            word_counts.update(words)
        
        common_words = {word for word, count in word_counts.items() if count >= 2}
        new_categories = defaultdict(list)
        
        for file_path in uncategorized_books:
            file_name = os.path.basename(file_path).lower()
            words = set(file_name.replace("_", " ").replace("-", " ").split())
            common_category = words & common_words
            
            if common_category:
                category_name = " ".join(sorted(common_category))  # Create a meaningful category name
                new_categories[category_name].append(file_path)
            
        # Add new categories to main categorization
        for category, files in new_categories.items():
            categorized_books[category] = files
    
    return categorized_books

def determine_header_category(category):
    for header, subcategories in HEADER_CATEGORIES.items():
        if category in subcategories:
            return header
    return "Other"  # Create a new category if it doesn’t exist

def move_books(categorized_books, base_directory):
    for category, files in categorized_books.items():
        header_folder = determine_header_category(category)
        category_folder = os.path.join(base_directory, header_folder, category)
        os.makedirs(category_folder, exist_ok=True)

        for file_path in files:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(category_folder, file_name)

            # Handle duplicates
            counter = 1
            while os.path.exists(destination_path):
                name, ext = os.path.splitext(file_name)
                new_file_name = f"{name}_{counter}{ext}"
                destination_path = os.path.join(category_folder, new_file_name)
                counter += 1

            shutil.move(file_path, destination_path)
            print(f"Moved: {file_path} → {destination_path}")

def save_books_to_file(categorized_books, output_file):
    with open(output_file, "w") as f:
        for category, files in categorized_books.items():
            f.write(f"\n{category} ({len(files)} books):\n")
            for file in files:
                f.write(f"{file}\n")
    print(f"\nCategorized book list saved to {output_file}")

def main():
    books_directory = "/media/name/D2F4AB0EF4AAF3BF/mohamed"
    output_file = os.path.join(books_directory, "categorized_books.txt")

    categorized_books = categorize_books(books_directory)
    save_books_to_file(categorized_books, output_file)
    move_books(categorized_books, books_directory)

if __name__ == "__main__":
    main()
