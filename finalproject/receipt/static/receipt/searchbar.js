document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('#searchform').onsubmit = () => {
		const query = document.querySelector('#searchquery').value;
		if(!query) {
			return false;
		}
	};
});