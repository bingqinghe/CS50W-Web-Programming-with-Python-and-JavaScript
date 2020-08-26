function editpost(id) {
	fetch(`/postapi/${id}`)
	.then(response => response.json())
	.then(post => {
		cardbody = document.querySelector(`#card-body-${id}`);
		cardbody.innerHTML = `<form id='editform-${post.id}'><div class='form-group'><label for="textarea"> Edit Your Post: </label><textarea class="form-control" id="textarea-${post.id}" rows='5'> ${post.content} </textarea><br><button class="btn btn-primary" type="submit"> Save </button></form>`;
		const form = document.querySelector(`#editform-${post.id}`);
		form.onsubmit = () => {
			const updatedpost = document.getElementById(`textarea-${id}`).value;
			fetch(`/postapi/${post.id}`, {
				method: 'PUT',
				body: JSON.stringify({
					content: updatedpost,
					username: post.username
				})
			})
			document.querySelector(`#card-body-${id}`).innerHTML = updatedpost;
			return false;
		}
	})
}
