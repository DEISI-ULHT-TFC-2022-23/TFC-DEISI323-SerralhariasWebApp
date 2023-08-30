const smallImages = document.querySelectorAll('.small-image')
const imageDisplay = document.querySelectorAll('.image_display')[0]

console.log(smallImages)
console.log(imageDisplay)

smallImages.forEach(smallImage => {
    smallImage.addEventListener('click', () => {
        smallImages.forEach(otherImage => {
            otherImage.classList.remove("active")
        })
        smallImage.classList.add("active")
        imageDisplay.src = smallImage.src
    })
})