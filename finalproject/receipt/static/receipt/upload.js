function loadInput(fileinput, filters) {
	if(fileinput.files && fileinput.files[0]) {
		const reader = new FileReader();
		reader.onload = (e) => {
			const img = new Image();
			img.addEventListener('load', () => {
				let image_tag = document.querySelector('img#new-photo');
				let canvas_tag = document.querySelector('canvas#new-photo');
				if(image_tag == null) {
					document.querySelector('#image-placeholder').innerHTML = '';
					image_tag_string = '<img id="new-photo" src="' + img.src + '" alt="">';
					document.querySelector('#image-placeholder').innerHTML = image_tag_string;
					image_tag = document.querySelector('img#new-photo');
				} else if(canvas_tag == null) {
					image_tag.src = img.src;
				}

				Caman(image_tag, () => {
					this.render(function() {
						document.querySelector('canvas#new-photo').onclick = () => {
							fileinput.click();
						};
					});
				});
			});
			img.src = e.target.result;
		};
		reader.readAsDataURL(fileinput.files[0]);
	}
}

function uploadPhoto(imageData, title, preview, receipt) {
	return new Promise(function(resolve, reject) {
		const request = new XMLHttpRequest();
		request.onload = () => {
			window.location.href = '/upload';
		}
		request.onerror = reject;
		request.open('POST', 'upload');
		const data = new FormData();
		data.append('image', imageData);
		data.append('title', title);
		data.append('preview', preview);
		data.append('receipt', receipt);
		request.send(data);
	});
}

document.addEventListener("DOMContentLoaded", () => {
	let filters = {};
	const fileinput = document.querySelector('#upload-photo');
	document.querySelector('img#new-photo').onclick = () => {
		fileinput.click();
	}
	fileinput.onchange = () => {
		loadInput(fileinput, filters);
	};

	document.querySelector('#upload-photo-btn').onclick = (e) => {
		const canvas = document.querySelector('canvas#new-photo');
		const dataURL = canvas.toDataURL();
		const title = document.getElementById('title').value;
		const preview = document.getElementById('preview').value;
		const receipt = document.getElementById('receipt').value;

		uploadPhoto(dataURL, title, preview, receipt);
	}
})