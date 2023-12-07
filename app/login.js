document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Store the JWT token in local storage or cookie
            localStorage.setItem('access_token', data.access_token);
            // Redirect to the home page or dashboard
            window.location.href = '/dashboard.html';
        } else {
            alert('Login failed: ' + data.msg);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});
