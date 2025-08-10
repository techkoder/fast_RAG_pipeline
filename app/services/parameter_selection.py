def select_llm_parameters(pages, words, sections):
 
    words_per_section = words / sections
    sections_per_page = sections / pages

    # Determine chunk size
    # Determine chunk size
    if pages > 500 or words > 250000:
        chunk_size = 1400  # Very long, continuous content
    elif words_per_section < 150 and sections_per_page > 4.5:
        chunk_size = 1000  # Short clauses / table-heavy
    elif 150 <= words_per_section <= 800 and sections_per_page <= 4.5:
        chunk_size = 1200  # Medium mixed content
    else:
        chunk_size = 1000  # Default fallback

    # Determine overlap
    overlap = 200 if words_per_section < 150 else 150
    # --------------------------
    print(f"The chunk size is {chunk_size}\nThe words are {words}\nThe sections are {sections}\nThe pages are {pages}\nThe overlap size is{overlap}")

    return {
        "chunk_size": chunk_size,
        "overlap": overlap,
    }
