// Returns list of dictionaries for all clubs in database (one dict for each club), if none exist returns empty list
async function fetchApprovedClubData() {
  const response = await fetch("/all_approved_clubs", {
    method: "GET",
  });
  if (!response.ok) {
    throw new Error("Failed to retrieve club names");
  };
  const clubs = await response.json();
  return clubs;
};

// Returns list of dictionaries for current users subscriptions (one dict for each), if none exist returns empty list
async function fetchClubSubscriptions() {
  const response = await fetch("/user_subs", {
    method: "GET",
  });
  if (!response.ok) {
    throw new Error("Failed to retrieve user subscriptions");
  };
  const subs = await response.json();
  return subs;
};

// Returns list of dictionaries for open events, if none exist returns empty list
async function fetchOpenEvents() {
  const response = await fetch("/open_events", {
    method: "GET",
  });
  if (!response.ok) {
    throw new Error("Failed to retrieve open events");
  };
  const events = await response.json();
  return events;
};

/* Returns null if no handicap set or the float value
  Note positive handicaps e.g. +3.0 are returned as a negitive value
*/
async function fetchHandicap() {
  const response = await fetch("/update_hc", {
    method: "GET",
  });
  if (!response.ok) {
    throw new Error("Failed to retrieve handicap");
  };
  const hc = await response.json();
  if (hc.success){
    let hc_s = hc.hc;

    // Check if string includes decimals
    if (!hc_s.includes('.')) {
      hc_s += '.0';
    }

    // If positive handicap, convets to negative value
    if (hc_s.startsWith('+')) {
      hc_s = hc_s.replace('+', '-');
    };

    // converts to float and rounds to 1 decimal
    let hc_f = parseFloat(hc_s).toFixed(1);

    return hc_f;
  };

  return null;
};
