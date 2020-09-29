function loadProfile(upload_field, image_tag) {
	if(upload_field.files && upload_field.files[0]) {
		const reader = new FileReader();
		reader.onload = (e) => {
			const img = new Image();
			img.addEventListener("load", () => {
				const canvas = document.createElement('canvas');
				const ctx = canvas.getContext('2d');
				if(img.height >= img.width) {
					canvas.width = img.width;
					canvas.height = img.width;
					ctx.drawImage(img, 0, (img.height-img.width)/2, img.width, img.width, 0, 0, canvas.width, canvas.height);
				} else {
					canvas.height = img.height;
					canvas.width = img.height;
					ctx.drawImage(img, (img.width-img.height)/2, 0, img.height, img.height, 0, 0, canvas.width, canvas.height);
				}
				image_tag.src = canvas.toDataURL();
				uploadProfile(image_tag.src);
			});
			img.src = e.target.result;
		};
		reader.readAsDataURL(upload_field.files[0]);
	}
}

function uploadProfile(imagedata) {
	return new Promise(function(resolve, reject) {
		const request = new XMLHttpRequest();
		request.onload = function() {};
		request.onerror = reject;
		request.open('POST', '/profile');
		
		const data = new FormData();
		data.append('image', imagedata);
		request.send(data);
	});
}

function sendFollow(user_to_follow) {
	return new Promise(function(resolve, reject) {
		const request = new XMLHttpRequest();
		request.onload = () => {
			resolve(JSON.parse(this.responseText));
		};
		request.onerror = reject;
		request.open('POST', '/follow');

		const data = new FormData();
		data.append('user_to_follow', user_to_follow);
		request.send(data);
	});
}

document.addEventListener("DOMContentLoaded", () => {
	const profile_change = document.querySelector('#change_profile_link');
	const img_tag = document.querySelector('#profile_img');

	if(profile_change != null) {
		const upload_field = document.querySelector('#upload_profile');
		upload_field.onchange = (e) => {
			loadProfile(upload_field, img_tag);
		};
		profile_change.onclick = (e) => {
			upload_field.click();
		};
	};

	document.querySelectorAll('.img-gallery').forEach(element => {
		element.onclick = (e) => {
			window.location.href = '/post/' + e.target.dataset.postId;
		};
		element.onmouseover = (e) => {
			e.target.style.cursor = 'pointer';
		};
		$('[data-toggle="tooltip"]').tooltip();
	});

	const follow_btn = document.querySelector('button#follow-btn');
	if(follow_btn != null && !(follow_btn.disabled)) {
		follow_btn.onclick = (e) => {
			const u = parseInt(window.location.pathname.split('/')[2]);
			sendFollow(u)
			.then(result => {
				document.querySelector('#followers_count').innerText = result.followers;
			})
			.then(result => {
				e.target.disabled = true;
			});
		};
	}
})