def search_user(users, query):
    query = query.strip().lower()
 
    if not query:
        return False, "Search query cannot be empty.", []
 
    matches = [username for username in users if query in username.lower()]
 
    if not matches:
        return False, f"No users found matching '{query}'.", []
 
    return True, f"{len(matches)} user(s) found.", matches
 