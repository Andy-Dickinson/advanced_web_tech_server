// Returns list of dictionaries for all clubs in database (one dict for each club), if none exist returns empty list
async function fetchApprovedClubData() {
    const response = await fetch("/all_approved_clubs", {
      method: 'GET'
    });
    if (!response.ok) {
      throw new Error("Failed to retrieve club names");
    }
    const clubs = await response.json();
    return clubs;
  }
  
  // Returns list of dictionaries for current users subscriptions (one dict for each), if none exist returns empty list
  async function fetchClubSubscriptions() {
    const response = await fetch("/user_subs", {
      method: 'GET'
    });
    if (!response.ok) {
      throw new Error("Failed to retrieve user subscriptions");
    }
    const subs = await response.json();
    return subs;
  }


  // Returns list of dictionaries for open events, if none exist returns empty list
  async function fetchOpenEvents() {
    const response = await fetch("/open_events", {
      method: 'GET'
    });
    if (!response.ok) {
      throw new Error("Failed to retrieve open events");
    }
    const events = await response.json();
    return events;
  }