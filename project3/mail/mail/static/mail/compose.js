document.addEventListener('DOMContentLoaded', function() {
	const form = document.querySelector('#compose-form');
	form.onsubmit = () => {
		const recipient = document.querySelector('#compose-recipients');
		const subject = document.querySelector('#compose-subject');
		const body = document.querySelector('#compose-body');
		if(recipient.length == 0 || body.length == 0) { return; }

		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: recipient.value,
				subject: subject.value,
				body: body.value
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
			console.log(result.status);
			load_mailbox('sent');
		});
		return false;
	}
})