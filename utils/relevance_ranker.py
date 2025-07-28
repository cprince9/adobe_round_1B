from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # Auto-downloads model

def rank_sections(sections, persona_text, top_k=5):
    persona_emb = model.encode(persona_text, convert_to_tensor=True)
    for sec in sections:
        sec_emb = model.encode(sec["text"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(persona_emb, sec_emb).item()
        sec["score"] = score
    sections.sort(key=lambda x: -x["score"])
    return sections[:top_k]
