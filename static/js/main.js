function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

//$("[type='number']").keypress(function (evt) {
//    evt.preventDefault();
//});

$(".ask-button").on("click", function(e){
    console.log("ask pressed")
    window.location = "/ask/"
})

$(".like-button-input").on("click", function(e){
    console.log("click")
    console.log(e.which + " " + e.key)
    console.log(e)
    const request = new Request("/like_question/", {
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        },
        method: "POST",
        body: "question_id=" + $(this).data("id")
    });

    fetch(request).then(response_raw => response_raw.json().then(
        response_json => {
            console.log(response_json)
            if (response_json.status == "ok") {
                console.log("OK")
//                $(this).attr("value", response_json.likes_count)
                this.innerHTML = response_json.likes_count
            }
        }
    ))
//    fetch(request).then(function(response){
//       console.log("got response ")
//       return response.json()
//    }).then(function(json) {
//        console.log(json)
//        e.target
//    });
})


$(".answer-correct-checkbox").on("click", function(e){
    console.log("click checkbox")
    console.log(e.which + " " + e.key)
    console.log(e)
    const request = new Request("/check_answer/", {
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        },
        method: "POST",
        body: "answer_id=" + $(this).data("id")
    });

    fetch(request).then(response_raw => response_raw.json().then(
        response_json => {
            console.log(response_json)
            if (response_json.status == "ok" && response_json.checked) {
                console.log("OK")
                $(this).attr("checked")
            } else {
                $(this).removeAttr("checked")
            }
        }
    ))
})