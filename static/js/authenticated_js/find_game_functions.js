// Adds each club as an option in the dropdown box
// Checked option is set in fetchOpenEvents
async function addDropdownOptions() {
    try {
        const approvedClubs = await fetchApprovedClubData();

        const dropdown = document.getElementById('dropdown');

        approvedClubs.forEach(club => {
            const optionElement = document.createElement('option');
            optionElement.value = club.id;
            optionElement.textContent = club.name + " - " + club.postcode;
            dropdown.appendChild(optionElement);
        });
    } catch (error) {
        console.error('Error creating dropdown options: ', error);
    };
};


/*
Called on load along with any changes of the dropdown, or date selectors.
Note the function is also called from event listeners in modals.js after a successful submit of either handicap update or change of subscriptions
*/
async function displayEvents(onLoad) {
    try {
        const open_events = await fetchOpenEvents();
        const user_subs = await fetchClubSubscriptions();
        const clubs = await fetchApprovedClubData();
        const hc = Number(await fetchHandicap());

        // Sets selected dropdown option on page load based on if user has subscriptions
        if (onLoad) {
            let default_option;
            
            if (user_subs.length > 0) {
                default_option = "sub_option";
            } else {
                default_option = "all_option";
            }

            document.getElementById(default_option).selected = true;
        };
        
        const events_board = document.querySelector('.find-game-board');

        // Removes any content before updating
        while (events_board.firstChild) {
            events_board.removeChild(events_board.firstChild);
        };
        
        events_board.appendChild(document.createElement('hr'));
        
        if (open_events.length > 0) {
            const dropdown_selection = document.getElementById('dropdown').value;
            const start_date = document.getElementById('start-datetime').value;
            const end_date = document.getElementById('end-datetime').value;
            
            events_to_keep = [];

            // Choose events based on dropdown
            if (dropdown_selection === 'subscribed') {
                // Subscribed selected
                user_subs.forEach(sub => {
                    open_events.forEach(event => {
                        if (sub.club_id === event.club_id) {
                            events_to_keep.push(event);
                        };
                    });
                });
            } else if (dropdown_selection !== 'all') {
                // Specific club selected
                open_events.forEach(event => {
                    if (String(event.club_id) === dropdown_selection) {
                        events_to_keep.push(event);
                    };
                })
            } else {
                // All selected
                events_to_keep = [...open_events];
            };
            
            // Remove from list if not in time/date selection
            events_to_display = [];
            events_to_keep.forEach(event => {
                const event_date = new Date(event.planned_date);
                const f_event_date = event_date.toISOString().slice(0,16);
                
                if (start_date <= f_event_date && (f_event_date <= end_date || end_date==='')) {
                    events_to_display.push(event);
                };
            });

            // Sorts by soonest planned date
            events_to_display = events_to_display.sort((a, b) => {
                const date_a = new Date(a.planned_date);
                const date_b = new Date(b.planned_date);
                return date_a - date_b;
            });            
            
            // Display events
            events_to_display.forEach((event, i) => {
                // Link to event chat
                const chat_link = document.createElement('a');
                
                if (hc) {
                    let min_hc_s = String(event.min_hc);
                    let max_hc_s = String(event.max_hc);

                    if (min_hc_s.startsWith('+')){
                        min_hc_s = min_hc_s.replace('+', '-');
                    }

                    if (max_hc_s.startsWith('+')){
                        max_hc_s = max_hc_s.replace('+', '-');
                    }

                    let min_hc_f = parseFloat(min_hc_s);
                    let max_hc_f = parseFloat(max_hc_s);
                    // check for when min or max does not exist, also doesn't currently work for any range ------------------------------------------------------
                    if (min_hc_f <= hc <= max_hc_f) {
                        chat_link.href = '/add_user_chat?event_id=' + event.id;
                    } else {
                        chat_link.onclick = function() {displayAlertMessage('Handicap not in required range to join this event!', true);};
                    }
                } else {
                    chat_link.onclick = function() {displayAlertMessage('Handicap required to join this event!', true);};
                }

                // First row contains information which will always be in database (nullable=false) - club name, postcode, planned_datetime, participants
                const row1 = document.createElement('div');
                row1.className = 'd-flex flex-wrap justify-content-between mx-auto';
                const club_name = document.createElement('div');
                club_name.className = 'px-2 py-1 order-1';
                const postcode = document.createElement('div');
                postcode.className = 'px-2 py-1 order-2';
                for (var i=0; i<clubs.length;i++){
                    if (clubs[i].id === event.club_id){
                        club_name.textContent = clubs[i].name;
                        postcode.textContent = clubs[i].postcode;
                        break;
                    };
                };
                row1.appendChild(club_name);
                row1.appendChild(postcode);
                const scheduled = document.createElement('div');
                scheduled.className = 'px-2 py-1 order-3';
                scheduled.textContent = event.planned_date.slice(0,22);
                row1.appendChild(scheduled);
                const participants = document.createElement('div');
                participants.className = 'px-2 py-1 order-4';
                const icon = document.createElement('i');
                icon.className = 'fa-solid fa-user';
                participants.appendChild(icon);
                const participants_text = document.createElement('span');
                participants_text.textContent = " " + event.current_participants + "/" + event.max_capacity;
                participants.appendChild(participants_text);
                row1.appendChild(participants);
                chat_link.appendChild(row1);

                // Row 2 contains optional information, event name, min and max handicap restrictions
                if (event.event_name || event.min_hc || event.max_hc) {
                    
                    const row2 = document.createElement('div');
                    row2.className = 'd-flex flex-wrap justify-content-between mx-auto';
                    if (event.event_name) {
                        const event_name = document.createElement('div');
                        event_name.className = 'd-flex align-items-center justify-content-center px-2 py-1 order-1';
                        event_name.textContent = event.event_name;
                        row2.appendChild(event_name);
                    }
                    if (event.min_hc || event.max_hc) {
                        if (!event.event_name){
                            row2.className = 'd-flex flex-wrap justify-content-end mx-auto'
                        }
                        const hc_restriction = document.createElement('div');
                        hc_restriction.className = 'd-flex px-2 py-1 order-2';
                        const icon_col = document.createElement('div');
                        icon_col.className = 'd-flex align-items-center justify-content-center p-2'
                        const hc_icon = document.createElement('i');
                        hc_icon.className = "fa-solid fa-golf-ball-tee";
                        icon_col.appendChild(hc_icon);
                        hc_restriction.appendChild(icon_col);

                        const hc_col = document.createElement('div');
                        hc_col.className = 'd-flex flex-column'

                        if (event.min_hc) {
                            const min_hc = document.createElement('div');
                            min_hc.textContent = ' Min. hc: ' + event.min_hc;
                            hc_col.appendChild(min_hc);
                        }

                        if (event.max_hc) {
                            const max_hc = document.createElement('div');
                            max_hc.textContent = ' Max. hc: ' + event.max_hc;
                            hc_col.appendChild(max_hc);
                        }

                        hc_restriction.appendChild(hc_col);
                        row2.appendChild(hc_restriction);
                    }

                    chat_link.appendChild(row2);

                    // Row 3 contains optional event description
                    if(event.description) {
                        const row3 = document.createElement('div');
                        row3.className = 'd-flex flex-wrap justify-content-start mx-auto';
                        const description = document.createElement('div');
                        description.className = 'px-2 py-1 order-1';
                        description.textContent = event.description;
                        row3.appendChild(description);
                        chat_link.appendChild(row3);
                    }
                }
                events_board.appendChild(chat_link);
                
                if (event.id !== events_to_display[events_to_display.length-1].id){
                    events_board.appendChild(document.createElement('hr'));
                };
            });
        } else {
            // When nothing to display
            p = document.createElement('p');
            p.className = "col-7 mx-5 col-sm-11 mx-sm-auto";
            p.textContent = "No open events at present. Try creating one, or changing selected dates and display options."
            events_board.appendChild(p);
        };
        
    } catch (error) {
        console.error('Error displaying events: ', error);
    };
};

// Call functions when page loads - adds options, displays events and adds event listeners
document.addEventListener('DOMContentLoaded', addDropdownOptions);
document.addEventListener('DOMContentLoaded', () => displayEvents(true));
document.addEventListener('DOMContentLoaded', function () {
    
    const dropdown = document.getElementById('dropdown');
    const startDatetime = document.getElementById('start-datetime');
    const endDatetime = document.getElementById('end-datetime');
    const modal = document.getElementById('')

    // Dropdown
    dropdown.addEventListener('change', function () {
        const selectedValue = dropdown.value;
        displayEvents(false);
    });

    // Start datetime
    startDatetime.addEventListener('change', function () {
        const startDateValue = startDatetime.value;
        displayEvents(false);
        if (startDateValue){
            endDatetime.min = startDateValue;
        } else {
            endDatetime.min = startDatetime.min;
        }
    });

    // End datetime
    endDatetime.addEventListener('change', function () {
        const endDateValue = endDatetime.value;
        displayEvents(false)
        
        if(endDateValue) {
            startDatetime.max = endDateValue;
        } else {
            startDatetime.max = null;
        }
    });
});
