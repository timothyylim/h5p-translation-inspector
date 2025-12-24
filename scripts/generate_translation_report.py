import os
import sys
from datetime import datetime

# Assuming translation_checker.py is in the same directory
# Add the directory of the current script to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from translation_checker import check_translations_for_library

def generate_markdown_report(all_library_results, output_filepath="translation_report.md"):
    """
    Generates a Markdown report from the collected translation results.
    """
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(f"# H5P Translation Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary of French Coverage\n\n")
        f.write("| Library Name | Percentage French Coverage |\n")
        f.write("| :----------- | :------------------------- |\n")
        
        for result in all_library_results:
            if result['error']:
                f.write(f"| {result['library_name']} | Error: {result['error']} |\n")
            else:
                f.write(f"| {result['library_name']} | {result['coverage_percentage']:.2f}% |\n")
        f.write("\n")

        f.write("## Detailed Discrepancies\n\n")
        for result in all_library_results:
            if result['error']:
                f.write(f"### {result['library_name']}\n")
                f.write(f"Error: {result['error']}\n\n")
                continue

            if result['missing_translations'] or result['extra_translations'] or result['identical_strings']:
                f.write(f"### {result['library_name']} (Coverage: {result['coverage_percentage']:.2f}%)\n\n")
                
                f.write("#### Missing translations in French\n")
                if result['missing_translations']:
                    for item in result['missing_translations']:
                        f.write(f"- English key `{item['path']}` (value: '{item['en_value']}') is missing in French.\n")
                else:
                    f.write("- None found.\n")
                f.write("\n")

                f.write("#### Extra translations in French\n")
                if result['extra_translations']:
                    for item in result['extra_translations']:
                        f.write(f"- French key `{item['path']}` (value: '{item['fr_value']}') is not found in English semantics.\n")
                else:
                    f.write("- None found.\n")
                f.write("\n")

                f.write("#### Potential untranslated entries (English and French identical)\n")
                if result['identical_strings']:
                    for item in result['identical_strings']:
                        f.write(f"- Identical: `{item['path']}`: English='{item['en_value']}', French='{item['fr_value']}'\n")
                else:
                    f.write("- None found.\n")
                f.write("\n")
            else:
                f.write(f"### {result['library_name']} (Coverage: {result['coverage_percentage']:.2f}%)\n\n")
                f.write("No discrepancies found.\n\n")

    print(f"Report generated successfully: {output_filepath}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
    libraries_root = os.path.join(project_root, "libraries")

    all_library_results = []

    if not os.path.exists(libraries_root):
        print(f"Error: 'libraries' directory not found at {libraries_root}")
        return

    print(f"Scanning H5P libraries in {libraries_root}...")
    for item_name in os.listdir(libraries_root):
        library_path = os.path.join(libraries_root, item_name)
        if os.path.isdir(library_path):
            # Check if it looks like an H5P library directory
            # (e.g., contains semantics.json and a language subdirectory)
            if os.path.exists(os.path.join(library_path, "semantics.json")) and \
               os.path.exists(os.path.join(library_path, "language", "fr.json")):
                
                print(f"Processing library: {item_name}...")
                result = check_translations_for_library(library_path)
                all_library_results.append(result)
            else:
                print(f"Skipping '{item_name}': Not an H5P library or missing fr.json.")

    if all_library_results:
        generate_markdown_report(all_library_results)
    else:
        print("No H5P libraries with French translations found to report on.")

if __name__ == "__main__":
    main()
