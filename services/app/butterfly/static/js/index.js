//THE DIV THAT HOLDS ALL THE POSTS
const posts = document.querySelector('.feeds')

//THESE ARE USED TO FETCH NEW POSTS
var postsOffSet = 2
const postsLimit = 2

//THESE ARE USED TO FETCH NEW COMMENTS
var commentsOffSet = 2
const commentsLimit = 2

//VIEW COMMENTS
const postComments = document.querySelector('.post-comments')
document.addEventListener('click', (e) => {
    if(e.target.classList.contains('view-comments-btn')){
        const postId = e.target.closest('.feed').id
        const postCommentsPopup = postComments.querySelector('.post-comments-popup')
        var child = postCommentsPopup.lastElementChild; 
        while (child) {
            postCommentsPopup.removeChild(child);
            child = postCommentsPopup.lastElementChild;
        }
        postCommentsPopup.id = postId
        fetch(`http://127.0.0.1:5000/post/load_more_comments?post_id=${postId}`, {
            method: 'GET'
        }).then(
            response => response.json()
        ).then(
            response => {
                commentsOffSet = commentsOffSet + commentsLimit;
                console.log(JSON.stringify(response))
                insertNewComments(response,postCommentsPopup)
            }
        )
        postComments.style.display = 'block'
        postCommentsPopup
    }
})

const closeCommentsBtn = document.querySelector('.create-post-btn')

document.addEventListener('click', (e) => {
    if(e.target.classList.contains('close-comments')){
        postComments.style.display = 'none'
    }
})


// THE OBSERVER THAT LOADS POSTS DYNAMICALLY
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('intersecting')
            fetch(`http://localhost:5000/post/load_more_posts?offset=${postsOffSet}&limit=${postsLimit}`, {
                method: 'GET'
            }).then(
                response => response.json()
            ).then(
                response => {
                    postsOffSet = postsOffSet + postsLimit;
                    insertNewPosts(response)
                    // console.log(JSON.stringify(response))
                }
            )
        }
    })
},
    {
        threshold: 0.2
    }
)

const loader = document.querySelectorAll('.loader')

for (let i = 0; i < loader.length; i++) {
    const elements = loader[i];

    observer.observe(elements);
}

//INSERT THE NEW LOADED POSTS
const insertNewPosts = (new_posts) => {
    new_posts.forEach(new_post => {
        feed = document.createElement('div');
        feed.classList.add('feed')
        feed.id = new_post.id
        createPostHead(new_post, feed)
        createPost(new_post, feed)
        posts.appendChild(feed, posts.firstChild)
    })
}

//CREATE THE POST HEAD
const createPostHead = (new_post, feed) => {
    head = document.createElement('div');
    head.classList.add('head')

    user = document.createElement('div');
    user.classList.add('user')

    profilePhoto = document.createElement('div');
    profilePhoto.classList.add('profile-photo')

    profileImg = document.createElement('img');
    profileImg.src = new_post.author.profile_picture

    profilePhoto.appendChild(profileImg)

    ingo = document.createElement('div');
    ingo.classList.add('ingo')

    h3 = document.createElement('h3');
    h3.innerHTML = new_post.author.name
    small = document.createElement('small');
    small.innerHTML = `${new_post.location}, ${new_post.date_published} MINUTES AGO`

    ingo.appendChild(h3)
    ingo.appendChild(small)

    user.appendChild(profilePhoto)
    user.appendChild(ingo)   
    head.appendChild(user)
    createFriendAction(head)
    feed.appendChild(head)
}

const createFriendAction = (head) => {
    span = document.createElement('span')
    span.classList.add('edit')
    span.innerHTML = `
    <i class="uil uil-ellipsis-h post-menu-btn"></i>

    <div class="post-menu">
        <div class="dropdownmenu">
            <div class="card">
                <div class="befriend ctx-menu">
                    <span>
                        <i class="fa-solid fa-user-plus"></i>
                    </span>
                    <small class="menu-item">Befriend</small>
                </div>
                <div class="unfriend ctx-menu">
                    <span>
                        <i class="fa-solid fa-user-minus" ></i>
                    </span>
                    <small class="menu-item">Unfriend</small>
                </div>
            </div>
        </div>
    </div>
    `
    head.appendChild(span)
}

const createPost = (new_post, feed) => {
    postText = document.createElement('div');
    postText.classList.add('post-text')
    postText.classList.add('text-muted')
    postText.innerHTML = new_post.text

    postPhoto = document.createElement('div');
    postPhoto.classList.add('photo')

    postImg = document.createElement('img');
    postImg.src = new_post.image

    postPhoto.appendChild(postImg)
    feed.appendChild(postText)
    feed.appendChild(postPhoto)
}

// THE OBSERVER THAT LOADS COMMENTS DYNAMICALLY
const commentsObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const postCommentsPopup = postComments.querySelector('.post-comments-popup')
            const postId = postCommentsPopup.id
            fetch(`http://127.0.0.1:5000/post/load_more_comments?post_id=${postId}`, {
                method: 'GET'
            }).then(
                response => response.json()
            ).then(
                response => {
                    commentsOffSet = commentsOffSet + commentsLimit;
                    console.log(JSON.stringify(response))
                    insertNewComments(response,postCommentsPopup)
                }
            )
            console.log('comments')
        }
    })
},
    {
        threshold: 0.2
    }
)

const commentsLoader = document.querySelectorAll('.comments-loader')

for (let i = 0; i < commentsLoader.length; i++) {
    const elements = commentsLoader[i];

    commentsObserver.observe(elements);
}

const insertNewComments = (new_comments,postCommentsPopup) => {
    new_comments.forEach(comment => {
        const div = document.createElement('div')
        const profilePhoto = document.createElement('div')
        profilePhoto.classList.add('profile-photo')
        profilePhoto.classList.add('profile-menu')
        const img = document.createElement('img')
        img.src = comment.author.profile_picture
        profilePhoto.appendChild(img)
        const body = document.createElement('div')
        body.classList.add('notification-body')
        body.innerHTML = `<b>${comment.author.name}</b> ${comment.text}`
        div.appendChild(profilePhoto)
        div.appendChild(body)
        postCommentsPopup.appendChild(div)
    })
}