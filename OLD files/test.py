
# function validateForm(formData, formType) {
#     const username = formData.get('username');
#     const password = formData.get('password');

#     if (username.length < 4 || username.length > 25) {
#         return 'Username must be between 4 and 25 characters';
#     }
    
#     if (password.length < 8) {
#         return 'Password must be at least 8 characters';
#     }

#     const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$/;
#     if (!passwordPattern.test(password)) {
#         return 'Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character';
#     }

#     if (formType === 'signup') {
#         const first_name = formData.get('first_name');
#         const surname = formData.get('surname');
#         const email = formData.get('email');
#         const password2 = formData.get('password2');

#         if (first_name.length > 100) {
#             return 'First name must be 100 characters or less';
#         }

#         if (surname.length > 100) {
#             return 'Surname must be 100 characters or less';
#         }
        
#         if (email.length > 255) {
#             return 'Email must be 255 characters or less';
#         }

#         if (email.length > 0) {
#             const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
#             if (!emailPattern.test(email)) {
#                 return 'Invalid email format';
#             }
#         }
        
#         if (password !== password2) {
#             return 'Passwords do not match';
#         }
#     }


#     return null; // Validation passed
# }
