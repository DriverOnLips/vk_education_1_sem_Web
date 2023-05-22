function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function sendAnswerVoteRequest(answer_id, mark_name, csrf_token) {
  const formData = new FormData();
  formData.append('answer_id', answer_id);
  formData.append('mark_name', mark_name);
  formData.append('csrfmiddlewaretoken', csrf_token);
  const request = new Request('/vote_answer/', {method: 'POST', body: formData});
  return fetch(request).then(
      response_raw => response_raw.json().then(
          response_json => $('.likes#' + answer_id).text(response_json.new_rating)
      )
  );
}

$(".answer-like-btn").on('click', function (ev) {
    console.log('answer-like');
    const answer_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("answer-like-btn")) {
        console.log('answer-like');
        sendAnswerVoteRequest(answer_id, 'like', csrf_token);
    } else {
        sendAnswerVoteRequest(answer_id, '', csrf_token);
    }
});

$(".answer-dislike-btn").on('click', function (ev) {
    console.log('answer-like');
    const answer_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("answer-dislike-btn")) {
        console.log('answer-dislike');
        sendAnswerVoteRequest(answer_id, 'dislike', csrf_token);
    } else {
        sendAnswerVoteRequest(answer_id, '', csrf_token);
    }
});