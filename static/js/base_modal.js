// NEED TO FIND A WAY TO PASS IN OR USE ROUTES FOR THE HREF URL

function openModal(modalType) {
    const modal = document.getElementById("myModal");
    const modalTitle = modal.querySelector(".modal-title");
    const modalContent = modal.querySelector(".modal-body");

    // Remove any child elements (form elements) from the modal content
    while (modalContent.firstChild) {
        modalContent.removeChild(modalContent.firstChild);
    };

    if (modalType === 'login') {
        modalTitle.textContent = 'Log in';

        const form = document.createElement('form');
        form.method = "POST";

        const user_gp = document.createElement('div');
        user_gp.className = "form-group";
        const user_label = document.createElement('label');
        user_label.for = "username";
        user_label.innerHTML = "Username";
        user_gp.appendChild(user_label);
        const user_input = document.createElement('input');
        user_input.type = "text";
        user_input.class = "form-control";
        user_input.autocomplete = "username";
        user_input.id = "username";
        user_input.name = "username";
        user_input.placeholder = "Enter username";
        user_gp.appendChild(user_input);
        form.appendChild(user_gp);

        const pw_gp = document.createElement('div');
        pw_gp.className = "form-group";
        const pw_label = document.createElement('label');
        pw_label.for = "password";
        pw_label.innerHTML = "Password";
        pw_gp.appendChild(pw_label);
        const pw_input = document.createElement('input');
        pw_input.type = "password";
        pw_input.class = "form-control";
        pw_input.autocomplete = "current-password";
        pw_input.id = "password";
        pw_input.name = "password";
        pw_input.placeholder = "Enter password";
        pw_gp.appendChild(pw_input);
        form.appendChild(pw_gp);

        form.appendChild(document.createElement('br'));

        const form_btn = document.createElement('button');
        form_btn.className = "btn btn-primary";
        form_btn.type = "submit";
        form_btn.href = "/login";
        form_btn.innerHTML = "Log in";
        form.appendChild(form_btn);


        // Append the content div to the modal content
        modalContent.appendChild(form);

        // Link to switch to the sign-up modal
        const switchToSignupLink = document.createElement('a');
        switchToSignupLink.href = "javascript:void(0);";
        switchToSignupLink.textContent = "Don't have an account? Sign up here";
        switchToSignupLink.onclick = function () {
            openModal('signup'); // Change the modal type to 'signup' when clicked
        };

        // Append the login form and the switch link to the modal content
        modalContent.appendChild(switchToSignupLink);

    } else if (modalType === 'signup') {
        modalTitle.textContent = 'Sign up';

        const form = document.createElement('form');
        form.method = "POST";

        const user_gp = document.createElement('div');
        user_gp.className = "form-group";
        const user_label = document.createElement('label');
        user_label.for = "username";
        user_label.innerHTML = "Username";
        user_gp.appendChild(user_label);
        const user_input = document.createElement('input');
        user_input.type = "text";
        user_input.class = "form-control";
        user_input.autocomplete = "username";
        user_input.id = "username";
        user_input.name = "username";
        user_input.placeholder = "Enter a username";
        user_gp.appendChild(user_input);
        form.appendChild(user_gp);

        const fName_gp = document.createElement('div');
        fName_gp.className = "form-group";
        const fName_label = document.createElement('label');
        fName_label.for = "first_name";
        fName_label.innerHTML = "First name";
        fName_gp.appendChild(fName_label);
        const fName_input = document.createElement('input');
        fName_input.type = "text";
        fName_input.class = "form-control";
        fName_input.autocomplete = "given-name";
        fName_input.id = "first_name";
        fName_input.name = "first_name";
        fName_input.placeholder = "Enter your first name";
        fName_gp.appendChild(fName_input);
        form.appendChild(fName_gp);

        const sName_gp = document.createElement('div');
        sName_gp.className = "form-group";
        const sName_label = document.createElement('label');
        sName_label.for = "surname";
        sName_label.innerHTML = "Surname";
        sName_gp.appendChild(sName_label);
        const sName_input = document.createElement('input');
        sName_input.type = "text";
        sName_input.class = "form-control";
        sName_input.autocomplete = "family-name";
        sName_input.id = "surname";
        sName_input.name = "surname";
        sName_input.placeholder = "Enter your surname";
        sName_gp.appendChild(sName_input);
        form.appendChild(sName_gp);

        const hc_gp = document.createElement('div');
        hc_gp.className = "form-group";
        const hc_label = document.createElement('label');
        hc_label.for = "handicap";
        hc_label.innerHTML = "Handicap Index";
        hc_gp.appendChild(hc_label);
        const hc_input = document.createElement('input');
        hc_input.type = "text";
        hc_input.class = "form-control";
        hc_input.id = "handicap";
        hc_input.name = "handicap";
        hc_input.pattern = "|[+]?\d(\.\d{0,1})?|54(\.0{0,1})?";
        hc_input.placeholder = "Enter your handicap index e.g. +1.5, 15, 25.4";
        hc_gp.appendChild(hc_input);
        form.appendChild(hc_gp);

        const email_gp = document.createElement('div');
        email_gp.className = "form-group";
        const email_label = document.createElement('label');
        email_label.for = "email";
        email_label.innerHTML = "Email";
        email_gp.appendChild(email_label);
        const email_input = document.createElement('input');
        email_input.type = "email";
        email_input.class = "form-control";
        email_input.autocomplete = "email";
        email_input.id = "email";
        email_input.name = "email";
        email_input.placeholder = "Enter your email";
        email_gp.appendChild(email_input);
        form.appendChild(email_gp);

        const pw_gp = document.createElement('div');
        pw_gp.className = "form-group";
        const pw_label = document.createElement('label');
        pw_label.for = "password";
        pw_label.innerHTML = "Password";
        pw_gp.appendChild(pw_label);
        const pw_input = document.createElement('input');
        pw_input.type = "password";
        pw_input.class = "form-control";
        pw_input.autocomplete = "current-password";
        pw_input.id = "password";
        pw_input.name = "password";
        pw_input.placeholder = "Enter a password";
        pw_gp.appendChild(pw_input);
        form.appendChild(pw_gp);

        const pw2_gp = document.createElement('div');
        pw2_gp.className = "form-group";
        const pw2_label = document.createElement('label');
        pw2_label.for = "password2";
        pw2_label.innerHTML = "Confirm password";
        pw2_gp.appendChild(pw2_label);
        const pw2_input = document.createElement('input');
        pw2_input.type = "password";
        pw2_input.class = "form-control";
        pw2_input.autocomplete = "current-password";
        pw2_input.id = "password2";
        pw2_input.name = "password2";
        pw2_input.placeholder = "Confirm your password";
        pw2_gp.appendChild(pw2_input);
        form.appendChild(pw2_gp);

        form.appendChild(document.createElement('br'));

        const form_btn = document.createElement('button');
        form_btn.className = "btn btn-primary";
        form_btn.type = "submit";
        form_btn.href = "/signup";
        form_btn.innerHTML = "Sign up";
        form.appendChild(form_btn);

        // Append the content div to the modal content
        modalContent.appendChild(form);
    }
    
    $(modal).modal("show");
}
