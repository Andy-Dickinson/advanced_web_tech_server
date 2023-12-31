function displayAlertMessage(message, error, small) {
    const errorContainer = document.getElementById("flash-messages");
    let alert_type;

    if (error === true) {
        alert_type = "alert-danger";
    }else {
        alert_type = "alert-success";
    }

    // Create a new error alert
    const errorAlert = document.createElement('div');
    errorAlert.className = "alert " + alert_type + " alert-dismissible fade show fixed-top";
    if (small){
        errorAlert.className += " small-alert";
    }
    errorAlert.textContent = message;
    errorAlert.setAttribute('role', 'alert');

    // Append error alert
    errorContainer.appendChild(errorAlert);

    // Alert messages fade after 2 sec delay
    removeMessageAfterTimeout(errorAlert, 2000);
}


// Timeout param sets delay until starts to fade
function removeMessageAfterTimeout(messageElement, timeout) {
    setTimeout(() => {
        messageElement.style.opacity = 0; // Trigger the fade-out transition
        setTimeout(() => {
            messageElement.remove();
        }, 500); // Transition fade duration in css should match this delay for removal
    }, timeout);
}


// Find and remove flash messages with alert class, delay to fade 1 sec
document.addEventListener("DOMContentLoaded", function () {
    var flashMessages = document.querySelectorAll(".alert");
    flashMessages.forEach(function (flashMessage) {
        removeMessageAfterTimeout(flashMessage, 1000);
    });
});


function validateInput(formData, field) {
    switch (field) {
        case 'username':
            const user_format = /^[a-zA-Z0-9]+$/;
            
            if (formData.length < 4) {
                return 'Too short. (Minimum 4 characters)';
            } else if (formData.length >25) {
                return 'Too long. (Maximum 25 characters)';
            } else if (!user_format.test(formData)) {
                return 'Invalid characters. (Use only letters and numbers)';
            }
            break
            
        case 'password': 
            const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9\s])[^\s]{8,}$/;
            if (formData.length < 8) {
                return 'Too short. (Minimum 8 characters)';
            } else if (!passwordPattern.test(formData)) {
                return 'Invalid format. (Must contain at least one uppercase letter, lowercase letter, digit and special character)';
            }
            break

        case 'password2':
            if (formData[0] !== formData[1]) {
                return 'Passwords do not match';
            }
            break

        case 'first_name':
        case 'surname':
            const name_format = /^[a-zA-Z-' ]+$/;

            if (formData.length > 100) {
                return 'Too long. (Maximum 100 characters)';
            } else if (!name_format.test(formData)) {
                return 'Invalid characters. (Use only letters, hyphens, and spaces)';
            }
            break

        case 'handicap':
            const hc_pattern = /^(?:(?:\+(?:[0-9](?:\.[0-9])?|10(?:\.0)?)|0(?:\.[0-9])?)|(?:[0-9](?:\.[0-9])?)|(?:[0-4][0-9](?:\.[0-9])?)|(?:[5][0-3](?:\.[0-9])?)|(?:[5][4](?:\.[0])?))$/;

            if (!hc_pattern.test(formData)) {
                return 'Invalid format. (Enter a valid handicap index, e.g., +1.5, 15, 25.4)';
            }
            break

        case 'email':
            const emailPattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

            if (formData.length > 255) {
                return 'Too long. (Maximum 255 characters)';
            } else if (!emailPattern.test(formData)) {
                return 'Invalid format. (Enter a valid email address)';
            }
            break
    }

    return ""; // Validation passed
}

