const checkboxAll = document.querySelectorAll('.checkbox-all')
checkboxAll.forEach(input => {
	let userCheckbox =  document.querySelectorAll('.user-checkbox');
	input.addEventListener('click', ()=>{
		if (!input.classList.contains('active')) {
			input.classList.add('active')
			for (let i = 0; i < userCheckbox.length; i++) {
				userCheckbox[i].checked = input.checked
				selectActive(userCheckbox[i])
			}
		}else{
			input.classList.remove('active')
			for (let i = 0; i < userCheckbox.length; i++) {
				userCheckbox[i].checked = input.checked
				selectActive(userCheckbox[i])
			}
		}
	})
	for (let i = 0; i < userCheckbox.length; i++) {
		selectActive(userCheckbox[i])
		userCheckbox[i].addEventListener('click', ()=>{
			input.checked = false
			selectActive(userCheckbox[i])
		})		
	}
});
function selectActive(input) {
	if (input.checked) {
		input.closest('tr').classList.add('active')
	}else{
		input.closest('tr').classList.remove('active')
	}
}

// FAQ ACCORDION
const accoWrap = document.querySelectorAll('.acco-box-wrap')
	accoWrap.forEach(wrap => {
		let accoBox = wrap.querySelectorAll('.acco-box')
		accoBox.forEach(bx => {
			let title = bx.querySelector('.acco-box-title')
			let body = bx.querySelector('.acco-box-body')
			if (bx.classList.contains('active')) {
				body.style.maxHeight = body.scrollHeight + 'px'
			}
			title.addEventListener('click', ()=>{
				if (bx.classList.contains('active')) {
					bx.classList.remove('active')
					body.style.maxHeight = null;
				}else{
					for (let i = 0; i < accoBox.length; i++) {
						accoBox[i].classList.remove('active')
						accoBox[i].querySelector('.acco-box-body').style.maxHeight = null;
					}
					bx.classList.add('active')
					body.style.maxHeight = body.scrollHeight + 'px';
				}
			})
		});
	});