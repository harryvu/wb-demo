def split_into_chunks(text, chunk_size, overlap):
    """
    Splits the text into chunks of size chunk_size with an overlap of overlap tokens.
    """
    tokens = text.split()  # Simple whitespace-based tokenization
    chunks = []
    
    for i in range(0, len(tokens) - chunk_size + 1, chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i+chunk_size]))
        
    return chunks