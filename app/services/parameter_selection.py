def select_llm_parameters(pages, words, sections):
 
    words_per_section = words / sections
    sections_per_page = sections / pages

    # Determine chunk size
    if words > 200000 or pages > 500:
        chunk_size = 1500
    elif words_per_section > 1000:
        chunk_size = 1500 if words_per_section > 1500 else 1200
    elif 500 < words_per_section <= 1000:
        chunk_size = 1200
    else:
        chunk_size = 1000

    # Determine overlap
    if sections_per_page > 8:   # many small sections per page (e.g., tabular)
        overlap = 250
    elif 5 < sections_per_page <= 8:
        overlap = 200
    else:
        overlap = 150
    # --------------------------
    print(f"The chunk size is {chunk_size}\nThe words are {words}\nThe sections are {sections}\nThe pages are {pages}\nThe overlap size is{overlap}")

    return {
        "chunk_size": chunk_size,
        "overlap": overlap,
    }
