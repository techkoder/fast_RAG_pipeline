def select_llm_parameters(pages, words, sections):
    # --------- Calculate averages ---------
    avg_sections_per_page = sections / pages if pages else 0
    # --------- Chunk Size (tokens) ---------
    # Moderate scaling by words and sections; capped at 1200
    chunk_size = int(500 + 0.005 * words + 2 * sections)
    chunk_size = min(max(chunk_size, 700), 1200)  # Bound within 700-1200

    # --------- Overlap (tokens) ---------
    # Scales with structure density; capped at 180
    overlap = int(100 + 0.3 * avg_sections_per_page * pages)
    overlap = min(max(overlap, 100), 180)  # Bound within 100-180

    # --------- MMR (k, fetch_k, lambda) ---------
    k = 5 + int(pages / 100)
    fetch_k = 2 * k
    # Lambda scales slightly with section density
    lam = 0.3 + 0.05 * min(avg_sections_per_page / 3, 1)  # Between 0.3 and 0.35

    # --------- Score Threshold ---------
    # Baseline at 0.75; slight bump for large/complex docs
    if pages > 300 or sections > 300:
        score_threshold = 0.78
    elif pages > 100 or sections > 150:
        score_threshold = 0.76
    else:
        score_threshold = 0.74

    # --------- Temperature (LLM Temperature) ---------
    # Lower for long/complex; slightly higher for very small/simple docs
    temperature = 0.1
    if pages > 300 or words > 100000:
        temperature = 0.05
    elif pages < 20 or words < 10000:
        temperature = 0.15

    # --------- Return as dictionary ---------
    return {
        "chunk_size": chunk_size,
        "overlap": overlap,
        "mmr_k": k,
        "mmr_fetch_k": fetch_k,
        "mmr_lambda": round(lam, 2),
        "score_threshold": round(score_threshold, 2),
        "temperature": temperature
    }
