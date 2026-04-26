def handle(prompt: str):
    p = prompt.lower()

    # 🧠 PRIORITÉ : compress
    if "consolide" in p or "compresse" in p or "compress" in p:
        report = {
            "total_before": 0,
            "total_after_active": 0,
            "dedup_archived": 0,
            "decay_archived": 0,
            "groups_processed": 0,
        }

        try:
            from app.mempalace import compress
            r = compress()
            report = {
                "total_before": r.total_before,
                "total_after_active": r.total_after_active,
                "dedup_archived": r.dedup_archived,
                "decay_archived": r.decay_archived,
                "groups_processed": r.groups_processed,
            }
        except Exception as e:
            pass

        return {
            "action": "MEMORY_COMPRESS",
            "output": {"status": "done", "report": report},
        }

    # 📖 Lecture mémoire
    if "memoire" in p or "mémoire" in p:
        hits = []
        try:
            from app.mempalace import search_memory
            results = search_memory(prompt, top_k=5, touch=True)
            hits = [
                {
                    "id": h.entry.id,
                    "type": h.entry.type,
                    "content": h.entry.content,
                    "summary": h.entry.summary,
                    "score": round(h.score, 3),
                }
                for h in results
            ]
        except Exception:
            pass

        return {
            "action": "MEMORY_READ",
            "output": hits,
        }
