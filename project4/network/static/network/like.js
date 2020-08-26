function likepost(id, likedby) {
	console.log(`${id} liked by: ${likedby}`);
	fetch(`/postapi/${id}`)
	.then(response => response.json())
	.then(post => {
		console.log('post: '+post);
		const likecount = post.likes;
		fetch(`/likeapi/${id}`, {
			method: 'POST',
			body: JSON.stringify({
				'id': id,
				'likes': likecount+1,
				'likedby': likedby[0]
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log('result: '+result);
			likeblock = document.querySelector(`#like-${id}`);
			likeblock.innerHTML = `<p><img class="unlikebtn" id="unlikebtn-${id}" src="https://img.icons8.com/ultraviolet/40/000000/hearts.png"/><b> ${likecount+1} </b></p>`
			unlikebtn = document.querySelector(`#unlikebtn-${id}`);
			unlikebtn.onclick = () =>{
				unlikepost(id, likedby)
			}
		})
	})
}

function unlikepost(id, unlikedby) {
	console.log(`${id} unliked by: ${unlikedby}`);
	fetch(`/postapi/${id}`)
	.then(response => response.json())
	.then(post => {
		console.log('likes: '+post.likes);
		const likecount = post.likes;
		fetch(`/likeapi/${id}`, {
			method: 'DELETE',
			body: JSON.stringify({
				'id': id,
				'likes': likecount-1,
				'unlikedby': unlikedby[0]
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log('result: '+result);
			likeblock = document.querySelector(`#like-${id}`);
			likeblock.innerHTML = `<p><img class="likebtn" id="likebtn-${id}" src="https://img.icons8.com/office/16/000000/hearts.png"/><b> ${likecount-1} </b></p>`
			likebtn = document.querySelector(`#likebtn-${id}`);
			likebtn.onclick = () =>{
				likepost(id, unlikedby)
			}
		})
	})
}