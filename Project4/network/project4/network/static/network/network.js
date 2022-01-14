document.addEventListener('DOMContentLoaded', function() {

    let LikeLinks = document.querySelectorAll('.like-post-link');

    LikeLinks.forEach(div => {
        div.onclick = function(e) {

            const id = div.dataset.id
            console.log("ID:" + id)

            fetch(`/like/${this.dataset.id}`, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    id: this.dataset.id
                    })
            })   
            .then (response => response.json())
            .then (post => {
                document.querySelector("#like_btn_" + id).className = post.css_class;
                console.log(post.total_likes)
                document.querySelector("#counter_" + id).innerHTML = post.total_likes;
            });

    }})

    // Display the edit form and hide the post content
    let editLinks = document.querySelectorAll('.edit-post-link');

    editLinks.forEach(link => {
        link.onclick = function (event) {
            event.preventDefault();
            const data_id = this.dataset.id;
            let PostContent = document.querySelector("#post_content_" + data_id);
            let EditForm = document.querySelector("#edit_form_" + data_id);
            PostContent.style.display = 'none';
            EditForm.querySelector('#edit_post').value = PostContent.innerHTML;
            EditForm.style.display = 'block';

            EditForm.addEventListener('submit', function(e) {
                e.preventDefault();

                let edit_data = EditForm.querySelector('#edit_post').value;
                console.log(edit_data);

                fetch(`/edit/${this.dataset.id}`, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        },
                    body: JSON.stringify({
                        id: data_id,
                        content: edit_data,
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })
                .catch(error => {
                    console.log('Error', error);
                })

                EditForm.style.display = 'none';
                document.querySelector("#post_content_" + data_id).innerHTML = edit_data
                document.querySelector("#post_content_" + data_id).style.display = 'block';
            })
        }
    })
})



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}