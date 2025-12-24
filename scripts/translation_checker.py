import json
import os

def load_json_file(filepath):
    """Loads a JSON file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def extract_translatable_strings(data, path=""):
    """
    Recursively extracts string values from 'label', 'description', and 'default' keys
    and their full paths from a JSON object.
    Returns a dictionary where keys are canonical paths and values are strings.
    """
    strings = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if key in ["label", "description", "default"] and isinstance(value, str):
                strings[new_path] = value
            elif isinstance(value, (dict, list)):
                strings.update(extract_translatable_strings(value, new_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            # Always use index for list items to ensure consistent path generation
            item_identifier = f"[{i}]"
            new_path = f"{path}{item_identifier}"
            strings.update(extract_translatable_strings(item, new_path))
    return strings

def check_translations_for_library(library_path):
    """
    Checks translation discrepancies for a single H5P library.
    Returns a dictionary of results including coverage and discrepancies.
    """
    library_name = os.path.basename(library_path)
    semantics_filepath = os.path.join(library_path, "semantics.json")
    fr_filepath = os.path.join(library_path, "language", "fr.json")

    en_data_raw = load_json_file(semantics_filepath)
    fr_data_raw = load_json_file(fr_filepath)

    results = {
        'library_name': library_name,
        'coverage_percentage': 0,
        'missing_translations': [],
        'extra_translations': [],
        'identical_strings': [],
        'error': None
    }

    if en_data_raw is None:
        results['error'] = f"semantics.json not found or invalid for {library_name}"
        return results
    if fr_data_raw is None:
        results['error'] = f"fr.json not found or invalid for {library_name}"
        return results

    en_wrapped_data = {"semantics": en_data_raw}
    fr_semantics_list = fr_data_raw.get('semantics')

    if not isinstance(en_data_raw, list):
        results['error'] = f"semantics.json root is not a list for {library_name}"
        return results
    if not isinstance(fr_semantics_list, list):
        results['error'] = f"'semantics' key in fr.json is not a list or is missing for {library_name}"
        return results

    en_strings = extract_translatable_strings(en_wrapped_data)
    fr_strings = extract_translatable_strings({"semantics": fr_semantics_list})

    total_en_strings = len(en_strings)
    covered_strings = 0

    for path, en_str in en_strings.items():
        if path not in fr_strings:
            results['missing_translations'].append({'path': path, 'en_value': en_str})
        else:
            covered_strings += 1
            fr_str = fr_strings[path]
            if en_str == fr_str and en_str.strip() != "":
                results['identical_strings'].append({'path': path, 'en_value': en_str, 'fr_value': fr_str})

    for path, fr_str in fr_strings.items():
        if path not in en_strings:
            results['extra_translations'].append({'path': path, 'fr_value': fr_str})

    if total_en_strings > 0:
        results['coverage_percentage'] = (covered_strings / total_en_strings) * 100

    return results

if __name__ == "__main__":
    # This block will still allow direct execution for testing a single library
    # For general use, the new script will import and call check_translations_for_library
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
    
    # Assuming the current working directory is the project root when called directly
    # Adjust this path for testing specific libraries if needed
    test_library_path = os.path.join(project_root, "libraries", "H5P.Video-1.5")
    
    print(f"Checking translations for {os.path.basename(test_library_path)}...")
    result = check_translations_for_library(test_library_path)

    if result['error']:
        print(f"Error checking {result['library_name']}: {result['error']}")
    else:
        print(f"\n--- Results for {result['library_name']} ---")
        print(f"French Coverage: {result['coverage_percentage']:.2f}%")
        
        print("\n--- Missing translations in French ---")
        if result['missing_translations']:
            for item in result['missing_translations']:
                print(f"  - English key '{item['path']}' (value: '{item['en_value']}') is missing in French.")
        else:
            print("  None found.")
        
        print("\n--- Extra translations in French ---")
        if result['extra_translations']:
            for item in result['extra_translations']:
                print(f"  - French key '{item['path']}' (value: '{item['fr_value']}') is not found in English semantics.")
        else:
            print("  None found.")
            
        print("\n--- Potential untranslated entries (English and French identical) ---")
        if result['identical_strings']:
            for item in result['identical_strings']:
                print(f"  - Identical: '{item['path']}': English='{item['en_value']}', French='{item['fr_value']}'")
        else:
            print("  None found.")

    print("\nNote: Identical strings might indicate a missing translation or it could be a common term/placeholder (e.g., 'Video', numbers, URLs, HTML tags).")
