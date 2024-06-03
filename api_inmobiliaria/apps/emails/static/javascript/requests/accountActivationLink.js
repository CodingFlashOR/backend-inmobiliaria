document.addEventListener('DOMContentLoaded', (event) => {
    // Selectors
    const requestNewLink = document.querySelector('.requestNewLink')
    const modal = document.querySelector('.modal')
    const modalContainer = document.querySelector('.modal__container')
    const buttonModal = document.querySelector('.modal__container a')
    const textModal = document.querySelector('.modal__container .container__message p')
    const imgModal = document.querySelector('.modal__container .container__message img')

    // Function to handle the data
    function handleData({ data, ok }) {
        textModal.textContent = data.detail.message;
        imgModal.setAttribute(
            'src', imgModal.dataset.src + (ok ? 'EmailMessage.png' : 'EmailMessageError.png')
        )
        if (!ok) {
            buttonModal.setAttribute('href', data.detail.redirect.url)
            buttonModal.textContent = data.detail.redirect.text
        } else {
            buttonModal.style.display = 'none'
        }
        modalContainer.classList.add('modal__container--animation')
        modal.classList.add('modal--show')
    }

    // Event listener
    if(requestNewLink) {
        requestNewLink.addEventListener('click', (e) => {
            e.preventDefault()
            fetch(requestNewLink.dataset.endpoint, {method: 'GET'})
                .then(response => {
                    return response.json().then(data => ({ data, ok: response.ok }))
                })
                .then(result => handleData(result))
        })
    }
})