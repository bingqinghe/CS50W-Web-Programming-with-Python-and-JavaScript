function sendComment(postid) {
	return new Promise(function(resolve, reject) {
		const request = new XMLHttpRequest();
		request.onload = function() {
			resolve(JSON.parse(this.responseText));
		};
		request.onerror = reject;
		request.open('POST', '/comment');
		const data = new FormData(document.querySelector("#comment-form"));
		data.append('post_id', postid);
		request.send(data);
	})
}

function renewComment(comments) {
	const list = document.querySelector('#comments-list');
	list.innerHTML = "";
	comments.forEach((comment) => {
		outer = document.createElement("div");
		outer.classList.add("card");

		head = document.createElement("div");
		head.classList.add("card-header");
		head.innerHTML = `<a href="/user/${comment.author_id}">` + comment.author_name + `</a>`

		body = document.createElement("div");
		body.classList.add("card-body");

		bq = document.createElement("blockquote");
		bq.classList.add("blockquote");
		bq.classList.add("mb-0");

		bqp = document.createElement("p");
		bqp.innerHTML = comment.comments;

		bqf = document.createElement("footer");
		bqf.classList.add("blockquote-footer");
		bqf.innerHTML = comment.time.strftime(' %b %d %Y, %H:%M:%S ');

		bq.appendChild(bqp);
		bq.appendChild(bqf);
		body.appendChild(bq);
		outer.appendChild(head);
		outer.appendChild(body);
		list.appendChild(outer);
	})
}

function sendLike(postid) {
	return new Promise(function(resolve, reject) {
		const request = new XMLHttpRequest();
		request.onload = function() {
			resolve(JSON.parse(this.responseText));
		};
		request.onerror = reject;
		request.open('POST', '/like');
		const data = new FormData();
		data.append('post_id', postid);
		request.send(data);
	})
}

document.addEventListener("DOMContentLoaded", () => {
	document.querySelector("#comment-form").onsubmit = (e) => {
		const postId = parseInt(window.location.pathname.split("/")[2]);

		sendComment(postId)
		.then(result => {
			renewComment(result.comments);
		})
		.then(result => {
			let count = parseInt(document.querySelector("#comments-count"));
			count += 1;
			document.querySelector("#comments-count").innerText = count;
		});

		document.querySelector("#comment-input").value = "";
		return false;
	}

	document.querySelector("button.like-btn").onclick = (e) => {
		const postId = parseInt(window.location.pathname.split("/")[2]);

		sendLike(postId)
		.then(result => {
			document.querySelector("#likes-count").innerText = result.likes;
		})
		.then(result => {
			e.target.disabled = true;
		});
	}
})
