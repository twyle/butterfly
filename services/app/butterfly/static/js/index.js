//SIDEBAR 
const menuItems = document.querySelectorAll('.menu-item');

//NOTIFICATIONS
const notifications = document.querySelector('#notifications')
const notificationsPopup = document.querySelector('.notifications-popup')

//BOOKMARKS
const bookmarks = document.querySelector('#bookmarks')
const bookmarksPopup = document.querySelector('.bookmarks-popup')

//MESSAGES
const messagesNotification = document.querySelector('#messages-notification')
const messages = document.querySelector('.messages');
const message = messages.querySelectorAll('.message');
const messageSearch = document.querySelector('#message-search')

//THEME
const theme = document.querySelector('#theme')
const themeModal = document.querySelector('.customize-theme')
const fontSizes = document.querySelectorAll('.choose-size span')

var root = document.querySelector(':root')

const colorPallette = document.querySelectorAll('.choose-color span')

const bg1 = document.querySelector('.bg-1')
const bg2 = document.querySelector('.bg-2')
const bg3 = document.querySelector('.bg-3')

//ANALYTICS
const analytics = document.querySelector('#analytics')
const analyticsModal = document.querySelector('.view-analytics')

//MESSAGE SOMEONE
const messageUser = document.querySelector('#message-user')
const messageUserModal = document.querySelector('.create-message')

// remove active class from all menu items
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

//EDIT PROFILE
// const editProfile = document.querySelector('#edit-user-profile')
const editProfile = document.querySelector('.user-profile')
const editProfileModal = document.querySelector('.edit-profile')

//CONTEXT MENU DROPDOWN
const contextMenuDropdown = document.querySelector('#context-dropdown')
const contextMenuDropdownModal = document.querySelector('.dropdownmenu')

//BOOKMARK
const bookmarkButtons = document.querySelectorAll('.bookmark-button')
bookmarkButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const bookmarkButtonSolid = btn.querySelector('.fa-solid')
        const bookmarkButtonRegular = btn.querySelector('.fa-regular')
        bookmarkButtonSolid.classList.toggle('active')
        bookmarkButtonRegular.classList.toggle('active')
    })
})

//COMMENT
const commentButtons = document.querySelectorAll('.fa-comment')
commentButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const feed = btn.closest('.feed')
        const comment = feed.querySelector('.comment-box')
        comment.style.display = 'block'
    })
})
//Close comment box
const submitCommentButtons = document.querySelectorAll('.submit-comment')
submitCommentButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        comment = btn.closest('.comment-box')
        comment.style.display = 'none'
    })
})

//DELETE
const deleteBox = document.querySelector('.delete-post')
const deleteButtons = document.querySelectorAll('.fa-trash-can')
// deleteButtons.forEach(btn => {
//     addEventListener('click', () => {
//         alert('hey')
//     })
// })
deleteButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        currentFeed = btn.closest('.feed')
        currentFeed.remove()
        // Get the post id
        fetch('http://localhost:5000/post?id=1',{
            method: 'DELETE',
        }).then(
            response => response.json()
        ).then(
            response => {
                console.log(JSON.stringify(response))
            }
        )
    })
})

//EDIT
const editButtons = document.querySelectorAll('.fa-pen-to-square')
const editBox = document.querySelector('.edit-post')
editBox.addEventListener('submit', (e) => {
    e.preventDefault()
    formData = new FormData(editBox)
    formData.append("file", image);
    fetch(editBox.action,{
        method: 'POST',
        body: formData
    }).then(
        response => response.json()
    ).then(
        response => {
            console.log(JSON.stringify(response))
        }
    )
    editBox.style.display = 'none'
    console.log(editBox)
    oldPhoto = oldPost.querySelector('.photo')
    image = oldPhoto.querySelector('img')
    oldText = oldPost.querySelector('.post-text')

    newPhoto = editBox.querySelector('.photo')
    newImage = newPhoto.querySelector('img').src
    newText = editBox.querySelector('input')
    image.src = newImage
    oldText.textContent = newText.value
})

//LIKE
const likeButtons = document.querySelectorAll('.like-button')
likeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const likeButtonSolid = btn.querySelector('.fa-solid')
        const likeButtonRegular = btn.querySelector('.fa-regular')
        likeButtonSolid.classList.toggle('active')
        likeButtonRegular.classList.toggle('active')
        likeButtonSolid.style.color = 'red'
        likeButtonSolid.style.fontSize = '2rem'
        setTimeout(() => {
            likeButtonSolid.style.fontSize = '1.4rem'
        }, 1000)
    })
})

//Primary messages
const primaryMessages = document.querySelector('#primary')

//Friend requests
const friendRequests = document.querySelector('#requests')
const requests = document.querySelectorAll('.request');

//Friend Request Buttons
const requestsButtons = document.querySelectorAll('.fr');

//Create post
const createPostButton = document.querySelector('#cr')
const createPostButton1 = document.querySelector('#create-post-btn-top')

createPostButton1.addEventListener('click', () => {
    alert('hey')
})


//COMMENTS
const commentsButton = document.querySelector('#pcb')
const postCommentsBox = document.querySelector('.post-comments')

//Message actions
const messageActionButtons = document.querySelectorAll('.message-actions-buttons')
//Message actions
messageActionButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        nextSibling = btn.nextElementSibling
        dropDownMenu = nextSibling.querySelector('.dropdownmenu')
        dropDownMenu.style.display = 'block'

        setTimeout(() => {
            dropDownMenu.style.display = 'none'
        }, 3000)
    })
})

//Submite edited post
const submitEdittedPostButtons = document.querySelectorAll('.submit-edited-post')

//old post
let oldPost;

//Post Image update
let image;
const uploadPostImageButtons = document.querySelectorAll('.post-image-upload')

// uploadPostImageButtons.forEach(btn => {
//     btn.addEventListener('click', () => {
//         var input = document.createElement('input');
//     input.type = 'file';

//     input.onchange = event => { 
//         const imageFiles = event.target.files
//         const imageFilesLength = imageFiles.length
//         if (imageFilesLength > 0){
//             image = imageFiles[0]
//             const imageSrc = URL.createObjectURL(imageFiles[0])
//             editPostPhoto = editBox.querySelector('.photo')
//             editPhoto = editPostPhoto.querySelector('img')
//             editPhoto.src = imageSrc
//         }
//      }

//     input.click();
//     })
// })

//REPLY TO MESSAGE
const replyButtons = document.querySelectorAll('.fa-message')
const messageBox = document.querySelector('.reply-message')

replyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        messageBox.style.display = 'grid'
    })
})

messageBox.addEventListener('click', e => {
    if(e.target.classList.contains('reply-message')){
        messageBox.style.display = 'none'
    }
})

//CLOSE MESSAGE
const closeMessageButtons = document.querySelectorAll('.fa-rectangle-xmark')
closeMessageButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const message = btn.closest('.message')
        message.remove()
    })
})

// Send reply
const replyMessageButon = document.querySelector('#reply-message-button')
replyMessageButon.addEventListener('click', e => {
    messageBox.style.display = 'none'
})

menuItems.forEach(item => {
    item.addEventListener('click', ()=>{
        changeActiveItem();
        item.classList.add('active');
        // if(item.id != 'notifications'){
        //     document.querySelector('.notifications-popup').
        //     style.display = 'none';
        // }
        // else{
        //     document.querySelector('.notifications-popup').
        //     style.display = 'block';
        //     document.querySelector('#notifications .notification-count').
        //     style.display = 'none';
        // }
    })
})

notifications.addEventListener('click', ()=>{
    notificationsPopup.style.display = 'block';
    document.querySelector('#notifications .notification-count').
    style.display = 'none';
    setTimeout(() => {
        notificationsPopup.style.display = 'none';
    }, 2000)
})

bookmarks.addEventListener('click', ()=>{
    bookmarksPopup.style.display = 'block';
    setTimeout(() => {
        bookmarksPopup.style.display = 'none';
    }, 2000)
})

// MESSAGES

//search chat
const searchMessage = () => {
    const val = messageSearch.value.toLowerCase();
    console.log(val)
    message.forEach(chat => {
        let name = chat.querySelector('h5').textContent.toLowerCase()
        if(name.indexOf(val) != -1){
            chat.style.display = 'flex'
        }
        else{
            chat.style.display = 'none'
        }
    })
}

messageSearch.addEventListener('keyup', searchMessage)

// Highlight message box when message
messagesNotification.addEventListener('click', ()=>{
    messages.style.boxShadow = '0 0 1rem var(--color-primary)';
    messagesNotification.querySelector('.notification-count').
    style.display = 'none';
    setTimeout(() => {
        messages.style.boxShadow = 'none'
    }, 2000)
})

//THEME CUSTOMIZATION

//open modal
const openThemeModal = () => {
    themeModal.style.display = 'grid';
}

const closeThemeModal = (e) => {
    if(e.target.classList.contains('customize-theme')){
        themeModal.style.display = 'none'
        notificationsPopup.style.display = 'none';
    }
}

//close modal
themeModal.addEventListener('click', closeThemeModal);

theme.addEventListener('click', openThemeModal);

//remove active class from font selector
const removeSizeSelector = () => {
    fontSizes.forEach(size => {
        size.classList.remove('active')
    })
}

//FONTS
fontSizes.forEach(size => {

    size.addEventListener('click', () => {
        removeSizeSelector()
        let fontSize;
        size.classList.toggle('active')

        if (size.classList.contains('font-size-1')){
            fontSize = '10px'
            root.style.setProperty('----sticky-top-left', '5.4rem')
            root.style.setProperty('----sticky-top-right', '5.4rem')
        }
        else if(size.classList.contains('font-size-2')){
            fontSize = '13px'
            root.style.setProperty('----sticky-top-left', '5.4rem')
            root.style.setProperty('----sticky-top-right', '-7rem')
        }
        else if(size.classList.contains('font-size-3')){
            fontSize = '16px'
            root.style.setProperty('----sticky-top-left', '-2rem')
            root.style.setProperty('----sticky-top-right', '-17rem')
        }
        else if(size.classList.contains('font-size-4')){
            fontSize = '19px'
            root.style.setProperty('----sticky-top-left', '-5rem')
            root.style.setProperty('----sticky-top-right', '-25rem')
        }
        else if(size.classList.contains('font-size-5')){
            fontSize = '22px'
            root.style.setProperty('----sticky-top-left', '-12rem')
            root.style.setProperty('----sticky-top-right', '-35rem')
        }

        //change font size for root element
        document.querySelector('html').style.fontSize = fontSize;
    })

})

//remove active class from colors
const changeActiveColorClass = () => {
    colorPallette.forEach(colorPicker => {
        colorPicker.classList.remove('active')
    })
}

//change primary colors
colorPallette.forEach(color => {
    color.addEventListener('click', () => {
        let primaryHue;
        changeActiveColorClass()

        if(color.classList.contains('color-1')){
            primaryHue = 252
        }
        else if(color.classList.contains('color-2')){
            primaryHue = 52
        }
        else if(color.classList.contains('color-3')){
            primaryHue = 352
        }
        else if(color.classList.contains('color-4')){
            primaryHue = 152
        }
        else if(color.classList.contains('color-5')){
            primaryHue = 202
        }

        color.classList.add('active')
        root.style.setProperty('--primary-color-hue', primaryHue)
    })
})

//theme background values
let lightColorLightness;
let whiteColorLightness;
let darkColorLightness;

//changes background color
const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightColorLightness)
    root.style.setProperty('--white-color-lightness', whiteColorLightness)
    root.style.setProperty('--dark-color-lightness', darkColorLightness)
}

bg1.addEventListener('click', () => {
    //add active class
    bg1.classList.add('active')
    //remove active class from others
    bg3.classList.remove('active')
    bg2.classList.remove('active')
    window.location.reload()
})

bg2.addEventListener('click', () => {
    darkColorLightness = '95%'
    whiteColorLightness = '20%'
    lightColorLightness = '15%'

    //add active class
    bg2.classList.add('active')
    //remove active class from others
    bg1.classList.remove('active')
    bg3.classList.remove('active')
    changeBG()
})

bg3.addEventListener('click', () => {
    darkColorLightness = '95%'
    whiteColorLightness = '10%'
    lightColorLightness = '0%'

    //add active class
    bg3.classList.add('active')
    //remove active class from others
    bg1.classList.remove('active')
    bg2.classList.remove('active')
    changeBG()
})


//open modal
const openAnalyticsModal = () => {
    analyticsModal.style.display = 'grid';
}

const closeAnalyticsModal = (e) => {
    if(e.target.classList.contains('view-analytics')){
        analyticsModal.style.display = 'none'
    }
}

//close modal
analyticsModal.addEventListener('click', closeAnalyticsModal);

analytics.addEventListener('click', openAnalyticsModal);

//open modal
const openEditProfileModal = () => {
    editProfileModal.style.display = 'grid';
}

const closeEditProfileModal = (e) => {
    if(e.target.classList.contains('edit-profile')){
        editProfileModal.style.display = 'none'
    }
}

form = document.querySelector("#update-user-form")
form.addEventListener('submit', e => {
    e.preventDefault()
    formData = new FormData(form)
    fetch(form.action,{
        method: 'POST',
        body: formData
    }).then(
        response => response.json()
    ).then(
        response => {
            console.log(JSON.stringify(response))
        }
    )
    editProfileModal.style.display = 'none'
})

//close modal
editProfileModal.addEventListener('click', closeEditProfileModal);

editProfile.addEventListener('click', openEditProfileModal);

//open modal
const openMessageUserModal = () => {
    messageUserModal.style.display = 'grid';
}

const closeMessageUserModal = (e) => {
    if(e.target.classList.contains('create-message')){
        messageUserModal.style.display = 'none'
    }
}

//close modal
messageUserModal.addEventListener('click', closeMessageUserModal);

messageUser.addEventListener('click', openMessageUserModal);

//open modal
const openDropDownMenuModal = () => {
    contextMenuDropdownModal.style.display = 'block';
    setTimeout(() => {
        contextMenuDropdownModal.style.display = 'none';
    }, 2000)
}

contextMenuDropdown.addEventListener('click', openDropDownMenuModal);


//open modal
const openEditPostModal = () => {
    editBox.style.display = 'grid';
}

const closeEditPostModal = (e) => {
    if(e.target.classList.contains('edit-post')){
        editBox.style.display = 'none'
    }
}

//close modal
editBox.addEventListener('click', closeEditPostModal);

editButtons.forEach(editButton => {
    editButton.addEventListener('click', () => {
        post = editButton.closest('.feed')
        oldPost = post
        user = post.querySelector('.head')
        profilePicture = user.querySelector('img')
        ingo = user.querySelector('.ingo')
        userName = ingo.querySelector('.user-name')
        // location = ingo.querySelector('.location')
        postPhoto = post.querySelector('.photo')
        photo = postPhoto.querySelector('img')

        postText = post.querySelector('.post-text')
        console.log(postText)

        editUser = editBox.querySelector('.head')
        editProfilePicture = editUser.querySelector('img')
        editProfilePicture.src = profilePicture.src

        editIngo = editUser.querySelector('.ingo')
        editUserName = document.querySelector('.edit-user-name')
        editUserName.textContent = userName.textContent

        editUserLocation = document.querySelector('.edit-user-location')

        editPostPhoto = editBox.querySelector('.photo')
        editPhoto = editPostPhoto.querySelector('img')
        editPhoto.src = photo.src

        editPostText = editBox.querySelector('input')
        editPostText.value = postText.textContent
        editPostText.focus()

        addImageButton = editBox.querySelector('.uil-image-plus')
        console.log(addImageButton)
        editBox.style.display = 'grid';

    })
})

const editPostForm = document.querySelector('edit-post')
editPostForm.addEventListener('submit', e => {
    alert('submit')
})

uploadPostImageButtons.forEach(
    btn => btn.addEventListener(
        'click', () => {
            alert('hey')
        }
    )
)



submitEdittedPostButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        editPostPhoto = editBox.querySelector('.photo')
        editPhoto = editPostPhoto.querySelector('img')
        editPostText = editBox.querySelector('input')
        console.log(editPhoto)

        oldPhoto = oldPost.querySelector('.photo')
        oldPhoto = oldPhoto.querySelector('img')
        oldPhoto.src = editPhoto.src
        oldText = oldPost.querySelector('.post-text')
        oldText.textContent = editPostText.value
        editBox.style.display = 'none';
    })
})


primaryMessages.addEventListener('click', () => {
    primaryMessages.style.color = 'black'
    primaryMessages.classList.add('active')
    friendRequests.classList.remove('active')
    friendRequests.style.color = 'var(--color-primary)'
    messages.style.boxShadow = '0 0 1rem var(--color-primary)';
    setTimeout(() => {
        messages.style.boxShadow = 'none'
    }, 2000)
})

friendRequests.addEventListener('click', () => {
    primaryMessages.classList.remove('active')
    primaryMessages.style.color = 'var(--color-primary)'
    friendRequests.classList.add('active')
    friendRequests.style.color = 'black'

    requests.forEach(req => {
        req.style.boxShadow = '0 0 1rem var(--color-primary)';
        setTimeout(() => {
            req.style.boxShadow = 'none'
        }, 2000)
    })
})


requestsButtons.forEach(rq => {
    rq.addEventListener('click', e => {
        elem = rq.closest('#request-div')
        if (rq.classList.contains('btn-primary')){
            elem.style.boxShadow = '0 0 1rem var(--color-primary)';
            setTimeout(() => {
                elem.style.boxShadow = 'none'
                elem.remove()
            }, 800)
        }
        else{
            elem.style.boxShadow = '0 0 1rem var(--color-danger)';
            setTimeout(() => {
                elem.style.boxShadow = 'none'
                elem.remove()
            }, 800)
        }
        // elem.remove()
    })
})

const createPostForm = document.querySelector("#create-post-form");
createPostForm.addEventListener('submit', e => {
    e.preventDefault();
    const newFeed = document.querySelector('.very-new-post')
    newFeedBox = newFeed.querySelector('.create-post')
    profilePicture = newFeedBox.querySelector('img')
    postPhoto = newFeed.querySelector('.photo')
    newPhoto = postPhoto.querySelector('img')

    newPostText = newFeed.querySelector('#create-post')
    console.log(newPostText.value)
    console.log(profilePicture.src)

    feedO = document.querySelector('.feed-o')

    feed = document.createElement( 'div' );
    feed.classList.add('feed')

    head = document.createElement( 'div' );
    head.classList.add('head')

    user = document.createElement( 'div' );
    user.classList.add('user')

    profilePhoto = document.createElement( 'div' );
    profilePhoto.classList.add('profile-photo')

    profileImg = document.createElement('img');
    profileImg.src = profilePicture.src

    profilePhoto.appendChild(profileImg)

    ingo = document.createElement( 'div' );
    ingo.classList.add('ingo')

    h3 = document.createElement( 'h3' );
    h3.innerHTML = 'Lyle Okoth'
    small = document.createElement( 'small' );
    small.innerHTML = 'Nairobi, 15 MINUTES AGO'

    ingo.appendChild(h3)
    ingo.appendChild(small)

    user.appendChild(profilePhoto)
    user.appendChild(ingo)

    span = document.createElement('span')
    span.classList.add('edit')
    span.innerHTML = `
        <i class="uil uil-ellipsis-h" id="context-dropdown"></i>
                            
        <div class="context-menu">
            <div class="dropdownmenu">
                <div class="card">

                </div>
            </div>
        </div>
    `
    head.appendChild(user)
    head.appendChild(span)

    postText = document.createElement('div');
    postText.classList.add('post-text')
    postText.classList.add('text-muted')
    post = 'A brand new post'
    postText.innerHTML = newPostText.value

    postPhoto = document.createElement( 'div' );
    postPhoto.classList.add('photo')

    postImg = document.createElement('img');
    postImg.src = newPhoto.src

    postPhoto.appendChild(postImg)

    actionButtons = document.createElement('div')
    actionButtons.classList.add('action-buttons')

    
    actionButtons.innerHTML = `
    <div class="interaction-button">
        <div class="like-button">
            <span>
                <i class="fa-solid fa-heart"></i>
            </span>
            <span>
                <i class="fa-regular fa-heart active"></i>
            </span>
        </div>
        <span>
            <i class="fa-regular fa-comment active"></i>
        </span>
    </div>

    <div class="bookmark">
        <span>
            <i class="fa-regular fa-pen-to-square active"></i>
        </span>
        <span>
            <i class="fa-regular fa-trash-can active"></i>
        </span>
        <div class="bookmark-button">
            <span>
                <i class="fa-regular fa-bookmark active"></i>
            </span>
            <span>
                <i class="fa-solid fa-bookmark"></i>
            </span>
        </div>
        
    </div>

    `
    // actionButtons.innerHTML = `
    // Hey tere
    // `

    feed.appendChild(head)
    feed.appendChild(postText)
    feed.appendChild(postPhoto)
    feed.appendChild(actionButtons)

    feedO.appendChild(feed)

    formData = new FormData(createPostForm)
    fetch(createPostForm.action,{
        method: 'POST',
        body: formData
    }).then(
        response => response.json()
    ).then(
        response => {
            console.log(JSON.stringify(response))
        }
    )

    newPhoto.src = ''
    newPostText.value = ''
    newFeedBox = newFeed.querySelector('.create-post')
    newFeedBox.style.boxShadow = 'none'
    newFeed.classList.remove('feed')
})

// const openDeletePostModal = () => {
//     deleteBox.style.display = 'grid';
// }

// const closeDeletePostModal = (e) => {
//     if(e.target.classList.contains('delete-post')){
//         deleteBox.style.display = 'none'
//     }
// }

// //close modal
// deleteBox.addEventListener('click', closeDeletePostModal);

// deleteButton.addEventListener('click', openDeletePostModal);

const previewImage = (event) => {
    const imageFiles = event.target.files
    const imageFilesLength = imageFiles.length
    const newFeed = document.querySelector('.very-new-post')
    const postBox = document.querySelector('#new-post')
    if (imageFilesLength > 0){
        const imageSrc = URL.createObjectURL(imageFiles[0])
        const imagePreviewElement = document.querySelector('#preview-selected-image')
        imagePreviewElement.src = imageSrc
        newFeed.classList.add('feed')
        postBox.style.boxShadow = '0 0 1rem var(--color-primary)';
    }
    console.log(imageFilesLength)
}

commentsButton.addEventListener('click', () => {
    postCommentsBox.style.display = 'grid'
})

const closePostCommentsModal = (e) => {
    if(e.target.classList.contains('post-comments')){
        postCommentsBox.style.display = 'none'
    }
}

//close modal
postCommentsBox.addEventListener('click', closePostCommentsModal);
