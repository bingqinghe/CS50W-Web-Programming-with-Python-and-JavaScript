document.addEventListener("DOMContentLoaded", () => {
	$('#nav-tab a#nav-login-tab').on('click', (e) => {
		e.preventDefault();
		$(this).tab('show');
	});

	$('#nav-tab a#nav-register-tab').on('click', (e) => {
		e.preventDefault();
		$(this).tab('show');
	});

	document.querySelector('#form-register').onsubmit = () => {
		const password = document.querySelector('#r-password').value;
		const confirmp = document.querySelector('#c-password').value;
		if(password != confirmp) {
			alert('Passwords Not Match');
			return false;
		}
	};
})