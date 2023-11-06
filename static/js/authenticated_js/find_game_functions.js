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


async function displayEvents() {
    try {
        const open_games = await fetchOpenEvents();
        
        list_ele = document.querySelector('.find-game-games');

        // Removes any content before updating
        while (list_ele.firstChild) {
            list_ele.removeChild(list_ele.firstChild);
        }

        header_container = document.createElement('div');
        header = document.createElement('h5');
        header.className = "text-center";
        header_container.appendChild(header);
        header_container.appendChild(document.createElement('hr'));
        list_ele.appendChild(header_container);

        if (open_games.length > 0) {
            console.log("open present");
        } else {
            p = document.createElement('p');
            p.className = "col-7 mx-5 col-sm-11 mx-sm-auto";
            p.textContent = "No open events current. Try creating one."
            list_ele.appendChild(p);
        }
        
    } catch (error) {
        console.error('Error displaying events: ', error);
    }
}

// Call functions when page loads
document.addEventListener('DOMContentLoaded', addDropdownOptions);
document.addEventListener('DOMContentLoaded', displayEvents);
