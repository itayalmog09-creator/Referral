_db: dict[int, dict] = {}
 
_next_id = 1
_db[1] = {
    "id": 1,
    "name": "דוד לוי",
    "status": "in_progress",
    "assigned_to": "נועם",
    "next_followup_date": "2026-05-12"
}
_next_id = 2
 
def get_all() -> list[dict]:
    return list(_db.values())
 
 
def get_by_id(referral_id: int) -> dict | None:
    return _db.get(referral_id)
 
 
def insert(record: dict) -> dict:
    global _next_id
    record["id"] = _next_id
    _db[_next_id] = record
    _next_id += 1
    return record
 
 
def update(referral_id: int, fields: dict) -> dict:
    _db[referral_id].update(fields)
    return _db[referral_id]
 
 
def delete(referral_id: int) -> None:
    del _db[referral_id]
 