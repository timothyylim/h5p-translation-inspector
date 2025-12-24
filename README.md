# H5P Translation Inspector

This project provides tools for inspecting the translation status of H5P libraries, specifically focusing on French language coverage.

## Overview

The core functionality is provided by two Python scripts located in `h5p-node.backend.eclasse/scripts/`:

1.  `generate_translation_report.py`: This script orchestrates the translation checking process across multiple H5P libraries and generates a comprehensive Markdown report.
2.  `translation_checker.py`: This module contains the detailed logic for comparing English semantics (from `semantics.json`) with French translations (from `fr.json`) for a single H5P library.

## How it Works

### `translation_checker.py`

This script (or module when imported) performs the following checks for a given H5P library:

*   **Loads Data**: It loads `semantics.json` (English structure and default strings) and `language/fr.json` (French translations).
*   **Extracts Translatable Strings**: It recursively goes through the `semantics.json` structure to identify all strings marked as translatable (e.g., `label`, `description`, `default` fields).
*   **Compares Translations**: It then compares these extracted English strings with their corresponding entries in `fr.json`.
*   **Identifies Discrepancies**:
    *   **Missing Translations**: English strings that do not have a French equivalent.
    *   **Extra Translations**: French strings that do not correspond to any English translatable string in `semantics.json`.
    *   **Identical Strings**: English and French strings that are identical, potentially indicating an untranslated string.
*   **Calculates Coverage**: It calculates a percentage of French translation coverage based on the number of English strings found that have a corresponding (and non-identical) French translation.

### `generate_translation_report.py`

This script is the main entry point for generating a full translation report:

1.  **Scans Libraries**: It scans a predefined `libraries` directory (relative to its own location) for H5P library folders. It identifies valid H5P libraries by checking for the presence of `semantics.json` and `language/fr.json`.
2.  **Processes Each Library**: For each identified H5P library, it calls the `check_translations_for_library` function from `translation_checker.py`.
3.  **Generates Markdown Report**: It compiles the results from all libraries into a single Markdown file named `translation_report.md`. This report includes:
    *   A summary table of French coverage percentages for all libraries.
    *   Detailed sections for each library, listing missing translations, extra translations, and identical strings.

## Usage

To generate a translation report:

1.  Ensure you have Python installed.
2.  Navigate to the `h5p-node.backend.eclasse/scripts/` directory.
3.  Run the `generate_translation_report.py` script:
    ```bash
    python generate_translation_report.py
    ```
4.  A file named `translation_report.md` will be created in the current directory, containing the detailed report.
