function openModal(modalType) {
  const modal = document.getElementById("myModal");
  const modalTitle = modal.querySelector(".modal-title");
  const modalContent = modal.querySelector(".modal-body");

  // Remove any child elements (form elements) from the modal content
  while (modalContent.firstChild) {
    modalContent.removeChild(modalContent.firstChild);
  }

  // Update handicap modal
  if (modalType === "hc") {
    let current_hc;
    modalTitle.textContent = "Update handicap";

    const form = document.createElement("form");
    form.id = "hc";

    // handicap
    const hc_gp = document.createElement("div");
    hc_gp.className = "form-group";
    const hc_label = document.createElement("label");
    hc_label.id = "hc_label";
    hc_label.htmlFor = "handicap";
    // Get current handicap index
    fetch("/update_hc", {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        current_hc = data.hc;
        hc_label.innerHTML = "Current handicap index: " + current_hc;
      })
      .catch((error) =>
        console.error("Error fetching current handicap:", error)
      );
    hc_gp.appendChild(hc_label);
    const hc_input = document.createElement("input");
    hc_input.type = "text";
    hc_input.form = "hc";
    hc_input.className = "form-control";
    hc_input.id = "handicap";
    hc_input.name = "handicap";
    hc_input.placeholder = "Enter your handicap index e.g. +1.5, 15, 25.4";
    hc_input.form = "signup";
    // validates client side
    hc_input.addEventListener("input", function () {
      hc_input.setCustomValidity(validateInput(hc_input.value, "handicap"));
    });
    hc_gp.appendChild(hc_input);
    form.appendChild(hc_gp);

    form.appendChild(document.createElement("br"));

    // Submit button
    const form_btn = document.createElement("button");
    form_btn.className = "btn btn-primary";
    form_btn.type = "submit";
    form_btn.form = "hc";
    form_btn.textContent = "Update handicap index";
    form.appendChild(form_btn);

    // Event listener for sending data to server
    form.addEventListener("submit", function (e) {
      e.preventDefault(); // prevents reloading of the page
      const formData = new FormData(form);

      // Does not Post if nothing entered
      if (formData.get("handicap").trim() === "") {
        displayAlertMessage("Please enter a handicap index", true, true);
        return;
      }

      // Send form data to server
      fetch("/update_hc", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) {
            displayAlertMessage(data.message, true, true);
          }

          // Update display and placeholder when successful
          if (data.success) {
            displayAlertMessage("Handicap index updated to " + data.hc, false, true);
            document.getElementById("hc_label").innerHTML =
              "Current handicap index: " + data.hc;
            const hc_input = document.getElementById("handicap");
            hc_input.value = "";
            hc_input.placeholder =
              "Enter your handicap index e.g. +1.5, 15, 25.4";

            // Updates displayed events
            if (window.location.pathname === '/find_game'){
              displayEvents(false);
            }
          }
        })
        .catch((error) => console.error("Error submit function:", error));
    });

    // Append form to modal content
    modalContent.appendChild(form);

    // Manage subscriptions modal
  } else if (modalType === "subs") {
    fetchApprovedClubData().then((approved_clubs) => {
        fetchClubSubscriptions().then(user_subs => {

      modalTitle.textContent = "Manage subscriptions";

      // Link to add club
      const switchToLoginLink = document.createElement("a");
      switchToLoginLink.className = "link";
      switchToLoginLink.href = "#add_club";
      switchToLoginLink.textContent = "Club not listed? Click here to add";
      modalContent.appendChild(switchToLoginLink);

      modalContent.appendChild(document.createElement("br"));

      const form = document.createElement("form");
      form.id = "subs";

      // Create a div for the scrollable container
      const scrollContainer = document.createElement("div");
      scrollContainer.className = "modal-scroll container";

      const row = document.createElement("div");
      row.className = "row d-flex align-items-center select-all";

      if (approved_clubs.length > 0) {
        // Select all only added if multiple clubs
        if (approved_clubs.length > 1) {
            const isSubscribedToAll = user_subs.length === approved_clubs.length;

            // Select All label
            const selectAllLabel = document.createElement("div");
            selectAllLabel.className = "col-8 toggle-label";
            selectAllLabel.textContent = "Select all";
            row.appendChild(selectAllLabel);

            // Select All actual switch
            const selectAllSwitch = document.createElement("div");
            selectAllSwitch.className = "col-4";
            const switchLabel = document.createElement("label");
            switchLabel.className = "switch";
            const selectInput = document.createElement("input");
            selectInput.type = "checkbox";
            selectInput.name = "select-all-checkbox"
            selectInput.form = "subs";
            selectInput.checked = isSubscribedToAll;
            // Event listener for the "Select All" switch
            selectInput.addEventListener("change", () => {
                const allSwitches = document.querySelectorAll(".switch input[type='checkbox']");
                allSwitches.forEach(switchInput => {
                    switchInput.checked = selectInput.checked;
                });
            });
            switchLabel.appendChild(selectInput);
            const selectSlider = document.createElement("slider");
            selectSlider.className = "slider";
            switchLabel.appendChild(selectSlider);
            selectAllSwitch.appendChild(switchLabel);
            row.appendChild(selectAllSwitch);

            // Adds label and switch row to scroll container
            scrollContainer.appendChild(row);
            scrollContainer.appendChild(document.createElement("hr"));
        }

        // Sorts alphabetically by club name
        approved_clubs = approved_clubs.sort((a, b) => {
          const name_a = a.name.toUpperCase(); 
          const name_b = b.name.toUpperCase();

          if (name_a < name_b) {
              return -1;
          } else if (name_a > name_b) {
              return 1;
          } else {
              return 0; // Club names start with same letter
          }
        })
        
        // add toggle switch for each club
        approved_clubs.forEach((club, i) => {
            const clubRow = document.createElement("div");
            clubRow.className = "row d-flex align-items-center club";

            // Club label
            const clubLabel = document.createElement("div");
            clubLabel.className = "col-8 toggle-label";
            clubLabel.textContent = club.name + " - " + club.postcode;
            clubRow.appendChild(clubLabel);

            // Club switch
            const clubSwitch = document.createElement("div");
            clubSwitch.className = "col-4";
            const switchLabel = document.createElement("label");
            switchLabel.className = "switch";
            const switchInput = document.createElement("input");
            switchInput.type = "checkbox";
            switchInput.name = "club-checkbox"
            switchInput.className = "club-data"
            switchInput.form = "subs";
            switchInput.dataset.clubName = club.name;
            // Check if the user is subscribed to this club and set the checked status accordingly
            if (user_subs.some(sub => sub.club_id === club.id)) {
                switchInput.checked = true;
            }
            switchLabel.appendChild(switchInput);
            const selectSlider = document.createElement("slider");
            selectSlider.className = "slider";
            switchLabel.appendChild(selectSlider);
            clubSwitch.appendChild(switchLabel);
            clubRow.appendChild(clubSwitch);

            // Add the club row to the scroll container
            scrollContainer.appendChild(clubRow);

            if (i < approved_clubs.length - 1) {
                scrollContainer.appendChild(document.createElement("hr"));
            }
        });

      } else {
            const label = document.createElement("div");
            label.className = "col-8 toggle-label";
            label.textContent = "Currently no approved clubs";
            row.appendChild(label);

            scrollContainer.appendChild(row);
      }

      form.appendChild(scrollContainer);

      // Create "Save" and "Cancel" buttons
      const buttonGp = document.createElement("div");
      buttonGp.className = "modal-buttons row justify-content-center";

      const saveButton = document.createElement("button");
      saveButton.className = "btn col-sm-3 mx-2 my-1 btn-primary";
      saveButton.type = "submit";
      saveButton.form = "subs";
      saveButton.textContent = "Save";
      buttonGp.appendChild(saveButton);

      const cancelButton = document.createElement("button");
      cancelButton.className = "btn col-sm-3 mx-2 my-1 btn-primary";
      cancelButton.type = "button";
      cancelButton.textContent = "Cancel";
      cancelButton.addEventListener("click", function () {
        $("#myModal").modal("hide");
        toggleNavbarCollapse();
      });
      buttonGp.appendChild(cancelButton);

      form.appendChild(buttonGp);

      // Save button event listener - update server
      form.addEventListener("submit", function (e) {
        e.preventDefault();

        const selectedClubs = [];

        // Select all toggle switches
        const checkboxInputs = document.querySelectorAll('.club-data');
        // Get the club name for each which is checked
        checkboxInputs.forEach(input => {
            if (input.checked) {
                selectedClubs.push(input.dataset.clubName);
            }
        });
        
        // Send to server
        fetch('/user_subs', {
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ selectedClubs })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayAlertMessage(data.message, false, false);
                $("#myModal").modal("hide");
                toggleNavbarCollapse();

                // Updates displayed events
                if (window.location.pathname === '/find_game'){
                  displayEvents(true);  // Changes dropdown to subscribed
                }
            } else {
                displayAlertMessage(data.message, true, true);
            }
        })
        .catch(error => {
            console.error('Error sending subscription data:', error);
        });
    });

      modalContent.appendChild(form);

    
    })
    .catch(error => {
        console.error('Error fetching club subscriptions data:', error);
    })
})
    .catch(error => {
        console.error('Error fetching approved club data:', error);
      });
  }

  $(modal).modal("show");
}


