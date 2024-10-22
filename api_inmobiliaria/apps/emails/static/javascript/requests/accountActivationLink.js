const DEFAULT_ERROR_MESSAGE = 'Lo sentimos, se ha producido un error inesperado en nuestro sistema. No se ha podido completar tu solicitud en este momento. Por favor, inténtalo de nuevo más tarde. Si el problema persiste, puedes ponerte en contacto con nuestro equipo de soporte al cliente para obtener más ayuda. Disculpa las molestias y gracias por tu paciencia.'
const IMG_OK = 'EmailMessage.png'
const IMG_ERROR = 'Error.png'

// Selectors
const requestNewLink = document.querySelector('.requestNewLink')
const modal = document.querySelector('.modal')
const modalContainer = document.querySelector('.modal__container')
const buttonModal = document.querySelector('.modal__container a')
const textModal = document.querySelector('.modal__container .container__message p')
const imgModal = document.querySelector('.modal__container .container__message img')

const showModal = (message, imgSrc, buttonText = '', buttonHref = '') => {
    textModal.innerText = message
    imgModal.setAttribute('src', imgModal.dataset.src + imgSrc)
    buttonModal.style.display = buttonText ? 'block' : 'none'
    if (buttonHref) {
        buttonModal.innerText = buttonText
        buttonModal.setAttribute('href', buttonHref)
    }
    modalContainer.classList.add('modal__container--animation')
    modal.classList.add('modal--show')
}

const handleData = ({ data, response }) => {
    const { message, redirect } = data.detail

    switch (response.status) {
        case 200:
            showModal(message, IMG_OK)
            break
        case 500:
            showModal(DEFAULT_ERROR_MESSAGE, IMG_ERROR)
            break
        case 404:
            showModal(message, IMG_ERROR, redirect.action, redirect.url)
            break
        case 401:
            showModal(message, IMG_ERROR, redirect.action, redirect.url)
            break
        default:
            showModal(DEFAULT_ERROR_MESSAGE, IMG_ERROR)
    }
}

const request = async (endpoint) => {
    try {
        const response = await fetch(endpoint)
        const data = await response.json()
        handleData({ data, response })
    } catch (error) {
        showModal(DEFAULT_ERROR_MESSAGE, IMG_ERROR)
    }
}

if(requestNewLink) {
    requestNewLink.addEventListener('click', (e) => {
        e.preventDefault()
        request(requestNewLink.dataset.endpoint)
    })
}
