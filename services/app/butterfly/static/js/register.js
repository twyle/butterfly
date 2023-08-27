const imageInput = document.querySelector('.avatar-input')

imageInput.onchange = event => {
    const imageFiles = event.target.files;
    const imageFilesLength = imageFiles.length;
    if (imageFilesLength > 0){
        const imageSrc = URL.createObjectURL(imageFiles[0])
        const userImg = document.querySelector('.user-avatar')
        userImg.src = imageSrc
    }
}