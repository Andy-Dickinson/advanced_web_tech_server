// Adds each club as an option in the dropdown box
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
    }
}


async function displayEvents(onLoad) {
    try {
        const open_games = await fetchOpenEvents();
        const user_subs = await fetchClubSubscriptions();

        console.log("open_games retrieved: ", open_games);

        // Sets selected dropdown option on page load based on if user has subscriptions
        if (onLoad) {
            let default_option;
            
            if (user_subs.length > 0) {
                default_option = "sub_option";
            } else {
                default_option = "all_option";
            }

            document.getElementById(default_option).selected = true;
        }
        
        events_board = document.querySelector('.find-game-games');

        // Removes any content before updating
        while (events_board.firstChild) {
            events_board.removeChild(events_board.firstChild);
        }

        header_container = document.createElement('div');
        header = document.createElement('h5');
        header.className = "text-center";
        header_container.appendChild(header);
        header_container.appendChild(document.createElement('hr'));
        events_board.appendChild(header_container);

        if (open_games.length > 0) {
            console.log("open present");
        } else {
            p = document.createElement('p');
            p.className = "col-7 mx-5 col-sm-11 mx-sm-auto";
            p.textContent = "No open events at present. Try creating one, or changing selected dates and display options."
            events_board.appendChild(p);
        }
        
    } catch (error) {
        console.error('Error displaying events: ', error);
    }
}

// Call functions when page loads
document.addEventListener('DOMContentLoaded', addDropdownOptions);
document.addEventListener('DOMContentLoaded', () => displayEvents(true));
